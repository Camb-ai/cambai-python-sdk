"""Microphone helper backed by :mod:`sounddevice` (optional extra).

Install with::

    pip install "camb-sdk[microphone]"

The dependency is loaded lazily; importing this module without
``sounddevice`` installed succeeds and only raises if you instantiate
:class:`Microphone`.
"""

from __future__ import annotations

import asyncio
import queue
import typing

from .errors import MicrophoneUnavailableError


class Microphone:
    """Capture raw 16-bit PCM audio from the default input device.

    The default ``sample_rate`` and ``chunk_size`` align with the server's
    defaults (16 kHz, 100 ms frames). Tune ``device`` to a non-default
    input by name or ``sounddevice`` index.
    """

    def __init__(
        self,
        sample_rate: int = 16000,
        chunk_size: int = 1600,
        device: typing.Optional[typing.Union[int, str]] = None,
    ) -> None:
        try:
            import sounddevice  # noqa: F401
        except ImportError as exc:
            raise MicrophoneUnavailableError(
                "The 'sounddevice' package is required for the Microphone helper. "
                "Install it with: pip install 'camb-sdk[microphone]'"
            ) from exc

        self._sample_rate = sample_rate
        self._chunk_size = chunk_size
        self._device = device
        self._queue: "queue.Queue[bytes]" = queue.Queue()
        self._stream: typing.Any = None
        self._running = False

    @property
    def sample_rate(self) -> int:
        return self._sample_rate

    @property
    def chunk_size(self) -> int:
        return self._chunk_size

    def start(self) -> None:
        import sounddevice as sd

        if self._running:
            return

        def _callback(indata, _frames, _time_info, _status):  # noqa: ANN001
            # ``indata`` is a numpy array of int16 samples. ``tobytes`` gives
            # the little-endian byte layout the server expects (``linear16``).
            self._queue.put(bytes(indata))

        self._stream = sd.RawInputStream(
            samplerate=self._sample_rate,
            blocksize=self._chunk_size,
            device=self._device,
            dtype="int16",
            channels=1,
            callback=_callback,
        )
        self._stream.start()
        self._running = True

    def stop(self) -> None:
        if self._stream is not None:
            self._stream.stop()
            self._stream.close()
            self._stream = None
        self._running = False
        # Sentinel so any pending consumer can unblock.
        self._queue.put(b"")

    def read(self, timeout: typing.Optional[float] = None) -> bytes:
        return self._queue.get(timeout=timeout)

    async def __aiter__(self) -> typing.AsyncIterator[bytes]:
        if not self._running:
            self.start()
        loop = asyncio.get_running_loop()
        while True:
            chunk = await loop.run_in_executor(None, self._queue.get)
            if not chunk:
                return
            yield chunk

    async def close(self) -> None:
        self.stop()

    def __enter__(self) -> "Microphone":
        self.start()
        return self

    def __exit__(self, *exc: typing.Any) -> None:
        self.stop()
