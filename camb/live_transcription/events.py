"""Typed server events emitted over the live transcription WebSocket.

Adding a new server event requires exactly three edits:

1. Add a member to :class:`ServerMessageType`.
2. Define a payload model below.
3. Register the pair in :data:`PARSER_REGISTRY` so the session dispatcher
   can build the typed payload for handlers.
"""

from __future__ import annotations

import enum
import typing

import pydantic


class ServerMessageType(str, enum.Enum):
    """Stable identifiers for every event the client may dispatch to handlers."""

    READY = "Ready"
    RESULTS = "Results"
    FINAL = "Final"
    ERROR = "Error"
    CLOSED = "Closed"


class _LiveModel(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(extra="allow")


class ReadyEvent(_LiveModel):
    """Emitted once the upstream transcription session is accepting audio."""


class Word(_LiveModel):
    word: str
    start: float
    end: float
    confidence: float


class Alternative(_LiveModel):
    transcript: str = ""
    confidence: float = 0.0
    words: typing.List[Word] = pydantic.Field(default_factory=list)


class Channel(_LiveModel):
    alternatives: typing.List[Alternative] = pydantic.Field(default_factory=list)


class ModelInfo(_LiveModel):
    name: typing.Optional[str] = None
    version: typing.Optional[str] = None


class Metadata(_LiveModel):
    request_id: typing.Optional[str] = None
    model_uuid: typing.Optional[str] = None
    model_info: typing.Optional[ModelInfo] = None


class ResultsEvent(_LiveModel):
    """Cumulative transcript for the current utterance.

    Each event carries the full transcript so far, so replace your
    in-progress UI state with ``transcript`` rather than concatenating.
    ``is_final`` is ``False`` for interim refinements and ``True`` on the
    frame that finalizes the utterance; after a final the next event
    begins a new utterance from scratch, so commit the text when
    ``is_final`` is ``True`` to keep finished utterances.
    """

    is_final: bool = False
    start: float = 0.0
    duration: float = 0.0
    channel: Channel
    metadata: typing.Optional[Metadata] = None

    @property
    def transcript(self) -> str:
        if not self.channel.alternatives:
            return ""
        return self.channel.alternatives[0].transcript

    @property
    def confidence(self) -> float:
        if not self.channel.alternatives:
            return 0.0
        return self.channel.alternatives[0].confidence

    @property
    def words(self) -> typing.List[Word]:
        if not self.channel.alternatives:
            return []
        return self.channel.alternatives[0].words


class FinalEvent(ResultsEvent):
    """Reserved for a future server release that emits ``is_final=True``.

    The current backend never emits this. It is wired so applications can
    register a handler today without refactoring when finals ship.
    """

    is_final: bool = True


class ErrorEvent(_LiveModel):
    """Server-reported error. The connection closes immediately after."""

    code: typing.Optional[str] = None
    message: str
    raw: typing.Dict[str, typing.Any] = pydantic.Field(default_factory=dict)


class ClosedEvent(_LiveModel):
    """Synthetic event the SDK emits when the transport closes."""

    code: int
    reason: str = ""


PARSER_REGISTRY: typing.Dict[ServerMessageType, typing.Type[_LiveModel]] = {
    ServerMessageType.READY: ReadyEvent,
    ServerMessageType.RESULTS: ResultsEvent,
    ServerMessageType.FINAL: FinalEvent,
    ServerMessageType.ERROR: ErrorEvent,
    ServerMessageType.CLOSED: ClosedEvent,
}
"""Single source of truth mapping wire ``type`` strings to payload models."""
