import os
import time
from dotenv import load_dotenv
from camb.client import CambAI

load_dotenv()

POLL_INTERVAL_SECONDS = 3


def main() -> None:
    client = CambAI(api_key=os.environ["CAMB_API_KEY"])
    create_out = client.text_to_voice.create_text_to_voice(
        text="A confident narrator introducing a documentary.",
        voice_description="Deep, measured baritone. Calm and authoritative.",
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
    client.text_to_voice.get_text_to_voice_result(run_id)


if __name__ == "__main__":
    main()
