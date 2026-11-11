"""Polling helpers for async task workflows.

Long-running workflows (dubbing, transcription, subtitles, text-to-audio)
create a task and require repeated status checks until ``SUCCESS``. These
helpers remove the hand-written loop::

    from camb.polling import poll_dubbing

    status = poll_dubbing(client.dub, task_id=task_id, timeout=600)
    result = client.dub.get_dubbed_run_info(status.run_id)

Three states exist: ``SUCCESS``, ``PENDING`` and ``ERROR`` (see
``camb.types.TaskStatus``). Polling stops as soon as a terminal state is
seen; an ``ERROR`` status raises immediately, and a missing ``SUCCESS``
before ``timeout`` raises :class:`PollTimeoutError`.
"""

from __future__ import annotations

import asyncio
import time
import typing

SUCCESS = "SUCCESS"
PENDING = "PENDING"
ERROR = "ERROR"

Status = typing.Any  # any object with .status (TaskStatus) and .run_id


class PollError(Exception):
    """Base class for every exception raised by ``camb.polling``."""


class PollTimeoutError(PollError):
    """The task did not reach a terminal state within the deadline."""


class PollFailureError(PollError):
    """The task reported an ``ERROR`` status."""


def poll_until_complete(
    get_status: typing.Callable[[], Status],
    *,
    interval: float = 5.0,
    timeout: typing.Optional[float] = None,
) -> Status:
    """Poll ``get_status`` until it reports ``SUCCESS``.

    Parameters
    ----------
    get_status : typing.Callable[[], Status]
        A zero-argument callable returning a status object with ``status``
        and ``run_id`` attributes (e.g. ``lambda: client.dub.get_dubbing_status(task_id=...)``).
    interval : float
        Seconds to wait between status checks (default 5).
    timeout : typing.Optional[float]
        Total seconds allowed before raising :class:`PollTimeoutError`.
        ``None`` (default) polls indefinitely.

    Returns
    -------
    Status
        The status object that reported ``SUCCESS`` (carries ``run_id``).
    """
    deadline = None if timeout is None else time.monotonic() + timeout
    while True:
        status = get_status()
        if status.status == SUCCESS:
            return status
        _check_terminal(status)
        if deadline is not None and time.monotonic() >= deadline:
            raise PollTimeoutError(f"Task did not complete within {timeout}s")
        time.sleep(interval)


async def apoll_until_complete(
    aget_status: typing.Callable[[], typing.Awaitable[Status]],
    *,
    interval: float = 5.0,
    timeout: typing.Optional[float] = None,
) -> Status:
    """Async equivalent of :func:`poll_until_complete` for ``Async*Client``s."""
    deadline = None if timeout is None else time.monotonic() + timeout
    while True:
        status = await aget_status()
        if status.status == SUCCESS:
            return status
        _check_terminal(status)
        if deadline is not None and time.monotonic() >= deadline:
            raise PollTimeoutError(f"Task did not complete within {timeout}s")
        await asyncio.sleep(interval)


def _check_terminal(status: Status) -> None:
    if status.status == ERROR:
        reason = getattr(status, "message", None) or getattr(status, "exception_reason", None) or ""
        details = f": {reason}" if reason else ""
        raise PollFailureError(f"Task ended with ERROR status{details}")


def poll_dubbing(dub_client: typing.Any, task_id: str, **kwargs: typing.Any) -> Status:
    """Poll ``dub_client.get_dubbing_status`` until complete.

    Fetch the final outputs with ``dub_client.get_dubbed_run_info(status.run_id)``.
    """
    return poll_until_complete(
        lambda: dub_client.get_dubbing_status(task_id=task_id), **kwargs
    )


async def apoll_dubbing(dub_client: typing.Any, task_id: str, **kwargs: typing.Any) -> Status:
    return await apoll_until_complete(
        lambda: dub_client.get_dubbing_status(task_id=task_id), **kwargs
    )


def poll_transcription(transcription_client: typing.Any, task_id: str, **kwargs: typing.Any) -> Status:
    """Poll ``transcription_client.get_transcription_task_status`` until complete.

    Fetch the final output with ``transcription_client.get_transcription_result(status.run_id)``.
    """
    return poll_until_complete(
        lambda: transcription_client.get_transcription_task_status(task_id=task_id), **kwargs
    )


async def apoll_transcription(transcription_client: typing.Any, task_id: str, **kwargs: typing.Any) -> Status:
    return await apoll_until_complete(
        lambda: transcription_client.get_transcription_task_status(task_id=task_id), **kwargs
    )


def poll_subtitle(subtitles_client: typing.Any, task_id: str, **kwargs: typing.Any) -> Status:
    """Poll ``subtitles_client.get_subtitle_task_status`` until complete.

    Fetch the final output with ``subtitles_client.get_subtitle_result(status.run_id)``.
    """
    return poll_until_complete(
        lambda: subtitles_client.get_subtitle_task_status(task_id=task_id), **kwargs
    )


async def apoll_subtitle(subtitles_client: typing.Any, task_id: str, **kwargs: typing.Any) -> Status:
    return await apoll_until_complete(
        lambda: subtitles_client.get_subtitle_task_status(task_id=task_id), **kwargs
    )


def poll_text_to_audio(text_to_audio_client: typing.Any, task_id: str, **kwargs: typing.Any) -> Status:
    """Poll ``text_to_audio_client.get_text_to_audio_status`` until complete.

    Fetch the final output with ``text_to_audio_client.get_text_to_audio_result(status.run_id)``.
    """
    return poll_until_complete(
        lambda: text_to_audio_client.get_text_to_audio_status(task_id=task_id), **kwargs
    )


async def apoll_text_to_audio(text_to_audio_client: typing.Any, task_id: str, **kwargs: typing.Any) -> Status:
    return await apoll_until_complete(
        lambda: text_to_audio_client.get_text_to_audio_status(task_id=task_id), **kwargs
    )