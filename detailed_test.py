import os
import time
import json

import requests
import cambai
from cambai.api import apis_api
from cambai.rest import ApiException
from cambai.models.create_tts_request_payload import CreateTTSRequestPayload
from cambai.models.output_type import OutputType

def print_separator():
    print("\n" + "="*80 + "\n")

# Create an instance of the API class
print("Creating API instance...")
api_instance = apis_api.ApisApi()
print("API instance created successfully")
print_separator()

try:
    # Call the list voices API
    print("Listing available voices...")
    voices = api_instance.list_voices()
    print(f"Found {len(voices)} voices:")
    for voice in voices:
        print(f"  - ID: {voice.id}, Name: {voice.voice_name}, Gender: {voice.gender}, Language: {voice.language}")
    print_separator()
    
    # Create a TTS request
    print("Creating TTS request...")
    request_payload = CreateTTSRequestPayload(
        text="Hello World, this is a test of the Camb AI Text-to-Speech API.", 
        voice_id=20303,  # Using Arielle voice
        language=1
    )
    print(f"Request payload: text='{request_payload.text}', voice_id={request_payload.voice_id}, language={request_payload.language}")
    
    task_id_obj = api_instance.create_tts(request_payload)
    print(f"Received task ID object: {task_id_obj}")
    
    # Extract the task_id string
    task_id_str = task_id_obj.task_id
    print(f"Extracted task ID string: {task_id_str}")
    print_separator()
    
    # Wait for processing
    wait_time = 10
    print(f"Waiting {wait_time} seconds for processing...")
    time.sleep(wait_time)
    print("Wait complete")
    print_separator()
    
    # Get the result using the task_id string
    print(f"Getting result for task ID: {task_id_str}")
    print(f"Type of task_id_str: {type(task_id_str)}")
    result = api_instance.get_tts_result_by_id(task_id_str)
    print(f"Result: {result}")
    print_separator()
    
    # If the result has a run_id, we can get more details
    if hasattr(result, 'run_id') and result.run_id is not None:
        print(f"Run ID found: {result.run_id}")
        # Suppose result.run_id == 228650
        url_string = api_instance.get_tts_run_info_by_id(result.run_id,  output_type=OutputType.FILE_URL)
        print("Download audio here:", url_string)
        
        print_separator()
        print("Test completed successfully!")
    else:
        print("No run_id found in the result")
        print_separator()
        print("Test completed with partial success (no run_id)")
    
except ApiException as e:
    print(f"Exception when calling API: {e}")
    print(f"Status code: {e.status}")
    print(f"Reason: {e.reason}")
    print(f"Body: {e.body}")
    print(f"Headers: {e.headers}")
    print_separator()
    print("Test failed due to API exception")