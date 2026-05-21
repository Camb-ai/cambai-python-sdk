import os
import time
from dotenv import load_dotenv
from camb.client import CambAI

load_dotenv()

POLL_INTERVAL_SECONDS = 3


def main() -> None:
    client = CambAI(api_key=os.environ["CAMB_API_KEY"])
    with open(os.environ["AUDIO_SEPARATION_MEDIA_PATH"], "rb") as f:
        response = client.audio_separation.create_audio_separation(media_file=f)
    task_id = response.task_id
    assert task_id is not None

    while True:
        status = client.audio_separation.get_audio_separation_status(task_id=task_id)
        if status.status == "SUCCESS":
            result = client.audio_separation.get_audio_separation_run_info(run_id=status.run_id)
            print(result.foreground_audio_url)
            print(result.background_audio_url)
            return
        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
