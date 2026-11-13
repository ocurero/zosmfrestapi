import logging

import httpx2
from zosmfrestapi.exceptions.commons import ZosmfError

logger = logging.getLogger(__name__)


class ZosmfDatasetError(ZosmfError):
    """Raised when a data set REST request fails with an HTTP status error."""


class ZosmfDatasetNotFoundError(ZosmfDatasetError):
    """Raised when z/OSMF reports that the requested data set is not found."""

    def __init__(self, response: httpx2.Response) -> None:
        pass
