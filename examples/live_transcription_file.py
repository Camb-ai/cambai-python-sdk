"""Stream a local WAV file to the CAMB live transcription WebSocket.

Useful when you cannot capture audio (CI, server, no sox/portaudio) but
still want to exercise the live transcription pipeline end to end. The
file is paced at real time so the server sees arrival patterns
equivalent to a live capture.

Run with:

    export CAMB_API_KEY=...
    python examples/live_transcription_file.py path/to/audio.wav
"""

import asyncio
import os
import sys

from camb.client import CambAI
from camb.live_transcription import FileAudioSource, ServerMessageType


async def main(path: str) -> None:
    import wave

    with wave.open(path, "rb") as wf:
        sample_rate = wf.getframerate()
        channels = wf.getnchannels()

    client = CambAI(api_key=os.environ["CAMB_API_KEY"])
    session = await client.live_transcription.connect(
        model="boli-v5",
        language="en-us",
        encoding="linear16",
        sample_rate=sample_rate,
        channels=channels,
    )

    @session.on(ServerMessageType.READY)
    def _(_):
        print(f"Streaming {path} at {sample_rate} Hz...")

    @session.on(ServerMessageType.RESULTS)
    def _(msg):
        text = msg.transcript.strip()
        if not text:
            return
        # Interim frames refine the current utterance; print them as they
        # arrive. On is_final the utterance is done — commit it on its own
        # line so the next utterance starts fresh instead of overwriting it.
        if not msg.is_final:
            print(f"[Interim] {text}\n", end="", flush=True)
        else:
            print(f"\r\033[K{text}\n", end="", flush=True)

    @session.on(ServerMessageType.ERROR)
    def _(err):
        # Leading newline: an interim line may be in progress (no newline yet).
        print(f"\n[error] {err.code}: {err.message}")

    @session.on(ServerMessageType.CLOSED)
    def _(info):
        print(f"\nClosed: code={info.code} reason={info.reason!r}")

    async with session:
        await session.wait_until_ready(timeout=10)
        await session.stream_audio(FileAudioSource(path, chunk_ms=100, real_time=True))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python examples/live_transcription_file.py PATH_TO_WAV", file=sys.stderr)
        sys.exit(2)
    asyncio.run(main(sys.argv[1]))
