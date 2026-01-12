import asyncio
import os
from camb.client import AsyncCambAI, save_async_stream_to_file
from camb.types.stream_tts_output_configuration import StreamTtsOutputConfiguration

# Initialize the async client
client = AsyncCambAI(api_key=os.getenv("CAMB_API_KEY"))

async def main():
    # Stream the TTS generation
    voices = await client.voice_cloning.list_voices()
    voice_id = voices[1]["id"]
    print(f">>> using voice id: {voice_id}")
    response = client.text_to_speech.tts(
        text="Experience ultra-low latency streaming with Camb AI.",
        language="en-us",
        speech_model="mars-pro",
        voice_id=voice_id,
        output_configuration=StreamTtsOutputConfiguration(
            format="wav"
        )
    )
    
    # Save the stream to a file (or process chunks as they arrive)
    await save_async_stream_to_file(response, "async_stream_output.wav")
    print("Audio stream saved to async_stream_output.wav")

if __name__ == "__main__":
    asyncio.run(main())