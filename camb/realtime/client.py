"""Resource client exposed as :attr:`CambAI.realtime`."""

from __future__ import annotations

import typing

from ..core.client_wrapper import SyncClientWrapper
from .errors import RealtimeConnectError
from .session import (
    DEFAULT_REALTIME_BASE_URL,
    RealtimeSession,
    connect as _connect,
)
from .session_pair import RealtimeSessionPair, connect_session_pair as _connect_session_pair
from .transport import Transport


class RealtimeClient:
    """Entry point for the realtime speech translation WebSocket.

    Usage::

        from camb import CambAI
        from camb.realtime import ServerEventType

        client = CambAI(api_key="...")
        session = await client.realtime.connect(
            source_language="en-US",
            target_language="de-DE",
        )

        @session.on(ServerEventType.AUDIO_DELTA)
        def on_audio(event):
            play(event.data)

        async with session:
            await session.wait_until_ready()
            async for chunk in microphone:
                await session.send_audio(chunk)
    """

    def __init__(
        self,
        *,
        client_wrapper: SyncClientWrapper,
        realtime_base_url: typing.Optional[str] = None,
    ) -> None:
        self._client_wrapper = client_wrapper

    async def connect(
        self,
        *,
        transport: typing.Optional[Transport] = None,
        **options: typing.Any,
    ) -> RealtimeSession:
        """Open a realtime translation session.

        Keyword arguments are forwarded to
        :class:`~camb.realtime.options.ConnectOptions`:

        - ``source_language`` *(required)* — IETF BCP-47 tag, e.g. ``"en-US"``, or ``"auto"`` to
          detect it (``"slow"`` mode)
        - ``target_language`` — IETF BCP-47 tag, e.g. ``"de-DE"``; required unless
          ``source_language`` is ``"auto"``
        - ``speaker_setup``, ``source_language_candidates`` — tune automatic detection; see
          :class:`~camb.realtime.options.ConnectOptions`
        - ``mode`` — ``"fast"`` (default) or ``"slow"``; see
          :class:`~camb.realtime.options.RealtimeMode` for the latency/quality tradeoff
        - ``output_modalities`` — list of ``"text"`` and/or ``"audio"`` (default: both)
        - ``voice_id`` — ID of one of your cloned voices to synthesize the
          translation with (default: a built-in voice for ``target_language``)

        Returns an open :class:`~camb.realtime.session.RealtimeSession`.  The
        session is not yet ready to accept audio; call
        ``await session.wait_until_ready()`` (or register a
        ``ServerEventType.SESSION_CREATED`` handler) before sending audio.
        """
        return await _connect(
            api_key=self._api_key(),
            base_url=DEFAULT_REALTIME_BASE_URL,
            transport=transport,
            extra_headers=self._client_wrapper.get_custom_headers(),
            **options,
        )

    async def connect_session_pair(
        self,
        *,
        local_speaker: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        other_party: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        transport_factory: typing.Optional[typing.Callable[[], Transport]] = None,
        **shared_options: typing.Any,
    ) -> RealtimeSessionPair:
        """Open both directions of a call, each translating into the language the other speaks.

        Both sessions detect their source language, and whenever one changes, it becomes the other
        session's target language. Keyword arguments other than ``local_speaker`` and
        ``other_party`` apply to both sessions; those two override them per direction. See
        :func:`~camb.realtime.session_pair.connect_session_pair`.

        Example::

            pair = await client.realtime.connect_session_pair(
                mode="slow",
                local_speaker={"source_language_candidates": ["en-US", "de-DE"]},
            )
        """
        return await _connect_session_pair(
            self._api_key(),
            local_speaker=local_speaker,
            other_party=other_party,
            base_url=DEFAULT_REALTIME_BASE_URL,
            transport_factory=transport_factory,
            extra_headers=self._client_wrapper.get_custom_headers(),
            **shared_options,
        )

    def _api_key(self) -> str:
        api_key = self._client_wrapper.api_key
        if not api_key:
            raise RealtimeConnectError(
                "CambAI was constructed without an api_key; cannot open a realtime session."
            )
        return api_key
