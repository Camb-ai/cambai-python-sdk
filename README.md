# Camb AI Python SDK 🎙️

[![PyPI version](https://img.shields.io/pypi/v/camb-ai-sdk.svg?style=flat-square)](https://pypi.org/project/camb-ai-sdk/)  
[![License](https://img.shields.io/pypi/l/camb-ai-sdk.svg?style=flat-square)](https://github.com/your-org/camb-ai-python-sdk/blob/main/LICENSE)  
[![Build Status](https://img.shields.io/github/actions/workflow/status/your-org/camb-ai-python-sdk/ci.yml?branch=main&style=flat-square)](https://github.com/your-org/camb-ai-python-sdk/actions)

The official Python SDK for interacting with Camb AI's powerful voice and audio generation APIs. Create expressive speech, unique voices, and rich soundscapes with just a few lines of Python.

---

## ✨ Features

- **Expressive Text-to-Speech**: Convert text into natural-sounding speech using a wide range of pre-existing voices.  
- **Generative Voices**: Create entirely new, unique voices from text prompts and descriptions.  
- **Soundscapes from Text**: Generate ambient audio and sound effects from textual descriptions.  
- Access to voice cloning, translation, and more (refer to full API documentation).

---

## 📦 Installation

You'll need **Python 3.9** or higher.

Install the SDK using pip:

```bash
pip install camb-ai-sdk
````

> If the package is not yet on PyPI, you can install it directly from GitHub for now:
>
> ```bash
> pip install git+https://github.com/your-org/camb-ai-python-sdk.git
> ```

---

## 🔑 Authentication

To use the Camb AI SDK, you'll need an API key. You can authenticate in either of the following ways:

### 1. Pass the API key directly

```python
from cambai.api import apis_api

client = apis_api.CambAI(api_key="YOUR_CAMB_AI_API_KEY")
```

### 2. Use an environment variable
Set your API key as an environment variable named `CAMB_AI_API_KEY`:

   ```bash
   export CAMB_AI_API_KEY="your_actual_api_key_here"
   ```
---

## 🚀 Getting Started: Core Capabilities

Below are examples of how to use some of the core features of the Camb AI SDK.

### 1. Text-to-Speech (TTS)

Convert text into spoken audio using one of Camb AI's high-quality voices.

#### a) Get an Audio URL

This is useful if you want to play the audio in a web application or share a link.

```python
from cambai.api import apis_api
from cambai.rest import ApiException

# Initialize client (ensure API key is set)
# client = apis_api.CambAI(api_key="YOUR_CAMB_AI_API_KEY")

try:
    print("Generating speech and getting audio URL...")
    audio_url = client.text_to_speech(
        text="Hello from Camb AI! This is a test of our Text-to-Speech API.",
        voice_id=20303  # Example voice ID, find more with client.list_voices()
    )
    print(f"Success! Your audio is ready at: {audio_url}")

except ApiException as e:
    print(f"API Exception when calling text_to_speech: {e}\n")
```

#### b) Save Audio Directly to a File

Generate speech and save it as an MP3 file (or other supported formats).

```python
from cambai.api import apis_api
from cambai.models.output_type import OutputType  # Make sure to import OutputType
from cambai.rest import ApiException

# Initialize client
# client = apis_api.CambAI(api_key="YOUR_CAMB_AI_API_KEY")

file_path = "my_generated_speech.mp3"

try:
    print(f"Generating speech and saving to {file_path}...")
    # This function will return None if save_to_file is specified and output_type is RAW_BYTES,
    # as the file is written directly.
    client.text_to_speech(
        text="This is another test, saving directly to a file.",
        voice_id=20303,                # Example voice ID
        output_type=OutputType.RAW_BYTES,  # Specify raw bytes for direct saving
        save_to_file=file_path,
        verbose=True                   # For more detailed logging from the SDK
    )
    print(f"Success! Audio saved to {file_path}")

except ApiException as e:
    print(f"API Exception when calling text_to_speech (save to file): {e}\n")
```

#### c) List Available Voices

You can list available voices to find a `voice_id` that suits your needs:

```python
try:
    voices = client.list_voices()
    print(f"Found {len(voices)} voices:")
    for voice in voices[:5]:  # Print first 5 as an example
        print(f"  - ID: {voice.id}, Name: {voice.voice_name}, Gender: {voice.gender}, Language: {voice.language}")
except ApiException as e:
    print(f"Could not list voices: {e}")
```

---

### 2. Text-to-Voice (Generative Voice)

Create completely new and unique voices from a textual description of the desired voice characteristics.

```python
from cambai.api import apis_api
from cambai.rest import ApiException

# Initialize client
# client = apis_api.CambAI(api_key="YOUR_CAMB_AI_API_KEY")

output_file = "generated_voice_output.mp3"

try:
    print("Generating a new voice and speech...")
    # The 'text_to_voice' method returns a dict consisting of 3 sample URLs
    result = client.text_to_voice(
        text="Crafting a unique voice with a hint of mystery and warmth.",
        voice_description="A smooth, baritone voice with a slight echo, perfect for storytelling.",
        verbose=True
    )
    print(result)

except ApiException as e:
    print(f"API Exception when calling text_to_voice: {e}\n")
```

---

### 3. Text-to-Audio (Sound Generation)

Generate sound effects or ambient audio from a descriptive prompt.

```python
from cambai.api import apis_api
from cambai.rest import ApiException

# Initialize client
# client = apis_api.CambAI(api_key="YOUR_CAMB_AI_API_KEY")

output_file = "generated_sound_effect.mp3"

try:
    print(f"Generating sound effect and saving to {output_file}...")
    # Similar to text_to_speech, this will save the file and return None.
    client.text_to_audio(
        prompt="A gentle breeze rustling through autumn leaves in a quiet forest.",
        duration=10,       # Duration of the audio in seconds
        save_to_file=output_file,
        verbose=True
    )
    print(f"Success! Sound effect saved to {output_file}")

except ApiException as e:
    print(f"API Exception when calling text_to_audio: {e}\n")
```

---

## ⚙️ Advanced Usage & Other Features

The Camb AI SDK offers a wide range of capabilities beyond these examples, including:

* Voice Cloning
* Translated TTS
* Audio Dubbing
* Transcription
* And more!

Please refer to the [**Official Camb AI API Documentation**](https://docs.camb.ai/introduction) for a comprehensive list of features and advanced usage patterns.

---



## Documentation for API Endpoints

All URIs are relative to *https://client.camb.ai/apis*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*ApisApi* | [**create_audio_separation**](docs/ApisApi.md#create_audio_separation) | **POST** /audio-separation | Create Audio Separation
*ApisApi* | [**create_custom_voice**](docs/ApisApi.md#create_custom_voice) | **POST** /create-custom-voice | Create Custom Voice
*ApisApi* | [**create_end_to_end_dubbing**](docs/ApisApi.md#create_end_to_end_dubbing) | **POST** /dub | End To End Dubbing
*ApisApi* | [**create_story**](docs/ApisApi.md#create_story) | **POST** /story | Create Story
*ApisApi* | [**create_text_to_sound**](docs/ApisApi.md#create_text_to_sound) | **POST** /text-to-sound | Create Text to Sound
*ApisApi* | [**create_transcription**](docs/ApisApi.md#create_transcription) | **POST** /transcribe | Create Transcription
*ApisApi* | [**create_translated_story**](docs/ApisApi.md#create_translated_story) | **POST** /translated-story/{run_id} | Create Translated Story
*ApisApi* | [**create_translated_tts**](docs/ApisApi.md#create_translated_tts) | **POST** /translated-tts | Create Translated Tts
*ApisApi* | [**create_translation**](docs/ApisApi.md#create_translation) | **POST** /translate | Create Translation
*ApisApi* | [**create_translation_stream**](docs/ApisApi.md#create_translation_stream) | **POST** /translation/stream | Create Translation Stream
*ApisApi* | [**create_tts**](docs/ApisApi.md#create_tts) | **POST** /tts | Create Tts
*ApisApi* | [**create_tts_stream**](docs/ApisApi.md#create_tts_stream) | **POST** /tts-stream | Create TTS Stream
*ApisApi* | [**create_voice_from_description**](docs/ApisApi.md#create_voice_from_description) | **POST** /text-to-voice | Create Voice from Description
*ApisApi* | [**dictionaries_get**](docs/ApisApi.md#dictionaries_get) | **GET** /dictionaries | Get Workspace Dictionaries
*ApisApi* | [**get_audio_separation_run_info_by_id**](docs/ApisApi.md#get_audio_separation_run_info_by_id) | **GET** /audio-separation-result/{run_id} | Get Audio Separation Run Info
*ApisApi* | [**get_audio_separation_status_by_id**](docs/ApisApi.md#get_audio_separation_status_by_id) | **GET** /audio-separation/{task_id} | Get Audio Separation Status
*ApisApi* | [**get_dubbed_run_info_by_id**](docs/ApisApi.md#get_dubbed_run_info_by_id) | **GET** /dub-result/{run_id} | Get Dubbed Run Info
*ApisApi* | [**get_end_to_end_dubbing_status_by_id**](docs/ApisApi.md#get_end_to_end_dubbing_status_by_id) | **GET** /dub/{task_id} | Get End To End Dubbing Status
*ApisApi* | [**get_source_languages**](docs/ApisApi.md#get_source_languages) | **GET** /source-languages | Get Source Languages
*ApisApi* | [**get_story_run_info_by_id**](docs/ApisApi.md#get_story_run_info_by_id) | **GET** /story-result/{run_id} | Get Story Run Info
*ApisApi* | [**get_story_status_by_id**](docs/ApisApi.md#get_story_status_by_id) | **GET** /story/{task_id} | Get Story Status
*ApisApi* | [**get_target_languages**](docs/ApisApi.md#get_target_languages) | **GET** /target-languages | Get Target Languages
*ApisApi* | [**get_text_to_audio_status_by_id**](docs/ApisApi.md#get_text_to_audio_status_by_id) | **GET** /text-to-sound/{task_id} | Get Text To Audio Status
*ApisApi* | [**get_text_to_sound_run_result_by_id**](docs/ApisApi.md#get_text_to_sound_run_result_by_id) | **GET** /text-to-sound-result/{run_id} | Get Text to Sound Run Result
*ApisApi* | [**get_text_to_voice_run_result_by_id**](docs/ApisApi.md#get_text_to_voice_run_result_by_id) | **GET** /text-to-voice-result/{run_id} | Get Text-to-Voice Run Result
*ApisApi* | [**get_transcription_result_by_id**](docs/ApisApi.md#get_transcription_result_by_id) | **GET** /transcription-result/{run_id} | Get Transcription Result
*ApisApi* | [**get_transcription_task_status_by_id**](docs/ApisApi.md#get_transcription_task_status_by_id) | **GET** /transcribe/{task_id} | Create Transcription Task Status
*ApisApi* | [**get_translated_story_run_info**](docs/ApisApi.md#get_translated_story_run_info) | **GET** /translated-story-result/{run_id}/{target_language} | Get Translated Story Run Info
*ApisApi* | [**get_translated_story_status_by_id**](docs/ApisApi.md#get_translated_story_status_by_id) | **GET** /translated-story/{task_id} | Get Translated Story Status
*ApisApi* | [**get_translated_tts_task_status_by_id**](docs/ApisApi.md#get_translated_tts_task_status_by_id) | **GET** /translated-tts/{task_id} | Create Translated Tts Task Status
*ApisApi* | [**get_translation_result_by_id**](docs/ApisApi.md#get_translation_result_by_id) | **GET** /translation-result/{run_id} | Get Translation Result
*ApisApi* | [**get_translation_task_status_by_id**](docs/ApisApi.md#get_translation_task_status_by_id) | **GET** /translate/{task_id} | Create translation Task Status
*ApisApi* | [**get_tts_result_by_id**](docs/ApisApi.md#get_tts_result_by_id) | **GET** /tts/{id} | Get Tts Result
*ApisApi* | [**get_tts_run_info_by_id**](docs/ApisApi.md#get_tts_run_info_by_id) | **GET** /tts-result/{run_id} | Get Tts Run Info
*ApisApi* | [**list_voices**](docs/ApisApi.md#list_voices) | **GET** /list-voices | List Voices
*ApisApi* | [**text_to_voice_task_id_get**](docs/ApisApi.md#text_to_voice_task_id_get) | **GET** /text-to-voice/{task_id} | Get Text-to-Voice Task Status
*AudioSeparationApi* | [**create_audio_separation**](docs/AudioSeparationApi.md#create_audio_separation) | **POST** /audio-separation | Create Audio Separation
*AudioSeparationApi* | [**get_audio_separation_run_info_by_id**](docs/AudioSeparationApi.md#get_audio_separation_run_info_by_id) | **GET** /audio-separation-result/{run_id} | Get Audio Separation Run Info
*AudioSeparationApi* | [**get_audio_separation_status_by_id**](docs/AudioSeparationApi.md#get_audio_separation_status_by_id) | **GET** /audio-separation/{task_id} | Get Audio Separation Status
*DictionariesApi* | [**dictionaries_get**](docs/DictionariesApi.md#dictionaries_get) | **GET** /dictionaries | Get Workspace Dictionaries
*DubApi* | [**get_dubbed_output_in_alt_format_status_by_id**](docs/DubApi.md#get_dubbed_output_in_alt_format_status_by_id) | **GET** /dub-alt-format/{task_id} | Get Dubbed Output in Alt Format Status
*DubApi* | [**get_dubbed_run_transcript**](docs/DubApi.md#get_dubbed_run_transcript) | **GET** /transcript/{run_id}/{language} | Get Dubbed Run Transcript
*DubApi* | [**request_dubbed_output_in_alt_format**](docs/DubApi.md#request_dubbed_output_in_alt_format) | **POST** /dub-alt-format/{run_id}/{language} | Get Dubbed Output in Alt Format
*StoriesApi* | [**create_story**](docs/StoriesApi.md#create_story) | **POST** /story | Create Story
*StoriesApi* | [**create_translated_story**](docs/StoriesApi.md#create_translated_story) | **POST** /translated-story/{run_id} | Create Translated Story
*StoriesApi* | [**get_story_run_info_by_id**](docs/StoriesApi.md#get_story_run_info_by_id) | **GET** /story-result/{run_id} | Get Story Run Info
*StoriesApi* | [**get_translated_story_run_info**](docs/StoriesApi.md#get_translated_story_run_info) | **GET** /translated-story-result/{run_id}/{target_language} | Get Translated Story Run Info
*StoriesApi* | [**get_translated_story_status_by_id**](docs/StoriesApi.md#get_translated_story_status_by_id) | **GET** /translated-story/{task_id} | Get Translated Story Status
*TextToAudioApi* | [**create_text_to_sound**](docs/TextToAudioApi.md#create_text_to_sound) | **POST** /text-to-sound | Create Text to Sound
*TextToAudioApi* | [**get_text_to_audio_status_by_id**](docs/TextToAudioApi.md#get_text_to_audio_status_by_id) | **GET** /text-to-sound/{task_id} | Get Text To Audio Status
*TextToAudioApi* | [**get_text_to_sound_run_result_by_id**](docs/TextToAudioApi.md#get_text_to_sound_run_result_by_id) | **GET** /text-to-sound-result/{run_id} | Get Text to Sound Run Result
*TextToSpeechApi* | [**create_tts**](docs/TextToSpeechApi.md#create_tts) | **POST** /tts | Create Tts
*TextToSpeechApi* | [**get_tts_result_by_id**](docs/TextToSpeechApi.md#get_tts_result_by_id) | **GET** /tts/{id} | Get Tts Result
*TextToVoiceApi* | [**create_voice_from_description**](docs/TextToVoiceApi.md#create_voice_from_description) | **POST** /text-to-voice | Create Voice from Description
*TextToVoiceApi* | [**get_text_to_voice_run_result_by_id**](docs/TextToVoiceApi.md#get_text_to_voice_run_result_by_id) | **GET** /text-to-voice-result/{run_id} | Get Text-to-Voice Run Result
*TextToVoiceApi* | [**text_to_voice_task_id_get**](docs/TextToVoiceApi.md#text_to_voice_task_id_get) | **GET** /text-to-voice/{task_id} | Get Text-to-Voice Task Status


## Documentation For Models

 - [AudioOutputFileURLResponse](docs/AudioOutputFileURLResponse.md)
 - [AudioOutputType](docs/AudioOutputType.md)
 - [AudioSeparationRunInfoResponse](docs/AudioSeparationRunInfoResponse.md)
 - [BodyTranslateTranslatePost](docs/BodyTranslateTranslatePost.md)
 - [CreateAPIKeyRequestPayload](docs/CreateAPIKeyRequestPayload.md)
 - [CreateCustomVoiceOut](docs/CreateCustomVoiceOut.md)
 - [CreateTTSRequestPayload](docs/CreateTTSRequestPayload.md)
 - [CreateTTSStreamRequestPayload](docs/CreateTTSStreamRequestPayload.md)
 - [CreateTextToAudioRequestPayload](docs/CreateTextToAudioRequestPayload.md)
 - [CreateTextToVoiceRequestPayload](docs/CreateTextToVoiceRequestPayload.md)
 - [CreateTranslatedStoryRequestPayload](docs/CreateTranslatedStoryRequestPayload.md)
 - [CreateTranslatedTTSRequestPayload](docs/CreateTranslatedTTSRequestPayload.md)
 - [CreateTranslationStreamRequestPayload](docs/CreateTranslationStreamRequestPayload.md)
 - [DialogueItem](docs/DialogueItem.md)
 - [Dictionary](docs/Dictionary.md)
 - [DubAltFormatResponseBody](docs/DubAltFormatResponseBody.md)
 - [DubbedOutputInAltFormatRequestPayload](docs/DubbedOutputInAltFormatRequestPayload.md)
 - [EndToEndDubbingRequestPayload](docs/EndToEndDubbingRequestPayload.md)
 - [ExpireAPIKeyRequestPayload](docs/ExpireAPIKeyRequestPayload.md)
 - [Formalities](docs/Formalities.md)
 - [Gender](docs/Gender.md)
 - [HTTPValidationError](docs/HTTPValidationError.md)
 - [LanguageItem](docs/LanguageItem.md)
 - [Languages](docs/Languages.md)
 - [OrchestratorPipelineResult](docs/OrchestratorPipelineResult.md)
 - [OutputAPIKey](docs/OutputAPIKey.md)
 - [OutputFormat](docs/OutputFormat.md)
 - [OutputType](docs/OutputType.md)
 - [RequestDubbedOutputInAltFormat200Response](docs/RequestDubbedOutputInAltFormat200Response.md)
 - [RunInfoResponse](docs/RunInfoResponse.md)
 - [StoryRunInfoResponse](docs/StoryRunInfoResponse.md)
 - [TTSStreamOutputFormat](docs/TTSStreamOutputFormat.md)
 - [TaskID](docs/TaskID.md)
 - [TaskStatus](docs/TaskStatus.md)
 - [TextToVoiceRunInfoResponse](docs/TextToVoiceRunInfoResponse.md)
 - [TranscriptDataType](docs/TranscriptDataType.md)
 - [TranscriptFileFormat](docs/TranscriptFileFormat.md)
 - [TranslationResult](docs/TranslationResult.md)
 - [ValidationError](docs/ValidationError.md)
 - [ValidationErrorLocInner](docs/ValidationErrorLocInner.md)
 - [VideoOutputTypeWithoutAVI](docs/VideoOutputTypeWithoutAVI.md)
 - [VoiceItem](docs/VoiceItem.md)


<a id="documentation-for-authorization"></a>
## Documentation For Authorization


Authentication schemes defined for the API:
<a id="APIKeyHeader"></a>
### APIKeyHeader

- **Type**: API key
- **API key parameter name**: x-api-key
- **Location**: HTTP header


## Author




