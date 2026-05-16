import os
import time
from dotenv import load_dotenv
from camb.client import CambAI
from camb.types.language_enums import Languages

load_dotenv()

SOURCE_LANGUAGE = Languages.EN_US
TARGET_LANGUAGE = Languages.FR_FR
TEXTS = [
    "Hello, how are you today?",
    "This translation was created with the Camb Python SDK.",
]
# Seconds between polls while the translation job runs.
POLL_INTERVAL_SECONDS = 2


def main() -> None:
    client = CambAI(api_key=os.environ["CAMB_API_KEY"])
    create_response = client.translation.create_translation(
        texts=TEXTS,
        source_language=SOURCE_LANGUAGE,
        target_language=TARGET_LANGUAGE,
    )
    task_id = create_response["task_id"]

    run_id = None
    while True:
        status_response = client.translation.get_translation_task_status(task_id)
        if status_response.status == "SUCCESS":
            run_id = status_response.run_id
            break
        time.sleep(POLL_INTERVAL_SECONDS)

    assert run_id is not None
    result = client.translation.get_translation_result(run_id=run_id)
    for line in result.texts:
        print(line)


if __name__ == "__main__":
    main()
