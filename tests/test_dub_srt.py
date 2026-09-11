import asyncio
import json
import unittest

import httpx

from camb import DubSRTInput, DubTargetSRTInput
from camb.client import AsyncCambAI, CambAI
from camb.errors import UnprocessableEntityError


SOURCE = "1\n00:00:00,500 --> 00:00:02,800\nWelcome back.\n"
TARGET = "1\n00:00:00,500 --> 00:00:02,800\n¡Bienvenidos!\n"
BASE = {"video_url": "https://example.com/video.mp4", "source_language": 1, "target_languages": [4]}


class DubSRTTests(unittest.TestCase):
    def invoke(self, *, asynchronous, raw, options, status=200, response=None):
        requests = []

        def handler(request):
            requests.append(request)
            return httpx.Response(status, json=response or {"task_id": "test-task"})

        transport = httpx.MockTransport(handler)
        if asynchronous:

            async def run():
                async with httpx.AsyncClient(transport=transport) as http:
                    sdk = AsyncCambAI(api_key="test-key", httpx_client=http)
                    method = sdk.dub.with_raw_response.end_to_end_dubbing if raw else sdk.dub.create_dub
                    return await method(**BASE, **options)

            result = asyncio.run(run())
        else:
            with httpx.Client(transport=transport) as http:
                sdk = CambAI(api_key="test-key", httpx_client=http)
                method = sdk.dub.with_raw_response.end_to_end_dubbing if raw else sdk.dub.create_dub
                result = method(**BASE, **options)
        self.assertEqual((result.data if raw else result).task_id, "test-task")
        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0].method, "POST")
        self.assertTrue(requests[0].url.path.endswith("/dub"))
        self.assertEqual(requests[0].headers["x-api-key"], "test-key")
        return json.loads(requests[0].content)

    def test_scripts_serialize_in_all_clients(self):
        for asynchronous in (False, True):
            for raw in (False, True):
                for typed in (False, True):
                    for mode in ("source", "target", "both"):
                        with self.subTest(asynchronous=asynchronous, raw=raw, typed=typed, mode=mode):
                            source = {"content": SOURCE, "format": "srt"}
                            target = {"content": TARGET, "format": "srt", "language": "es-es"}
                            options = {}
                            if mode in ("source", "both"):
                                options["source_transcript"] = DubSRTInput(**source) if typed else source
                            if mode in ("target", "both"):
                                options["target_transcripts"] = [DubTargetSRTInput(**target) if typed else target]
                            body = self.invoke(asynchronous=asynchronous, raw=raw, options=options)
                            if mode in ("source", "both"):
                                self.assertEqual(body["source_transcript"], source)
                            else:
                                self.assertNotIn("source_transcript", body)
                            if mode in ("target", "both"):
                                self.assertEqual(body["target_transcripts"], [target])
                            else:
                                self.assertNotIn("target_transcripts", body)

    def test_omitted_and_explicit_null_scripts(self):
        for asynchronous in (False, True):
            for raw in (False, True):
                for options in ({}, {"source_transcript": None, "target_transcripts": None}):
                    with self.subTest(asynchronous=asynchronous, raw=raw, options=options):
                        body = self.invoke(asynchronous=asynchronous, raw=raw, options=options)
                        self.assertEqual(body["transcription_mode"], "fast")
                        for field in ("source_transcript", "target_transcripts"):
                            if field in options:
                                self.assertIsNone(body[field])
                            else:
                                self.assertNotIn(field, body)

    def test_preserves_server_validation_exception(self):
        error = {
            "detail": [
                {
                    "loc": ["body", "source_transcript", "content"],
                    "msg": "SRT content could not be parsed",
                    "type": "value_error",
                }
            ]
        }
        for asynchronous in (False, True):
            for raw in (False, True):
                with self.subTest(asynchronous=asynchronous, raw=raw):
                    with self.assertRaises(UnprocessableEntityError) as caught:
                        self.invoke(
                            asynchronous=asynchronous,
                            raw=raw,
                            options={"source_transcript": {"content": "bad SRT"}},
                            status=422,
                            response=error,
                        )
                    self.assertEqual(caught.exception.status_code, 422)
                    self.assertEqual(caught.exception.body.detail[0].loc, error["detail"][0]["loc"])

    def test_models_exported_and_numeric_language_preserved(self):
        from camb.types import DubSRTInput as ExportedSource
        from camb.types import DubTargetSRTInput as ExportedTarget

        self.assertIs(ExportedSource, DubSRTInput)
        self.assertIs(ExportedTarget, DubTargetSRTInput)
        self.assertEqual(DubSRTInput(content=SOURCE).format, "srt")
        self.assertEqual(DubTargetSRTInput(content=TARGET, language=4).language, 4)


if __name__ == "__main__":
    unittest.main()
