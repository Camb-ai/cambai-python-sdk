import asyncio
import os
from dotenv import load_dotenv
from camb.client import AsyncCambAI, save_async_stream_to_file
from camb.types.stream_tts_output_configuration import StreamTtsOutputConfiguration

load_dotenv()

async def main() -> None:
    client = AsyncCambAI(api_key=os.environ["CAMB_API_KEY"])
    stream = client.text_to_speech.tts(
        text="Streaming TTS with the async client.",
        language="en-us",
        speech_model="mars-pro",
        voice_id=147320,  # GET /list-voices: await client.voice_cloning.list_voices()
        output_configuration=StreamTtsOutputConfiguration(format="wav"),
    )
    out_path = os.getenv("TTS_OUT_PATH", "async_stream_output.wav")
    await save_async_stream_to_file(stream, out_path)


if __name__ == "__main__":
    asyncio.run(main())
