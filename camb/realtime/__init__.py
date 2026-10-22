"""Realtime speech-to-speech translation WebSocket client.

This package wraps the ``/v1/realtime`` WebSocket endpoint documented in the
AsyncAPI spec under ``realtime.camb.ai``.

Quick start::

    import asyncio
    from camb import CambAI
    from camb.realtime import ServerEventType
    from camb.live_transcription import Microphone

    async def main():
        client = CambAI(api_key="...")
        session = await client.realtime.connect(
            source_language="en-US",
            target_language="de-DE",
        )

        @session.on(ServerEventType.SESSION_STARTING)
        def _(_):
            print("Booting pipeline...")

        @session.on(ServerEventType.AUDIO_DELTA)
        def _(event):
            play_audio(event.data)

        @session.on(ServerEventType.TEXT_DONE)
        def _(event):
            print("Translation:", event.text)

        async with session:
            await session.wait_until_ready()
            mic = Microphone(sample_rate=24000)
            await session.stream_audio(mic)

    asyncio.run(main())
"""

from .client import RealtimeClient
from .errors import (
    RealtimeConnectError,
    RealtimeError,
    RealtimeProtocolError,
)
from .events import (
    AudioDeltaEvent,
    AudioDoneEvent,
    ClosedEvent,
    ErrorEvent,
    PARSER_REGISTRY,
    ServerEventType,
    SessionConfig,
    SessionCreatedEvent,
    SessionInfo,
    SessionStartingEvent,
    SessionUpdatedEvent,
    SourceLanguageChangedEvent,
    SourceLanguageSwitchConfirmationRequestedEvent,
    TextDeltaEvent,
    TextDoneEvent,
    TranscriptCompletedEvent,
    TranscriptDeltaEvent,
)
from .options import (
    AUTOMATIC_SOURCE_LANGUAGE,
    LEGACY_ENGINE_CODENAMES,
    ConnectOptions,
    OutputModality,
    RealtimeMode,
    SpeakerSetup,
    resolve_mode,
)
from .session import RealtimeSession, connect
from .session_pair import RealtimeSessionPair, connect_session_pair

__all__ = [
    "AUTOMATIC_SOURCE_LANGUAGE",
    "AudioDeltaEvent",
    "AudioDoneEvent",
    "ClosedEvent",
    "ConnectOptions",
    "ErrorEvent",
    "LEGACY_ENGINE_CODENAMES",
    "OutputModality",
    "PARSER_REGISTRY",
    "RealtimeClient",
    "RealtimeConnectError",
    "RealtimeError",
    "RealtimeMode",
    "RealtimeProtocolError",
    "RealtimeSession",
    "RealtimeSessionPair",
    "ServerEventType",
    "SessionConfig",
    "SessionCreatedEvent",
    "SessionInfo",
    "SessionStartingEvent",
    "SessionUpdatedEvent",
    "SourceLanguageChangedEvent",
    "SourceLanguageSwitchConfirmationRequestedEvent",
    "SpeakerSetup",
    "TextDeltaEvent",
    "TextDoneEvent",
    "TranscriptCompletedEvent",
    "TranscriptDeltaEvent",
    "connect",
    "connect_session_pair",
    "resolve_mode",
]
