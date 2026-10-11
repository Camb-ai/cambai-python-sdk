"""Wire parity with client-microservice transcription.py and its audio-cleaning PR."""

import asyncio
import inspect
import json
from email.parser import BytesParser
from email.policy import default
import unittest

import httpx
from camb.client import CambAI, AsyncCambAI
from camb.errors import UnprocessableEntityError
from camb.transcription.client import TranscriptionClient, AsyncTranscriptionClient
from camb.transcription.raw_client import (
    RawTranscriptionClient,
    AsyncRawTranscriptionClient,
)
from camb.types.subtitle_formatting_options import SubtitleFormattingOptions

TRACE = "00-0123456789abcdef0123456789abcdef-0123456789abcdef-01"
CREATE_FIELDS = {
    "language",
    "media_file",
    "media_url",
    "file",
    "audio_url",
    "project_name",
    "project_description",
    "folder_id",
    "transcription_mode",
    "run_audio_cleaning",
    "include_music_in_fg",
    "formatting_options",
    "traceparent",
}
TRANSCRIPT = {
    "transcript": [{"start": 0.0, "end": 1.5, "text": "Hello", "speaker": "SPEAKER_0"}]
}


class TranscriptionParityTests(unittest.TestCase):
    def invoke(
        self, method, options, response, asynchronous=False, raw=False, status=200
    ):
        captured = []

        def handler(request):
            captured.append(request)
            return httpx.Response(status, json=response)

        transport = httpx.MockTransport(handler)
        if asynchronous:

            async def run():
                async with httpx.AsyncClient(transport=transport) as http:
                    client = AsyncCambAI(
                        api_key="test", httpx_client=http
                    ).transcription
                    return await getattr(
                        client.with_raw_response if raw else client, method
                    )(**options)

            result = asyncio.run(run())
        else:
            with httpx.Client(transport=transport) as http:
                client = CambAI(api_key="test", httpx_client=http).transcription
                result = getattr(client.with_raw_response if raw else client, method)(
                    **options
                )
        return captured[0], result.data if raw else result

    def fields(self, request):
        msg = BytesParser(policy=default).parsebytes(
            ("Content-Type: " + request.headers["content-type"] + "\r\n\r\n").encode()
            + request.content
        )
        return {
            part.get_param("name", header="content-disposition"): part.get_payload(
                decode=True
            ).decode()
            for part in msg.iter_parts()
        }

    def test_create_signature_matches_all_api_inputs(self):
        for cls in [
            TranscriptionClient,
            AsyncTranscriptionClient,
            RawTranscriptionClient,
            AsyncRawTranscriptionClient,
        ]:
            params = inspect.signature(cls.create_transcription).parameters
            self.assertEqual(
                set(params) - {"self", "request_options", "run_id"}, CREATE_FIELDS
            )
            for flag in ["include_music_in_fg", "run_audio_cleaning"]:
                self.assertIs(params[flag].default, True)
            self.assertEqual(params["transcription_mode"].default, "fast")

    def test_all_create_fields_and_boolean_combinations(self):
        for asynchronous in [False, True]:
            for raw in [False, True]:
                for music in [None, False, True]:
                    for cleaning in [False, True]:
                        for upload in ["media_file", "file"]:
                            with self.subTest(
                                asynchronous=asynchronous,
                                raw=raw,
                                music=music,
                                cleaning=cleaning,
                                upload=upload,
                            ):
                                options = dict(
                                    language="auto",
                                    media_url="https://example.com/media.wav",
                                    audio_url="https://example.com/legacy.wav",
                                    project_name="Demo",
                                    project_description="Notes",
                                    folder_id=7,
                                    transcription_mode="slow",
                                    run_audio_cleaning=cleaning,
                                    formatting_options={
                                        "max_characters_in_segment": 40
                                    },
                                    traceparent=TRACE,
                                    run_id=99,
                                )
                                options[upload] = (
                                    "clip.wav",
                                    b"RIFFaudio",
                                    "audio/wav",
                                )
                                if music is not None:
                                    options["include_music_in_fg"] = music
                                request, result = self.invoke(
                                    "create_transcription",
                                    options,
                                    {"task_id": "task"},
                                    asynchronous,
                                    raw,
                                )
                                fields = self.fields(request)
                                self.assertEqual(fields[upload], "RIFFaudio")
                                self.assertEqual(
                                    fields["include_music_in_fg"],
                                    "false" if music is False else "true",
                                )
                                self.assertEqual(
                                    fields["run_audio_cleaning"], str(cleaning).lower()
                                )
                                for key in [
                                    "language",
                                    "media_url",
                                    "audio_url",
                                    "project_name",
                                    "project_description",
                                    "folder_id",
                                    "transcription_mode",
                                ]:
                                    self.assertEqual(fields[key], str(options[key]))
                                self.assertEqual(
                                    json.loads(fields["formatting_options"]),
                                    options["formatting_options"],
                                )
                                self.assertEqual(
                                    set(fields),
                                    CREATE_FIELDS
                                    - {
                                        "traceparent",
                                        "file"
                                        if upload == "media_file"
                                        else "media_file",
                                    },
                                )
                                self.assertEqual(request.headers["traceparent"], TRACE)
                                self.assertFalse(request.url.query)
                                self.assertEqual(result.task_id, "task")

    def test_formatting_model_dictionary_and_json_string(self):
        data = {
            "max_segment_duration_in_seconds": 6.0,
            "min_segment_duration_in_seconds": 1.0,
            "max_characters_in_segment": 40,
            "max_reading_speed_in_cps": 20.0,
            "min_gap_between_segments_in_frames": 2,
        }
        for asynchronous in [False, True]:
            for raw in [False, True]:
                for value in [
                    data,
                    SubtitleFormattingOptions(**data),
                    json.dumps(data),
                ]:
                    request, _ = self.invoke(
                        "create_transcription",
                        dict(
                            language=1,
                            media_url="https://example.com/a.wav",
                            formatting_options=value,
                        ),
                        {"task_id": "t"},
                        asynchronous,
                        raw,
                    )
                    self.assertEqual(
                        json.loads(self.fields(request)["formatting_options"]), data
                    )

    def test_status_structured_export_and_bulk_results(self):
        for asynchronous in [False, True]:
            for raw in [False, True]:
                request, result = self.invoke(
                    "get_transcription_task_status",
                    dict(task_id="task", traceparent=TRACE, run_id=99),
                    {"status": "SUCCESS", "run_id": 7},
                    asynchronous,
                    raw,
                )
                self.assertEqual(request.url.path, "/apis/transcribe/task")
                self.assertFalse(request.url.query)
                self.assertEqual(request.headers["traceparent"], TRACE)
                self.assertEqual(result.run_id, 7)
                for format_type in [None, "txt", "srt", "vtt"]:
                    for data_type in [None, "file", "raw_data"]:
                        exported = format_type is not None or data_type is not None
                        body = (
                            {
                                "transcript": "https://example.com/result"
                                if data_type != "raw_data"
                                else "Hello"
                            }
                            if exported
                            else TRANSCRIPT
                        )
                        opts = dict(
                            run_id=7, traceparent=TRACE, word_level_timestamps=True
                        )
                        if format_type:
                            opts["format_type"] = format_type
                        if data_type:
                            opts["data_type"] = data_type
                        request, result = self.invoke(
                            "get_transcription_result", opts, body, asynchronous, raw
                        )
                        self.assertEqual(
                            request.url.path, "/apis/transcription-result/7"
                        )
                        self.assertEqual(
                            dict(request.url.params),
                            {
                                k: v
                                for k, v in opts.items()
                                if k in ["format_type", "data_type"]
                            },
                        )
                        self.assertEqual(request.headers["traceparent"], TRACE)
                        if exported:
                            self.assertEqual(result.transcript, body["transcript"])
                        else:
                            self.assertEqual(result.transcript[0].speaker, "SPEAKER_0")
                request, result = self.invoke(
                    "get_transcription_results",
                    dict(run_ids=[7, 8], run_id=99, traceparent=TRACE),
                    {"7": TRANSCRIPT, "8": TRANSCRIPT},
                    asynchronous,
                    raw,
                )
                self.assertEqual(request.method, "POST")
                self.assertEqual(request.url.path, "/apis/transcription-results")
                self.assertFalse(request.url.query)
                self.assertEqual(json.loads(request.content), {"run_ids": [7, 8]})
                self.assertEqual(request.headers["traceparent"], TRACE)
                self.assertEqual(result["7"].transcript[0].text, "Hello")

    def test_server_validation_errors_are_preserved(self):
        for asynchronous in [False, True]:
            for raw in [False, True]:
                with self.assertRaises(UnprocessableEntityError) as caught:
                    self.invoke(
                        "create_transcription",
                        dict(language="bad", media_url="https://example.com/a.wav"),
                        {
                            "detail": [
                                {
                                    "loc": ["body", "language"],
                                    "msg": "Invalid language",
                                    "type": "value_error",
                                }
                            ]
                        },
                        asynchronous,
                        raw,
                        status=422,
                    )
                self.assertEqual(caught.exception.status_code, 422)
