import base64
import os

from dotenv import load_dotenv
from camb.client import CambAI, save_stream_to_file

load_dotenv()

client = CambAI(
    tts_provider="baseten",
    provider_params={
        "api_key": os.environ["BASETEN_API_KEY"],
        "mars_url": os.getenv("BASETEN_MARS_URL") or os.getenv("BASETEN_MARS_PRO_URL"),
    },
)


def main() -> None:
    with open("audio.wav", "rb") as f:
        reference_audio = base64.b64encode(f.read()).decode("utf-8")

    stream = client.text_to_speech.tts(
        text="Hello from a Baseten-hosted MARS deployment.",
        language="en-us",
        speech_model="mars-flash",
        request_options={
            "additional_body_parameters": {
                "reference_audio": reference_audio,
                "reference_language": "en-us",  # required
            },
            "timeout_in_seconds": 300,
        },
    )
    save_stream_to_file(stream, "tts_output.wav")
    print("Success! Audio saved to tts_output.wav")


if __name__ == "__main__":
    main()
