# Camb.ai Python SDK

<div id="top" align="center">

![Banner](assets/banner5_720.jpg)

<h3><a href="https://camb.ai/">Camb.ai</a></h3>

[![PyPI version](https://img.shields.io/pypi/v/camb-sdk.svg?style=flat-square)](https://pypi.org/project/camb-sdk/)
[![License](https://img.shields.io/pypi/l/camb-sdk.svg?style=flat-square)](https://github.com/Camb-ai/cambai-python-sdk/blob/main/LICENSE)
[![Build status](https://github.com/Camb-ai/cambai-python-sdk/actions/workflows/python.yml/badge.svg)](https://github.com/Camb-ai/cambai-python-sdk/actions/workflows/python.yml)

</div>

Official Python client for Camb.ai APIs: text-to-speech, dubbing, translation, transcription, voice tools, and more. Full API behavior, models, and patterns are documented on **[docs.camb.ai](https://docs.camb.ai/sdk-guides/python-sdk)**. This repository holds the SDK source and **runnable examples** in [`examples/`](examples/).

## Installation

Requires Python 3.9+.

```bash
pip install camb-sdk
```

Install from GitHub:

```bash
pip install git+https://github.com/Camb-ai/cambai-python-sdk
```

## Authentication

Create an API key in [Camb.ai Studio](https://studio.camb.ai). Pass it from the environment so it does not live in source code:

```python
import os
from camb.client import CambAI, AsyncCambAI

client = CambAI(api_key=os.environ["CAMB_API_KEY"])
async_client = AsyncCambAI(api_key=os.environ["CAMB_API_KEY"])
```

Use `CambAI` for synchronous scripts and `AsyncCambAI` for async frameworks.

Do **not** name your entry script `camb.py`. Python will import your file instead of the installed `camb` package and raise import errors.

## Quick start (streaming TTS)

```python
import os
from camb.client import CambAI, save_stream_to_file

client = CambAI(api_key=os.environ["CAMB_API_KEY"])
stream = client.text_to_speech.tts(
    text="Hello from Camb.ai.",
    language="en-us",
    voice_id=147320,
    speech_model="mars-flash",
)
save_stream_to_file(stream, "output.wav")
```

Use a real `voice_id` from your account (for example from `client.voice_cloning.list_voices()`). See the [Python SDK guide](https://docs.camb.ai/sdk-guides/python-sdk) for models, languages, async streaming, and error handling.

## Capabilities

| Capability | Docs | Example |
| ---------- | ---- | ------- |
| Streaming TTS (sync / async) | [Quick start & models](https://docs.camb.ai/sdk-guides/python-sdk#quick-start) | [`examples/tts_stream_sync.py`](examples/tts_stream_sync.py), [`examples/async_tts_call.py`](examples/async_tts_call.py) |
| Text-to-audio (sound / music) | [Text-to-Audio](https://docs.camb.ai/sdk-guides/python-sdk#text-to-audio) | [`examples/text_to_audio.py`](examples/text_to_audio.py) |
| Translation | [Translation](https://docs.camb.ai/sdk-guides/python-sdk#translation) | [`examples/translation.py`](examples/translation.py) |
| Dubbing | [Dubbing](https://docs.camb.ai/sdk-guides/python-sdk#dubbing) | [`examples/perform_dubbing.py`](examples/perform_dubbing.py) |
| Transcription | [Transcription](https://docs.camb.ai/sdk-guides/python-sdk#transcription) | [`examples/transcription.py`](examples/transcription.py) |
| Translated TTS | [Translated TTS](https://docs.camb.ai/sdk-guides/python-sdk#translated-tts) | [`examples/translated_tts.py`](examples/translated_tts.py) |
| Text-to-voice | [Text-to-Voice](https://docs.camb.ai/sdk-guides/python-sdk#text-to-voice) | [`examples/text_to_voice.py`](examples/text_to_voice.py) |
| Custom TTS provider (Baseten) | [Custom provider](https://docs.camb.ai/sdk-guides/python-sdk#custom-provider) | [`examples/baseten_provider_example.py`](examples/baseten_provider_example.py) |

Voice cloning, stories, dictionaries, audio separation, and other endpoints are covered in the [same guide](https://docs.camb.ai/sdk-guides/python-sdk). For REST details, see the [API reference](https://docs.camb.ai/api-reference/endpoint/create-tts-stream).

`provider_params` accepts `mars_url` or `mars_pro_url` for Baseten (see [`camb/text_to_speech/baseten.py`](camb/text_to_speech/baseten.py)). Other self-hosted or cloud provider setups are described under [Custom Cloud Providers](https://docs.camb.ai/custom-cloud-providers).

## Examples

See [`examples/README.md`](examples/README.md) for environment variables, `python-dotenv` / `.env` setup (`pip install -e ".[examples]"` or `pip install python-dotenv`), and how to run each script.

## Resources

- [Python SDK guide](https://docs.camb.ai/sdk-guides/python-sdk)
- [PyPI: camb-sdk](https://pypi.org/project/camb-sdk/)
- [GitHub: camb-ai/cambai-python-sdk](https://github.com/camb-ai/cambai-python-sdk)

## License

MIT. See [LICENSE](LICENSE).
