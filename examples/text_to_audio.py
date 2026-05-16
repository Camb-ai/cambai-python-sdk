import os
import time
from dotenv import load_dotenv
from camb.client import CambAI, save_stream_to_file
load_dotenv()

# audio_type: "sound" or "music"
POLL_INTERVAL_SECONDS = 2


def main() -> None:
    client = CambAI(api_key=os.environ["CAMB_API_KEY"])
    response = client.text_to_audio.create_text_to_audio(
        prompt="A futuristic sci-fi laser sound effect",
        duration=3.0,
        audio_type="sound",
    )
    task_id = response.task_id
    assert task_id is not None

    while True:
        status_response = client.text_to_audio.get_text_to_audio_status(task_id=task_id)
        if status_response.status == "SUCCESS":
            stream = client.text_to_audio.get_text_to_audio_result(status_response.run_id)
            out_path = os.getenv("TEXT_TO_AUDIO_OUT_PATH", "text_to_audio_output.mp3")
            save_stream_to_file(stream, out_path)
            return
        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
