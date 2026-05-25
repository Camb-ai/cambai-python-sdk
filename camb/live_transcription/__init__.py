"""Live transcription WebSocket client.

This package wraps the ``/apis/transcription/listen`` WebSocket endpoint
documented in ``public_docs/api-reference/websockets/listen.mdx``.

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

from .audio_source import AudioSource, FileAudioSource
from .client import LiveTranscriptionClient
from .errors import (
    LiveTranscriptionConnectError,
    LiveTranscriptionError,
    LiveTranscriptionProtocolError,
    MicrophoneUnavailableError,
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
from .microphone import Microphone
from .options import ConnectOptions, Encoding
from .session import LiveTranscriptionSession, connect

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
    "MicrophoneUnavailableError",
    "ModelInfo",
    "PARSER_REGISTRY",
    "ReadyEvent",
    "ResultsEvent",
    "ServerMessageType",
    "Word",
    "connect",
]
