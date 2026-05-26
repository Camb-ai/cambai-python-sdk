"""Stream microphone audio to the CAMB live transcription WebSocket.

Run with:

    pip install camb-sdk
    CAMB_API_KEY=... python examples/live_transcription_microphone.py
"""

import asyncio
import os

from camb.client import CambAI
from camb.live_transcription import Microphone, ServerMessageType


async def main() -> None:
    client = CambAI(api_key=os.environ["CAMB_API_KEY"])

    session = await client.live_transcription.connect(
        model="boli-v5",
        language="en-us",
        sample_rate=16000,
    )

    @session.on(ServerMessageType.READY)
    def _ready(_):
        print("Session ready. Speak into the microphone; Ctrl-C to stop.")

    @session.on(ServerMessageType.RESULTS)
    def _results(msg):
        text = msg.transcript.strip()
        if not text:
            return
        if not msg.is_final:
            print(f"[Interim] {text}\n", end="", flush=True)
        else:
            print(f"\r\033[K{text}\n", end="", flush=True)

    @session.on(ServerMessageType.ERROR)
    def _error(err):
        # Leading newline: an interim line may be in progress (no newline yet).
        print(f"\nServer error: {err.code} {err.message}")

    @session.on(ServerMessageType.CLOSED)
    def _closed(info):
        print(f"\nClosed: code={info.code} reason={info.reason!r}")

    async with session:
        mic = Microphone(sample_rate=16000, chunk_size=1600)
        try:
            await session.stream_audio(mic)
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    asyncio.run(main())
