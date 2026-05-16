import os
import time
from dotenv import load_dotenv
from camb.client import CambAI
from camb.types.language_enums import Languages

load_dotenv()

POLL_INTERVAL_SECONDS = 5


def main() -> None:
    client = CambAI(api_key=os.environ["CAMB_API_KEY"])
    with open(os.environ["STORY_FILE_PATH"], "rb") as f:
        response = client.story.create_story(
            file=f,
            source_language=Languages.EN_US,
            title=os.getenv("STORY_TITLE", "My Story"),
        )
    task_id = response.task_id
    assert task_id is not None

    while True:
        status = client.story.get_story_status(task_id=task_id)
        if status.status == "SUCCESS":
            info = client.story.get_story_run_info(run_id=status.run_id)
            print(info.get("audio_url"))
            return
        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
