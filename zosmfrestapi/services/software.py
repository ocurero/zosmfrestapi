import logging
import time
from typing import Any
from dataclasses import asdict

import pendulum
from dacite import Config, from_dict

from zosmfrestapi.exceptions.software import (
    ZosmfSoftwareInstanceNotFoundError,
    ZosmfSoftwareManagementError,
    ZosmfSoftwareManagementRequestError,
)
from zosmfrestapi.models.software import (
    CsiEntry,
    DataSet,
    DataSetProperty,
    DataSetPropertyLabel,
    NonSmpeManagedDataset,
    NonSmpeProduct,
    Product,
    ProductProperty,
    SmpeManagedDataset,
    SmpeManagedUnixDataset,
    SoftwareInstance,
    SoftwareInstanceWorkflow,
)
from zosmfrestapi.utils import _parse_datetime, remap

from . import ZosmfBase

logger = logging.getLogger(__name__)


class SoftwareServices(ZosmfBase):
    """Manage z/OSMF software instances and query their SMP/E CSI data."""

    def list_swis(self) -> list[SoftwareInstance]:
        """List the software instances available on the z/OSMF server.

        Returns:
            A list of ``SoftwareInstance`` objects.

        Raises:
            ZosmfAuthError: If z/OSMF returns HTTP 401.
            ZosmfError: If z/OSMF returns another unsuccessful HTTP status.
            httpx2.RequestError: If the request fails before an HTTP response
                is received.
        """
        resp = self.http.get("/zosmf/swmgmt/swi")
        self._raise_for_status(resp)
        return [
            from_dict(
                data_class=SoftwareInstance,
                data=remap(swi, SoftwareInstance),
                config=Config(
                    type_hooks={
                        pendulum.DateTime: _parse_datetime,
                    }
                ),
            )
            for swi in resp.json()["swilist"]
        ]

    def _get_swi(self, path: str) -> SoftwareInstance:
        resp = self.http.get(path)
        if resp.status_code == 404:
            raise ZosmfSoftwareInstanceNotFoundError(resp)
        self._raise_for_status(resp, exc_handler=ZosmfSoftwareManagementError)
        return from_dict(
            data_class=SoftwareInstance,
            data=remap(resp.json(), SoftwareInstance),
            config=Config(
                type_hooks={
                    pendulum.DateTime: _parse_datetime,
                    list[DataSet]: lambda v: [] if v is None else v,
                    list[Product]: lambda v: [] if v is None else v,
                    list[NonSmpeProduct]: lambda v: [] if v is None else v,
                    list[SoftwareInstanceWorkflow]: lambda v: [] if v is None else v,
                    list[DataSetProperty]: lambda v: [] if v is None else v,
                    list[DataSetPropertyLabel]: lambda v: [] if v is None else v,
                    list[ProductProperty]: lambda v: [] if v is None else v,
                }
            ),
        )

    def get_swi_by_uuid(self, swiuuid: str) -> SoftwareInstance:
        """Retrieve a software instance by UUID.

        Args:
            swiuuid: UUID of the software instance.

        Returns:
            The matching ``SoftwareInstance``.

        Raises:
            ZosmfSoftwareInstanceNotFoundError: If z/OSMF returns HTTP 404.
            ZosmfAuthError: If z/OSMF returns HTTP 401.
            ZosmfSoftwareManagementError: If z/OSMF returns another
                unsuccessful HTTP status.
            httpx2.RequestError: If the request fails before an HTTP response
                is received.
        """
        return self._get_swi(f"/zosmf/swmgmt/swi/{swiuuid}")

    def get_swi_by_name(self, name: str, system: str) -> SoftwareInstance:
        """Retrieve a software instance by name and system.

        Args:
            name: Name of the software instance.
            system: System where the software instance is defined.

        Returns:
            The matching ``SoftwareInstance``.

        Raises:
            ZosmfSoftwareInstanceNotFoundError: If z/OSMF returns HTTP 404.
            ZosmfAuthError: If z/OSMF returns HTTP 401.
            ZosmfSoftwareManagementError: If z/OSMF returns another
                unsuccessful HTTP status.
            httpx2.RequestError: If the request fails before an HTTP response
                is received.
        """
        return self._get_swi(f"/zosmf/swmgmt/swi/{system}/{name}")

    def _get_swi_datasets(self, path: str) -> dict[
        str,
        list[SmpeManagedDataset]
        | list[SmpeManagedUnixDataset]
        | list[NonSmpeManagedDataset],
    ]:
        resp = self.http.post(path)
        if resp.status_code == 404:
            raise ZosmfSoftwareInstanceNotFoundError(resp)
        self._raise_for_status(resp, exc_handler=ZosmfSoftwareManagementError)
        status_monitor_url = resp.json()["statusurl"]
        status = self.http.get(status_monitor_url)
        while status.json()["status"] == "running":
            time.sleep(2)
            status = self.http.get(status_monitor_url)
            self._raise_for_status(status, exc_handler=ZosmfSoftwareManagementError)
        return {
            "smpemanageddatasets": [
                from_dict(data_class=SmpeManagedDataset, data=dataset)
                for dataset in status.json()["smpemanageddatasets"] or []
            ],
            "smpemanagedunixdatasets": [
                from_dict(data_class=SmpeManagedUnixDataset, data=missing)
                for missing in status.json()["smpemanagedunixdatasets"] or []
            ],
            "nonsmpemanageddatasets": [
                from_dict(data_class=NonSmpeManagedDataset, data=missing)
                for missing in status.json()["nonsmpemanageddatasets"] or []
            ],
        }

    def get_swi_datasets_by_uuid(self, swiuuid: str) -> dict[
        str,
        list[SmpeManagedDataset]
        | list[SmpeManagedUnixDataset]
        | list[NonSmpeManagedDataset],
    ]:
        """Retrieve dataset inventories for a software instance by UUID.

        z/OSMF processes this request asynchronously; this method polls its
        status endpoint until the inventory is ready.

        Args:
            swiuuid: UUID of the software instance.

        Returns:
            A dictionary with ``smpemanageddatasets``,
            ``smpemanagedunixdatasets``, and ``nonsmpemanageddatasets`` keys.
            Each value is a list of the corresponding parsed dataset model.

        Raises:
            ZosmfSoftwareInstanceNotFoundError: If z/OSMF returns HTTP 404.
            ZosmfAuthError: If a request returns HTTP 401.
            ZosmfSoftwareManagementRequestError: If a request returns another
                unsuccessful HTTP status.
            httpx2.RequestError: If a request fails before an HTTP response is
                received.
        """
        return self._get_swi_datasets(f"/zosmf/swmgmt/swi/{swiuuid}/datasets")

    def get_swi_datasets_by_name(self, name: str, system: str) -> dict[
        str,
        list[SmpeManagedDataset]
        | list[SmpeManagedUnixDataset]
        | list[NonSmpeManagedDataset],
    ]:
        """Retrieve dataset inventories for a software instance by name.

        z/OSMF processes this request asynchronously; this method polls its
        status endpoint until the inventory is ready.

        Args:
            name: Name of the software instance.
            system: System where the software instance is defined.

        Returns:
            A dictionary with ``smpemanageddatasets``,
            ``smpemanagedunixdatasets``, and ``nonsmpemanageddatasets`` keys.
            Each value is a list of the corresponding parsed dataset model.

        Raises:
            ZosmfSoftwareInstanceNotFoundError: If z/OSMF returns HTTP 404.
            ZosmfAuthError: If a request returns HTTP 401.
            ZosmfSoftwareManagementRequestError: If a request returns another
                unsuccessful HTTP status.
            httpx2.RequestError: If a request fails before an HTTP response is
                received.
        """
        return self._get_swi_datasets(f"/zosmf/swmgmt/swi/{system}/{name}/datasets")

    def add_swi(self, swi: SoftwareInstance) -> bool:
        """Add a new software instance.

        Args:
            swi: Validated software-instance data to submit, including its name
                and system and any configured zones, data sets, products, or
                workflows.

        Returns:
            ``True`` when z/OSMF responds with HTTP 201; ``False`` for another
            successful response status.

        Raises:
            ZosmfAuthError: If z/OSMF returns HTTP 401.
            ZosmfSoftwareManagementRequestError: If z/OSMF returns another
                unsuccessful HTTP status.
            httpx2.RequestError: If the request fails before an HTTP response
                is received.
        """
        resp = self.http.post(
            "/zosmf/swmgmt/swi",
            json={
                "name": swi.name,
                "system": swi.system,
                "description": swi.description if swi.description else "",
                "globalzone": swi.globalzone if swi.globalzone else "",
                "targetzones": swi.targetzones if swi.targetzones else [],
                "categories": swi.categories if swi.categories else [],
                "datasets": swi.datasets if swi.datasets else [],
                "products": (
                    [
                        {
                            "prodname": product.prodname,
                            "prodid": product.productid,
                            "release": product.release,
                            "vendor": product.vendor,
                            "url": product.url,
                            "features": (
                                [feature.feature for feature in product.features]
                                if product.features
                                else []
                            ),
                            "generalavailability": product.generalavailability,
                            "endofservice": product.endofservice,
                        }
                        for product in swi.products
                    ]
                    if swi.products
                    else []
                ),
                "workflows": (
                    [asdict(workflow) for workflow in swi.workflows]
                    if swi.workflows
                    else []
                ),
            },
        )
        self._raise_for_status(resp, exc_handler=ZosmfSoftwareManagementRequestError)
        return resp.status_code == 201

    def _remove_sw_instance(self, path: str) -> bool:
        resp = self.http.delete(path)
        if resp.status_code == 404:
            raise ZosmfSoftwareInstanceNotFoundError(resp)
        self._raise_for_status(resp, exc_handler=ZosmfSoftwareManagementRequestError)
        return resp.status_code == 200

    def remove_sw_instance_by_uuid(self, swiuuid: str) -> bool:
        """Delete a software instance identified by UUID.

        Args:
            swiuuid: UUID of the software instance to delete.

        Returns:
            ``True`` when z/OSMF responds with HTTP 200; ``False`` for another
            successful response status.

        Raises:
            ZosmfSoftwareInstanceNotFoundError: If z/OSMF returns HTTP 404.
            ZosmfAuthError: If z/OSMF returns HTTP 401.
            ZosmfSoftwareManagementRequestError: If z/OSMF returns another
                unsuccessful HTTP status.
            httpx2.RequestError: If the request fails before an HTTP response
                is received.
        """
        return self._remove_sw_instance(f"/zosmf/swmgmt/swi/{swiuuid}")

    def remove_sw_instance_by_name(self, name: str, system: str) -> bool:
        """Delete a software instance identified by name.

        Args:
            name: Name of the software instance to delete.
            system: System where the software instance is defined.

        Returns:
            ``True`` when z/OSMF responds with HTTP 200; ``False`` for another
            successful response status.

        Raises:
            ZosmfSoftwareInstanceNotFoundError: If z/OSMF returns HTTP 404.
            ZosmfAuthError: If z/OSMF returns HTTP 401.
            ZosmfSoftwareManagementRequestError: If z/OSMF returns another
                unsuccessful HTTP status.
            httpx2.RequestError: If the request fails before an HTTP response
                is received.
        """
        return self._remove_sw_instance(f"/zosmf/swmgmt/swi/{system}/{name}")

    def _query_csi(
        self,
        path: str,
        zones: list[str],
        entries: list[str],
        subentries: list[str],
        filter: str | None,
        zosmf_auth: tuple[str, ...],
        proxy_auth: tuple[str, ...],
        wait: bool,
    ) -> list[CsiEntry] | dict[str, Any]:
        if "*" in entries and len(entries) > 1:
            raise ZosmfSoftwareManagementError(
                "'*' cannot be combined with other entry types."
            )
        elif "*" in subentries and len(subentries) > 1:
            raise ZosmfSoftwareManagementError(
                "'*' cannot be combined with other subentry types."
            )
        resp = self.http.post(
            path,
            json={
                "zones": zones,
                "entries": entries,
                "subentries": subentries,
                "filter": filter or "",
            },
        )
        self._raise_for_status(resp, exc_handler=ZosmfSoftwareManagementRequestError)
        if wait:
            status = self.get_query_csi_status(resp.json()["statusurl"], wait=True)
            return status
        return resp.json()

    def query_csi_by_uuid(
        self,
        uuid: str,
        zones: list[str],
        entries: list[str],
        subentries: list[str] = ["*"],
        filter: str | None = None,
        zosmf_auth: tuple[str, ...] = (),
        proxy_auth: tuple[str, ...] = (),
        wait: bool = True,
    ) -> list[CsiEntry] | dict[str, Any]:
        """Query CSI data for a software instance identified by its UUID.

        Args:
            uuid: UUID of the software instance to query.
            zones: CSI zones to search.
            entries: Entry types to retrieve. ``"*"`` cannot be combined with
                other entry types.
            subentries: Subentry types to retrieve. ``"*"`` cannot be combined
                with other subentry types.
            filter: Optional filter expression sent to z/OSMF.
            zosmf_auth: Reserved compatibility argument; currently not applied.
            proxy_auth: Reserved compatibility argument; currently not applied.
            wait: If true, poll until the query completes and return its entries.

        Returns:
            A list of ``CsiEntry`` objects when ``wait`` is true; otherwise,
            the initial response dictionary from z/OSMF.

        Raises:
            ZosmfSoftwareManagementError: If ``"*"`` is combined with
                other entry or subentry types.
            ZosmfAuthError: If z/OSMF returns HTTP 401.
            ZosmfSoftwareManagementRequestError: If z/OSMF returns another
                unsuccessful HTTP status.
            httpx2.RequestError: If a request fails before an HTTP response is
                received.
        """
        return self._query_csi(
            f"/zosmf/swmgmt/swi/{uuid}/csiquery",
            zones,
            entries,
            subentries,
            filter,
            zosmf_auth=zosmf_auth,
            proxy_auth=proxy_auth,
            wait=wait,
        )

    def query_csi_by_name(
        self,
        name: str,
        system: str,
        zones: list[str],
        entries: list[str],
        subentries: list[str] = ["*"],
        filter: str | None = None,
        zosmf_auth: tuple[str, ...] = (),
        proxy_auth: tuple[str, ...] = (),
        wait: bool = True,
    ) -> list[CsiEntry] | dict[str, Any]:
        """Query CSI data for a software instance identified by name and system.

        Args:
            name: Name of the software instance to query.
            system: System where the software instance is defined.
            zones: CSI zones to search.
            entries: Entry types to retrieve. ``"*"`` cannot be combined with
                other entry types.
            subentries: Subentry types to retrieve. ``"*"`` cannot be combined
                with other subentry types.
            filter: Optional filter expression sent to z/OSMF.
            zosmf_auth: Reserved compatibility argument; currently not applied.
            proxy_auth: Reserved compatibility argument; currently not applied.
            wait: If true, poll until the query completes and return its entries.

        Returns:
            A list of ``CsiEntry`` objects when ``wait`` is true; otherwise,
            the initial response dictionary from z/OSMF.

        Raises:
            ZosmfSoftwareManagementError: If ``"*"`` is combined with
                other entry or subentry types.
            ZosmfAuthError: If z/OSMF returns HTTP 401.
            ZosmfSoftwareManagementRequestError: If z/OSMF returns another
                unsuccessful HTTP status.
            httpx2.RequestError: If a request fails before an HTTP response is
                received.
        """
        return self._query_csi(
            f"/zosmf/swmgmt/swi/{system}/{name}/csiquery",
            zones,
            entries,
            subentries,
            filter,
            zosmf_auth=zosmf_auth,
            proxy_auth=proxy_auth,
            wait=wait,
        )

    def _get_query_csi_status(self, statusurl: str) -> dict[str, Any]:
        resp = self.http.get(statusurl)
        self._raise_for_status(resp, exc_handler=ZosmfSoftwareManagementRequestError)
        return resp.json()

    def get_query_csi_status(self, statusurl: str, wait: bool = True) -> list[CsiEntry]:
        """Retrieve the entries for a CSI query, optionally waiting for completion.

        Args:
            statusurl: Status URL returned by a CSI query submission.
            wait: Poll every two seconds while the status is ``"running"`` when
                true. When false, parse the entries in the first status response.

        Returns:
            Parsed ``CsiEntry`` objects from the final status response, or from
            the initial response when ``wait`` is false.

        Raises:
            ZosmfAuthError: If z/OSMF returns HTTP 401.
            ZosmfSoftwareManagementRequestError: If z/OSMF returns another
                unsuccessful HTTP status.
            httpx2.RequestError: If a request fails before an HTTP response is
                received.
        """
        status = self._get_query_csi_status(statusurl)
        if wait:
            while status["status"] == "running":
                time.sleep(2)
                status = self._get_query_csi_status(statusurl)
        return [
            from_dict(data_class=CsiEntry, data=entry) for entry in status["entries"]
        ]
