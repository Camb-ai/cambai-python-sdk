import os
import time

from camb.client import CambAI
from camb.types.language_enums import Languages

client = CambAI(api_key=os.getenv("CAMB_API_KEY"))


def wait_until_success(task_id: str) -> None:
    while True:
        status = client.image_translation.get_image_translation_status(task_id)
        print(f">> status: {status.status}")
        if status.status == "SUCCESS":
            return
        if status.status == "ERROR":
            raise RuntimeError(status.exception_reason)
        time.sleep(5)


def main() -> None:
    created = client.image_translation.create_image_translation(
        source_language=Languages.EN_US,
        target_languages=[Languages.ES_ES],
        media_url="https://example.com/poster.png",
        content_kind="generic",
        project_name="Poster ES",
    )
    print(f">> created run_id={created.run_id}")
    wait_until_success(created.task_id)

    project = client.image_translation.get_image_translation_project(created.run_id)
    result = client.image_translation.get_image_translation_result(created.run_id)
    print(f">> translated images: {result.download_url}")

    region = project.pages[0].regions[0]
    ft = client.image_translation.fine_tune_image_translation(
        run_id=created.run_id,
        target_language_id=Languages.ES_ES,
        region_id=region.region_id,
        prompt="Make the headline shorter",
    )
    wait_until_success(ft.task_id)

    exported = client.image_translation.export_image_translation(
        run_id=created.run_id,
        export_format="PDF",
    )
    if exported.task_id:
        wait_until_success(exported.task_id)

    result = client.image_translation.get_image_translation_result(created.run_id)
    print(f">> updated images: {result.download_url}")


if __name__ == "__main__":
    main()
