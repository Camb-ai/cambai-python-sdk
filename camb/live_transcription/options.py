"""Connection options for the live transcription WebSocket."""

from __future__ import annotations

import enum
import typing

import pydantic


class Encoding(str, enum.Enum):
    LINEAR16 = "linear16"
    LINEAR32 = "linear32"
    ALAW = "alaw"
    MULAW = "mulaw"


class ConnectOptions(pydantic.BaseModel):
    """Query-string options sent on the WebSocket upgrade.

    Defaults match the server-side defaults documented in the AsyncAPI
    spec under ``api-reference/websockets/asyncapi.json``. Every field is
    optional; omit any to let the server fall back to its default.
    """

    model: str = "boli-v5"
    language: str = "en-us"
    encoding: Encoding = Encoding.LINEAR16
    sample_rate: int = 16000
    channels: int = 1

    def to_query(self) -> typing.Dict[str, str]:
        return {
            "model": self.model,
            "language": self.language,
            "encoding": self.encoding.value,
            "sample_rate": str(self.sample_rate),
            "channels": str(self.channels),
        }
