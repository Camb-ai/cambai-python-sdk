"""Tests for realtime option serialization and URL building."""

from __future__ import annotations

from urllib.parse import parse_qs, urlparse

from camb.realtime.options import ConnectOptions, OutputModality, RealtimeModel
from camb.realtime.session import DEFAULT_REALTIME_BASE_URL, _build_url


def test_build_url_defaults() -> None:
    opts = ConnectOptions(source_language="en-US", target_language="de-DE")

    url = _build_url(DEFAULT_REALTIME_BASE_URL, opts)

    parsed = urlparse(url)
    assert parsed.scheme == "wss"
    assert parsed.netloc == "realtime.camb.ai"
    assert parsed.path == "/v1/realtime"
    assert parse_qs(parsed.query) == {"model": ["lilac"]}


def test_build_url_rewrites_schemes_and_strips_slash() -> None:
    url = _build_url("https://example.com/", ConnectOptions(source_language="en-US", target_language="fr-FR"))

    assert url.startswith("wss://example.com/v1/realtime?")
    assert "example.com//v1" not in url


def test_to_query_only_carries_model() -> None:
    opts = ConnectOptions(model=RealtimeModel.IRIS, source_language="en-US", target_language="de-DE")

    assert opts.to_query() == {"model": "iris"}


def test_to_session_payload_default_modalities() -> None:
    opts = ConnectOptions(source_language="en-US", target_language="de-DE")

    assert opts.to_session_payload() == {
        "model": "lilac",
        "source_language": "en-US",
        "target_language": "de-DE",
        "output_modalities": ["text", "audio"],
    }


def test_to_session_payload_custom_modalities() -> None:
    opts = ConnectOptions(
        model=RealtimeModel.VIOLET,
        source_language="en-US",
        target_language="de-DE",
        output_modalities=[OutputModality.TEXT],
    )

    assert opts.to_session_payload()["output_modalities"] == ["text"]
    assert opts.to_session_payload()["model"] == "violet"


def test_to_session_payload_voice_id() -> None:
    opts = ConnectOptions(source_language="en-US", target_language="de-DE", voice_id=147320)

    payload = opts.to_session_payload()

    assert payload["voice"] == {"type": "cloned", "voice_id": 147320}


def test_to_session_payload_no_voice() -> None:
    opts = ConnectOptions(source_language="en-US", target_language="de-DE")

    assert "voice" not in opts.to_session_payload()