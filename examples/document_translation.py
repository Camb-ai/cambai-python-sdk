import os
import time

from camb.client import CambAI
from camb.types.language_enums import Languages


POLL_INTERVAL_SECONDS = 5


def main() -> None:
    api_key = os.getenv("CAMB_API_KEY")
    document_path = os.getenv("CAMB_DOCUMENT_PATH")
    document_url = os.getenv("CAMB_DOCUMENT_URL")

    if not api_key:
        print("Set CAMB_API_KEY to run this example.")
        return
    if not document_path and not document_url:
        print("Set CAMB_DOCUMENT_PATH (local DOCX/SRT) or CAMB_DOCUMENT_URL to run this example.")
        return

    client = CambAI(api_key=api_key)

    if document_path:
        with open(document_path, "rb") as document:
            create_response = client.translation.create_doc_translation(
                source_language=Languages.EN_US,
                target_language=Languages.ES_ES,
                media_file=document,
            )
    else:
        create_response = client.translation.create_doc_translation(
            source_language=Languages.EN_US,
            target_language=Languages.ES_ES,
            media_url=document_url,
        )

    task_id = create_response.task_id
    print(f">> document translation task created: {task_id}")
    while True:
        status_response = client.translation.get_doc_translation_task_status(task_id)
        print(f">> task status: {status_response.status}")
        if status_response.status == "SUCCESS":
            break
        if status_response.status == "ERROR":
            print(f">> document translation failed: {status_response.exception_reason}")
            return
        time.sleep(POLL_INTERVAL_SECONDS)

    run_id = status_response.run_id
    if run_id is None:
        print(">> task succeeded but no run_id was returned.")
        return

    result = client.translation.get_doc_translation_result(run_id)
    print(f">> translated document: {result.download_url}")


if __name__ == "__main__":
    main()
