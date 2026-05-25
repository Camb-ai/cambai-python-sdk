"""Exceptions raised by the live transcription client."""


class LiveTranscriptionError(Exception):
    """Base class for every exception raised by ``camb.live_transcription``."""


class LiveTranscriptionConnectError(LiveTranscriptionError):
    """The WebSocket handshake failed or the server rejected the upgrade."""


class LiveTranscriptionProtocolError(LiveTranscriptionError):
    """The server sent a frame the client could not decode or validate."""


class MicrophoneUnavailableError(LiveTranscriptionError):
    """A microphone helper was used but its optional audio dependency is missing."""
