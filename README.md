# CAMB.AI Python SDK

<div id="top" align="center">

![Banner](assets/banner5_720.jpg)

[![PyPI version](https://img.shields.io/pypi/v/camb-sdk.svg?style=flat-square)](https://pypi.org/project/camb-sdk/) [![License](https://img.shields.io/pypi/l/camb-sdk.svg?style=flat-square)](https://github.com/Camb-ai/cambai-python-sdk/blob/main/LICENSE) [![Build status](https://github.com/Camb-ai/cambai-python-sdk/actions/workflows/installer.yml/badge.svg)](https://github.com/Camb-ai/cambai-python-sdk/actions/workflows/installer.yml)

</div>

The official Python client for [Camb.ai](https://camb.ai/). Use it to call our speech APIs from scripts, backends, and async apps—with typed request/response models, sync and async clients, and helpers for saving streamed audio.

See the [Python SDK guide](https://docs.camb.ai/sdk-guides/python-sdk) for full patterns. Explore the examples here: [`examples/`](examples/).

## Features

- **Streaming text-to-speech** — Turn text into speech with library or cloned voices; stream chunks to disk or your own pipeline.
- **Translated TTS** — Translate copy and synthesize it in the target language in one job.
- **Text-to-audio** — Generate sound effects or music-style audio from a text prompt.
- **Text-to-voice** — Describe a voice in words and preview generated samples.
- **Dubbing** — Localize video with translated speech matched to the original speaker.
- **Translation** — Batch-translate strings across supported language pairs.
- **Transcription** — Transcribe audio or video from a URL or upload.
- **Voice cloning** — Create custom voices and browse your voice library.
- **Audio separation** — Split a mix into stems such as vocals and background.
- **Stories & folders** — Build long-form narration from documents and organize projects.
- **Custom providers** — Point TTS at your own MARS deployment (for example on Baseten) via `provider_params`.

## Installation

Requires Python 3.8+.

```bash
pip install camb-sdk
```

## Authentication

Create an API key in [Camb.ai Studio](https://studio.camb.ai), then pass it from the environment:

```python
import os
from camb import CambAI, AsyncCambAI

client = CambAI(api_key=os.environ["CAMB_API_KEY"])
async_client = AsyncCambAI(api_key=os.environ["CAMB_API_KEY"])
```

Use `CambAI` for synchronous code and `AsyncCambAI` with `asyncio`, FastAPI, and similar stacks.

**Note:** Do not name your entry script `camb.py`. Python will import that file instead of the installed package.

## Usage

### Streaming TTS

```python
import os
from camb.client import CambAI, save_stream_to_file

client = CambAI(api_key=os.environ["CAMB_API_KEY"])

stream = client.text_to_speech.tts(
    text="Hello from the Camb Python SDK.",
    language="en-us",
    voice_id=147320,  # browse voices: client.voice_cloning.list_voices()
    speech_model="mars-flash",
)
save_stream_to_file(stream, "output.wav")
```

### Translation

Long-running jobs return a `task_id`. Poll until the status is `SUCCESS`, then fetch the result:

```python
import os
import time
from camb import CambAI
from camb.types.language_enums import Languages

client = CambAI(api_key=os.environ["CAMB_API_KEY"])

create = client.translation.create_translation(
    texts=["Hello, how are you today?"],
    source_language=Languages.EN_US,
    target_language=Languages.FR_FR,
)
task_id = create["task_id"]

while True:
    status = client.translation.get_translation_task_status(task_id)
    if status.status == "SUCCESS":
        break
    time.sleep(3)

result = client.translation.get_translation_result(run_id=status.run_id)
print(result.texts)
```

### Dubbing

```python
import os
import time
from camb import CambAI
from camb.types.language_enums import Languages

client = CambAI(api_key=os.environ["CAMB_API_KEY"])

response = client.dub.create_dub(
    video_url=os.environ["VIDEO_URL"],
    source_language=Languages.EN_US,
    target_language=Languages.HI_IN,
)
task_id = response.task_id

while True:
    status = client.dub.get_dubbing_status(task_id=task_id)
    if status.status == "SUCCESS":
        info = client.dub.get_dubbed_run_info(status.run_id)
        print(info.video_url or info.audio_url)
        break
    time.sleep(5)
```

## API overview

| Feature | Documentation | Example |
| --- | --- | --- |
| Streaming TTS | [Guide](https://docs.camb.ai/sdk-guides/python-sdk#quick-start) | [`examples/tts_stream_sync.py`](examples/tts_stream_sync.py) |
| Async TTS | [Guide](https://docs.camb.ai/sdk-guides/python-sdk#quick-start) | [`examples/async_tts_call.py`](examples/async_tts_call.py) |
| Translated TTS | [Guide](https://docs.camb.ai/sdk-guides/python-sdk#translated-tts) | [`examples/translated_tts.py`](examples/translated_tts.py) |
| Text-to-audio | [Guide](https://docs.camb.ai/sdk-guides/python-sdk#text-to-audio) | [`examples/text_to_audio.py`](examples/text_to_audio.py) |
| Text-to-voice | [Guide](https://docs.camb.ai/sdk-guides/python-sdk#text-to-voice) | [`examples/text_to_voice.py`](examples/text_to_voice.py) |
| Dubbing | [Guide](https://docs.camb.ai/sdk-guides/python-sdk#dubbing) | [`examples/perform_dubbing.py`](examples/perform_dubbing.py) |
| Translation | [Guide](https://docs.camb.ai/sdk-guides/python-sdk#translation) | [`examples/translation.py`](examples/translation.py) |
| Transcription | [Guide](https://docs.camb.ai/sdk-guides/python-sdk#transcription) | [`examples/transcription.py`](examples/transcription.py) |
| Custom provider (Baseten) | [Guide](https://docs.camb.ai/sdk-guides/python-sdk#custom-provider) | [`examples/baseten_provider_example.py`](examples/baseten_provider_example.py) |

Self-hosted MARS deployments are covered in [Custom Cloud Providers](https://docs.camb.ai/custom-cloud-providers).

## Links

- [Python SDK guide](https://docs.camb.ai/sdk-guides/python-sdk)
- [API reference](https://docs.camb.ai/api-reference)
- [PyPI — camb-sdk](https://pypi.org/project/camb-sdk/)
- [TypeScript SDK](https://github.com/Camb-ai/cambai-node-sdk)

## License

MIT. See [LICENSE](LICENSE).
