import logging
from . import ZosmfBase
from dacite import from_dict
from zosmfrestapi import _utils
from zosmfrestapi.models.topology import Group, System

logger = logging.getLogger(__name__)


class TopologyServices(ZosmfBase):
    """Read groups and systems from the z/OSMF topology REST API."""

    def get_groups(self) -> dict[str, Group]:
        """Return z/OSMF groups keyed by each group's name.

        Returns:
            A mapping from group name to its parsed :class:`Group` model.

        Raises:
            ZosmfAuthError: If z/OSMF returns HTTP 401.
            ZosmfError: If z/OSMF returns another unsuccessful HTTP status.
            httpx2.RequestError: If the request fails before an HTTP response
                is received.
        """
        resp = self.http.get("/zosmf/resttopology/groups")
        self._raise_for_status(resp)
        return {
            item["name"]: from_dict(Group, data=_utils.remap(item, Group))
            for item in resp.json()["items"]
        }

    def get_systems(self) -> dict[str, System]:
        """Return z/OSMF systems keyed by each system's topology name.

        Returns:
            A mapping from the system name to its parsed :class:`System` model.

        Raises:
            ZosmfAuthError: If z/OSMF returns HTTP 401.
            ZosmfError: If z/OSMF returns another unsuccessful HTTP status.
            httpx2.RequestError: If the request fails before an HTTP response
                is received.
        """
        resp = self.http.get("/zosmf/resttopology/systems")
        self._raise_for_status(resp)
        return {
            item["systemName"]: from_dict(System, data=_utils.remap(item, System))
            for item in resp.json()["items"]
        }
