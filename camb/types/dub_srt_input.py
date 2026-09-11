import typing

import pydantic

from ..core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel


class DubSRTInput(UniversalBaseModel):
    """Inline SRT text, not a filename, URL, or base64-encoded file.

    Read files with ``Path(...).read_text(encoding="utf-8")``.
    SRT parsing and byte-size limits are enforced by the API.
    """

    content: str
    format: typing.Literal["srt"] = "srt"

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="forbid", frozen=True)
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.forbid
