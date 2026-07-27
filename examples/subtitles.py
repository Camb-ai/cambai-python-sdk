import os
import time

from camb.client import CambAI
from camb.types.language_enums import Languages
from camb.types.subtitle_formatting_options import SubtitleFormattingOptions


POLL_INTERVAL_SECONDS = 5


def main() -> None:
    api_key = os.getenv("CAMB_API_KEY")
    media_url = os.getenv("CAMB_MEDIA_URL")

    if not api_key:
        print("Set CAMB_API_KEY to run this example.")
        return
    if not media_url:
        print("Set CAMB_MEDIA_URL to run this example.")
        return

    client = CambAI(api_key=api_key)
    formatting_options = SubtitleFormattingOptions(
        max_segment_duration_in_seconds=6,
        max_characters_in_segment=42,
    )

    create_response = client.subtitles.create_subtitle(
        source_language=Languages.EN_US,
        target_languages=[Languages.ES_ES],
        media_url=media_url,
        formatting_options=formatting_options,
    )

    task_id = create_response.task_id
    if not task_id:
        print("Failed to create subtitle task.")
        return

    print(f">> subtitle task created: {task_id}")
    while True:
        status_response = client.subtitles.get_subtitle_task_status(task_id)
        print(f">> task status: {status_response.status}")
        if status_response.status == "SUCCESS":
            break
        time.sleep(POLL_INTERVAL_SECONDS)

    result = client.subtitles.get_subtitle_result_for_language(
        status_response.run_id,
        Languages.ES_ES,
        format_type="vtt",
        data_type="raw_data",
    )
    print(">> exported subtitle:")
    print(result["transcript"] if isinstance(result, dict) else result.transcript)


if __name__ == "__main__":
    main()
