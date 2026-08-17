"""Tests for live transcription URL building and connection options."""

from __future__ import annotations

from urllib.parse import parse_qs, urlparse

from camb.live_transcription.options import ConnectOptions, Encoding
from camb.live_transcription.session import (
    DEFAULT_LIVE_TRANSCRIPTION_BASE_URL,
    _build_url,
)


def test_default_base_url_is_realtime_host() -> None:
    assert DEFAULT_LIVE_TRANSCRIPTION_BASE_URL == "wss://realtime.camb.ai"


def test_build_url_defaults() -> None:
    url = _build_url(DEFAULT_LIVE_TRANSCRIPTION_BASE_URL, ConnectOptions())

    parsed = urlparse(url)
    assert parsed.scheme == "wss"
    assert parsed.netloc == "realtime.camb.ai"
    assert parsed.path == "/streaming-transcription/listen"
    assert parse_qs(parsed.query) == {
        "model": ["boli-v5"],
        "language": ["en-us"],
        "encoding": ["linear16"],
        "sample_rate": ["16000"],
        "channels": ["1"],
    }


def test_build_url_rewrites_https_and_http_to_ws() -> None:
    https_url = _build_url("https://example.com/", ConnectOptions())
    http_url = _build_url("http://example.com", ConnectOptions())

    assert https_url.startswith("wss://example.com/streaming-transcription/listen?")
    assert http_url.startswith("ws://example.com/streaming-transcription/listen?")


def test_build_url_strips_trailing_slash() -> None:
    url = _build_url("wss://realtime.camb.ai/", ConnectOptions())

    assert "realtime.camb.ai//streaming" not in url
    assert url.startswith("wss://realtime.camb.ai/streaming-transcription/listen?")


def test_build_url_reflects_custom_options() -> None:
    opts = ConnectOptions(
        model="boli-v6",
        language="de-de",
        encoding=Encoding.MULAW,
        sample_rate=8000,
        channels=2,
    )

    url = _build_url(DEFAULT_LIVE_TRANSCRIPTION_BASE_URL, opts)

    assert parse_qs(urlparse(url).query) == {
        "model": ["boli-v6"],
        "language": ["de-de"],
        "encoding": ["mulaw"],
        "sample_rate": ["8000"],
        "channels": ["2"],
    }


def test_connect_options_defaults() -> None:
    opts = ConnectOptions()

    assert opts.to_query() == {
        "model": "boli-v5",
        "language": "en-us",
        "encoding": "linear16",
        "sample_rate": "16000",
        "channels": "1",
    }