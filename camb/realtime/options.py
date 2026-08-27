"""Connection options for the realtime WebSocket."""

from __future__ import annotations

import enum
import typing
import warnings

import pydantic


class RealtimeMode(str, enum.Enum):
    """Latency/quality tradeoff for a realtime session.

    ``FAST`` is ready to accept audio almost immediately and translates with the lowest latency,
    but supports fewer languages. ``SLOW`` supports the full language list and translates more
    accurately, at the cost of a 30s+ cold boot before the session is ready.

    Replaces the former ``RealtimeModel`` engine codenames (``lilac``/``violet``/``iris``/
    ``orchid``), which are still accepted and mapped — see
    :data:`LEGACY_ENGINE_CODENAMES`.
    """

    FAST = "fast"
    SLOW = "slow"


#: The retired engine codenames, each mapped onto the mode running the closest pipeline.
#:
#: ``iris`` was the only engine without a cold boot, so it becomes :attr:`RealtimeMode.FAST`; the
#: rest become :attr:`RealtimeMode.SLOW`. Accepted rather than rejected because an SDK consumer
#: upgrades on their own schedule — breaking them on a rename would be our choice, not theirs.
#:
#: Mirrors ``LEGACY_ENGINE_CODENAMES`` in realtime-api-server's ``protocol.rs``; the two must agree.
LEGACY_ENGINE_CODENAMES: typing.Mapping[str, RealtimeMode] = {
    "iris": RealtimeMode.FAST,
    "lilac": RealtimeMode.SLOW,
    "violet": RealtimeMode.SLOW,
    "orchid": RealtimeMode.SLOW,
}


def resolve_mode(value: str) -> typing.Optional[RealtimeMode]:
    """Resolve a selector, accepting ``fast``/``slow`` and the retired codenames.

    Returns ``None`` for a value that was never valid, so the caller can reject it — accepting the
    codenames must not degrade into accepting anything.
    """
    try:
        return RealtimeMode(value)
    except ValueError:
        return LEGACY_ENGINE_CODENAMES.get(value)


class OutputModality(str, enum.Enum):
    TEXT = "text"
    AUDIO = "audio"


class ConnectOptions(pydantic.BaseModel):
    """Options for a realtime translation session.

    ``source_language`` and ``target_language`` are required; all other fields
    have server-side defaults.

    Language values use IETF BCP-47 tags (e.g. ``"en-US"``, ``"de-DE"``).
    """

    # Unknown options are an error, not something to drop. ``connect(**options)`` funnels every
    # caller through this one constructor, so pydantic's default ``extra="ignore"`` would have made
    # a typo'd option vanish and the session run with a default the caller never asked for. The
    # retired ``model`` option is exempt — the validator below resolves it before field validation.
    model_config = pydantic.ConfigDict(extra="forbid")

    mode: RealtimeMode = RealtimeMode.FAST
    source_language: str
    target_language: str
    output_modalities: typing.List[OutputModality] = pydantic.Field(
        default_factory=lambda: [OutputModality.TEXT, OutputModality.AUDIO]
    )
    voice_id: typing.Optional[int] = None
    """Synthesize the translation with one of your cloned voices.

    Pass the ID of a voice you own (from ``client.voice_cloning.list_voices()``
    or a custom voice you created). When omitted, a built-in voice for
    ``target_language`` is used.

    For the most natural-sounding results, choose a voice whose reference
    language matches ``target_language``.
    """

    @pydantic.model_validator(mode="before")
    @classmethod
    def _accept_retired_model_option(cls, payload: typing.Any) -> typing.Any:
        """Accept the retired ``model`` option and the retired engine codenames.

        Runs before field validation so ``mode`` only ever sees a value the enum accepts — which is
        also what keeps ``extra="forbid"`` above from rejecting ``model`` outright.

        Two things can be stale independently: the option name (``model`` instead of ``mode``) and
        the value (a codename instead of a mode). ``mode`` wins when both are given, being the
        option the caller migrated to. A ``DeprecationWarning`` fires in either case: the call keeps
        working, and the migration stays visible instead of becoming invisible forever.
        """
        if not isinstance(payload, dict):
            return payload

        payload = dict(payload)
        retired_model = payload.pop("model", None)
        # Warned about on being supplied, not on winning: a caller passing both is still using the
        # retired option. Matches the server-side shim, which keys off the same condition.
        if retired_model is not None:
            warnings.warn(
                "The realtime `model` option is deprecated; use `mode` with 'fast' or 'slow'.",
                DeprecationWarning,
                stacklevel=2,
            )
        selector = payload.get("mode")
        if selector is None:
            selector = retired_model
        if not isinstance(selector, str):
            # Not a string (None, an already-resolved RealtimeMode, or junk) — leave it to field
            # validation, which reports the type error better than this hook could.
            return payload

        resolved = resolve_mode(selector)
        if resolved is not None and resolved.value != selector:
            warnings.warn(
                f"The realtime engine codename '{selector}' is deprecated; "
                f"use mode='{resolved.value}'.",
                DeprecationWarning,
                stacklevel=2,
            )
        # An unresolvable value passes through unchanged so the enum raises the ValidationError,
        # which names the option and lists what it accepts.
        payload["mode"] = resolved if resolved is not None else selector
        return payload

    def to_query(self) -> typing.Dict[str, str]:
        """Query-string parameters sent on the WebSocket upgrade URL."""
        return {"mode": self.mode.value}

    def to_session_payload(self) -> typing.Dict[str, typing.Any]:
        """Body of the ``session.update`` message sent after the WS handshake."""
        session: typing.Dict[str, typing.Any] = {
            "mode": self.mode.value,
            "source_language": self.source_language,
            "target_language": self.target_language,
            "output_modalities": [m.value for m in self.output_modalities],
        }
        if self.voice_id is not None:
            session["voice"] = {"type": "cloned", "voice_id": self.voice_id}
        return session
