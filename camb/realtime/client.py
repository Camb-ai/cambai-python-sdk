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

        - ``source_language`` *(required)* — IETF BCP-47 tag, e.g. ``"en-US"``
        - ``target_language`` *(required)* — IETF BCP-47 tag, e.g. ``"de-DE"``
        - ``model`` — one of ``"lilac"`` (default), ``"violet"``, ``"iris"``, ``"orchid"``
        - ``output_modalities`` — list of ``"text"`` and/or ``"audio"`` (default: both)
        - ``voice_id`` — ID of one of your cloned voices to synthesize the
          translation with (default: a built-in voice for ``target_language``)

        Returns an open :class:`~camb.realtime.session.RealtimeSession`.  The
        session is not yet ready to accept audio; call
        ``await session.wait_until_ready()`` (or register a
        ``ServerEventType.SESSION_CREATED`` handler) before sending audio.
        """
        api_key = self._client_wrapper.api_key
        if not api_key:
            raise RealtimeConnectError(
                "CambAI was constructed without an api_key; cannot open a realtime session."
            )
        return await _connect(
            api_key=api_key,
            base_url=DEFAULT_REALTIME_BASE_URL,
            transport=transport,
            extra_headers=self._client_wrapper.get_custom_headers(),
            **options,
        )
