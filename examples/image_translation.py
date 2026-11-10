import os
import time

from camb.client import CambAI
from camb.types.language_enums import Languages

POLL_INTERVAL_SECONDS = 5

client = CambAI(api_key=os.getenv("CAMB_API_KEY"))


def main() -> None:
    created = client.image_translation.create_image_translation(
        source_language=Languages.EN_US,
        target_languages=[Languages.ES_ES],
        media_url="https://example.com/poster.png",
        content_kind="generic",
        project_name="Poster ES",
    )
    print(f">> image translation task created: {created.task_id} run_id={created.run_id}")

    while True:
        status_response = client.image_translation.get_image_translation_status(created.task_id)
        print(f">> task status: {status_response.status}")
        if status_response.status == "SUCCESS":
            break
        if status_response.status == "ERROR":
            raise RuntimeError(status_response.exception_reason)
        time.sleep(POLL_INTERVAL_SECONDS)

    result = client.image_translation.get_image_translation_result(created.run_id)
    print(result.download_url)

    project = client.image_translation.get_image_translation_project(created.run_id)
    print(f">> pages: {len(project.pages)}")


if __name__ == "__main__":
    main()
