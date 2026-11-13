import httpx2


class ZosmfError(Exception):
    """Base exception for errors raised by the z/OSMF REST API client."""

    pass


class ZosmfAuthError(ZosmfError):
    """Raised when z/OSMF rejects a request with HTTP 401.

    The triggering ``httpx2.HTTPStatusError`` is available as
    :attr:`http_exception`.
    """

    def __init__(self, exc: httpx2.HTTPStatusError) -> None:
        self.http_exception = exc
