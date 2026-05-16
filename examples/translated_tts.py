import os
import time

from dotenv import load_dotenv
from camb.client import CambAI
from camb.types.get_tts_result_out_file_url import GetTtsResultOutFileUrl
from camb.types.language_enums import Languages

load_dotenv()

POLL_INTERVAL_SECONDS = 3


def main() -> None:
    client = CambAI(api_key=os.environ["CAMB_API_KEY"])
    create_out = client.translated_tts.create_translated_tts(
        text="Good morning, welcome to our service.",
        voice_id=147320, # more voices: client.voice_cloning.list_voices()
        source_language=Languages.EN_US,
        target_language=Languages.HI_IN,
    )
    task_id = create_out.task_id

    run_id = None
    while True:
        status = client.translated_tts.get_translated_tts_task_status(task_id)
        if status.status == "SUCCESS":
            run_id = status.run_id
            break
        time.sleep(POLL_INTERVAL_SECONDS)

    assert run_id is not None
    info = client.text_to_speech.get_tts_run_info(run_id, output_type="FILE_URL")
    if isinstance(info, GetTtsResultOutFileUrl):
        print(info.output_url)
    else:
        print(info)


if __name__ == "__main__":
    main()
