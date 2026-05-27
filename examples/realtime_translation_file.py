"""Realtime speech-to-speech translation from a WAV file.

Streams a local WAV at real-time pace, prints the transcript and translated
text, and writes the translated audio to an output WAV. Useful on machines
with no microphone or speaker (CI, servers) to exercise the realtime pipeline
end to end.

The input WAV must be 16-bit PCM, mono, 24 kHz (the rate the realtime endpoint
expects). Output is written at the same format.

Run with:

    export CAMB_API_KEY=...
    python examples/realtime_translation_file.py input_24k_mono.wav [out.wav] [en-US] [es-ES]
"""

import asyncio
import os
import sys
import wave

from camb.client import CambAI
from camb.live_transcription import FileAudioSource
from camb.realtime import ServerEventType

SAMPLE_RATE = 24000


async def main(in_path: str, out_path: str, source_language: str, target_language: str) -> None:
    api_key = os.environ.get("CAMB_API_KEY")
    if not api_key:
        print("Set CAMB_API_KEY", file=sys.stderr)
        sys.exit(2)

    with wave.open(in_path, "rb") as wf:
        if (wf.getframerate(), wf.getnchannels(), wf.getsampwidth()) != (SAMPLE_RATE, 1, 2):
            print(
                f"Warning: expected 24 kHz mono 16-bit PCM; got "
                f"{wf.getframerate()} Hz, {wf.getnchannels()} ch, {wf.getsampwidth() * 8}-bit. "
                f"Re-encode with: ffmpeg -i {in_path} -ar 24000 -ac 1 -sample_fmt s16 input_24k_mono.wav",
                file=sys.stderr,
            )

    client = CambAI(api_key=api_key)
    session = await client.realtime.connect(
        source_language=source_language,
        target_language=target_language,
    )

    out_audio = bytearray()
    audio_done = asyncio.Event()

    @session.on(ServerEventType.SESSION_STARTING)
    def _(_):
        print("Booting the translation pipeline (this can take 30s+)...")

    @session.on(ServerEventType.SESSION_CREATED)
    def _(_):
        print(f"Ready. Streaming {os.path.basename(in_path)} ({source_language} -> {target_language})...")

    @session.on(ServerEventType.TRANSCRIPT_COMPLETED)
    def _(event):
        print(f"[you]         {event.transcript}")

    @session.on(ServerEventType.TEXT_DONE)
    def _(event):
        print(f"[translation] {event.text}")

    @session.on(ServerEventType.AUDIO_DELTA)
    def _(event):
        out_audio.extend(event.data)

    @session.on(ServerEventType.AUDIO_DONE)
    def _(_):
        audio_done.set()

    @session.on(ServerEventType.ERROR)
    def _(err):
        print(f"Server error: {err.message}", file=sys.stderr)

    async with session:
        await session.wait_until_ready()
        await session.stream_audio(FileAudioSource(in_path, real_time=True))
        # Input is exhausted; give the server time to flush the final
        # translated audio before we close.
        try:
            await asyncio.wait_for(audio_done.wait(), timeout=30)
        except asyncio.TimeoutError:
            print("(no audio.done within 30s; writing what we received)", file=sys.stderr)

    if out_audio:
        with wave.open(out_path, "wb") as out:
            out.setnchannels(1)
            out.setsampwidth(2)
            out.setframerate(SAMPLE_RATE)
            out.writeframes(bytes(out_audio))
        print(f"Wrote {len(out_audio) / (SAMPLE_RATE * 2):.1f}s of translated audio to {out_path}")
    else:
        print("No audio received.", file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "usage: python examples/realtime_translation_file.py INPUT.wav [OUT.wav] [SRC] [TGT]",
            file=sys.stderr,
        )
        sys.exit(2)
    in_path = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else "translated_output.wav"
    src = sys.argv[3] if len(sys.argv) > 3 else "en-US"
    tgt = sys.argv[4] if len(sys.argv) > 4 else "es-ES"
    asyncio.run(main(in_path, out_path, src, tgt))
