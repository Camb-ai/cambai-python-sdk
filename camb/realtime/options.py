"""Connection options for the realtime WebSocket."""

from __future__ import annotations

import enum
import typing

import pydantic


class RealtimeModel(str, enum.Enum):
    LILAC = "lilac"
    VIOLET = "violet"
    IRIS = "iris"
    ORCHID = "orchid"


class OutputModality(str, enum.Enum):
    TEXT = "text"
    AUDIO = "audio"


class ConnectOptions(pydantic.BaseModel):
    """Options for a realtime translation session.

    ``source_language`` and ``target_language`` are required; all other fields
    have server-side defaults.

    Language values use IETF BCP-47 tags (e.g. ``"en-US"``, ``"de-DE"``).
    """

    model: RealtimeModel = RealtimeModel.IRIS
    source_language: str
    target_language: str
    output_modalities: typing.List[OutputModality] = pydantic.Field(
        default_factory=lambda: [OutputModality.TEXT, OutputModality.AUDIO]
    )
    voice_id: typing.Optional[int] = None
    """Synthesize the translation with one of your cloned voices.

    Pass the ID of a voice you own (from ``client.voice_cloning.list_voices()``
    or a custom voice you created). When omitted, a built-in voice for
    ``target_language`` is used.

    For the most natural-sounding results, choose a voice whose reference
    language matches ``target_language``.
    """

    def to_query(self) -> typing.Dict[str, str]:
        """Query-string parameters sent on the WebSocket upgrade URL."""
        return {"model": self.model.value}

    def to_session_payload(self) -> typing.Dict[str, typing.Any]:
        """Body of the ``session.update`` message sent after the WS handshake."""
        session: typing.Dict[str, typing.Any] = {
            "model": self.model.value,
            "source_language": self.source_language,
            "target_language": self.target_language,
            "output_modalities": [m.value for m in self.output_modalities],
        }
        if self.voice_id is not None:
            session["voice"] = {"type": "cloned", "voice_id": self.voice_id}
        return session
