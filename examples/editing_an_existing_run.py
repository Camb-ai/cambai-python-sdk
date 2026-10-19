import os
import time

from camb.client import CambAI
from camb.types.language_enums import Languages


POLL_INTERVAL_SECONDS = 5
PENDING_STATUS = "PENDING"


def wait_for(poll, task_id: str):
    while True:
        result = poll(task_id=task_id)
        if result.status != PENDING_STATUS:
            return result
        time.sleep(POLL_INTERVAL_SECONDS)


def main() -> None:
    api_key = os.getenv("CAMB_API_KEY")
    run_id = os.getenv("CAMB_RUN_ID")

    if not api_key:
        print("Set CAMB_API_KEY to run this example.")
        return
    if not run_id:
        print("Set CAMB_RUN_ID to a finished dub run to edit.")
        return

    client = CambAI(api_key=api_key)
    run_id = int(run_id)

    # Re-transcribe one window instead of redoing the whole run. Omit the window
    # to redo all of it, and omit source_language to use the run's own.
    task = client.spot_transcription.create_spot_transcription(
        run_id=run_id,
        start_seconds=30,
        end_seconds=45,
    )
    result = wait_for(client.spot_transcription.get_spot_transcription_status, task.task_id)
    print(f"spot transcription: {result.status}")

    # Re-translate named lines only. target_language picks which of the run's
    # translations to redo, so the run must already have a transcript in it.
    # fix_duration keeps the original timing, which matters once the audio is
    # cut to picture; rephrase lets it move.
    task = client.spot_translation.create_spot_translation(
        run_id=run_id,
        dialogue_ids=["8842"],
        source_language=Languages.EN_US,
        target_language=Languages.ES_ES,
        generation_type="fix_duration",
    )
    result = wait_for(client.spot_translation.get_spot_translation_status, task.task_id)
    print(f"spot translation: {result.status}")

    # Narrate what happens on screen. Name a speaker_id or voice_id, or omit
    # both and let the pipeline choose.
    task = client.scene_audio_description.create_scene_audio_description(run_id=run_id)
    result = wait_for(
        client.scene_audio_description.get_scene_audio_description_status, task.task_id
    )
    print(f"audio description: {result.status}")

    # Pull one layer out of the finished mix: dialogue, background or foreground.
    task = client.export_stems.create_export_stems(
        run_id=run_id,
        audio_to_export="background",
        type="wav",
    )
    result = wait_for(client.export_stems.get_export_stems_status, task.task_id)
    print(f"stem export: {result.status}")


if __name__ == "__main__":
    main()
