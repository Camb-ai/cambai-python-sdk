import os
import time
from dotenv import load_dotenv
from camb.client import CambAI
from camb.types.language_enums import Languages

load_dotenv()

# Seconds between polls while the transcription job runs.
POLL_INTERVAL_SECONDS = 3


def main() -> None:
    client = CambAI(api_key=os.environ["CAMB_API_KEY"])
    response = client.transcription.create_transcription(
        language=Languages.EN_US,
        media_url=os.environ["TRANSCRIPTION_MEDIA_URL"],
    )
    task_id = response.task_id
    assert task_id is not None

    run_id = None
    while True:
        status = client.transcription.get_transcription_task_status(task_id)
        if status.status == "SUCCESS":
            run_id = status.run_id
            break
        time.sleep(POLL_INTERVAL_SECONDS)

    assert run_id is not None
    client.transcription.get_transcription_result(
        run_id=run_id,
        word_level_timestamps=True,
    )


if __name__ == "__main__":
    main()
