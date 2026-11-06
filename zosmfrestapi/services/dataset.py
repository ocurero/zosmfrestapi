import logging

from zosmfrestapi.exceptions.dataset import ZosmfDatasetError, ZosmfDatasetNotFoundError

from . import ZosmfBase

logger = logging.getLogger(__name__)


class DatasetServices(ZosmfBase):
    """Read sequential or partitioned data sets through z/OSMF Files REST APIs."""

    def _read_dataset(self, path: str) -> str:
        resp = self.http.get(path)
        if resp.status_code == 404:
            raise ZosmfDatasetNotFoundError(resp)
        self._raise_for_status(resp, exc_handler=ZosmfDatasetError)
        return resp.text

    def read_dataset(self, dataset: str, volser: str | None = None) -> str:
        """Read a dataset or dataset member through the z/OSMF Files REST API.

        Args:
            dataset: Fully qualified data set name, optionally including a
                member in parentheses, for example ``USER.PDS(MEMBER)``.
            volser: Optional volume serial for a data set that is not cataloged.
                When supplied, it is included in the z/OSMF request path.

        Returns:
            The contents returned by z/OSMF as text.

        Raises:
            ZosmfDatasetNotFoundError: If z/OSMF returns HTTP 404 for the data
                set request.
            ZosmfAuthError: If z/OSMF rejects the request with HTTP 401.
            ZosmfDatasetError: If z/OSMF returns another unsuccessful HTTP
                status.
            httpx2.HTTPError: If a transport-level HTTP error occurs.
        """
        if volser:
            return self._read_dataset(f"/zosmf/restfiles/ds/-({volser})/{dataset}")
        return self._read_dataset(f"/zosmf/restfiles/ds/{dataset}")
