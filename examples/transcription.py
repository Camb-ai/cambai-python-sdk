import time

from camb.client import CambAI

client = CambAI()  # Set the CAMB_API_KEY environment variable.

# Edit these values for your request.
job = client.transcription.create_transcription(
    media_url="https://example.com/meeting.mp3",
    language="auto",             # Or "en-us".
    # transcription_mode="slow" can be chosen; the default is "fast".
    run_audio_cleaning=False,     # Skip source separation.
    include_music_in_fg=False,   # Only applies when cleaning is enabled.
)
print("Task ID:", job.task_id)

while True:
    status = client.transcription.get_transcription_task_status(job.task_id)
    if status.status == "ERROR":
        raise RuntimeError(status.exception_reason)
    if status.status == "SUCCESS":
        break
    time.sleep(5)

result = client.transcription.get_transcription_result(status.run_id)
print(result)
