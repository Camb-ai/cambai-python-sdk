"""Realtime translation session — one open WebSocket and its event pump."""

from __future__ import annotations

import asyncio
import base64
import inspect
import json
import logging
import typing
from urllib.parse import urlencode

import pydantic

from .errors import RealtimeConnectError, RealtimeProtocolError
from .events import (
    PARSER_REGISTRY,
    AudioDeltaEvent,
    ClosedEvent,
    ErrorEvent,
    ServerEventType,
)
from .options import ConnectOptions
from .transport import Transport, WebsocketsTransport

_log = logging.getLogger(__name__)

SESSION_READY_TIMEOUT = 90.0
DEFAULT_REALTIME_BASE_URL = "wss://realtime.camb.ai"
_REALTIME_PATH = "/v1/realtime"

Handler = typing.Callable[[typing.Any], typing.Union[None, typing.Awaitable[None]]]
WildcardHandler = typing.Callable[
    [ServerEventType, typing.Any], typing.Union[None, typing.Awaitable[None]]
]


class RealtimeSession:
    """One realtime translation connection.

    Construct via :func:`connect` or the resource client on ``CambAI``;
    direct construction is supported but the factory wires the transport
    and handles URL building.

    Typical usage::

        session = await client.realtime.connect(
            source_language="en-US",
            target_language="de-DE",
        )

        @session.on(ServerEventType.AUDIO_DELTA)
        def on_audio(event):
            play(event.data)

        async with session:
            await session.wait_until_ready()
            async for chunk in microphone:
                await session.send_audio(chunk)
    """

    def __init__(
        self,
        *,
        transport: Transport,
        url: str,
        headers: typing.Dict[str, str],
        session_payload: typing.Dict[str, typing.Any],
    ) -> None:
        self._transport = transport
        self._url = url
        self._headers = headers
        self._session_payload = session_payload
        self._handlers: typing.Dict[ServerEventType, typing.List[Handler]] = {}
        self._wildcard_handlers: typing.List[WildcardHandler] = []
        self._reader_task: typing.Optional[asyncio.Task[None]] = None
        self._closed = asyncio.Event()
        self._ready = asyncio.Event()
        self._send_lock = asyncio.Lock()
        self._is_closing = False

    # ---------------------------- lifecycle ----------------------------

    async def __aenter__(self) -> "RealtimeSession":
        await self._open()
        return self

    async def __aexit__(self, *exc: typing.Any) -> None:
        await self.close()

    async def _open(self) -> None:
        # Idempotent: the factory's connect() already calls _open; wrapping the
        # returned session in `async with session:` re-enters here and must not
        # spawn a second reader task.
        if self._reader_task is not None:
            return
        await self._transport.connect(self._url, self._headers)
        await self._transport.send_text(json.dumps(self._session_payload))
        self._reader_task = asyncio.create_task(self._read_loop())

    @property
    def is_ready(self) -> bool:
        """True once the server has sent ``session.created``."""
        return self._ready.is_set()

    @property
    def is_closed(self) -> bool:
        return self._closed.is_set()

    async def wait_until_ready(
        self, timeout: typing.Optional[float] = SESSION_READY_TIMEOUT
    ) -> None:
        """Block until the server confirms the session is active.

        ``"fast"`` mode is ready almost immediately; ``"slow"`` mode cold-boots for 30+ seconds.
        The server sends ``session.starting`` (and WebSocket keepalive pings) during that window
        to signal it is still working. Raises :class:`RealtimeConnectError` if ``timeout`` elapses
        or the socket closes before ``session.created`` arrives.

        The default covers both modes' normal cold boot, but not the first-ever session for a given
        ``voice_id``: that one additionally waits while the cloned voice is registered with the
        synthesis provider, which can take minutes and happens once per voice. This applies in
        **either** mode, because a cloned voice is always synthesized by the provider — in
        ``"fast"`` mode, passing a ``voice_id`` is what switches synthesis away from the translation
        model's own audio. Sessions without a ``voice_id`` never wait for it. Pass a larger
        ``timeout`` when you know you are in that case, rather than raising this default and making
        every voice-less session slow to fail.
        """
        try:
            await asyncio.wait_for(self._ready.wait(), timeout=timeout)
        except asyncio.TimeoutError:
            raise RealtimeConnectError(
                f"Timed out waiting for session.created after {timeout}s"
            )
        if self._closed.is_set():
            raise RealtimeConnectError(
                "WebSocket closed before the session became ready"
            )

    async def run_until_closed(self) -> None:
        """Suspend until the transport closes."""
        await self._closed.wait()

    # --------------------------- subscription --------------------------

    def on(
        self,
        event_type: ServerEventType,
        handler: typing.Optional[Handler] = None,
    ) -> typing.Any:
        """Register a handler for ``event_type``.

        Usable as a direct call (``session.on(t, fn)``) or as a decorator
        (``@session.on(t)``).
        """

        def _register(fn: Handler) -> Handler:
            self._handlers.setdefault(event_type, []).append(fn)
            return fn

        if handler is None:
            return _register
        return _register(handler)

    def off(self, event_type: ServerEventType, handler: Handler) -> None:
        if event_type in self._handlers:
            try:
                self._handlers[event_type].remove(handler)
            except ValueError:
                pass

    def on_any(self, handler: WildcardHandler) -> WildcardHandler:
        """Receive every event, including types added in future server releases."""
        self._wildcard_handlers.append(handler)
        return handler

    # ----------------------------- sending -----------------------------

    async def send_audio(self, chunk: bytes) -> None:
        """Send a raw PCM chunk to the server as a base64-encoded audio append."""
        async with self._send_lock:
            payload = json.dumps(
                {
                    "type": "input_audio_buffer.append",
                    "audio": base64.b64encode(chunk).decode(),
                }
            )
            await self._transport.send_text(payload)

    async def stream_audio(self, source: typing.AsyncIterable[bytes]) -> None:
        """Pump chunks from ``source`` into the session until it is exhausted.

        If ``source`` has a ``close()`` coroutine it is called on exit.
        """
        try:
            async for chunk in source:
                if self._closed.is_set():
                    break
                await self.send_audio(chunk)
        finally:
            close_fn = getattr(source, "close", None)
            if close_fn is not None:
                await close_fn()

    async def close(self) -> None:
        if self._is_closing or self._closed.is_set():
            return
        self._is_closing = True
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
                    # Binary frame: raw PCM from the server (optimization path).
                    event = AudioDeltaEvent(data=bytes(frame))
                    await self._fan_out(ServerEventType.AUDIO_DELTA, event)
                    await self._fan_out_wildcard(ServerEventType.AUDIO_DELTA, event)
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
            event_type = ServerEventType(wire_type)
        except ValueError:
            # Forward-compat: unknown type still reaches on_any handlers.
            await self._fan_out_wildcard(wire_type, raw)
            return

        payload: typing.Any

        if event_type is ServerEventType.AUDIO_DELTA:
            # JSON audio delta: base64-decode the delta field into raw bytes.
            try:
                data = base64.b64decode(raw.get("delta", ""))
            except Exception:
                data = b""
            payload = AudioDeltaEvent(data=data)

        elif event_type is ServerEventType.ERROR:
            # Wire format: {"type": "error", "error": {"message": "..."}}.
            # Flatten the nested object for the handler model.
            error_obj = raw.get("error", {})
            payload = ErrorEvent(
                message=error_obj.get("message", "Unknown error"),
                raw=raw,
            )

        else:
            model = PARSER_REGISTRY.get(event_type)
            if model is None:
                payload = raw
            else:
                fields = {k: v for k, v in raw.items() if k != "type"}
                try:
                    payload = model.model_validate(fields)
                except pydantic.ValidationError as exc:
                    raise RealtimeProtocolError(
                        f"Could not parse {event_type.value} frame: {exc}"
                    ) from exc

        if event_type is ServerEventType.SESSION_CREATED and not self._ready.is_set():
            self._ready.set()

        await self._fan_out(event_type, payload)
        await self._fan_out_wildcard(event_type, payload)

    async def _emit_close(self) -> None:
        if self._closed.is_set():
            return
        code = self._transport.close_code or 1000
        reason = self._transport.close_reason or ""
        payload = ClosedEvent(code=code, reason=reason)
        # Unblock wait_until_ready so callers fail fast if the socket dies
        # before the session ever becomes ready.
        if not self._ready.is_set():
            self._ready.set()
        await self._fan_out(ServerEventType.CLOSED, payload)
        await self._fan_out_wildcard(ServerEventType.CLOSED, payload)
        self._closed.set()

    async def _fan_out(
        self, event_type: ServerEventType, payload: typing.Any
    ) -> None:
        for handler in list(self._handlers.get(event_type, [])):
            await self._safe_call(handler, payload)

    async def _fan_out_wildcard(
        self,
        event_type: typing.Union[ServerEventType, str, None],
        payload: typing.Any,
    ) -> None:
        for handler in list(self._wildcard_handlers):
            await self._safe_call(handler, event_type, payload)

    async def _safe_call(
        self, handler: typing.Callable[..., typing.Any], *args: typing.Any
    ) -> None:
        try:
            result = handler(*args)
            if inspect.isawaitable(result):
                await result
        except Exception as exc:
            _log.exception("Handler raised: %s", exc)
            err = ErrorEvent(
                message=str(exc),
                raw={"handler": getattr(handler, "__qualname__", repr(handler))},
            )
            for fn in list(self._handlers.get(ServerEventType.ERROR, [])):
                if fn is handler:
                    continue
                try:
                    res = fn(err)
                    if inspect.isawaitable(res):
                        await res
                except Exception:
                    _log.exception("Error-handler also raised; dropping")


def _build_url(base_url: str, opts: ConnectOptions) -> str:
    base = base_url.rstrip("/")
    if base.startswith("https://"):
        base = "wss://" + base[len("https://"):]
    elif base.startswith("http://"):
        base = "ws://" + base[len("http://"):]
    query = urlencode(opts.to_query())
    return f"{base}{_REALTIME_PATH}?{query}"


async def connect(
    api_key: str,
    *,
    base_url: str = DEFAULT_REALTIME_BASE_URL,
    transport: typing.Optional[Transport] = None,
    extra_headers: typing.Optional[typing.Dict[str, str]] = None,
    **options: typing.Any,
) -> RealtimeSession:
    """Open a realtime translation session.

    For most users the convenience accessor on ``CambAI`` is preferred::

        async with await client.realtime.connect(
            source_language="en-US",
            target_language="de-DE",
        ) as session:
            ...

    Parameters mirror :class:`~camb.realtime.options.ConnectOptions`
    (``mode``, ``source_language``, ``target_language``, ``output_modalities``,
    ``voice_id``). An unrecognised option raises ``ValidationError`` rather than
    being ignored — notably the retired ``model`` parameter, replaced by ``mode``.
    """
    opts = ConnectOptions(**options)
    url = _build_url(base_url, opts)
    headers: typing.Dict[str, str] = extra_headers.copy() if extra_headers else {}
    session_payload: typing.Dict[str, typing.Any] = {
        "type": "session.update",
        "session": opts.to_session_payload(),
        "auth": {"api_key": api_key},
    }
    tport = transport if transport is not None else WebsocketsTransport()
    session = RealtimeSession(
        transport=tport,
        url=url,
        headers=headers,
        session_payload=session_payload,
    )
    await session._open()
    return session
