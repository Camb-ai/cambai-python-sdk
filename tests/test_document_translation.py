import asyncio
import unittest

import httpx

from camb import CreateDocTranslationOut, DocTranslationResult
from camb.client import AsyncCambAI, CambAI
from camb.errors import UnprocessableEntityError


def _form_fields(request):
    """Parse a multipart request into ({name: [values]}, {name: (filename, bytes)})."""
    boundary = request.headers["content-type"].split("boundary=")[1].encode()
    fields, files = {}, {}
    for part in request.content.split(b"--" + boundary)[1:-1]:
        head, _, body = part.strip(b"\r\n").partition(b"\r\n\r\n")
        disposition = head.decode().split("\r\n")[0]
        name = disposition.split('name="')[1].split('"')[0]
        if 'filename="' in disposition:
            files[name] = (disposition.split('filename="')[1].split('"')[0], body)
        else:
            fields.setdefault(name, []).append(body.decode())
    return fields, files


class DocTranslationTests(unittest.TestCase):
    def call(self, *, asynchronous, raw, method, args, kwargs, response):
        requests = []

        def handler(request):
            requests.append(request)
            status, body = response
            return httpx.Response(status, json=body)

        transport = httpx.MockTransport(handler)

        def pick(sdk):
            client = sdk.document_translation
            return getattr(client.with_raw_response if raw else client, method)

        if asynchronous:

            async def run():
                async with httpx.AsyncClient(transport=transport) as http:
                    return await pick(AsyncCambAI(api_key="test-key", httpx_client=http))(*args, **kwargs)

            result = asyncio.run(run())
        else:
            with httpx.Client(transport=transport) as http:
                result = pick(CambAI(api_key="test-key", httpx_client=http))(*args, **kwargs)
        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0].headers["x-api-key"], "test-key")
        return (result.data if raw else result), requests[0]

    def variants(self):
        for asynchronous in (False, True):
            for raw in (False, True):
                yield asynchronous, raw

    def test_create_with_file_sends_multipart_form(self):
        for asynchronous, raw in self.variants():
            with self.subTest(asynchronous=asynchronous, raw=raw):
                result, request = self.call(
                    asynchronous=asynchronous,
                    raw=raw,
                    method="create_doc_translation",
                    args=(),
                    kwargs=dict(
                        source_language="en-us",
                        target_language=76,
                        media_file=("contract.docx", b"DOCX-BYTES"),
                        project_name="Contract",
                        chosen_dictionaries=[3, 7],
                        translation_style="formal",
                    ),
                    response=(200, {"task_id": "t-1", "run_id": 42}),
                )
                self.assertIsInstance(result, CreateDocTranslationOut)
                self.assertEqual((result.task_id, result.run_id), ("t-1", 42))
                self.assertEqual(request.method, "POST")
                self.assertTrue(request.url.path.endswith("/translate-doc"))
                self.assertIn("multipart/form-data", request.headers["content-type"])
                fields, files = _form_fields(request)
                self.assertEqual(files, {"media_file": ("contract.docx", b"DOCX-BYTES")})
                self.assertEqual(fields["source_language"], ["en-us"])
                self.assertEqual(fields["target_language"], ["76"])
                self.assertEqual(fields["project_name"], ["Contract"])
                self.assertEqual(fields["chosen_dictionaries"], ["3", "7"])
                self.assertEqual(fields["translation_style"], ["formal"])
                for omitted in ("media_url", "project_description", "folder_id"):
                    self.assertNotIn(omitted, fields)

    def test_create_with_url_sends_no_file_part(self):
        for asynchronous, raw in self.variants():
            with self.subTest(asynchronous=asynchronous, raw=raw):
                result, request = self.call(
                    asynchronous=asynchronous,
                    raw=raw,
                    method="create_doc_translation",
                    args=(),
                    kwargs=dict(
                        source_language=1,
                        target_language="es-es",
                        media_url="https://example.com/subs.srt",
                    ),
                    response=(200, {"task_id": "t-2"}),
                )
                self.assertEqual(result.task_id, "t-2")
                self.assertIsNone(result.run_id)
                self.assertIn("multipart/form-data", request.headers["content-type"])
                fields, files = _form_fields(request)
                self.assertEqual(files, {})
                self.assertEqual(fields["media_url"], ["https://example.com/subs.srt"])
                self.assertEqual(set(fields), {"source_language", "target_language", "media_url"})

    def test_status_and_result(self):
        for asynchronous, raw in self.variants():
            with self.subTest(asynchronous=asynchronous, raw=raw):
                status, request = self.call(
                    asynchronous=asynchronous,
                    raw=raw,
                    method="get_doc_translation_task_status",
                    args=("t-1",),
                    kwargs={},
                    response=(200, {"status": "SUCCESS", "run_id": 42}),
                )
                self.assertEqual(request.method, "GET")
                self.assertTrue(request.url.path.endswith("/translate-doc/t-1"))
                self.assertEqual(status.run_id, 42)

                result, request = self.call(
                    asynchronous=asynchronous,
                    raw=raw,
                    method="get_doc_translation_result",
                    args=(42,),
                    kwargs={},
                    response=(200, {"download_url": "https://cdn.example.com/out.docx"}),
                )
                self.assertEqual(request.method, "GET")
                self.assertTrue(request.url.path.endswith("/translate-doc-result/42"))
                self.assertIsInstance(result, DocTranslationResult)
                self.assertEqual(result.download_url, "https://cdn.example.com/out.docx")

    def test_validation_error_raises(self):
        for asynchronous, raw in self.variants():
            with self.subTest(asynchronous=asynchronous, raw=raw):
                with self.assertRaises(UnprocessableEntityError):
                    self.call(
                        asynchronous=asynchronous,
                        raw=raw,
                        method="create_doc_translation",
                        args=(),
                        kwargs=dict(source_language=1, target_language=2, media_url="https://example.com/a.docx"),
                        response=(422, {"detail": [{"loc": ["body", "target_language"], "msg": "bad", "type": "x"}]}),
                    )


if __name__ == "__main__":
    unittest.main()
