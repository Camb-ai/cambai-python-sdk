"""CLI helpers for Deepgram-style live transcription output."""

from __future__ import annotations

import shutil
import sys
import typing

from .events import ServerMessageType
from .session import LiveTranscriptionSession


def _wrapped_line_count(text: str, width: int) -> int:
    if not text:
        return 0
    lines = 0
    for segment in text.split("\n"):
        lines += max(1, (len(segment) + width - 1) // width)
    return lines


class TranscriptPrinter:
    """Replace the previous transcript block in-place (handles terminal wrap)."""

    def __init__(self, *, file: typing.TextIO = sys.stdout) -> None:
        self._file = file
        self._prev_lines = 0
        self._last_text = ""

    def _rewrite_block(self, text: str) -> None:
        if not self._file.isatty():
            self._file.write(f"{text}\n")
            self._file.flush()
            self._prev_lines = 0
            return

        width = shutil.get_terminal_size(fallback=(80, 24)).columns
        if self._prev_lines > 0:
            if self._prev_lines > 1:
                self._file.write(f"\x1b[{self._prev_lines - 1}A")
            self._file.write("\r\x1b[0J")
        self._file.write(text)
        self._file.flush()
        self._prev_lines = _wrapped_line_count(text, width)

    def print_interim(self, transcript: str) -> None:
        text = transcript.strip()
        if not text or text == self._last_text:
            return
        self._last_text = text
        self._rewrite_block(text)

    def print_final(self, transcript: str) -> None:
        text = transcript.strip()
        if text:
            if text != self._last_text:
                self._rewrite_block(text)
            self._file.write("\n")
        elif self._prev_lines > 0:
            self._file.write("\n")
        self._file.flush()
        self._prev_lines = 0
        self._last_text = ""

    def newline(self) -> None:
        if self._prev_lines > 0:
            self._file.write("\n")
            self._file.flush()
        self._prev_lines = 0
        self._last_text = ""


def create_transcript_printer(*, file: typing.TextIO = sys.stdout) -> TranscriptPrinter:
    return TranscriptPrinter(file=file)


def bind_transcript_printer(session: LiveTranscriptionSession) -> TranscriptPrinter:
    """Attach interim/final CLI printing to a live session."""
    printer = create_transcript_printer()

    @session.on(ServerMessageType.RESULTS)
    def _results(msg) -> None:
        if msg.is_final:
            printer.print_final(msg.transcript)
        else:
            printer.print_interim(msg.transcript)

    @session.on(ServerMessageType.FINAL)
    def _final(msg) -> None:
        printer.print_final(msg.transcript)

    return printer
