"""Live transcription session — one open WebSocket and its event pump."""

from __future__ import annotations

import asyncio
import inspect
import json
import logging
import typing

import pydantic

from .audio_source import AudioSource
from .errors import LiveTranscriptionProtocolError
from .events import (
    PARSER_REGISTRY,
    ClosedEvent,
    ErrorEvent,
    ServerMessageType,
)
from .options import ConnectOptions
from .transport import Transport

_log = logging.getLogger(__name__)

Handler = typing.Callable[[typing.Any], typing.Union[None, typing.Awaitable[None]]]
WildcardHandler = typing.Callable[
    [ServerMessageType, typing.Any], typing.Union[None, typing.Awaitable[None]]
]


class LiveTranscriptionSession:
    """One live transcription connection.

    Construct via :func:`connect` or the resource client on ``CambAI``;
    direct construction is supported but the factory wires the transport
    and handles URL building.
    """

    def __init__(
        self,
        *,
        transport: Transport,
        url: str,
        headers: typing.Dict[str, str],
    ) -> None:
        self._transport = transport
        self._url = url
        self._headers = headers
        self._handlers: typing.Dict[ServerMessageType, typing.List[Handler]] = {}
        self._wildcard_handlers: typing.List[WildcardHandler] = []
        self._reader_task: typing.Optional[asyncio.Task[None]] = None
        self._closed = asyncio.Event()
        self._ready = asyncio.Event()
        self._send_lock = asyncio.Lock()
        self._is_closing = False

    # ---------------------------- lifecycle ----------------------------

    async def __aenter__(self) -> "LiveTranscriptionSession":
        await self._open()
        return self

    async def __aexit__(self, *exc: typing.Any) -> None:
        await self.close()

    async def _open(self) -> None:
        # Idempotent: the resource client's connect() already opens the
        # session before handing it back, and users typically wrap the
        # returned session in `async with session:` for cleanup. Re-running
        # _open here would spawn a second reader task on the same socket,
        # causing every event to fan out twice and races to wedge the
        # consumer iterator after a few frames.
        if self._reader_task is not None:
            return
        await self._transport.connect(self._url, self._headers)
        self._reader_task = asyncio.create_task(self._read_loop())

    @property
    def is_ready(self) -> bool:
        return self._ready.is_set()

    @property
    def is_closed(self) -> bool:
        return self._closed.is_set()

    async def wait_until_ready(self, timeout: typing.Optional[float] = None) -> None:
        await asyncio.wait_for(self._ready.wait(), timeout=timeout)

    async def run_until_closed(self) -> None:
        await self._closed.wait()

    # --------------------------- subscription --------------------------

    def on(
        self,
        event_type: ServerMessageType,
        handler: typing.Optional[Handler] = None,
    ) -> typing.Any:
        """Register a handler for ``event_type``.

        Usable as either a direct call (``session.on(t, fn)``) or as a
        decorator (``@session.on(t)``).
        """

        def _register(fn: Handler) -> Handler:
            self._handlers.setdefault(event_type, []).append(fn)
            return fn

        if handler is None:
            return _register
        return _register(handler)

    def off(self, event_type: ServerMessageType, handler: Handler) -> None:
        if event_type in self._handlers:
            try:
                self._handlers[event_type].remove(handler)
            except ValueError:
                pass

    def on_any(self, handler: WildcardHandler) -> WildcardHandler:
        """Receive every event (including ones added in future releases)."""
        self._wildcard_handlers.append(handler)
        return handler

    # ----------------------------- sending -----------------------------

    async def send_audio(self, chunk: bytes) -> None:
        async with self._send_lock:
            await self._transport.send_bytes(chunk)

    async def keep_alive(self) -> None:
        async with self._send_lock:
            await self._transport.send_text(json.dumps({"type": "KeepAlive"}))

    async def stream_audio(self, source: AudioSource) -> None:
        """Pump ``source`` chunks into the session until it is exhausted."""
        try:
            async for chunk in source:
                if self._closed.is_set():
                    break
                await self.send_audio(chunk)
        finally:
            await source.close()

    async def close(self) -> None:
        if self._is_closing or self._closed.is_set():
            return
        self._is_closing = True
        try:
            await self._transport.send_text(json.dumps({"type": "CloseStream"}))
        except Exception:  # transport may already be torn down
            _log.debug("CloseStream send failed; closing transport directly", exc_info=True)
        await self._transport.close(code=1000)
        if self._reader_task is not None:
            try:
                await asyncio.wait_for(self._reader_task, timeout=5.0)
            except asyncio.TimeoutError:
                self._reader_task.cancel()

    # ----------------------------- internals ---------------------------

    async def _read_loop(self) -> None:
        try:
            async for frame in self._transport:
                if isinstance(frame, (bytes, bytearray)):
                    # Server does not send binary frames today; ignore.
                    continue
                try:
                    data = json.loads(frame)
                except json.JSONDecodeError:
                    _log.warning("Discarding non-JSON server frame: %r", frame)
                    continue
                await self._dispatch(data)
        finally:
            await self._emit_close()

    async def _dispatch(self, raw: typing.Dict[str, typing.Any]) -> None:
        wire_type = raw.get("type")
        try:
            event_type = ServerMessageType(wire_type)
        except ValueError:
            # Forward-compat: unknown type still reaches on_any handlers.
            await self._fan_out_wildcard(wire_type, raw)
            return

        model = PARSER_REGISTRY.get(event_type)
        payload: typing.Any
        if model is None:
            payload = raw
        else:
            try:
                # ErrorEvent gets the raw frame attached for diagnostics.
                payload_fields = dict(raw)
                payload_fields.pop("type", None)
                if event_type is ServerMessageType.ERROR:
                    payload_fields["raw"] = raw
                payload = model.model_validate(payload_fields)
            except pydantic.ValidationError as exc:
                raise LiveTranscriptionProtocolError(
                    f"Could not parse {event_type.value} frame: {exc}"
                ) from exc

        if event_type is ServerMessageType.READY:
            self._ready.set()

        await self._fan_out(event_type, payload)
        await self._fan_out_wildcard(event_type, payload)

    async def _emit_close(self) -> None:
        if self._closed.is_set():
            return
        code = self._transport.close_code or 1000
        reason = self._transport.close_reason or ""
        payload = ClosedEvent(code=code, reason=reason)
        # Unblock anyone awaiting Ready: if we close without ever becoming
        # ready, set the event so callers fail fast rather than hanging.
        if not self._ready.is_set():
            self._ready.set()
        await self._fan_out(ServerMessageType.CLOSED, payload)
        await self._fan_out_wildcard(ServerMessageType.CLOSED, payload)
        self._closed.set()

    async def _fan_out(self, event_type: ServerMessageType, payload: typing.Any) -> None:
        for handler in list(self._handlers.get(event_type, [])):
            await self._safe_call(handler, payload)

    async def _fan_out_wildcard(
        self,
        event_type: typing.Union[ServerMessageType, str, None],
        payload: typing.Any,
    ) -> None:
        for handler in list(self._wildcard_handlers):
            await self._safe_call(handler, event_type, payload)

    async def _safe_call(self, handler: typing.Callable[..., typing.Any], *args: typing.Any) -> None:
        try:
            result = handler(*args)
            if inspect.isawaitable(result):
                await result
        except Exception as exc:
            _log.exception("Handler raised: %s", exc)
            # Surface to ErrorEvent subscribers so applications can react.
            err = ErrorEvent(
                code="handler_exception",
                message=str(exc),
                raw={"handler": getattr(handler, "__qualname__", repr(handler))},
            )
            for fn in list(self._handlers.get(ServerMessageType.ERROR, [])):
                if fn is handler:
                    continue  # avoid infinite recursion
                try:
                    res = fn(err)
                    if inspect.isawaitable(res):
                        await res
                except Exception:
                    _log.exception("Error-handler also raised; dropping")


# Live transcription runs on the dedicated realtime host, independent of the
# REST API base URL. Mirrors camb.realtime's DEFAULT_REALTIME_BASE_URL.
DEFAULT_LIVE_TRANSCRIPTION_BASE_URL = "wss://realtime.camb.ai"
_LIVE_TRANSCRIPTION_PATH = "/streaming-transcription/listen"


def _build_url(base_url: str, options: ConnectOptions) -> str:
    """Build the live transcription WSS URL from its base URL."""
    from urllib.parse import urlencode

    base = base_url.rstrip("/")
    if base.startswith("https://"):
        base = "wss://" + base[len("https://"):]
    elif base.startswith("http://"):
        base = "ws://" + base[len("http://"):]
    query = urlencode(options.to_query())
    return f"{base}{_LIVE_TRANSCRIPTION_PATH}?{query}"


async def connect(
    api_key: str,
    *,
    base_url: str = DEFAULT_LIVE_TRANSCRIPTION_BASE_URL,
    transport: typing.Optional[Transport] = None,
    extra_headers: typing.Optional[typing.Dict[str, str]] = None,
    **options: typing.Any,
) -> LiveTranscriptionSession:
    """Open a live transcription session.

    For most users the convenience accessor on ``CambAI`` is preferred:

    >>> async with client.live_transcription.connect() as session:
    ...     ...

    Parameters mirror :class:`ConnectOptions` (``model``, ``language``,
    ``encoding``, ``sample_rate``, ``channels``).
    """
    from .transport import WebsocketsTransport

    opts = ConnectOptions(**options)
    headers = {"x-api-key": api_key, **(extra_headers or {})}
    url = _build_url(base_url, opts)
    tport = transport if transport is not None else WebsocketsTransport()
    session = LiveTranscriptionSession(transport=tport, url=url, headers=headers)
    await session._open()
    return session
