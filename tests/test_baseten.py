"""Tests for the Baseten provider payload construction and streaming.

Requests are intercepted with ``httpx.MockTransport`` so no network I/O
happens; the handler captures the outgoing request for assertions.
"""

from __future__ import annotations

import asyncio
import json
import typing

import httpx
import pytest

from camb.client import CambAI, AsyncCambAI
from camb.core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from camb.core.http_response import AsyncHttpResponse, HttpResponse
from camb.text_to_speech.baseten import async_baseten_tts, baseten_tts
from camb.types.stream_tts_inference_options import StreamTtsInferenceOptions
from camb.types.stream_tts_output_configuration import StreamTtsOutputConfiguration
from camb.types.stream_tts_voice_settings import StreamTtsVoiceSettings


def _sync_wrapper(captured: typing.List[typing.Any]) -> SyncClientWrapper:
    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        return httpx.Response(200, content=b"audio-data")

    httpx_client = httpx.Client(transport=httpx.MockTransport(handler))
    return SyncClientWrapper(
        api_key="camb-key",
        base_url="https://client.camb.ai/apis",
        httpx_client=httpx_client,
        provider_params={"api_key": "baseten-key", "mars_url": "https://mars.baseten.app/call"},
    )


def _async_wrapper(captured: typing.List[typing.Any]) -> AsyncClientWrapper:
    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        return httpx.Response(200, content=b"audio-data")

    httpx_client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    return AsyncClientWrapper(
        api_key="camb-key",
        base_url="https://client.camb.ai/apis",
        httpx_client=httpx_client,
        provider_params={"api_key": "baseten-key", "mars_url": "https://mars.baseten.app/call"},
    )


def _base_options():
    return {
        "text": "Hello world",
        "language": "en-us",
        "output_configuration": StreamTtsOutputConfiguration(format="mp3", sample_rate=48000),
    }


def _extra_body(**params: typing.Any) -> typing.Any:
    return {"additional_body_parameters": {"reference_audio": "b64audio", "reference_language": "en-us", **params}}


def test_baseten_tts_payload_mapping() -> None:
    captured: typing.List[httpx.Request] = []

    kwargs = {
        **_base_options(),
        "voice_settings": StreamTtsVoiceSettings(
            enhance_reference_audio_quality=True,
            maintain_source_accent=True,
        ),
        "inference_options": StreamTtsInferenceOptions(
            temperature=0.8,
            inference_steps=10,
            speaker_similarity=0.7,  # mapped to campp_speaker_nudge 0.0
        ),
        "request_options": _extra_body(),
    }

    with baseten_tts(_sync_wrapper(captured), **kwargs) as response:
        assert isinstance(response, HttpResponse)
        assert b"".join(response.data) == b"audio-data"

    request = captured[0]
    payload = json.loads(request.content)
    assert request.headers["Authorization"] == "Api-Key baseten-key"
    assert payload["text"] == "Hello world"
    assert payload["language"] == "en-us"
    assert payload["output_format"] == "mp3"
    assert payload["stream"] is True
    assert payload["apply_ner_nlp"] is False
    assert payload["reference_language"] == "en-us"
    assert payload["audio_ref"] == "b64audio"
    assert payload["apply_ref_mpsenet"] is True
    assert payload["accent_nudge"] == 0.8
    assert payload["temperature"] == 0.8
    assert payload["inference_steps"] == 10
    assert payload["campp_speaker_nudge"] == 0.0


def test_speaker_similarity_clamped() -> None:
    captured: typing.List[httpx.Request] = []

    kwargs = {
        **_base_options(),
        "inference_options": StreamTtsInferenceOptions(speaker_similarity=0.35),
        "request_options": _extra_body(),
    }

    with baseten_tts(_sync_wrapper(captured), **kwargs):
        pass

    payload = json.loads(captured[0].content)
    assert payload["campp_speaker_nudge"] == pytest.approx(1.5 * (1 - 0.35 / 0.7))


def test_reference_audio_is_required() -> None:
    kwargs = {
        **_base_options(),
        "request_options": {"additional_body_parameters": {"reference_language": "en-us"}},
    }
    with pytest.raises(ValueError, match="reference_audio"):
        with baseten_tts(_sync_wrapper([]), **kwargs):
            pass


def test_reference_language_is_required() -> None:
    kwargs = {
        **_base_options(),
        "request_options": {"additional_body_parameters": {"reference_audio": "b64audio"}},
    }
    with pytest.raises(ValueError, match="reference_language"):
        with baseten_tts(_sync_wrapper([]), **kwargs):
            pass


def test_mars_url_is_required() -> None:
    kwargs = {"text": "hi", "language": "en-us"}

    def make_wrapper() -> SyncClientWrapper:
        httpx_client = httpx.Client(transport=httpx.MockTransport(lambda req: httpx.Response(200)))
        return SyncClientWrapper(
            api_key="k", base_url="https://client.camb.ai/apis", httpx_client=httpx_client,
            provider_params={"api_key": "baseten-key"},
        )

    with pytest.raises(ValueError, match="mars_url"):
        with baseten_tts(make_wrapper(), **kwargs):
            pass


def test_non_2xx_raises() -> None:
    captured: typing.List[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        return httpx.Response(400, content=b"bad request")

    httpx_client = httpx.Client(transport=httpx.MockTransport(handler))
    wrapper = SyncClientWrapper(
        api_key="k",
        base_url="https://client.camb.ai/apis",
        httpx_client=httpx_client,
        provider_params={"api_key": "baseten-key", "mars_url": "https://mars.baseten.app/call"},
    )

    kwargs = {**_base_options(), "request_options": _extra_body()}
    with pytest.raises(Exception, match="400"):
        with baseten_tts(wrapper, **kwargs):
            pass


def test_async_baseten_tts_payload_and_stream() -> None:
    captured: typing.List[httpx.Request] = []

    async def main() -> None:
        kwargs = {**_base_options(), "request_options": _extra_body()}
        async with async_baseten_tts(_async_wrapper(captured), **kwargs) as response:
            assert isinstance(response, AsyncHttpResponse)
            chunks = [c async for c in response.data]
            assert b"".join(chunks) == b"audio-data"

    asyncio.run(main())

    payload = json.loads(captured[0].content)
    assert payload["language"] == "en-us"
    assert payload["audio_ref"] == "b64audio"
    assert payload["reference_language"] == "en-us"


def test_cambai_provider_params_accepted() -> None:
    client = CambAI(tts_provider="baseten", provider_params={"api_key": "k", "mars_url": "u"})
    async_client = AsyncCambAI(tts_provider="baseten", provider_params={"api_key": "k", "mars_url": "u"})
    assert client._client_wrapper.tts_provider == "baseten"
    assert async_client._client_wrapper.tts_provider == "baseten"
    client._client_wrapper.httpx_client.httpx_client.close()
    asyncio.run(async_client._client_wrapper.httpx_client.httpx_client.aclose())