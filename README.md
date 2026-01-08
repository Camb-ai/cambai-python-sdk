# Camb.ai Python SDK

PyPI version
License
Build status

The official Python SDK for interacting with Camb AI's powerful voice and audio generation APIs. Create expressive speech, unique voices, and rich soundscapes with just a few lines of Python.

## ✨ Features

- **Dubbing**: Dub your videos into multiple languages with voice cloning!
- **Expressive Text-to-Speech**: Convert text into natural-sounding speech using a wide range of pre-existing voices.
- **Generative Voices**: Create entirely new, unique voices from text prompts and descriptions.
- **Soundscapes from Text**: Generate ambient audio and sound effects from textual descriptions.
- Access to voice cloning, translation, and more (refer to full API documentation).

## 📦 Installation

Install the SDK using pip, ensure Python 3.9+:

```bash
pip install camb-sdk
```

Or through

```bash
pip install git+https://github.com/Camb-ai/cambai-python-sdk
```

## 🔑 Authentication & Accessing Clients

To use the Camb AI SDK, you'll need an API key. You can authenticate it by:

```python
from camb.client import CambAI, AsyncCambAI

# Synchronous Client
client = CambAI(api_key="YOUR_CAMB_API_KEY")

# Asynchronous Client
async_client = AsyncCambAI(api_key="YOUR_CAMB_API_KEY")
```

## 🚀 Getting Started: Examples

### 1. Text-to-Speech (TTS)

Convert text into spoken audio using one of Camb AI's high-quality voices.

#### a) Get an Audio URL or Save to File

```python
from camb.client import CambAI, save_stream_to_file
from camb.types.stream_tts_output_configuration import StreamTtsOutputConfiguration

# Initialize client (ensure API key is set)
client = CambAI(api_key="YOUR_CAMB_API_KEY")

response = client.text_to_speech.tts(
    text="Hello from Camb AI! This is a test of our Text-to-Speech API.",
    voice_id=20303,  # Example voice ID, get from client.voice_cloning.list_voices()
    language="en-us",
    output_configuration=StreamTtsOutputConfiguration(
        format="mp3"
    )
)

save_stream_to_file(response, "tts_output.mp3")
print("Success! Audio saved to tts_output.mp3")
```

#### b) Async Text-to-Speech

You can also stream audio asynchronously using `AsyncCambAI`.

```python
import asyncio
from camb.client import AsyncCambAI, save_async_stream_to_file
from camb.types.stream_tts_output_configuration import StreamTtsOutputConfiguration

async_client = AsyncCambAI(api_key="YOUR_CAMB_API_KEY")

async def main():
    response = async_client.text_to_speech.tts(
        text="Hello, this is a test of the text to audio streaming capabilities.",
        language="en-us",
        voice_id=147319,
        output_configuration=StreamTtsOutputConfiguration(
            format="mp3"
        )
    )
    await save_async_stream_to_file(response, "text_to_audio_output.mp3")
    print("Success! Audio saved to text_to_audio_output.mp3")

asyncio.run(main())
```

#### c) List Available Voices

You can list available voices to find a voice_id that suits your needs:

```python
voices = client.voice_cloning.list_voices()
print(f"Found {len(voices)} voices:")
for voice in voices[:5]:  # Print first 5 as an example
    print(f"  - ID: {voice.id}, Name: {voice.voice_name}, Gender: {voice.gender}, Language: {voice.language}")
```

### 2. Text-to-Voice (Generative Voice)

Create completely new and unique voices from a textual description of the desired voice characteristics.

```python
from camb.client import CambAI

# Initialize client
client = CambAI(api_key="YOUR_CAMB_API_KEY")

try:
    print("Generating a new voice and speech...")
    # Returns 3 sample URLs
    result = client.text_to_voice.create_text_to_voice(
        text="Crafting a truly unique and captivating voice that carries a subtle air of mystery, depth, and gentle warmth.",
        voice_description="A smooth, rich baritone voice layered with a soft echo, ideal for immersive storytelling and emotional depth.",
    )
    print(result)

except Exception as e:
    print(f"Exception when calling text_to_voice: {e}\n")
```

### 3. Text-to-Audio (Sound Generation)

Generate sound effects or ambient audio from a descriptive prompt.

```python
from camb.client save_stream_to_file
import time

response = client.text_to_audio.create_text_to_audio(
    prompt="A gentle breeze rustling through autumn leaves in a quiet forest.",
    duration=10,
    audio_type="sound"
)
task_id = response.task_id
if task_id:
    while True:
        status = client.text_to_audio.get_text_to_audio_status(task_id=task_id)
        if status.status == "SUCCESS":
            result = client.text_to_audio.get_text_to_audio_result(status.run_id)
            save_stream_to_file(result, "sound_effect.mp3")
            print("Success! Sound effect saved to sound_effect.mp3")
            break
        time.sleep(2)
```

### 4. End-to-End Dubbing

Dub videos into different languages with voice cloning and translation capabilities.

```python
from camb.types.language_enums import Languages

result = client.dub.create_dub(
    video_url="your_accessible_video_url",
    source_language=Languages.EN_US,  # English (Or Check client.languages.get_source_languages())
    target_languages=Languages.HI_IN,  # Example target language
)
task_id = response.task_id
print(f"Dub Task created with ID: {task_id}")
while True:
    status_response = client.dub.get_dubbing_status(task_id=task_id)
    print(f"Current Status: {status_response.status}")
    if status_response.status == "SUCCESS":
        dubbed_run_info = client.dub.get_dubbed_run_info(status_response.run_id)
        print(f"Dubbed Video URL: {dubbed_run_info.audio_url}")
        print(f"Dubbed Video URL: {dubbed_run_info.transcript}")
        print(f"Dubbed Video URL: {dubbed_run_info.video_url}")
        break
    time.sleep(5)
```

## ⚙️ Advanced Usage & Other Features

The Camb AI SDK offers a wide range of capabilities beyond these examples, including:

- Voice Cloning
- Translated TTS
- Audio Dubbing
- Transcription
- And more!

Please refer to the Official Camb AI API Documentation for a comprehensive list of features and advanced usage patterns.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
