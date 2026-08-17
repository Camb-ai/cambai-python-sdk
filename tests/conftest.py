"""Shared test doubles: an in-memory WebSocket transport.

The session classes only depend on the ``Transport`` protocol, so a fake
transport can drive the full event pipeline without any network access.
"""

from __future__ import annotations

import json
import typing

import pytest


class FakeTransport:
    """In-memory :class:`Transport` that records sends and replays frames.

    Frames are yielded exactly once; the read loop then terminates and the
    session emits its synthetic ``Closed`` event. Pass ``hold_open=True`` to
    keep the iterator running (for timeout tests).
    """

    def __init__(
        self,
        frames: typing.Optional[typing.List[typing.Union[str, bytes]]] = None,
        *,
        hold_open: bool = False,
    ) -> None:
        self._frames = list(frames or [])
        self._hold_open = hold_open
        self.sent_text: typing.List[str] = []
        self.sent_bytes: typing.List[bytes] = []
        self.connected_url: typing.Optional[str] = None
        self.connected_headers: typing.Optional[typing.Dict[str, str]] = None
        self.closed_codes: typing.List[int] = []
        self._close_code: typing.Optional[int] = None
        self._close_reason = ""

    async def connect(self, url: str, headers: typing.Dict[str, str]) -> None:
        self.connected_url = url
        self.connected_headers = headers

    async def send_bytes(self, data: bytes) -> None:
        self.sent_bytes.append(data)

    async def send_text(self, data: str) -> None:
        self.sent_text.append(data)

    def __aiter__(self) -> typing.AsyncIterator[typing.Union[str, bytes]]:
        return self._iter()

    async def _iter(self) -> typing.AsyncIterator[typing.Union[str, bytes]]:
        for frame in self._frames:
            yield frame
        while self._hold_open:
            import asyncio

            await asyncio.sleep(3600)

    async def close(self, code: int = 1000) -> None:
        self.closed_codes.append(code)
        self._close_code = code

    @property
    def close_code(self) -> typing.Optional[int]:
        return self._close_code

    @property
    def close_reason(self) -> typing.Optional[str]:
        return self._close_reason


def json_frame(**fields: typing.Any) -> str:
    return json.dumps(fields)


@pytest.fixture
def fake_transport() -> typing.Callable[..., FakeTransport]:
    return lambda *args, **kwargs: FakeTransport(*args, **kwargs)