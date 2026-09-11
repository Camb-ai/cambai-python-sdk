import typing

from .dub_srt_input import DubSRTInput


class DubTargetSRTInput(DubSRTInput):
    """Translated SRT text for one requested target language.

    Language accepts a numeric ID or locale tag (for example ``"es-es"``).
    """

    language: typing.Union[int, str]
