"""Tests for the polling helpers in ``camb.polling``."""

from __future__ import annotations

import asyncio
import typing

import pytest

from camb.polling import (
    PollFailureError,
    PollTimeoutError,
    apoll_dubbing,
    apoll_subtitle,
    apoll_text_to_audio,
    apoll_transcription,
    apoll_until_complete,
    poll_dubbing,
    poll_subtitle,
    poll_text_to_audio,
    poll_transcription,
    poll_until_complete,
)


class _FakeStatus:
    def __init__(self, status: str, *, run_id: typing.Optional[int] = None, message: typing.Optional[str] = None) -> None:
        self.status = status
        self.run_id = run_id
        self.message = message


def _success() -> _FakeStatus:
    return _FakeStatus("SUCCESS", run_id=7)


def test_returns_immediately_on_success() -> None:
    calls = []

    def get_status() -> _FakeStatus:
        calls.append(1)
        return _success()

    status = poll_until_complete(get_status, interval=0.001)

    assert status.status == "SUCCESS"
    assert status.run_id == 7
    assert calls == [1]


def test_polls_until_success() -> None:
    statuses = iter(["PENDING", "PENDING", "SUCCESS"])

    status = poll_until_complete(lambda: _FakeStatus(next(statuses), run_id=3), interval=0.001, timeout=10)

    assert status.run_id == 3


def test_pending_is_not_terminal() -> None:
    statuses = iter(["PENDING", "SUCCESS"])

    status = poll_until_complete(lambda: _FakeStatus(next(statuses)), interval=0.001, timeout=5)

    assert status.status == "SUCCESS"


def test_error_raises_immediately() -> None:
    with pytest.raises(PollFailureError, match="ERROR"):
        poll_until_complete(lambda: _FakeStatus("ERROR"), interval=0.001)


def test_error_message_included() -> None:
    with pytest.raises(PollFailureError, match="boom"):
        poll_until_complete(
            lambda: _FakeStatus("ERROR", message="boom"), interval=0.001
        )


def test_timeout_raises() -> None:
    with pytest.raises(PollTimeoutError, match="within 0.1"):
        poll_until_complete(
            lambda: _FakeStatus("PENDING"), interval=0.01, timeout=0.1
        )


def test_wrapper_passes_task_id_to_status_getter() -> None:
    calls: typing.List[typing.Tuple[str, str]] = []
    client = type("FakeClient", (), _getters(calls))()

    status = poll_dubbing(client, task_id="task-1", interval=0.001)

    assert calls == [("get_dubbing_status", "task-1")]
    assert status.run_id == 42


def test_all_sync_wrappers_dispatch() -> None:
    for wrapper, getter in [
        (poll_dubbing, "get_dubbing_status"),
        (poll_transcription, "get_transcription_task_status"),
        (poll_subtitle, "get_subtitle_task_status"),
        (poll_text_to_audio, "get_text_to_audio_status"),
    ]:
        calls: typing.List[typing.Tuple[str, str]] = []
        client = type("FakeClient", (), _getters(calls))()
        status = wrapper(client, task_id="t", interval=0.001)
        assert status.status == "SUCCESS"
        assert calls[-1] == (getter, "t")


def test_all_async_wrappers_dispatch() -> None:
    names = [
        "get_dubbing_status",
        "get_transcription_task_status",
        "get_subtitle_task_status",
        "get_text_to_audio_status",
    ]

    def make(name: str):
        async def aget(self, task_id: str) -> _FakeStatus:
            return _FakeStatus("SUCCESS", run_id=42)

        return aget

    for wrapper, getter in [
        (apoll_dubbing, "get_dubbing_status"),
        (apoll_transcription, "get_transcription_task_status"),
        (apoll_subtitle, "get_subtitle_task_status"),
        (apoll_text_to_audio, "get_text_to_audio_status"),
    ]:
        got = {}

        async def main() -> None:
            client = type("FakeAsyncClient", (), {n: make(n) for n in names})()
            got["status"] = await wrapper(client, task_id="t", interval=0.001)

        _run(main())
        assert got["status"].status == "SUCCESS"


def _run(coro) -> None:
    asyncio.run(coro)


def test_async_returns_immediately_on_success() -> None:
    async def get_status() -> _FakeStatus:
        return _success()

    async def main() -> None:
        status = await apoll_until_complete(get_status, interval=0.001)
        assert status.status == "SUCCESS"

    _run(main())


def test_async_polls_until_success() -> None:
    statuses = iter(["PENDING", "SUCCESS"])

    async def get_status() -> _FakeStatus:
        return _FakeStatus(next(statuses))

    async def main() -> None:
        status = await apoll_until_complete(get_status, interval=0.001, timeout=5)
        assert status.status == "SUCCESS"

    _run(main())


def test_async_error_raises_immediately() -> None:
    async def get_status() -> _FakeStatus:
        return _FakeStatus("ERROR", message="kaput")

    async def main() -> None:
        with pytest.raises(PollFailureError, match="kaput"):
            await apoll_until_complete(get_status, interval=0.001)

    _run(main())


def test_async_timeout_raises() -> None:
    async def get_status() -> _FakeStatus:
        return _FakeStatus("PENDING")

    async def main() -> None:
        with pytest.raises(PollTimeoutError):
            await apoll_until_complete(get_status, interval=0.01, timeout=0.1)

    _run(main())


def test_all_async_wrappers_dispatch() -> None:
    names = [
        "get_dubbing_status",
        "get_transcription_task_status",
        "get_subtitle_task_status",
        "get_text_to_audio_status",
    ]

    def make(name: str):
        async def aget(self, task_id: str) -> _FakeStatus:
            return _FakeStatus("SUCCESS", run_id=42)

        return aget

    for wrapper, getter in [
        (apoll_dubbing, "get_dubbing_status"),
        (apoll_transcription, "get_transcription_task_status"),
        (apoll_subtitle, "get_subtitle_task_status"),
        (apoll_text_to_audio, "get_text_to_audio_status"),
    ]:
        got = {}

        async def main() -> None:
            client = type("FakeAsyncClient", (), {n: make(n) for n in names})()
            got["status"] = await wrapper(client, task_id="t", interval=0.001)

        _run(main())
        assert got["status"].status == "SUCCESS"


def _getters(calls: typing.List[typing.Tuple[str, str]]) -> typing.Dict[str, typing.Any]:
    names = [
        "get_dubbing_status",
        "get_transcription_task_status",
        "get_subtitle_task_status",
        "get_text_to_audio_status",
    ]

    def make(name: str):
        def get(self, task_id: str) -> _FakeStatus:
            calls.append((name, task_id))
            return _FakeStatus("SUCCESS", run_id=42)

        return get

    return {name: make(name) for name in names}


def test_poll_exceptions_hierarchy() -> None:
    assert issubclass(PollTimeoutError, Exception)
    assert issubclass(PollFailureError, Exception)