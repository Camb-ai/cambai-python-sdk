"""Realtime speech-to-speech translation from the microphone.

Speak into your mic in the source language; the translated speech is played
back through your speakers in near real time, and the translated text is
printed as it arrives.

Audio is PCM16 mono at 24 kHz in both directions.

Run with:

    pip install camb-sdk
    CAMB_API_KEY=... python examples/realtime_translation_microphone.py

Optionally override the languages:

    CAMB_API_KEY=... python examples/realtime_translation_microphone.py en-US de-DE
"""

import asyncio
import os
import sys
import threading

import sounddevice as sd

from camb.client import CambAI
from camb.live_transcription import Microphone
from camb.realtime import ServerEventType

SAMPLE_RATE = 24000  # PCM16 mono, both directions


class Speaker:
    """Plays raw PCM16 mono bytes through the default output device.

    A background PortAudio callback drains a thread-safe buffer that the
    realtime audio handler fills, so playback never blocks the event loop.
    """

    def __init__(self, sample_rate: int = SAMPLE_RATE) -> None:
        self._buf = bytearray()
        self._lock = threading.Lock()
        self._stream = sd.RawOutputStream(
            samplerate=sample_rate, channels=1, dtype="int16", callback=self._callback
        )

    def _callback(self, outdata, frames, time_info, status) -> None:  # noqa: ANN001
        want = len(outdata)
        with self._lock:
            take = min(want, len(self._buf))
            outdata[:take] = bytes(self._buf[:take])
            del self._buf[:take]
        if take < want:
            outdata[take:] = b"\x00" * (want - take)  # underrun → silence

    def start(self) -> None:
        self._stream.start()

    def feed(self, pcm: bytes) -> None:
        with self._lock:
            self._buf.extend(pcm)

    def close(self) -> None:
        self._stream.stop()
        self._stream.close()


async def main(source_language: str, target_language: str) -> None:
    api_key = os.environ.get("CAMB_API_KEY")
    if not api_key:
        print("Set CAMB_API_KEY", file=sys.stderr)
        sys.exit(2)

    client = CambAI(api_key=api_key)
    session = await client.realtime.connect(
        source_language=source_language,
        target_language=target_language,
        # fast is the low-latency mode (no cold-boot wait). It is also the default; passed
        # explicitly here to show where the choice goes.
        mode="fast",
    )

    speaker = Speaker()

    @session.on(ServerEventType.SESSION_STARTING)
    def _(_):
        print("Booting the translation pipeline (this can take 30s+)...")

    @session.on(ServerEventType.SESSION_CREATED)
    def _(_):
        print(f"Ready. Speak in {source_language}; you'll hear {target_language}. Ctrl-C to stop.")

    @session.on(ServerEventType.TRANSCRIPT_COMPLETED)
    def _(event):
        print(f"\n[you]         {event.transcript}")

    @session.on(ServerEventType.TEXT_DONE)
    def _(event):
        print(f"[translation] {event.text}")

    @session.on(ServerEventType.AUDIO_DELTA)
    def _(event):
        speaker.feed(event.data)

    @session.on(ServerEventType.ERROR)
    def _(err):
        print(f"\nServer error: {err.message}", file=sys.stderr)

    @session.on(ServerEventType.CLOSED)
    def _(info):
        print(f"\nClosed: code={info.code} reason={info.reason!r}")

    async with session:
        await session.wait_until_ready()
        speaker.start()
        mic = Microphone(sample_rate=SAMPLE_RATE, chunk_size=SAMPLE_RATE // 10)
        try:
            await session.stream_audio(mic)
        except KeyboardInterrupt:
            pass
        finally:
            speaker.close()


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "en-US"
    tgt = sys.argv[2] if len(sys.argv) > 2 else "es-ES"
    try:
        asyncio.run(main(src, tgt))
    except KeyboardInterrupt:
        pass
