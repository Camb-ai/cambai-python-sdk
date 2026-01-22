import base64
from camb.client import CambAI, AsyncCambAI, save_stream_to_file, save_async_stream_to_file

client = CambAI(
    tts_provider="baseten",
    provider_params={
        "api_key": "xyz",
        "mars_url": "https://model-xyz.api.baseten.co/environments/production/predict"
    }
)

def main():
    response = client.text_to_speech.tts(
        text="Hello World and my dear friends",
        language="en-us",
        speech_model="mars-flash",
        request_options={
            "additional_body_parameters": {
                "reference_audio": base64.b64encode(open("audio.wav", "rb").read()).decode('utf-8'),
                "reference_language": "en-us"  # required
            },
            "timeout_in_seconds": 300
        }
    )
    save_stream_to_file(response, "tts_output.wav")
    print("Success! Audio saved to tts_output.wav")

if __name__ == "__main__":
    main()
