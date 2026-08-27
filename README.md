# Camb.ai Python SDK

<div id="top" align="center">

   ![Banner](assets/banner5_720.jpg)
   <h3>
   <a href="https://camb.ai/"> Camb AI Website </a></h3>

[![PyPI version](https://img.shields.io/pypi/v/camb-sdk.svg?style=flat-square)](https://pypi.org/project/camb-sdk/)  
[![License](https://img.shields.io/pypi/l/camb-sdk.svg?style=flat-square)](https://github.com/Camb-ai/cambai-python-sdk/blob/main/LICENSE)  
[![Build status](https://github.com/Camb-ai/cambai-python-sdk/actions/workflows/python.yml/badge.svg)](https://github.com/Camb-ai/cambai-python-sdk/actions/workflows/python.yml)
</div>


The official Python SDK for interacting with Camb AI's powerful voice and audio generation APIs. Create expressive speech, unique voices, and rich soundscapes with just a few lines of Python.

## ✨ Features

- **Dubbing**: Dub your videos into multiple languages with voice cloning!
- **Expressive Text-to-Speech**: Convert text into natural-sounding speech using a wide range of pre-existing voices.
- **Generative Voices**: Create entirely new, unique voices from text prompts and descriptions.
- **Soundscapes from Text**: Generate ambient audio and sound effects from textual descriptions.
- **Transcripts & Subtitles**: Create async transcription/subtitle jobs and export TXT, SRT, or VTT results as raw data or files.
- **Live Transcription**: Stream microphone or file audio over a WebSocket and receive cumulative interim transcripts, word-level timing, and typed events.
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

# The SDK automatically reads the CAMB_API_KEY environment variable:
#   export CAMB_API_KEY=your_key_here
#   client = CambAI()

# Or pass the key explicitly:

# Synchronous Client
client = CambAI(api_key="YOUR_CAMB_API_KEY")

# Asynchronous Client
async_client = AsyncCambAI(api_key="YOUR_CAMB_API_KEY")
```


### Client with Specific MARS Pro Provider (e.g. Vertex, Baseten) 
#### Baseten
To deploy the model go to models from baseten example: https://app.baseten.co/deploy/mars8-flash and deploy then perform setup like below
```python
client_baseten = CambAI(
    tts_provider="baseten",
    provider_params={
        "api_key": "YOUR_BASETEN_API_KEY",
        "mars_url": "YOUR_BASETEN_URL"
    }
)

# Call TTS with Baseten
client_baseten.text_to_speech.tts(
    text="Hello World and my dear friends",
    language="en-us",
    speech_model="mars-flash",
    request_options={
        "additional_body_parameters": {
            "reference_audio": base64.b64encode(open("audio.wav", "rb").read()).decode('utf-8'),  # also support public/signed urls
            "reference_language": "en-us"  # required
        },
        "timeout_in_seconds": 300
    }
)
```

#### Vertex Support (In Progress)
```python
client_with_provider = CambAI(
    tts_provider="vertex",
    provider_params={"project_id": "my-project", "location": "us-central1"}
)
```

## 🚀 Getting Started: Examples
NOTE: For more examples and full ready to run files refer to the `examples/` directory.

### 1. Text-to-Speech (TTS)

Convert text into spoken audio using one of Camb AI's high-quality voices.

### Supported Models & Sample Rates

| Model Name | Sample Rate | Description |
| :--- | :--- | :--- |
| **mars-pro** | **48kHz** | High-fidelity, professional-grade speech synthesis. Ideal for long-form content and dubbing. |
| **mars-8.1-pro-beta** | **48kHz** | Beta MARS Pro model. Try this model with the same source references, as it may perform much better for pronunciation, expressiveness with high-pitch references, overall prosody, accent control, and coverage. |
| **mars-8.1-flash-beta** | **48kHz** | Beta MARS Pro model with faster speed. Try this model with the same source references, as it may perform much better for pronunciation, expressiveness with high-pitch references, overall prosody, accent control, and coverage. |
| **mars-instruct** | **22.05kHz** | optimized for instruction-following and nuance control. |
| **mars-flash** | **22.05kHz** | Low-latency model optimized for real-time applications and conversational AI. |

#### TTS request options

`client.text_to_speech.tts(...)` accepts the core request fields plus optional controls for model behavior and output format:

| Option | Description |
| :--- | :--- |
| `text` | Text to synthesize. For `mars-instruct`, you can include inline emotion or pacing tags. |
| `language` | BCP-47 locale such as `en-us`. |
| `voice_id` | Voice profile ID from `client.voice_cloning.list_voices()`. |
| `speech_model` | Model to use, such as `mars-8.1-flash-beta`, `mars-pro`, or `mars-instruct`. |
| `user_instructions` | Adds style, tone, pronunciation, or delivery guidance for the request. Available only with `speech_model="mars-instruct"`. |
| `output_configuration` | Output settings such as audio format. |
| `voice_settings` | Voice behavior controls such as speaking rate, reference enhancement, or accent preservation. |
| `inference_options` | Advanced generation controls for supported models. |
| `enhance_named_entities_pronunciation` | Improves pronunciation for names and other named entities when supported. |

```python
response = client.text_to_speech.tts(
    text="[warm, friendly] Great to meet you!",
    voice_id=147320,
    language="en-us",
    speech_model="mars-instruct",
    user_instructions="Speak warmly and with enthusiasm.",
    output_configuration=StreamTtsOutputConfiguration(format="wav"),
)
```

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
    speech_model="mars-8.1-flash-beta",  # options: mars-pro, mars-8.1-pro-beta, mars-flash, mars-instruct, auto
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
        speech_model="mars-8.1-flash-beta",  # options: mars-pro, mars-8.1-pro-beta, mars-flash, mars-instruct, auto
        voice_id=147319,
        output_configuration=StreamTtsOutputConfiguration(
            format="mp3"
        )
    )
    await save_async_stream_to_file(response, "text_to_audio_output.mp3")
    print("Success! Audio saved to text_to_audio_output.mp3")

asyncio.run(main())
```

#### c) Using Mars Flash (Low Latency)

For applications requiring faster responses, make sure you're using `mars-flash` (22.05kHz).

```python
response = client.text_to_speech.tts(
    text="Hey! I can respond much faster.",
    language="en-us",
    speech_model="mars-flash",
    voice_id=<id>,
    output_configuration=StreamTtsOutputConfiguration(
        format="wav"
    )
)
```

#### d) List Available Voices

You can list available voices to find a voice_id that suits your needs:

```python
voices = client.voice_cloning.list_voices()
print(f"Found {len(voices)} voices:")
for voice in voices[:5]:  # Print first 5 as an example
    print(f"  - ID: {voice["id"]}, Name: {voice["voice_name"]}, Gender: {voice["gender"]}, Language: {voice["language"]}")
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
from camb.client import save_stream_to_file
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

Dub videos into different languages with voice cloning and translation capabilities. `transcription_mode` defaults to `fast`; pass `"slow"` when you want a more thorough transcription pass.

```python
from camb.types.language_enums import Languages

result = client.dub.create_dub(
    video_url="your_accessible_video_url",
    source_language=Languages.EN_US,  # English (Or Check client.languages.get_source_languages())
    target_languages=[Languages.HI_IN],  # list of Languages like [Languages.HI_IN, Languages.FR_FR] or if you want single language then can use target_language=Languages.HI_IN
    transcription_mode="fast",  # fast (default) or slow for a more thorough transcription pass
)
task_id = result.task_id
print(f"Dub Task created with ID: {task_id}")
while True:
    status_response = client.dub.get_dubbing_status(task_id=task_id)
    print(f"Current Status: {status_response.status}")
    if status_response.status == "SUCCESS":
        dubbed_run_info = client.dub.get_dubbed_run_info(status_response.run_id)
        print(f"Dubbed Video URL: {dubbed_run_info.audio_url}")
        print(f"Transcript: {dubbed_run_info.transcript}")
        print(f"Video URL: {dubbed_run_info.video_url}")
        break
    time.sleep(5)
```

### 5. Live Transcription (Streaming WebSocket)

Stream audio over a single WebSocket and receive cumulative interim
transcripts, word-level timing, and typed events. The session exposes a
microphone helper, a file source for tests, and the same `on(event)`
dispatcher in both SDKs.

```python
import asyncio
import os

from camb.client import CambAI
from camb.live_transcription import Microphone, ServerMessageType


async def main():
    client = CambAI(api_key=os.environ["CAMB_API_KEY"])
    session = await client.live_transcription.connect(
        model="boli-v5",
        language="en-us",
        sample_rate=16000,
    )

    @session.on(ServerMessageType.RESULTS)
    def _(msg):
        # Cumulative transcript: replace the previous interim rather
        # than concatenating successive Results events.
        print(f"\r{msg.transcript}", end="", flush=True)

    @session.on(ServerMessageType.CLOSED)
    def _(info):
        print(f"\nClosed: code={info.code} reason={info.reason!r}")

    async with session:
        mic = Microphone(sample_rate=16000, chunk_size=1600)
        await session.stream_audio(mic)


asyncio.run(main())
```

Prefer streaming a file (no audio device dependency)? See
[`examples/live_transcription_file.py`](examples/live_transcription_file.py).
For the full event catalog (`Ready`, `Results`, `Final`, `Error`,
`Closed`), configuration options, and extensibility notes, see the
[Live Transcription tutorial](https://docs.camb.ai/tutorials/live-transcription-with-sdk)
and [SDK guide](https://docs.camb.ai/sdk-guides/live-transcription).

### 6. Realtime Speech-to-Speech Translation (Streaming WebSocket)

Speak (or stream a file) in one language and receive the translation as live
text and synthesized speech over a single WebSocket. Audio is PCM16 mono at
24 kHz in both directions.

```python
import asyncio
import os

from camb.client import CambAI
from camb.live_transcription import Microphone
from camb.realtime import ServerEventType


async def main():
    client = CambAI(api_key=os.environ["CAMB_API_KEY"])
    session = await client.realtime.connect(
        source_language="en-us",
        target_language="de-de",
    )

    @session.on(ServerEventType.TEXT_DONE)
    def _(event):
        print(f"[translation] {event.text}")

    @session.on(ServerEventType.AUDIO_DELTA)
    def _(event):
        ...  # event.data is raw PCM16 mono 24 kHz — play it through your speakers

    async with session:
        await session.wait_until_ready()
        mic = Microphone(sample_rate=24000, chunk_size=2400)
        await session.stream_audio(mic)


asyncio.run(main())
```

Sessions run in one of two modes, chosen with `mode`:

```python
session = await client.realtime.connect(
    source_language="en-us",
    target_language="de-de",
    mode="slow",  # "fast" (default) or "slow"
)
```

`"fast"` accepts audio almost immediately and translates with the lowest latency, but supports
fewer languages. `"slow"` supports the full language list and translates more accurately, at the
cost of a 30s+ cold boot before the session is ready — `wait_until_ready()` covers that wait.

`mode` replaced a `model` argument that took engine codenames. Both are still accepted, so existing
code keeps working: `model="iris"` resolves to `mode="fast"`, and `"lilac"`/`"violet"`/`"orchid"`
resolve to `"slow"`, each with a `DeprecationWarning`. Note the default changed — it was `"lilac"`,
whose language coverage matches today's `"slow"`. If you never passed `model` and translate a pair
outside `"fast"`'s narrower set, pass `mode="slow"` explicitly.

By default the translation is synthesized with a built-in voice for the target
language. Pass `voice_id` to use one of your cloned voices instead (get the ID
from `client.voice_cloning.list_voices()`):

```python
session = await client.realtime.connect(
    source_language="en-us",
    target_language="de-de",
    voice_id=147320,  # one of your cloned voices
)
```

For the most natural-sounding results, choose a voice whose reference language
matches `target_language`.

Runnable examples:
[`examples/realtime_translation_microphone.py`](examples/realtime_translation_microphone.py)
(mic in, translated speech out) and
[`examples/realtime_translation_file.py`](examples/realtime_translation_file.py)
(WAV in, translated WAV out — no audio device needed). For the full event
list and configuration, see the
[Realtime Speech Translation tutorial](https://docs.camb.ai/tutorials/realtime-translation-with-sdk)
and the [WebSocket API reference](https://docs.camb.ai/api-reference/websockets/realtime).

### 7. Transcription and Subtitles

Create transcription and subtitle jobs with formatting controls. You can pass
`SubtitleFormattingOptions` or a plain dict.

```python
from camb.types.language_enums import Languages
from camb.types.subtitle_formatting_options import SubtitleFormattingOptions

transcription = client.transcription.create_transcription(
    language=Languages.EN_US,
    media_url="https://example.com/video.mp4",
    formatting_options=SubtitleFormattingOptions(
        max_segment_duration_in_seconds=6,
        max_characters_in_segment=42,
    ),
)
print(f"Transcription task: {transcription.task_id}")

transcription_with_dict = client.transcription.create_transcription(
    language=Languages.EN_US,
    media_url="https://example.com/video.mp4",
    formatting_options={"max_reading_speed_in_cps": 18},
)
```

Generate subtitles for one or more target languages, then poll, fetch, or export
the result. Subtitle create requires a media URL (local file upload is not supported).

```python
import time

from camb.types.language_enums import Languages
from camb.types.subtitle_formatting_options import SubtitleFormattingOptions

subtitle = client.subtitles.create_subtitle(
    source_language=Languages.EN_US,
    target_languages=[Languages.ES_ES, Languages.FR_FR],
    media_url="https://example.com/video.mp4",
    formatting_options=SubtitleFormattingOptions(
        min_segment_duration_in_seconds=1,
        max_characters_in_segment=42,
    ),
)

while True:
    status = client.subtitles.get_subtitle_task_status(task_id=subtitle.task_id)
    if status.status == "SUCCESS":
        break
    time.sleep(5)

result = client.subtitles.get_subtitle_result(status.run_id)
spanish_result = client.subtitles.get_subtitle_result_for_language(
    status.run_id,
    Languages.ES_ES,
)

srt_file = client.subtitles.get_subtitle_result_for_language(
    status.run_id,
    Languages.ES_ES,
    format_type="srt",
    data_type="file",
)
```

## ⚙️ Advanced Usage & Other Features

The Camb AI SDK offers a wide range of capabilities beyond these examples, including:

- Voice Cloning
- Translations
- Translated TTS
- Audio Dubbing
- Transcription (async file/URL jobs) and subtitles (media URL jobs) with TXT/SRT/VTT exports
- Live Transcription (streaming WebSocket — see Example 5 above)
- And more!

Please refer to [examples](examples/) for direct runnable examples and Official Camb AI API Documentation for a comprehensive list of features and advanced usage patterns.

## 📖 Examples

Check out the `examples/` directory for complete, runnable examples:

- `async_tts_call.py` - Async text-to-speech example
- `text_to_audio.py` - Sound generation example
- `perform_dubbing.py` - Video dubbing workflow
- `transcription_formatting.py` - Async transcription with formatting options and TXT/SRT/VTT exports
- `subtitles.py` - Subtitle job creation, polling, and language-specific TXT/SRT/VTT exports
- `translation.py` - Text translation workflow
- `baseten_provider_example.py` - Using custom hosting providers
- `live_transcription_microphone.py` - Stream microphone audio over the WebSocket
- `live_transcription_file.py` - Stream a local audio file over the WebSocket
- `realtime_translation_microphone.py` - Realtime speech translation from microphone input
- `realtime_translation_file.py` - Realtime speech translation from file input

## License

This project is licensed under the MIT License - see the LICENSE file for details.
