"""Stream microphone audio to the CAMB live transcription WebSocket.

Requires ``sox`` on the host (e.g. ``brew install sox`` on macOS).

Run with::

    pip install camb-sdk
    export CAMB_API_KEY=...
    python examples/live_transcription_microphone.py
"""

import asyncio
import os
import sys

from camb.client import CambAI
from camb.live_transcription import Microphone, ServerMessageType, bind_transcript_printer


async def main() -> None:
    client = CambAI(api_key=os.environ["CAMB_API_KEY"])

    session = await client.live_transcription.connect(
        model="boli-v5",
        language="en-us",
        sample_rate=16000,
    )

    printer = bind_transcript_printer(session)

    @session.on(ServerMessageType.READY)
    def _ready(_):
        print("Session ready. Speak into the microphone; Ctrl-C to stop.")

    @session.on(ServerMessageType.ERROR)
    def _error(err):
        printer.newline()
        print(f"Server error: {err.code} {err.message}")

    @session.on(ServerMessageType.CLOSED)
    def _closed(info):
        printer.newline()
        print(f"Closed: code={info.code} reason={info.reason!r}")

    async with session:
        await session.wait_until_ready(timeout=10)
        mic = Microphone(sample_rate=16000, chunk_size=1600)
        try:
            await session.stream_audio(mic)
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    asyncio.run(main())
