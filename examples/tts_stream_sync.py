import os
from dotenv import load_dotenv
from camb.client import CambAI, save_stream_to_file
from camb.types.stream_tts_output_configuration import StreamTtsOutputConfiguration

load_dotenv()

def main() -> None:
    client = CambAI(api_key=os.environ["CAMB_API_KEY"])
    stream = client.text_to_speech.tts(
        text="Hello from the Camb Python SDK.",
        language="en-us",
        voice_id=147320, # more voices: client.voice_cloning.list_voices()
        speech_model="mars-flash",
        output_configuration=StreamTtsOutputConfiguration(format="mp3"),
    )
    out_path = os.getenv("TTS_OUT_PATH", "tts_output.mp3")
    save_stream_to_file(stream, out_path)


if __name__ == "__main__":
    main()
