import os
import time
from dotenv import load_dotenv
from camb.client import CambAI

load_dotenv()

POLL_INTERVAL_SECONDS = 3

SPEECH_TEXT = (
    "Good evening. Tonight, the city sleeps under a thin veil of rain, "
    "and every streetlight looks like a small sun trapped in glass. "
    "If you listen closely, you can hear the rhythm of footsteps fading "
    "into the distance—steady, unhurried, almost like a heartbeat. "
    "Somewhere, a clock strikes the hour, and for a moment, everything feels still."
)

VOICE_DESCRIPTION = (
    "Adult male, late 30s to early 40s, North American accent with a neutral, "
    "broadcast-quality tone. Deep, warm baritone with smooth resonance and clear "
    "diction. Pace is measured and unhurried, with gentle pauses at commas and "
    "a slight lift at the end of reflective sentences. Delivery is calm, intimate, "
    "and slightly wistful—like a late-night radio host reading poetry, not "
    "performing for a crowd. Low breath noise, minimal sibilance, consistent volume, "
    "and a soft, natural smile in the voice without sounding cheerful or salesy."
)


def main() -> None:
    client = CambAI(api_key=os.environ["PROD"])
    create_out = client.text_to_voice.create_text_to_voice(
        text=SPEECH_TEXT,
        voice_description=VOICE_DESCRIPTION,
    )
    task_id = create_out.task_id
    assert task_id is not None

    run_id = None
    while True:
        status = client.text_to_voice.get_text_to_voice_status(task_id)
        if status.status == "SUCCESS":
            run_id = status.run_id
            break
        time.sleep(POLL_INTERVAL_SECONDS)

    assert run_id is not None
    result=client.text_to_voice.get_text_to_voice_result(run_id)
    print(result)


if __name__ == "__main__":
    main()
