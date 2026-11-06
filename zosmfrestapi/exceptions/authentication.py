import httpx2

from . import ZosmfError


class ZosmfLoginError(ZosmfError):
    """Raised when the authentication endpoint rejects a login request.

    The response's return code, reason code, and message are exposed as
    ``return_code``, ``reason_code``, and ``message``.
    """

    def __init__(self, response: httpx2.Response) -> None:
        self.http_exception = None
        self.return_code = response.json()["returnCode"]
        self.reason_code = response.json()["reasonCode"]
        self.message = response.json()["message"]
