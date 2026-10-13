import asyncio
from email.parser import BytesParser
from email.policy import default
import unittest

import httpx
from camb.client import CambAI, AsyncCambAI


class TranscriptionOptionsTests(unittest.TestCase):
    def test_wire_options_in_sync_async_and_raw_clients(self):
        for asynchronous in (False, True):
            for raw in (False, True):
                for cleaning in (None, True, False):
                    for language in ("auto", "en-us", 1):
                        with self.subTest(
                            asynchronous=asynchronous,
                            raw=raw,
                            cleaning=cleaning,
                            language=language,
                        ):
                            captured = []

                            def handler(request):
                                captured.append(request)
                                return httpx.Response(
                                    200, json={"task_id": "test-task"}
                                )

                            options = {
                                "language": language,
                                "media_url": "https://example.com/clip.wav",
                                "formatting_options": {"max_characters_in_segment": 40},
                            }
                            if cleaning is not None:
                                options["run_audio_cleaning"] = cleaning
                            transport = httpx.MockTransport(handler)
                            if asynchronous:

                                async def run():
                                    async with httpx.AsyncClient(
                                        transport=transport
                                    ) as http:
                                        client = AsyncCambAI(
                                            api_key="test", httpx_client=http
                                        ).transcription
                                        return await (
                                            client.with_raw_response if raw else client
                                        ).create_transcription(**options)

                                result = asyncio.run(run())
                            else:
                                with httpx.Client(transport=transport) as http:
                                    client = CambAI(
                                        api_key="test", httpx_client=http
                                    ).transcription
                                    result = (
                                        client.with_raw_response if raw else client
                                    ).create_transcription(**options)
                            self.assertEqual(
                                (result.data if raw else result).task_id, "test-task"
                            )
                            request = captured[0]
                            message = BytesParser(policy=default).parsebytes(
                                (
                                    "Content-Type: "
                                    + request.headers["content-type"]
                                    + "\r\n\r\n"
                                ).encode()
                                + request.content
                            )
                            fields = {
                                part.get_param(
                                    "name", header="content-disposition"
                                ): part.get_payload(decode=True).decode()
                                for part in message.iter_parts()
                            }
                            self.assertEqual(fields["language"], str(language))
                            self.assertEqual(
                                fields["run_audio_cleaning"],
                                "false" if cleaning is False else "true",
                            )
                            self.assertIn("40", fields["formatting_options"])
                            self.assertTrue(request.url.path.endswith("/transcribe"))
