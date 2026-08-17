"""Live transcription WebSocket client.

This package wraps the ``wss://realtime.camb.ai/streaming-transcription/listen``
WebSocket endpoint documented in
``public_docs/api-reference/websockets/listen.mdx``.

Quick start::

    import asyncio
    from camb.client import CambAI
    from camb.live_transcription import Microphone, ServerMessageType

    async def main():
        client = CambAI(api_key="...")
        session = await client.live_transcription.connect()

        @session.on(ServerMessageType.RESULTS)
        def _(msg):
            print(msg.transcript)

        async with session:
            mic = Microphone()
            await session.stream_audio(mic)

    asyncio.run(main())
"""

from __future__ import annotations

import typing

from .audio_source import AudioSource, FileAudioSource
from .client import LiveTranscriptionClient
from .errors import (
    LiveTranscriptionConnectError,
    LiveTranscriptionError,
    LiveTranscriptionProtocolError,
)
from .events import (
    Alternative,
    Channel,
    ClosedEvent,
    ErrorEvent,
    FinalEvent,
    Metadata,
    ModelInfo,
    PARSER_REGISTRY,
    ReadyEvent,
    ResultsEvent,
    ServerMessageType,
    Word,
)
from .options import ConnectOptions, Encoding
from .session import LiveTranscriptionSession, connect


def __getattr__(attr_name: str) -> typing.Any:
    # Imported lazily: ``Microphone`` requires ``sounddevice`` (and PortAudio),
    # so only pull it in when actually referenced. Importing the package must
    # work on machines without audio hardware (e.g. CI, file-streaming servers).
    if attr_name == "Microphone":
        from .microphone import Microphone

        return Microphone
    raise AttributeError(f"module {__name__!r} has no attribute {attr_name!r}")


def __dir__() -> typing.List[str]:
    return sorted(set(globals()) | {"Microphone"})

__all__ = [
    "Alternative",
    "AudioSource",
    "Channel",
    "ClosedEvent",
    "ConnectOptions",
    "Encoding",
    "ErrorEvent",
    "FileAudioSource",
    "FinalEvent",
    "LiveTranscriptionClient",
    "LiveTranscriptionConnectError",
    "LiveTranscriptionError",
    "LiveTranscriptionProtocolError",
    "LiveTranscriptionSession",
    "Metadata",
    "Microphone",
    "ModelInfo",
    "PARSER_REGISTRY",
    "ReadyEvent",
    "ResultsEvent",
    "ServerMessageType",
    "Word",
    "connect",
]
