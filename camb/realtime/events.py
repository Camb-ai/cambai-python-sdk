"""Typed server events emitted over the realtime WebSocket.

Adding a new server event requires exactly three edits:

1. Add a member to :class:`ServerEventType`.
2. Define a payload model below.
3. Register the pair in :data:`PARSER_REGISTRY` (or add manual handling in
   ``RealtimeSession._dispatch`` for events that need transformation, such as
   ``AUDIO_DELTA`` and ``ERROR``).
"""

from __future__ import annotations

import enum
import typing

import pydantic


class ServerEventType(str, enum.Enum):
    """Stable identifiers for every event the client may dispatch to handlers."""

    SESSION_STARTING = "session.starting"
    SESSION_CREATED = "session.created"
    SESSION_UPDATED = "session.updated"
    TRANSCRIPT_DELTA = "conversation.item.input_audio_transcription.delta"
    TRANSCRIPT_COMPLETED = "conversation.item.input_audio_transcription.completed"
    TEXT_DELTA = "response.text.delta"
    TEXT_DONE = "response.text.done"
    # Synthetic, like CLOSED: the server frames output audio as raw binary WebSocket frames, never
    # as a JSON event. The read loop turns each binary frame into this event. _dispatch also accepts
    # a base64 JSON form under this name, which no server version sends — kept only so a future
    # server could introduce it without breaking older clients.
    AUDIO_DELTA = "response.audio.delta"
    AUDIO_DONE = "response.audio.done"
    ERROR = "error"
    # Synthetic — emitted by the SDK when the transport closes, never sent by server.
    CLOSED = "Closed"


class _RealtimeModel(pydantic.BaseModel):
    # `populate_by_name` so a field carrying a `validation_alias` (see `SessionInfo.mode`) can still
    # be constructed by its own name — tests and callers building these directly rely on it.
    model_config = pydantic.ConfigDict(extra="allow", populate_by_name=True)


class SessionStartingEvent(_RealtimeModel):
    """Emitted early during pipeline boot so clients can show a loading indicator.

    No payload beyond the event type. The session is not yet ready to accept
    audio; wait for :class:`SessionCreatedEvent` (or ``session.wait_until_ready()``)
    before sending audio.
    """


class SessionInfo(_RealtimeModel):
    id: str
    # Reads `mode`, falling back to the retired `model` key a pre-rename server sends.
    #
    # This field being *required* is what made the rename a hard break in the first place: a
    # server that stopped sending `model` did not leave this attribute unset, it failed the whole
    # `session.created` parse, which kills the reader task and closes the socket — surfacing as an
    # unexplained connection error. The alias makes this SDK parse either server, so an SDK and a
    # server on different sides of the rename no longer have to be deployed in lockstep.
    mode: str = pydantic.Field(validation_alias=pydantic.AliasChoices("mode", "model"))
    source_language: str
    target_language: str
    output_modalities: typing.List[str] = pydantic.Field(default_factory=list)
    # Resolved voice, e.g. {"type": "cloned", "voice_id": 123}. Omitted by the server (``None``
    # here) when the default built-in voice is used.
    voice: typing.Optional[typing.Dict[str, typing.Any]] = None


class SessionConfig(_RealtimeModel):
    mode: typing.Optional[str] = None
    source_language: str
    target_language: str
    output_modalities: typing.List[str] = pydantic.Field(default_factory=list)
    voice: typing.Optional[typing.Dict[str, typing.Any]] = None


class SessionCreatedEvent(_RealtimeModel):
    """The session has been authorised and the pipeline is ready to accept audio."""

    session: SessionInfo


class SessionUpdatedEvent(_RealtimeModel):
    """Echo of the session configuration, sent immediately after ``session.created``."""

    session: SessionConfig


class TranscriptDeltaEvent(_RealtimeModel):
    """Incremental transcript of what the user is saying, in the source language.

    Deltas are additive within one utterance and reset after the corresponding
    :class:`TranscriptCompletedEvent`. This is the live source-transcript stream — the counterpart
    to :class:`TextDeltaEvent`, which carries the translation.
    """

    delta: str


class TranscriptCompletedEvent(_RealtimeModel):
    """Final transcript for the most recent user utterance."""

    transcript: str


class TextDeltaEvent(_RealtimeModel):
    """Incremental translated text.

    Deltas are additive within one response; the accumulated text resets
    after the corresponding :class:`TextDoneEvent`.
    """

    delta: str


class TextDoneEvent(_RealtimeModel):
    """Complete translated text for the current response."""

    text: str


class AudioDeltaEvent(_RealtimeModel):
    """Synthesized output audio chunk.

    ``data`` always contains raw PCM bytes regardless of whether the server
    delivered them as a binary WebSocket frame or a base64-encoded JSON delta.
    This normalisation happens inside the session dispatcher before the event
    reaches handlers.
    """

    data: bytes


class AudioDoneEvent(_RealtimeModel):
    """The current synthesized audio response is complete."""


class ErrorEvent(_RealtimeModel):
    """Structured error from the server, or a handler exception surfaced by the SDK."""

    message: str
    raw: typing.Dict[str, typing.Any] = pydantic.Field(default_factory=dict)


class ClosedEvent(_RealtimeModel):
    """Synthetic event emitted by the SDK when the transport closes."""

    code: int
    reason: str = ""


# AUDIO_DELTA and ERROR are intentionally absent — they need transformation
# (base64 decode and nested-object flattening respectively) before the model
# can be constructed, so RealtimeSession._dispatch handles them manually.
PARSER_REGISTRY: typing.Dict[ServerEventType, typing.Optional[typing.Type[_RealtimeModel]]] = {
    ServerEventType.SESSION_STARTING: SessionStartingEvent,
    ServerEventType.SESSION_CREATED: SessionCreatedEvent,
    ServerEventType.SESSION_UPDATED: SessionUpdatedEvent,
    ServerEventType.TRANSCRIPT_DELTA: TranscriptDeltaEvent,
    ServerEventType.TRANSCRIPT_COMPLETED: TranscriptCompletedEvent,
    ServerEventType.TEXT_DELTA: TextDeltaEvent,
    ServerEventType.TEXT_DONE: TextDoneEvent,
    ServerEventType.AUDIO_DONE: AudioDoneEvent,
    ServerEventType.CLOSED: ClosedEvent,
}
"""Single source of truth mapping wire ``type`` strings to payload models."""
