"""Audio sources the live transcription session can consume.

An :class:`AudioSource` is anything that yields PCM byte chunks. The
:class:`Microphone` helper is one implementation; :class:`FileAudioSource`
is another useful for tutorials and integration tests.
"""

from __future__ import annotations

import asyncio
import contextlib
import time
import typing
import wave


class AudioSource(typing.Protocol):
    """Async iterable of audio byte chunks ready to send over the wire."""

    def __aiter__(self) -> typing.AsyncIterator[bytes]: ...

    async def close(self) -> None: ...


class FileAudioSource:
    """Stream a 16-bit PCM WAV file as if it were a live microphone.

    When ``real_time`` is true, chunks are paced to match wall-clock time so
    consumers see arrival patterns equivalent to a live capture.
    """

    def __init__(
        self,
        path: str,
        *,
        chunk_ms: int = 100,
        real_time: bool = True,
    ) -> None:
        self._path = path
        self._chunk_ms = chunk_ms
        self._real_time = real_time
        self._closed = False

    async def __aiter__(self) -> typing.AsyncIterator[bytes]:
        with contextlib.closing(wave.open(self._path, "rb")) as wf:
            sample_rate = wf.getframerate()
            channels = wf.getnchannels()
            sample_width = wf.getsampwidth()
            bytes_per_second = sample_rate * channels * sample_width
            chunk_size = max(1, int(bytes_per_second * self._chunk_ms / 1000))

            t0 = time.monotonic()
            bytes_sent = 0
            while not self._closed:
                chunk = wf.readframes(chunk_size // (channels * sample_width))
                if not chunk:
                    return
                yield chunk
                bytes_sent += len(chunk)
                if self._real_time:
                    expected = bytes_sent / bytes_per_second
                    drift = expected - (time.monotonic() - t0)
                    if drift > 0:
                        await asyncio.sleep(drift)

    async def close(self) -> None:
        self._closed = True
