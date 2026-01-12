import base64
from camb.client import CambAI, save_stream_to_file

client = CambAI(
    tts_provider="baseten",
    provider_params={
        "api_key": "xyz",
        "mars_pro_url": "https://model-xyz.api.baseten.co/environments/production/predict"
    }
)

def main():
    response = client.text_to_speech.tts(
        text="Hello World and my dear friends",
        language="en-us",
        speech_model="mars-pro",
        request_options={
            "additional_body_parameters": {
                "reference_audio": base64.b64encode(open("audio.wav", "rb").read()).decode('utf-8'),
                "reference_language": "en-us"  # required
            },
            "timeout_in_seconds": 300
        }
    )
    save_stream_to_file(response, "tts_output.mp3")
    print("Success! Audio saved to tts_output.mp3")

if __name__ == "__main__":
    main()
