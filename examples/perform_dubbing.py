import os
from camb.client import CambAI
import time
from camb.types.language_enums import Languages

client = CambAI(api_key=os.getenv("CAMB_API_KEY"))  

def perform_dubbing():
    response = client.dub.create_dub(
        video_url="https://www.youtube.com/...link...",
        source_language=Languages.EN_US,
        target_language=Languages.HI_IN
    )
    task_id = response.task_id
    print(f"Dub Task created with ID: {task_id}")
    while True:
        status_response = client.dub.get_dubbing_status(task_id=task_id)
        print(f"Current Status: {status_response.status}")
        if status_response.status == "SUCCESS":
            print(client.dub.get_dubbed_run_info(status_response.run_id))
            break
        time.sleep(5)

perform_dubbing()