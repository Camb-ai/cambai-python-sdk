"""Resource client exposed as :attr:`CambAI.live_transcription`."""

from __future__ import annotations

import typing

from ..core.client_wrapper import SyncClientWrapper
from .errors import LiveTranscriptionConnectError
from .session import (
    DEFAULT_LIVE_TRANSCRIPTION_BASE_URL,
    LiveTranscriptionSession,
    connect as _connect,
)


class LiveTranscriptionClient:
    """Entry point for the WebSocket live transcription stream.

    Usage::

        from camb.client import CambAI
        from camb.live_transcription import ServerMessageType

        client = CambAI(api_key="...")
        async with await client.live_transcription.connect() as session:
            @session.on(ServerMessageType.RESULTS)
            def _(msg):
                print(msg.transcript)
            await session.run_until_closed()
    """

    def __init__(self, *, client_wrapper: SyncClientWrapper) -> None:
        self._client_wrapper = client_wrapper

    async def connect(self, **options: typing.Any) -> LiveTranscriptionSession:
        api_key = self._client_wrapper.api_key
        if not api_key:
            raise LiveTranscriptionConnectError(
                "CambAI was constructed without an api_key; cannot open a live transcription stream."
            )
        return await _connect(
            api_key=api_key,
            base_url=DEFAULT_LIVE_TRANSCRIPTION_BASE_URL,
            extra_headers=self._client_wrapper.get_custom_headers(),
            **options,
        )
