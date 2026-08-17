"""Tests for the live transcription session event pump (no network).

Frames are replayed through a :class:`FakeTransport`; handlers observe
parsed, pydantic-validated events.
"""

from __future__ import annotations

import asyncio
import json
import typing

import pytest

from camb.live_transcription.errors import LiveTranscriptionProtocolError
from camb.live_transcription.events import ClosedEvent, ResultsEvent, ServerMessageType
from camb.live_transcription.session import LiveTranscriptionSession

from conftest import FakeTransport, json_frame


def _make_session(frames, *, hold_open=False) -> typing.Tuple[LiveTranscriptionSession, FakeTransport]:
    transport = FakeTransport(frames, hold_open=hold_open)
    session = LiveTranscriptionSession(
        transport=transport,
        url="wss://realtime.camb.ai/streaming-transcription/listen?model=boli-v5",
        headers={"x-api-key": "test"},
    )
    return session, transport


def _results_frame(transcript: str, *, is_final: bool = False) -> str:
    return json_frame(
        type="Results",
        is_final=is_final,
        start=0.0,
        duration=1.0,
        channel={"alternatives": [{"transcript": transcript, "confidence": 0.9, "words": []}]},
        metadata={"request_id": "abc", "model_uuid": "m1", "model_info": {"name": "boli-v5"}},
    )


def _run(coro) -> None:
    asyncio.run(coro)


def test_read_loop_dispatches_ready_and_results() -> None:
    received = []

    async def main() -> None:
        session, _ = _make_session(
            [json_frame(type="Ready"), _results_frame("hello world", is_final=True)]
        )

        @session.on(ServerMessageType.READY)
        def _(event) -> None:
            received.append(("ready", event))

        @session.on(ServerMessageType.RESULTS)
        def _(event: ResultsEvent) -> None:
            received.append(("results", event))

        await session._open()
        await session.run_until_closed()

    _run(main())

    assert [kind for kind, _ in received] == ["ready", "results"]

    results: ResultsEvent = received[1][1]
    assert isinstance(results, ResultsEvent)
    assert results.transcript == "hello world"
    assert results.is_final is True
    assert results.confidence == 0.9
    assert results.words == []


def test_on_works_as_decorator_and_direct_call() -> None:
    calls = []

    async def main() -> None:
        session, _ = _make_session([_results_frame("x")])

        @session.on(ServerMessageType.RESULTS)
        def decorated(event) -> None:
            calls.append(("decorated", event.transcript))

        def direct(event) -> None:
            calls.append(("direct", event.transcript))

        session.on(ServerMessageType.RESULTS, direct)
        await session._open()
        await session.run_until_closed()

    _run(main())

    assert calls == [("decorated", "x"), ("direct", "x")]


def test_off_unregisters_handler() -> None:
    calls = []

    async def main() -> None:
        session, _ = _make_session([_results_frame("x")])

        def handler(event) -> None:
            calls.append(event.transcript)

        session.on(ServerMessageType.RESULTS, handler)
        session.off(ServerMessageType.RESULTS, handler)
        await session._open()
        await session.run_until_closed()

    _run(main())

    assert calls == []


def test_unknown_event_reaches_wildcard_handlers() -> None:
    wildcard = []
    typed = []

    async def main() -> None:
        session, _ = _make_session([json_frame(type="FutureType", payload=42)])

        @session.on_any
        def _(event_type, raw) -> None:
            wildcard.append((event_type, raw))

        @session.on(ServerMessageType.READY)
        def _(event) -> None:
            typed.append(event)

        await session._open()
        await session.run_until_closed()

    _run(main())

    assert wildcard[0] == ("FutureType", {"type": "FutureType", "payload": 42})
    assert typed == []


def test_handler_exception_routed_to_error_subscribers() -> None:
    errors = []

    async def main() -> None:
        session, _ = _make_session([_results_frame("boom")])

        @session.on(ServerMessageType.RESULTS)
        def _(event) -> None:
            raise RuntimeError("handler exploded")

        @session.on(ServerMessageType.ERROR)
        def _(event) -> None:
            errors.append(event)

        await session._open()
        await session.run_until_closed()

    _run(main())

    assert len(errors) == 1
    assert errors[0].message == "handler exploded"


def test_binary_frames_are_ignored() -> None:
    received = []

    async def main() -> None:
        session, _ = _make_session([b"raw-pcm", json_frame(type="Ready")])

        @session.on(ServerMessageType.READY)
        def _(event) -> None:
            received.append(event)

        await session._open()
        await session.run_until_closed()

    _run(main())

    assert len(received) == 1


def test_non_json_frames_are_discarded() -> None:
    received = []

    async def main() -> None:
        session, _ = _make_session(["not json {", json_frame(type="Ready")])

        @session.on(ServerMessageType.READY)
        def _(event) -> None:
            received.append(event)

        await session._open()
        await session.run_until_closed()

    _run(main())

    assert len(received) == 1


def test_close_emits_closed_event_with_transport_code() -> None:
    closed = []
    state = {}

    async def main() -> None:
        session, _ = _make_session([])
        await session._open()

        @session.on(ServerMessageType.CLOSED)
        def _(event: ClosedEvent) -> None:
            closed.append(event)

        await session.close()
        state["is_closed"] = session.is_closed

    _run(main())

    assert len(closed) == 1
    assert closed[0].code == 1000
    assert state["is_closed"] is True


def test_close_sends_close_stream_frame_and_closes_transport() -> None:
    async def main() -> None:
        session, transport = _make_session([])
        await session._open()
        await session.close()

        assert json.loads(transport.sent_text[0]) == {"type": "CloseStream"}
        assert transport.closed_codes == [1000]

    _run(main())


def test_open_is_idempotent() -> None:
    async def main() -> None:
        session, _ = _make_session([json_frame(type="Ready")])
        await session._open()
        task = session._reader_task
        await session._open()
        assert session._reader_task is task
        await session.close()

    _run(main())


def test_wait_until_ready_fails_fast_when_socket_closes_pre_ready() -> None:
    async def main() -> None:
        session, _ = _make_session([])
        await session._open()
        await session.run_until_closed()

        # The SDK sets the ready flag on close so this must not hang, even
        # though the session never became ready.
        await session.wait_until_ready()
        assert session.is_closed

    _run(main())


def test_dispatch_raises_protocol_error_on_invalid_typed_frame() -> None:
    async def main() -> None:
        session, _ = _make_session([])
        with pytest.raises(LiveTranscriptionProtocolError):
            await session._dispatch({"type": "Results"})  # missing channel

    _run(main())


def test_stream_audio_pumps_chunks_until_source_done() -> None:
    sent = []
    closed = []

    class Source:
        def __init__(self) -> None:
            self._chunks = iter([b"a", b"bb", b"ccc"])

        def __aiter__(self):
            return self

        async def __anext__(self):
            try:
                return next(self._chunks)
            except StopIteration:
                raise StopAsyncIteration

        async def close(self) -> None:
            closed.append(True)

    async def main() -> None:
        session, transport = _make_session([], hold_open=True)
        await session._open()
        await session.stream_audio(Source())
        await session.close()
        sent.extend(transport.sent_bytes)

    _run(main())

    assert sent == [b"a", b"bb", b"ccc"]
    assert closed == [True]