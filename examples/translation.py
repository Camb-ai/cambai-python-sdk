import os
import time

from camb.client import CambAI
from camb.types.language_enums import Languages


SOURCE_LANGUAGE = Languages.EN_US
TARGET_LANGUAGE = Languages.FR_FR
TEXTS = [
    "Hello, how are you today?",
    "This translation was created with the Camb Python SDK.",
]
POLL_INTERVAL_SECONDS = 2

client = CambAI(api_key=os.getenv("CAMB_API_KEY"))


def main() -> None:
    print(f">> source enum: {SOURCE_LANGUAGE} ({SOURCE_LANGUAGE.value})")
    print(f">> target enum: {TARGET_LANGUAGE} ({TARGET_LANGUAGE.value})")

    create_response = client.translation.create_translation(
        texts=TEXTS,
        source_language=SOURCE_LANGUAGE,
        target_language=TARGET_LANGUAGE,
    )
    task_id = create_response["task_id"]

    print(f">> translation task created: {task_id}")
    while True:
        status_response = client.translation.get_translation_task_status(task_id)
        status = status_response.status
        run_id = status_response.run_id
        print(f">> task status: {status}")
        if status == "SUCCESS":
            break
        time.sleep(POLL_INTERVAL_SECONDS)

    result = client.translation.get_translation_result(run_id=run_id)
    print(">> translated texts:")
    for index, text in enumerate(result.texts, start=1):
        print(f"{index}. {text}")


if __name__ == "__main__":
    main()
