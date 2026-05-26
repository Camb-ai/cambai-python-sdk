"""Exceptions raised by the realtime translation client."""


class RealtimeError(Exception):
    """Base class for every exception raised by ``camb.realtime``."""


class RealtimeConnectError(RealtimeError):
    """The WebSocket handshake failed, the server rejected the upgrade, or
    the session did not become ready within the allowed timeout."""


class RealtimeProtocolError(RealtimeError):
    """The server sent a frame the client could not decode or validate."""
