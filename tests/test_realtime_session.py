"""Tests for the realtime translation session event pump (no network)."""

from __future__ import annotations

import asyncio
import base64
import json
import typing

import pytest

from camb.realtime.errors import RealtimeConnectError, RealtimeProtocolError
from camb.realtime.events import (
    AudioDeltaEvent,
    ClosedEvent,
    ErrorEvent,
    ServerEventType,
    TextDoneEvent,
)
from camb.realtime.session import RealtimeSession, connect

from conftest import FakeTransport, json_frame


def _make_session(frames, *, hold_open=False) -> typing.Tuple[RealtimeSession, FakeTransport]:
    transport = FakeTransport(frames, hold_open=hold_open)
    session = RealtimeSession(
        transport=transport,
        url="wss://realtime.camb.ai/v1/realtime?model=lilac",
        headers={},
        session_payload={"type": "session.update", "session": {}, "auth": {"api_key": "test"}},
    )
    return session, transport


def _run(coro) -> None:
    asyncio.run(coro)


def test_connect_builds_url_session_payload_and_opens() -> None:
    async def main() -> None:
        transport = FakeTransport([])
        session = await connect(
            "key123",
            transport=transport,
            source_language="en-US",
            target_language="de-DE",
            voice_id=147320,
        )
        assert transport.connected_url == (
            "wss://realtime.camb.ai/v1/realtime?model=lilac"
        )
        payload = json.loads(transport.sent_text[0])
        assert payload["type"] == "session.update"
        assert payload["auth"] == {"api_key": "key123"}
        assert payload["session"]["source_language"] == "en-US"
        assert payload["session"]["target_language"] == "de-DE"
        assert payload["session"]["voice"] == {"type": "cloned", "voice_id": 147320}
        await session.close()

    _run(main())


def test_session_starting_and_created_events() -> None:
    events = []

    async def main() -> None:
        session, _ = _make_session(
            [
                json_frame(type="session.starting"),
                json_frame(
                    type="session.created",
                    session={
                        "id": "s1",
                        "model": "lilac",
                        "source_language": "en-US",
                        "target_language": "de-DE",
                        "output_modalities": ["text", "audio"],
                    },
                ),
                json_frame(
                    type="session.updated",
                    session={"source_language": "en-US", "target_language": "de-DE", "output_modalities": ["text", "audio"]},
                ),
            ]
        )

        @session.on_any
        def _(event_type, event) -> None:
            events.append((event_type, event))

        await session._open()
        await session.run_until_closed()

    _run(main())

    assert [t for t, _ in events] == [
        ServerEventType.SESSION_STARTING,
        ServerEventType.SESSION_CREATED,
        ServerEventType.SESSION_UPDATED,
        ServerEventType.CLOSED,
    ]
    assert events[1][1].session.id == "s1"


def test_session_created_sets_ready() -> None:
    async def main() -> None:
        session, _ = _make_session(
            [
                json_frame(
                    type="session.created",
                    session={
                        "id": "s1",
                        "model": "lilac",
                        "source_language": "en-US",
                        "target_language": "de-DE",
                        "output_modalities": ["text", "audio"],
                    },
                )
            ]
        )
        await session._open()
        await session.wait_until_ready(timeout=1.0)
        assert session.is_ready

    _run(main())


def test_wait_until_ready_timeout_raises() -> None:
    async def main() -> None:
        session, transport = _make_session([], hold_open=True)
        await session._open()
        with pytest.raises(RealtimeConnectError):
            await session.wait_until_ready(timeout=0.05)
        await session.close()

    _run(main())


def test_close_before_ready_fails_fast() -> None:
    async def main() -> None:
        session, _ = _make_session([])
        await session._open()
        await session.run_until_closed()
        # wait_until_ready unblocks on close and then raises
        with pytest.raises(RealtimeConnectError):
            await session.wait_until_ready(timeout=1.0)

    _run(main())


def test_text_delta_and_text_done_dispatch() -> None:
    deltas = []
    done = []

    async def main() -> None:
        session, _ = _make_session(
            [
                json_frame(type="response.text.delta", delta="Hal"),
                json_frame(type="response.text.delta", delta="lo!"),
                json_frame(type="response.text.done", text="Hallo!"),
            ]
        )

        @session.on(ServerEventType.TEXT_DELTA)
        def _(event) -> None:
            deltas.append(event.delta)

        @session.on(ServerEventType.TEXT_DONE)
        def _(event: TextDoneEvent) -> None:
            done.append(event)

        await session._open()
        await session.run_until_closed()

    _run(main())

    assert deltas == ["Hal", "lo!"]
    assert len(done) == 1
    assert done[0].text == "Hallo!"


def test_binary_frame_becomes_audio_delta() -> None:
    audio = []

    async def main() -> None:
        session, _ = _make_session([b"\x00\x01\x02\x03"])

        @session.on(ServerEventType.AUDIO_DELTA)
        def _(event: AudioDeltaEvent) -> None:
            audio.append(event.data)

        await session._open()
        await session.run_until_closed()

    _run(main())

    assert audio == [b"\x00\x01\x02\x03"]


def test_json_audio_delta_is_base64_decoded() -> None:
    audio = []

    async def main() -> None:
        wire = json_frame(type="response.audio.delta", delta=base64.b64encode(b"pcm!").decode())
        session, _ = _make_session([wire])

        @session.on(ServerEventType.AUDIO_DELTA)
        def _(event: AudioDeltaEvent) -> None:
            audio.append(event.data)

        await session._open()
        await session.run_until_closed()

    _run(main())

    assert audio == [b"pcm!"]


def test_error_frame_is_flattened() -> None:
    errors = []

    async def main() -> None:
        session, _ = _make_session(
            [json_frame(type="error", error={"message": "auth failed", "code": 401})]
        )

        @session.on(ServerEventType.ERROR)
        def _(event: ErrorEvent) -> None:
            errors.append(event)

        await session._open()
        await session.run_until_closed()

    _run(main())

    assert len(errors) == 1
    assert errors[0].message == "auth failed"
    assert errors[0].raw["error"] == {"message": "auth failed", "code": 401}


def test_unknown_event_reaches_wildcard_handlers() -> None:
    wildcard = []

    async def main() -> None:
        session, _ = _make_session([json_frame(type="future.event", x=1)])

        @session.on_any
        def _(event_type, raw) -> None:
            wildcard.append((event_type, raw))

        await session._open()
        await session.run_until_closed()

    _run(main())

    assert wildcard[0] == ("future.event", {"type": "future.event", "x": 1})


def test_dispatch_raises_protocol_error_on_invalid_typed_frame() -> None:
    async def main() -> None:
        session, _ = _make_session([])
        with pytest.raises(RealtimeProtocolError):
            await session._dispatch({"type": "response.text.done"})  # missing text

    _run(main())


def test_send_audio_base64_encodes_chunk() -> None:
    async def main() -> None:
        session, transport = _make_session([], hold_open=True)
        await session._open()
        await session.send_audio(b"\x00\xff")
        # sent_text[0] is the session.update handshake; the append is [1]
        payload = json.loads(transport.sent_text[1])
        assert payload["type"] == "input_audio_buffer.append"
        assert payload["audio"] == base64.b64encode(b"\x00\xff").decode()
        await session.close()

    _run(main())


def test_close_emits_closed_event() -> None:
    closed = []
    state = {}

    async def main() -> None:
        session, transport = _make_session([])
        await session._open()

        @session.on(ServerEventType.CLOSED)
        def _(event: ClosedEvent) -> None:
            closed.append(event)

        await session.close()
        state["is_closed"] = session.is_closed

    _run(main())

    assert len(closed) == 1
    assert closed[0].code == 1000
    assert state["is_closed"] is True


def test_handler_exception_routed_to_error_subscribers() -> None:
    errors = []

    async def main() -> None:
        session, _ = _make_session([json_frame(type="response.text.done", text="hi")])

        @session.on(ServerEventType.TEXT_DONE)
        def _(event) -> None:
            raise ValueError("bad handler")

        @session.on(ServerEventType.ERROR)
        def _(event: ErrorEvent) -> None:
            errors.append(event)

        await session._open()
        await session.run_until_closed()

    _run(main())

    assert len(errors) == 1
    assert errors[0].message == "bad handler"