"""WebSocket transport abstraction.

The session does not import ``websockets`` directly; it talks to
:class:`Transport`. Swapping transports (for tests, mocks, alternative
libraries) is therefore a one-line change at construction.
"""

from __future__ import annotations

import typing

from .errors import LiveTranscriptionConnectError


class Transport(typing.Protocol):
    """Minimum surface a WebSocket implementation must expose."""

    async def connect(self, url: str, headers: typing.Dict[str, str]) -> None: ...

    async def send_bytes(self, data: bytes) -> None: ...

    async def send_text(self, data: str) -> None: ...

    def __aiter__(self) -> typing.AsyncIterator[typing.Union[str, bytes]]: ...

    async def close(self, code: int = 1000) -> None: ...

    @property
    def close_code(self) -> typing.Optional[int]: ...

    @property
    def close_reason(self) -> typing.Optional[str]: ...


class WebsocketsTransport:
    """Default :class:`Transport` backed by the ``websockets`` library."""

    def __init__(self) -> None:
        self._ws: typing.Any = None
        self._close_code: typing.Optional[int] = None
        self._close_reason: typing.Optional[str] = None

    async def connect(self, url: str, headers: typing.Dict[str, str]) -> None:
        try:
            import websockets
        except ImportError as exc:  # pragma: no cover
            raise LiveTranscriptionConnectError(
                "The 'websockets' package is required for live transcription."
            ) from exc

        try:
            # websockets >=12 prefers ``additional_headers``; older releases use
            # ``extra_headers``. Try the modern kwarg first and fall back.
            try:
                self._ws = await websockets.connect(url, additional_headers=headers)
            except TypeError:
                self._ws = await websockets.connect(url, extra_headers=headers)
        except Exception as exc:
            raise LiveTranscriptionConnectError(str(exc)) from exc

    async def send_bytes(self, data: bytes) -> None:
        await self._ws.send(data)

    async def send_text(self, data: str) -> None:
        await self._ws.send(data)

    def __aiter__(self) -> typing.AsyncIterator[typing.Union[str, bytes]]:
        return self._iter()

    async def _iter(self) -> typing.AsyncIterator[typing.Union[str, bytes]]:
        try:
            async for frame in self._ws:
                yield frame
        except Exception as exc:
            try:
                import websockets.exceptions as _ws_exc

                if isinstance(exc, _ws_exc.ConnectionClosed):
                    self._close_code = exc.code
                    self._close_reason = exc.reason or ""
                    return
            except ImportError:  # pragma: no cover
                pass
            raise

    async def close(self, code: int = 1000) -> None:
        if self._ws is not None:
            await self._ws.close(code=code)
            self._close_code = code

    @property
    def close_code(self) -> typing.Optional[int]:
        return self._close_code

    @property
    def close_reason(self) -> typing.Optional[str]:
        return self._close_reason
