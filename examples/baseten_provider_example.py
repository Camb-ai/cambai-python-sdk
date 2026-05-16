import base64
import os
from dotenv import load_dotenv
from camb.client import CambAI, save_stream_to_file

load_dotenv()


def main() -> None:
    api_key = os.environ["BASETEN_API_KEY"]
    mars_url = os.getenv("BASETEN_MARS_URL") or os.getenv("BASETEN_MARS_PRO_URL")
    ref_path = os.getenv("BASETEN_REFERENCE_AUDIO_PATH", "audio.wav")

    client = CambAI(
        tts_provider="baseten",
        provider_params={"api_key": api_key, "mars_url": mars_url},
    )

    with open(ref_path, "rb") as f:
        reference_audio = base64.b64encode(f.read()).decode("utf-8")

    stream = client.text_to_speech.tts(
        text="Hello from a Baseten-hosted MARS deployment.",
        language="en-us",
        speech_model="mars-flash",
        request_options={
            "additional_body_parameters": {
                "reference_audio": reference_audio,
                "reference_language": "en-us",
            },
            "timeout_in_seconds": 300,
        },
    )
    out_path = os.getenv("TTS_OUT_PATH", "tts_output.wav")
    save_stream_to_file(stream, out_path)


if __name__ == "__main__":
    main()
