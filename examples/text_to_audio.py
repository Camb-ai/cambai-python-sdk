import os
from camb.client import CambAI, save_stream_to_file
import time

client = CambAI(api_key=os.getenv("CAMB_API_KEY"))

def test_text_to_audio():
    # Note: audio_type values are "sound" or "music"
    response = client.text_to_audio.create_text_to_audio(
        prompt="A futuristic sci-fi laser sound effect",
        duration=3.0,
        audio_type="sound"
    )
    task_id = response.task_id
    print(f"Task created with ID: {task_id}")
    if not task_id:
        print("Failed to get task ID.")
        return
    # Poll for status
    print("Polling for status...")
    while True:
        status_response = client.text_to_audio.get_text_to_audio_status(task_id=task_id)
        print(f"Current Status: {status_response.status}")
        if status_response.status == "SUCCESS":
            save_stream_to_file(client.text_to_audio.get_text_to_audio_result(status_response.run_id), "text_to_audio_output.mp3")
            break
        time.sleep(2)

test_text_to_audio()