"""Automatic source language detection and the session pair that links a call's two directions.

The server is faked at the transport: each test pushes the JSON events the realtime server would
send and inspects the client events the SDK sent back.
"""

from __future__ import annotations

import asyncio
import json
import typing

import pydantic
import pytest

from camb.realtime import (
    ConnectOptions,
    ServerEventType,
    SourceLanguageChangedEvent,
    SpeakerSetup,
    TranscriptCompletedEvent,
    connect,
    connect_session_pair,
)

API_KEY = "test-api-key"


class FakeServerTransport:
    """A transport whose server side is driven by the test."""

    def __init__(self) -> None:
        self.sent_events: typing.List[typing.Dict[str, typing.Any]] = []
        self._server_frames: "asyncio.Queue[typing.Optional[str]]" = asyncio.Queue()
        self.close_code: typing.Optional[int] = None
        self.close_reason: typing.Optional[str] = None

    async def connect(self, url: str, headers: typing.Dict[str, str]) -> None:
        self.url = url

    async def send_text(self, data: str) -> None:
        self.sent_events.append(json.loads(data))

    async def send_bytes(self, data: bytes) -> None:
        raise AssertionError("the SDK sends audio as JSON text")

    def __aiter__(self) -> typing.AsyncIterator[str]:
        return self._receive_server_frames()

    async def _receive_server_frames(self) -> typing.AsyncIterator[str]:
        while True:
            frame = await self._server_frames.get()
            if frame is None:
                return
            yield frame

    async def close(self, code: int = 1000) -> None:
        self.close_code = code
        self._server_frames.put_nowait(None)

    def send_server_event(self, event: typing.Dict[str, typing.Any]) -> None:
        self._server_frames.put_nowait(json.dumps(event))

    def session_updates_after_the_first(self) -> typing.List[typing.Dict[str, typing.Any]]:
        return [
            event["session"]
            for event in self.sent_events[1:]
            if event["type"] == "session.update"
        ]


def session_created(source_language: str = "auto", target_language: str = "") -> typing.Dict[str, typing.Any]:
    return {
        "type": "session.created",
        "session": {
            "id": "session-id",
            "mode": "slow",
            "source_language": source_language,
            "target_language": target_language,
            "output_modalities": ["text", "audio"],
        },
    }


def session_updated(source_language: str, target_language: str) -> typing.Dict[str, typing.Any]:
    return {
        "type": "session.updated",
        "session": {"source_language": source_language, "target_language": target_language},
    }


def source_language_changed(language: str, previous_language: typing.Optional[str] = None) -> typing.Dict[str, typing.Any]:
    return {
        "type": "session.source_language_changed",
        "language": language,
        "previous_language": previous_language,
    }


async def let_events_arrive() -> None:
    for _ in range(20):
        await asyncio.sleep(0)


class TestConnectOptions:
    def test_an_automatic_source_language_needs_no_target(self) -> None:
        options = ConnectOptions(
            mode="slow",
            source_language="auto",
            speaker_setup="single_known_speaker",
            source_language_candidates=["en-US", "de-DE"],
        )
        assert options.to_session_payload() == {
            "mode": "slow",
            "source_language": "auto",
            "output_modalities": ["text", "audio"],
            "speaker_setup": "single_known_speaker",
            "source_language_candidates": ["en-US", "de-DE"],
        }

    def test_an_explicit_source_language_still_needs_a_target(self) -> None:
        with pytest.raises(pydantic.ValidationError, match="target_language is required"):
            ConnectOptions(source_language="en-US")

    def test_detection_settings_need_an_automatic_source_language(self) -> None:
        with pytest.raises(pydantic.ValidationError, match="only apply"):
            ConnectOptions(
                source_language="en-US",
                target_language="de-DE",
                speaker_setup=SpeakerSetup.CHANGING_SPEAKERS,
            )

    def test_explicit_languages_send_the_same_payload_as_before(self) -> None:
        options = ConnectOptions(source_language="en-US", target_language="de-DE")
        assert options.to_session_payload() == {
            "mode": "fast",
            "source_language": "en-US",
            "target_language": "de-DE",
            "output_modalities": ["text", "audio"],
        }


class TestSessionWithAutomaticSourceLanguage:
    def test_language_events_and_methods(self) -> None:
        async def scenario() -> None:
            transport = FakeServerTransport()
            session = await connect(
                API_KEY, transport=transport, mode="slow", source_language="auto"
            )
            changes: typing.List[SourceLanguageChangedEvent] = []
            transcripts: typing.List[TranscriptCompletedEvent] = []
            error_codes: typing.List[typing.Optional[str]] = []
            session.on(ServerEventType.SOURCE_LANGUAGE_CHANGED, changes.append)
            session.on(ServerEventType.TRANSCRIPT_COMPLETED, transcripts.append)
            session.on(
                ServerEventType.ERROR,
                lambda event: error_codes.append((event.code, event.error_type, event.param)),
            )

            # A session without a target yet must not fail to parse.
            transport.send_server_event(
                {"type": "session.created", "session": {"id": "s", "mode": "slow", "source_language": "auto"}}
            )
            transport.send_server_event(source_language_changed("de-DE"))
            transport.send_server_event(
                {
                    "type": "conversation.item.input_audio_transcription.completed",
                    "transcript": "Guten Tag",
                    "item_id": "item-1",
                    "language": "de-DE",
                    "passthrough": False,
                }
            )
            transport.send_server_event(
                {
                    "type": "error",
                    "error": {
                        "type": "invalid_request_error",
                        "code": "target_language_unsupported_for_mode",
                        "message": "unsupported",
                        "param": "session.target_language",
                    },
                }
            )
            await session.wait_until_ready()
            await let_events_arrive()

            await session.update_languages(target_language="en-US")
            await session.update_languages(source_language="de-DE")
            await session.ignore_utterance_for_language_detection("item-1")
            with pytest.raises(ValueError):
                await session.update_languages()
            await session.close()

            assert session.is_ready
            assert [(change.language, change.previous_language) for change in changes] == [("de-DE", None)]
            assert [(t.item_id, t.language, t.passthrough) for t in transcripts] == [("item-1", "de-DE", False)]
            assert error_codes == [
                ("target_language_unsupported_for_mode", "invalid_request_error", "session.target_language")
            ]
            assert transport.sent_events[1:] == [
                {"type": "session.update", "session": {"target_language": "en-US"}},
                {"type": "session.update", "session": {"source_language": "de-DE"}},
                {"type": "input_audio_buffer.ignore_for_language_detection", "item_id": "item-1"},
            ]

        asyncio.run(scenario())


class SessionPairFixture:
    def __init__(self) -> None:
        self.transports: typing.List[FakeServerTransport] = []

    def new_transport(self) -> FakeServerTransport:
        transport = FakeServerTransport()
        self.transports.append(transport)
        return transport

    @property
    def local_speaker_transport(self) -> FakeServerTransport:
        return self.transports[0]

    @property
    def other_party_transport(self) -> FakeServerTransport:
        return self.transports[1]


class TestSessionPair:
    def test_each_direction_translates_into_the_language_the_other_speaks(self) -> None:
        async def scenario() -> None:
            fixture = SessionPairFixture()
            pair = await connect_session_pair(
                API_KEY, transport_factory=fixture.new_transport, mode="slow"
            )
            local, other = fixture.local_speaker_transport, fixture.other_party_transport
            assert local.sent_events[0]["session"]["speaker_setup"] == "single_known_speaker"
            assert other.sent_events[0]["session"]["speaker_setup"] == "changing_speakers"
            assert local.sent_events[0]["session"]["source_language"] == "auto"

            local.send_server_event(session_created())
            other.send_server_event(session_created())
            await pair.wait_until_ready()
            await let_events_arrive()

            other.send_server_event(source_language_changed("de-DE"))
            local.send_server_event(source_language_changed("en-US"))
            await let_events_arrive()
            assert local.session_updates_after_the_first() == [{"target_language": "de-DE"}]
            assert other.session_updates_after_the_first() == [{"target_language": "en-US"}]

            # The same language again changes nothing; a new one is passed on.
            other.send_server_event(session_updated("auto", "en-US"))
            local.send_server_event(source_language_changed("en-US", "en-US"))
            other.send_server_event(source_language_changed("fr-FR", "de-DE"))
            await let_events_arrive()
            assert other.session_updates_after_the_first() == [{"target_language": "en-US"}]
            assert local.session_updates_after_the_first() == [
                {"target_language": "de-DE"},
                {"target_language": "fr-FR"},
            ]
            await pair.close()

        asyncio.run(scenario())

    def test_a_language_detected_before_the_other_session_is_ready_is_passed_on_once_it_is(self) -> None:
        async def scenario() -> None:
            fixture = SessionPairFixture()
            pair = await connect_session_pair(
                API_KEY, transport_factory=fixture.new_transport, mode="slow"
            )
            local, other = fixture.local_speaker_transport, fixture.other_party_transport
            other.send_server_event(session_created())
            other.send_server_event(source_language_changed("de-DE"))
            await let_events_arrive()
            assert local.session_updates_after_the_first() == []

            local.send_server_event(session_created())
            await let_events_arrive()
            assert local.session_updates_after_the_first() == [{"target_language": "de-DE"}]
            await pair.close()

        asyncio.run(scenario())

    def test_a_fixed_source_language_is_the_other_directions_target(self) -> None:
        async def scenario() -> None:
            fixture = SessionPairFixture()
            pair = await connect_session_pair(
                API_KEY,
                transport_factory=fixture.new_transport,
                mode="slow",
                local_speaker={"source_language": "en-US", "target_language": "de-DE"},
            )
            local, other = fixture.local_speaker_transport, fixture.other_party_transport
            assert "speaker_setup" not in local.sent_events[0]["session"]
            local.send_server_event(session_created("en-US", "de-DE"))
            other.send_server_event(session_created())
            await let_events_arrive()
            assert other.session_updates_after_the_first() == [{"target_language": "en-US"}]
            await pair.close()

        asyncio.run(scenario())

    def test_a_switch_confirmation_request_is_left_to_the_application(self) -> None:
        async def scenario() -> None:
            fixture = SessionPairFixture()
            pair = await connect_session_pair(
                API_KEY, transport_factory=fixture.new_transport, mode="slow"
            )
            local, other = fixture.local_speaker_transport, fixture.other_party_transport
            confirmation_requests: typing.List[str] = []
            pair.local_speaker_session.on(
                ServerEventType.SOURCE_LANGUAGE_SWITCH_CONFIRMATION_REQUESTED,
                lambda event: confirmation_requests.append(event.language),
            )
            local.send_server_event(session_created())
            other.send_server_event(session_created())
            local.send_server_event(
                {"type": "session.source_language_switch_confirmation_requested", "language": "de-DE"}
            )
            await let_events_arrive()
            assert confirmation_requests == ["de-DE"]
            assert other.session_updates_after_the_first() == []
            await pair.close()

        asyncio.run(scenario())

    def test_a_failed_open_closes_both_sessions(self) -> None:
        class RefusingTransport(FakeServerTransport):
            async def connect(self, url: str, headers: typing.Dict[str, str]) -> None:
                raise ConnectionRefusedError("refused")

        async def scenario() -> None:
            opened: typing.List[FakeServerTransport] = []

            def new_transport() -> FakeServerTransport:
                transport = FakeServerTransport() if not opened else RefusingTransport()
                opened.append(transport)
                return transport

            with pytest.raises(ConnectionRefusedError):
                await connect_session_pair(API_KEY, transport_factory=new_transport, mode="slow")
            assert opened[0].close_code == 1000

        asyncio.run(scenario())
