"""Submit one transcription job with configurable mode and audio preparation.

Set CAMB_API_KEY, then run:
    python examples/transcription_modes.py https://example.com/audio.mp3 --mode fast
    python examples/transcription_modes.py https://example.com/audio.mp3 --mode slow --no-audio-cleaning
"""

import argparse
import time

from camb.client import CambAI


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("media_url", help="Public or signed audio/video URL")
    parser.add_argument("--mode", choices=("fast", "slow"), default="fast")
    parser.add_argument("--language", default="auto", help='Locale such as en-us, or "auto"')
    parser.add_argument("--audio-cleaning", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--include-music-in-fg", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--format-subtitles", action="store_true")
    args = parser.parse_args()

    client = CambAI()  # Reads CAMB_API_KEY from the environment.
    options = {}
    if args.format_subtitles:
        options["formatting_options"] = {
            "max_segment_duration_in_seconds": 6,
            "max_characters_in_segment": 42,
        }
    job = client.transcription.create_transcription(
        media_url=args.media_url,
        language=args.language,
        transcription_mode=args.mode,
        run_audio_cleaning=args.audio_cleaning,
        # Only affects source separation when audio cleaning is enabled.
        include_music_in_fg=args.include_music_in_fg,
        **options,
    )
    print(f"Task: {job.task_id}")

    deadline = time.monotonic() + 900
    while time.monotonic() < deadline:
        status = client.transcription.get_transcription_task_status(job.task_id)
        print(f"Status: {status.status}")
        if status.status == "ERROR":
            raise RuntimeError(f"Transcription failed: {status.exception_reason}")
        if status.status == "SUCCESS":
            if status.run_id is None:
                raise RuntimeError("Successful task returned no run_id")
            result = client.transcription.get_transcription_result(status.run_id)
            print(result)
            return
        time.sleep(5)
    raise TimeoutError(f"Task {job.task_id} is still pending; poll it again later")


if __name__ == "__main__":
    main()
