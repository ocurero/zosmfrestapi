import httpx2

from . import ZosmfError


class ZosmfWorkflowBaseError(ZosmfError):
    """Base exception for z/OSMF workflow operations."""

    pass


class ZosmfWorkflowError(ZosmfWorkflowBaseError):
    """Raised when a workflow REST request fails with an HTTP status.

    When present in the response, ``status_code``, ``message_id``, ``message``,
    and ``body`` expose the z/OSMF error details.
    """

    def __init__(self, error: httpx2.HTTPStatusError | None = None) -> None:
        self.exc = error
        self.status_code = error.response.status_code if error else None
        self.message_id = error.response.json()["messageID"] if error else None
        self.message = error.response.json()["messageText"] if error else None
        self.body = error.response.text if error else None


class ZosmfWorkflowCanceledError(ZosmfWorkflowBaseError):
    """Reserved for workflow-specific cancellation failures."""

    pass
