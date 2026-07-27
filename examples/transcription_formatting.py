import os
import time

from camb.client import CambAI
from camb.types.language_enums import Languages
from camb.types.subtitle_formatting_options import SubtitleFormattingOptions


POLL_INTERVAL_SECONDS = 5


def main() -> None:
    api_key = os.getenv("CAMB_API_KEY")
    media_url = os.getenv("CAMB_MEDIA_URL")
    media_file_path = os.getenv("CAMB_MEDIA_FILE")

    if not api_key:
        print("Set CAMB_API_KEY to run this example.")
        return

    client = CambAI(api_key=api_key)
    formatting_options = SubtitleFormattingOptions(
        max_segment_duration_in_seconds=6,
        max_characters_in_segment=42,
    )

    if media_url:
        create_response = client.transcription.create_transcription(
            language=Languages.EN_US,
            media_url=media_url,
            formatting_options=formatting_options,
        )
    elif media_file_path:
        with open(media_file_path, "rb") as media_file:
            create_response = client.transcription.create_transcription(
                language=Languages.EN_US,
                media_file=media_file,
                formatting_options=formatting_options,
            )
    else:
        print("Set CAMB_MEDIA_URL or CAMB_MEDIA_FILE to run this example.")
        return

    task_id = create_response.task_id
    if not task_id:
        print("Failed to create transcription task.")
        return

    print(f">> transcription task created: {task_id}")
    while True:
        status_response = client.transcription.get_transcription_task_status(task_id)
        print(f">> task status: {status_response.status}")
        if status_response.status == "SUCCESS":
            break
        time.sleep(POLL_INTERVAL_SECONDS)

    result = client.transcription.get_transcription_result(
        status_response.run_id,
        format_type="srt",
        data_type="raw_data",
    )
    print(">> exported transcript:")
    print(result.transcript)


if __name__ == "__main__":
    main()
