import os
import time
from dotenv import load_dotenv
from camb.client import CambAI
from camb.types.language_enums import Languages

load_dotenv()

# Seconds between status polls (tune for your job size and rate limits).
POLL_INTERVAL = 5


def main() -> None:
    client = CambAI(api_key=os.environ["CAMB_API_KEY"])
    response = client.dub.create_dub(
        video_url=os.environ["VIDEO_URL"],
        source_language=Languages.EN_US,
        target_language=Languages.HI_IN,
    )
    task_id = response.task_id
    assert task_id is not None
    while True:
        status_response = client.dub.get_dubbing_status(task_id=task_id)
        if status_response.status == "SUCCESS":
            info = client.dub.get_dubbed_run_info(status_response.run_id)
            if info.video_url:
                print(info.video_url)
            print(info.audio_url)
            return
        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
