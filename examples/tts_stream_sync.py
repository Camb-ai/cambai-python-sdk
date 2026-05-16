import os
from dotenv import load_dotenv
from camb.client import CambAI, save_stream_to_file
from camb.types.stream_tts_output_configuration import StreamTtsOutputConfiguration

load_dotenv()


def first_voice_id(voices: list) -> int:
    v = voices[0]
    return int(v["id"]) if isinstance(v, dict) else int(v.id)


def main() -> None:
    client = CambAI(api_key=os.environ["CAMB_API_KEY"])
    voice_id_raw = os.getenv("TTS_VOICE_ID")
    if voice_id_raw:
        voice_id = int(voice_id_raw)
    else:
        voices = client.voice_cloning.list_voices()
        voice_id = first_voice_id(voices)

    # format: e.g. mp3, wav; speech_model matches models in the docs
    stream = client.text_to_speech.tts(
        text="Hello from the Camb Python SDK.",
        language="en-us",
        voice_id=voice_id,
        speech_model="mars-flash",
        output_configuration=StreamTtsOutputConfiguration(format="mp3"),
    )
    out_path = os.getenv("TTS_OUT_PATH", "tts_output.mp3")
    save_stream_to_file(stream, out_path)


if __name__ == "__main__":
    main()
