"""Tests for the sync/async stream-to-file helpers in ``camb.client``."""

from __future__ import annotations

import asyncio
import os

from camb.client import save_async_stream_to_file, save_stream_to_file


def test_save_stream_to_file(tmp_path) -> None:
    target = tmp_path / "out.bin"
    chunks = [b"a" * 256, b"b" * 256, b"c" * 256]

    save_stream_to_file(iter(chunks), str(target))

    assert target.read_bytes() == bytes(b"a" * 256 + b"b" * 256 + b"c" * 256)


def test_save_stream_to_file_empty_stream(tmp_path) -> None:
    target = tmp_path / "empty.bin"

    save_stream_to_file(iter([]), str(target))

    assert target.read_bytes() == b""


def _run(coro) -> None:
    asyncio.run(coro)


def test_save_async_stream_to_file(tmp_path) -> None:
    target = tmp_path / "async.bin"
    chunks = [bytes(range(256))] * 4

    async def gen():
        for chunk in chunks:
            yield chunk

    _run(save_async_stream_to_file(gen(), str(target)))

    assert target.read_bytes() == bytes(range(256)) * 4
    assert os.path.getsize(str(target)) == 1024


def test_save_async_stream_to_file_empty_stream(tmp_path) -> None:
    target = tmp_path / "empty_async.bin"

    async def gen():
        if False:
            yield b""

    _run(save_async_stream_to_file(gen(), str(target)))

    assert target.read_bytes() == b""