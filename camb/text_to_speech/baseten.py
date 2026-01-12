import contextlib
import typing

from ..core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ..core.http_response import AsyncHttpResponse, HttpResponse
from ..core.request_options import RequestOptions
from ..core.serialization import convert_and_respect_annotation_metadata
from ..types.stream_tts_inference_options import StreamTtsInferenceOptions
from ..types.stream_tts_output_configuration import StreamTtsOutputConfiguration
from ..types.stream_tts_voice_settings import StreamTtsVoiceSettings
from .types.create_stream_tts_request_payload_language import CreateStreamTtsRequestPayloadLanguage
from .types.create_stream_tts_request_payload_speech_model import CreateStreamTtsRequestPayloadSpeechModel

OMIT = typing.cast(typing.Any, ...)


@contextlib.contextmanager
def baseten_tts(
    client_wrapper: SyncClientWrapper,
    *,
    text: str,
    language: CreateStreamTtsRequestPayloadLanguage,
    voice_id: typing.Optional[int] = OMIT,
    speech_model: typing.Optional[CreateStreamTtsRequestPayloadSpeechModel] = OMIT,
    user_instructions: typing.Optional[str] = OMIT,
    enhance_named_entities_pronunciation: typing.Optional[bool] = OMIT,
    output_configuration: typing.Optional[StreamTtsOutputConfiguration] = OMIT,
    voice_settings: typing.Optional[StreamTtsVoiceSettings] = OMIT,
    inference_options: typing.Optional[StreamTtsInferenceOptions] = OMIT,
    request_options: typing.Optional[RequestOptions] = None,
) -> typing.Iterator[HttpResponse[typing.Iterator[bytes]]]:
    # Retrieve API key from provider_params
    provider_params = client_wrapper.provider_params or {}
    api_key = provider_params.get("api_key", "")
    mars_pro_url = provider_params.get("mars_pro_url")
    if not mars_pro_url:
        raise ValueError("mars_pro_url is required for using Baseten as provider")
    
    api_key_header_val = f"Api-Key {api_key}" if api_key else ""
    
    # Construct Payload
    # 1. Basic Fields
    payload = {
        "text": text,
        "language": str(language).lower().replace("_", "-"),
        "stream": True,
        "output_format": "mp3",  # Default
        "apply_ner_nlp": False, # Default based on doc
    }

    # 2. Output Configuration
    if output_configuration and output_configuration is not OMIT:
        if output_configuration.format:
            payload["output_format"] = str(output_configuration.format)

    # 3. Voice Settings
    if voice_settings and voice_settings is not OMIT:
        if voice_settings.enhance_reference_audio_quality is not None:
             payload["apply_ref_mpsenet"] = voice_settings.enhance_reference_audio_quality
        if voice_settings.maintain_source_accent:
             payload["accent_nudge"] = 0.8

    # 4. Inference Options
    if inference_options and inference_options is not OMIT:
        if inference_options.temperature is not None:
             payload["temperature"] = inference_options.temperature
        if inference_options.inference_steps is not None:
             payload["inference_steps"] = inference_options.inference_steps
            
        if inference_options.speaker_similarity is not None:
             # Formula from user snippet:
             s = max(0.0, min(0.7, inference_options.speaker_similarity))
             payload["campp_speaker_nudge"] = 1.5 * (1 - s / 0.7)

    # 5. Extract additional params (reference_audio, reference_language) from request_options if present
    #    This allows passing 'reference_audio' without breaking the explicit signature for now.
    extra_body = {}
    if request_options and request_options.get("additional_body_parameters"):
        extra_body = request_options.get("additional_body_parameters")
    
    if "reference_audio" not in extra_body:
        raise ValueError("reference_audio is required in additional_body_parameters for Baseten provider")
    if "reference_language" not in extra_body:
        raise ValueError("reference_language is required in additional_body_parameters for Baseten provider")

    payload["reference_language"] = extra_body["reference_language"]
    payload["audio_ref"] = extra_body["reference_audio"]
    payload["reference_audio"] = extra_body["reference_audio"]

    timeout = None
    if request_options and request_options.get("timeout_in_seconds") is not None:
        timeout = request_options.get("timeout_in_seconds")

    # Use the raw httpx client to avoid SDK wrapper injecting unwanted headers/params
    # that might interfere with Baseten's strict endpoint.
    with client_wrapper.httpx_client.httpx_client.stream(
        "POST",
        mars_pro_url,
        json=payload,
        headers={
            "Authorization": api_key_header_val,
            "content-type": "application/json",
        },
        timeout=timeout
    ) as _response:
        # Check status manually since we bypassed the wrapper's check
        if not (200 <= _response.status_code < 300):
             # Try to read error body
             _response.read()
             raise Exception(f"Baseten API Error: {_response.status_code} - {_response.text}")

        yield HttpResponse(
            response=_response,
            data=(_chunk for _chunk in _response.iter_bytes(chunk_size=None)),
        )


@contextlib.asynccontextmanager
async def async_baseten_tts(
    client_wrapper: AsyncClientWrapper,
    *,
    text: str,
    language: CreateStreamTtsRequestPayloadLanguage,
    voice_id: typing.Optional[int] = OMIT,
    speech_model: typing.Optional[CreateStreamTtsRequestPayloadSpeechModel] = OMIT,
    user_instructions: typing.Optional[str] = OMIT,
    enhance_named_entities_pronunciation: typing.Optional[bool] = OMIT,
    output_configuration: typing.Optional[StreamTtsOutputConfiguration] = OMIT,
    voice_settings: typing.Optional[StreamTtsVoiceSettings] = OMIT,
    inference_options: typing.Optional[StreamTtsInferenceOptions] = OMIT,
    request_options: typing.Optional[RequestOptions] = None,
) -> typing.AsyncIterator[AsyncHttpResponse[typing.AsyncIterator[bytes]]]:
    # Retrieve API key from provider_params
    provider_params = client_wrapper.provider_params or {}
    api_key = provider_params.get("api_key", "")
    mars_pro_url = provider_params.get("mars_pro_url")
    if not mars_pro_url:
        raise ValueError("mars_pro_url is required for using Baseten as provider")
    api_key_header_val = f"Api-Key {api_key}"

    # Construct Payload
    # 1. Basic Fields
    payload = {
        "text": text,
        "language": str(language).lower().replace("_", "-"),
        "stream": True,
        "output_format": "mp3",  # Default
        "apply_ner_nlp": False, # Default based on doc
    }

    # 2. Output Configuration
    if output_configuration and output_configuration is not OMIT:
        if output_configuration.format:
            payload["output_format"] = str(output_configuration.format)

    # 3. Voice Settings
    if voice_settings and voice_settings is not OMIT:
        if voice_settings.enhance_reference_audio_quality is not None:
             payload["apply_ref_mpsenet"] = voice_settings.enhance_reference_audio_quality
        if voice_settings.maintain_source_accent:
             payload["accent_nudge"] = 0.8

    # 4. Inference Options
    if inference_options and inference_options is not OMIT:
        if inference_options.temperature is not None:
             payload["temperature"] = inference_options.temperature
        if inference_options.inference_steps is not None:
             payload["inference_steps"] = inference_options.inference_steps
            
        if inference_options.speaker_similarity is not None:
             # Formula from user snippet:
             s = max(0.0, min(0.7, inference_options.speaker_similarity))
             payload["campp_speaker_nudge"] = 1.5 * (1 - s / 0.7)

    # 5. Extract additional params (reference_audio, reference_language) from request_options
    extra_body = {}
    if request_options and request_options.get("additional_body_parameters"):
        extra_body = request_options.get("additional_body_parameters")
    
    if "reference_audio" not in extra_body:
        raise ValueError("reference_audio is required in additional_body_parameters for Baseten provider")
    if "reference_language" not in extra_body:
        raise ValueError("reference_language is required in additional_body_parameters for Baseten provider")

    payload["reference_language"] = extra_body["reference_language"]
    payload["audio_ref"] = extra_body["reference_audio"]
    payload["reference_audio"] = extra_body["reference_audio"]

    timeout = None
    if request_options and request_options.get("timeout_in_seconds") is not None:
        timeout = request_options.get("timeout_in_seconds")
    
    # Use the raw httpx client to avoid SDK wrapper injecting unwanted headers/params
    # that might interfere with Baseten's strict endpoint.
    async with client_wrapper.httpx_client.httpx_client.stream(
        "POST",
        mars_pro_url,
        json=payload,
        headers={
            "Authorization": api_key_header_val,
            "content-type": "application/json",
        },
        timeout=timeout
    ) as _response:
        # Check status manually since we bypassed the wrapper's check
        if not (200 <= _response.status_code < 300):
             # Try to read error body
             await _response.aread()
             raise Exception(f"Baseten API Error: {_response.status_code} - {_response.text}")

        yield AsyncHttpResponse(
            response=_response,
            data=(_chunk async for _chunk in _response.aiter_bytes(chunk_size=None)),
        )
