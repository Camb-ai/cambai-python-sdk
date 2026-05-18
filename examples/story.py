import os
import time
from pathlib import Path

from dotenv import load_dotenv
from camb.client import CambAI
from camb.types.language_enums import Languages

load_dotenv()

RESOURCES_DIR = Path(__file__).resolve().parent / "resources"
STORY_FILE = RESOURCES_DIR / "sample_story.txt"

POLL_INTERVAL_SECONDS = 5

client = CambAI(api_key=os.getenv("CAMB_API_KEY"))


def main() -> None:
    with open(STORY_FILE, "rb") as f:
        response = client.story.create_story(
            file=f,
            source_language=Languages.EN_US,
            title="My Story",
        )
    task_id = response.task_id

    while True:
        status = client.story.get_story_status(task_id=task_id)
        if status.status == "SUCCESS":
            info = client.story.get_story_run_info(run_id=status.run_id)
            print(info.get("audio_url"))
            return
        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
