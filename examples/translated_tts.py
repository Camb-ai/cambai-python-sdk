import os
import time
from dotenv import load_dotenv
from camb.client import CambAI
from camb.types.get_tts_result_out_file_url import GetTtsResultOutFileUrl
from camb.types.language_enums import Languages

load_dotenv()

POLL_INTERVAL_SECONDS = 3


def first_voice_id(voices: list) -> int:
    v = voices[0]
    return int(v["id"]) if isinstance(v, dict) else int(v.id)


def main() -> None:
    client = CambAI(api_key=os.environ["CAMB_API_KEY"])
    voice_id_raw = os.getenv("VOICE_ID")
    if voice_id_raw:
        voice_id = int(voice_id_raw)
    else:
        voices = client.voice_cloning.list_voices()
        voice_id = first_voice_id(voices)

    create_out = client.translated_tts.create_translated_tts(
        text="Good morning, welcome to our service.",
        voice_id=voice_id,
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
