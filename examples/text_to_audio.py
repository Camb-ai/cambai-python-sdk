import os
import time

from dotenv import load_dotenv
from camb.client import CambAI, save_stream_to_file

load_dotenv()

# audio_type: "sound" or "music"
POLL_INTERVAL_SECONDS = 2

client = CambAI(api_key=os.getenv("CAMB_API_KEY"))


def test_text_to_audio() -> None:
    response = client.text_to_audio.create_text_to_audio(
        prompt="A futuristic sci-fi laser sound effect",
        duration=3.0,
        audio_type="sound",
    )
    task_id = response.task_id
    print(f"Task created with ID: {task_id}")
    if not task_id:
        print("Failed to get task ID.")
        return

    print("Polling for status...")
    while True:
        status_response = client.text_to_audio.get_text_to_audio_status(task_id=task_id)
        print(f"Current Status: {status_response.status}")
        if status_response.status == "SUCCESS":
            stream = client.text_to_audio.get_text_to_audio_result(status_response.run_id)
            save_stream_to_file(stream, "text_to_audio_output.mp3")
            print("Success! Sound effect saved to text_to_audio_output.mp3")
            break
        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    test_text_to_audio()
