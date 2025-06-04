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
pip install cambai
````

> If the package is not yet on PyPI, you can install it directly from GitHub for now:
>
> ```bash
> pip install git+https://github.com/Camb-ai/python-sdk
> ```

---

## 🔑 Authentication

To use the Camb AI SDK, you'll need an API key. You can authenticate in either of the following ways:

### 1. Pass the API key directly

```python
from cambai.api.apis_api import CambAI

client = CambAI(api_key="YOUR_CAMB_AI_API_KEY")
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
from cambai.api.apis_api import CambAI
from cambai.rest import ApiException

# Initialize client (ensure API key is set)
client = CambAI(api_key="YOUR_CAMB_AI_API_KEY")

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
from cambai.api.apis_api import CambAI
from cambai.models.output_type import OutputType 
from cambai.rest import ApiException

# Initialize client
client = CambAI(api_key="YOUR_CAMB_AI_API_KEY")

file_path = "my_generated_speech.mp3"

try:
    print(f"Generating speech and saving to {file_path}...")

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
from cambai.api.apis_api import CambAI
from cambai.rest import ApiException

# Initialize client
client = CambAI(api_key="YOUR_CAMB_AI_API_KEY")

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
from cambai.api.apis_api import CambAI
from cambai.rest import ApiException

# Initialize client
client = CambAI(api_key="YOUR_CAMB_AI_API_KEY")

output_file = "generated_sound_effect.mp3"

try:
    print(f"Generating sound effect and saving to {output_file}...")

    client.text_to_audio(
        prompt="A gentle breeze rustling through autumn leaves in a quiet forest.",
        duration=10,       
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




