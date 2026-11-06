from . import ZosmfError


class ZosmfSoftwareManagementError(ZosmfError):
    """Base exception for z/OSMF Software Management operations."""


class ZosmfSoftwareManagementRequestError(ZosmfSoftwareManagementError):
    """Raised when a Software Management request fails with an HTTP status.

    When the response includes the corresponding fields, ``status_code``,
    ``reason_code``, ``messages``, and ``body`` provide response details.
    """

    def __init__(self, error=None) -> None:
        self.status_code = error.response.status_code if error else None
        self.reason_code = error.response.json()["reason"] if error else None
        self.messages = error.response.json()["messages"] if error else None
        self.body = error.response.text if error else None


class ZosmfSoftwareInstanceNotFoundError(ZosmfSoftwareManagementError):
    """Raised when a requested software instance does not exist."""

    def __init__(self, response) -> None:
        super().__init__(response)
        self.messages = (
            response.json().get("messages", [])
            if response.headers.get("Content-Type").startswith("application/json")
            else [response.text]
        )

    def __str__(self) -> str:
        return ", ".join(self.messages) if self.messages else ""
