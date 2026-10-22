"""Both directions of one call, each translating into the language the other one speaks."""

from __future__ import annotations

import asyncio
import logging
import typing

from .events import (
    ServerEventType,
    SessionCreatedEvent,
    SessionUpdatedEvent,
    SourceLanguageChangedEvent,
)
from .options import AUTOMATIC_SOURCE_LANGUAGE, SpeakerSetup
from .session import (
    DEFAULT_REALTIME_BASE_URL,
    SESSION_READY_TIMEOUT,
    RealtimeSession,
    _create_session,
)
from .transport import Transport

_log = logging.getLogger(__name__)


class RealtimeSessionPair:
    """The two directions of one call, linked so each translates into the other's language.

    ``local_speaker_session`` carries the local microphone and ``other_party_session`` the other
    party's audio. Whenever one session's source language becomes known or changes, the pair sets
    it as the other session's target language, so each side hears the other in its own language.

    Everything else is done on the sessions themselves: sending audio, handling events, and
    confirming a ``SOURCE_LANGUAGE_SWITCH_CONFIRMATION_REQUESTED`` with
    ``update_languages(source_language=...)``. A confirmed switch is a source language change
    like any other, so the pair passes it on to the other session too.

    Usage::

        pair = await client.realtime.connect_session_pair(mode="slow")
        async with pair:
            await pair.wait_until_ready()
            await asyncio.gather(
                pair.local_speaker_session.stream_audio(microphone),
                pair.other_party_session.stream_audio(call_audio),
            )
    """

    def __init__(
        self,
        *,
        local_speaker_session: RealtimeSession,
        other_party_session: RealtimeSession,
    ) -> None:
        self.local_speaker_session = local_speaker_session
        self.other_party_session = other_party_session
        self._language_links = (
            _SourceLanguageToTargetLanguageLink(
                speaking_session=local_speaker_session, listening_session=other_party_session
            ),
            _SourceLanguageToTargetLanguageLink(
                speaking_session=other_party_session, listening_session=local_speaker_session
            ),
        )

    async def __aenter__(self) -> "RealtimeSessionPair":
        return self

    async def __aexit__(self, *exc: typing.Any) -> None:
        await self.close()

    async def wait_until_ready(
        self, timeout: typing.Optional[float] = SESSION_READY_TIMEOUT
    ) -> None:
        """Block until both sessions are ready; see :meth:`RealtimeSession.wait_until_ready`."""
        await asyncio.gather(
            self.local_speaker_session.wait_until_ready(timeout),
            self.other_party_session.wait_until_ready(timeout),
        )

    async def close(self) -> None:
        await asyncio.gather(self.local_speaker_session.close(), self.other_party_session.close())


class _SourceLanguageToTargetLanguageLink:
    """Keeps ``listening_session``'s target language equal to ``speaking_session``'s source.

    The source language is known once the speaking session reports it (or was opened with a fixed
    one); it is passed on as soon as the listening session is ready to take a change.
    """

    def __init__(
        self, *, speaking_session: RealtimeSession, listening_session: RealtimeSession
    ) -> None:
        self._speaking_session = speaking_session
        self._listening_session = listening_session
        self._speaking_session_language: typing.Optional[str] = None
        self._listening_session_target_language: typing.Optional[str] = None
        speaking_session.on(ServerEventType.SESSION_CREATED, self._on_speaking_session_created)
        speaking_session.on(
            ServerEventType.SOURCE_LANGUAGE_CHANGED, self._on_speaking_session_language_changed
        )
        listening_session.on(ServerEventType.SESSION_CREATED, self._on_listening_session_created)
        listening_session.on(ServerEventType.SESSION_UPDATED, self._on_listening_session_updated)

    async def _on_speaking_session_created(self, event: SessionCreatedEvent) -> None:
        if event.session.source_language != AUTOMATIC_SOURCE_LANGUAGE:
            self._speaking_session_language = event.session.source_language
            await self._pass_on_speaking_session_language()

    async def _on_speaking_session_language_changed(
        self, event: SourceLanguageChangedEvent
    ) -> None:
        self._speaking_session_language = event.language
        await self._pass_on_speaking_session_language()

    async def _on_listening_session_created(self, event: SessionCreatedEvent) -> None:
        self._listening_session_target_language = event.session.target_language
        await self._pass_on_speaking_session_language()

    def _on_listening_session_updated(self, event: SessionUpdatedEvent) -> None:
        self._listening_session_target_language = event.session.target_language

    async def _pass_on_speaking_session_language(self) -> None:
        language = self._speaking_session_language
        if (
            language is None
            or not self._listening_session.is_ready
            or self._listening_session.is_closed
            or _is_same_language_code(language, self._listening_session_target_language)
        ):
            return
        self._listening_session_target_language = language
        try:
            await self._listening_session.update_languages(target_language=language)
        except Exception:
            # The listening session closing mid-send is the usual cause; its own close event
            # reports that. Raising here would only surface as a handler error on the other session.
            _log.warning("Could not set the other session's target language to %s", language, exc_info=True)


def _is_same_language_code(
    first_language_code: str, second_language_code: typing.Optional[str]
) -> bool:
    return second_language_code is not None and (
        first_language_code.replace("_", "-").lower() == second_language_code.replace("_", "-").lower()
    )


def _direction_options(
    shared_options: typing.Mapping[str, typing.Any],
    direction_options: typing.Optional[typing.Mapping[str, typing.Any]],
    default_speaker_setup: SpeakerSetup,
) -> typing.Dict[str, typing.Any]:
    options: typing.Dict[str, typing.Any] = {
        "source_language": AUTOMATIC_SOURCE_LANGUAGE,
        **shared_options,
        **(direction_options or {}),
    }
    if options["source_language"] == AUTOMATIC_SOURCE_LANGUAGE:
        options.setdefault("speaker_setup", default_speaker_setup)
    return options


async def connect_session_pair(
    api_key: str,
    *,
    local_speaker: typing.Optional[typing.Mapping[str, typing.Any]] = None,
    other_party: typing.Optional[typing.Mapping[str, typing.Any]] = None,
    base_url: str = DEFAULT_REALTIME_BASE_URL,
    transport_factory: typing.Optional[typing.Callable[[], Transport]] = None,
    extra_headers: typing.Optional[typing.Dict[str, str]] = None,
    **shared_options: typing.Any,
) -> RealtimeSessionPair:
    """Open both directions of a call as a :class:`RealtimeSessionPair`.

    ``shared_options`` (e.g. ``mode``, ``output_modalities``) apply to both sessions;
    ``local_speaker`` and ``other_party`` override them per direction (e.g. ``voice_id``,
    ``source_language_candidates``). Both directions detect their source language unless given
    one. The local speaker defaults to ``speaker_setup="single_known_speaker"`` and the other party
    to ``"changing_speakers"``. Options are those of
    :class:`~camb.realtime.options.ConnectOptions`.
    """
    sessions = [
        _create_session(
            api_key,
            base_url=base_url,
            transport=transport_factory() if transport_factory is not None else None,
            extra_headers=extra_headers,
            **_direction_options(shared_options, direction_options, default_speaker_setup),
        )
        for direction_options, default_speaker_setup in (
            (local_speaker, SpeakerSetup.SINGLE_KNOWN_SPEAKER),
            (other_party, SpeakerSetup.CHANGING_SPEAKERS),
        )
    ]
    session_pair = RealtimeSessionPair(
        local_speaker_session=sessions[0], other_party_session=sessions[1]
    )
    # Both opens run to completion before deciding, so a session still connecting when the other
    # fails cannot finish connecting after the pair was closed and leak its socket.
    open_results = await asyncio.gather(
        *(session._open() for session in sessions), return_exceptions=True
    )
    open_failure = next(
        (result for result in open_results if isinstance(result, BaseException)), None
    )
    if open_failure is not None:
        await session_pair.close()
        raise open_failure
    return session_pair
