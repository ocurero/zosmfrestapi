import time
from typing import Any

import pendulum
from dacite import Config, from_dict
from zosmfrestapi.models.software_updates import (
    MissingFixcat,
    MissingUpdate,
    SoftwareUpdate,
    UpdateProcess,
)

from zosmfrestapi.exceptions.software import (
    ZosmfSoftwareManagementError,
    ZosmfSoftwareInstanceNotFoundError,
    ZosmfSoftwareManagementRequestError,
)
from zosmfrestapi.utils import _parse_datetime

from . import ZosmfBase


class SoftwareUpdatesServices(ZosmfBase):
    """Search, inspect, start, cancel, resume, and collect update processes.

    Starting or resuming an update can change the selected target zone. Methods
    with ``wait=True`` poll z/OSMF until the process is no longer running;
    without waiting, they return the process ID so callers can monitor it later.
    """

    def _list_sw_updates(self, path: str) -> list[UpdateProcess]:
        resp = self.http.get(path)
        if resp.status_code == 404:
            return []
        self._raise_for_status(resp, exc_handler=ZosmfSoftwareManagementRequestError)
        return [
            from_dict(
                data_class=UpdateProcess,
                data=upd,
                config=Config(
                    type_hooks={
                        pendulum.DateTime: _parse_datetime,
                    },
                    convert_key=lambda k: k.replace("_", "-"),
                ),
            )
            for upd in resp.json()["update-processes"]
        ]

    def list_sw_updates_by_uuid(
        self, swiuuid: str, last: bool = False
    ) -> list[UpdateProcess]:
        """List update processes for a software instance identified by UUID.

        If z/OSMF reports that the software instance has no update-process
        history (HTTP 404), this method returns an empty list.

        Args:
            swiuuid: UUID of the software instance.
            last: If true, retrieve the most recent process; otherwise retrieve
                all recorded processes.

        Returns:
            A list of ``UpdateProcess`` objects.

        Raises:
            ZosmfAuthError: If z/OSMF returns HTTP 401.
            ZosmfSoftwareManagementRequestError: If z/OSMF returns another
                unsuccessful HTTP status.
            httpx2.RequestError: If the request fails before an HTTP response
                is received.
        """
        return self._list_sw_updates(
            f"/zosmf/swmgmt/swi/{swiuuid}/swupdate{'' if last else '/all'}"
        )

    def list_sw_updates_by_name(
        self, name: str, system: str, last: bool = False
    ) -> list[UpdateProcess]:
        """List update processes for a software instance identified by name.

        If z/OSMF reports that the software instance has no update-process
        history (HTTP 404), this method returns an empty list.

        Args:
            name: Name of the software instance.
            system: System where the software instance is defined.
            last: If true, retrieve the most recent process; otherwise retrieve
                all recorded processes.

        Returns:
            A list of ``UpdateProcess`` objects.

        Raises:
            ZosmfAuthError: If z/OSMF returns HTTP 401.
            ZosmfSoftwareManagementRequestError: If z/OSMF returns another
                unsuccessful HTTP status.
            httpx2.RequestError: If the request fails before an HTTP response
                is received.
        """
        return self._list_sw_updates(
            f"/zosmf/swmgmt/swi/{system}/{name}/swupdate{'' if last else '/all'}"
        )

    def get_sw_updates(
        self, process_id: int, wait: bool = False
    ) -> list[UpdateProcess]:
        """Get the update-process records for a process ID.

        Args:
            process_id: ID returned when the update process was started.
            wait: If true, poll every two seconds while any process is running.

        Returns:
            A list of parsed ``UpdateProcess`` records from the latest status
            response. With ``wait=True``, this is the final polled response.

        Raises:
            ZosmfAuthError: If a status request returns HTTP 401.
            ZosmfSoftwareManagementRequestError: If a status request returns another
                unsuccessful HTTP status.
            httpx2.RequestError: If a status request fails before an HTTP
                response is received.
        """
        updates = self._get_sw_updates(process_id)
        while any(upd["status"] == "RUNNING" for upd in updates) and wait:
            time.sleep(2)
            updates = self._get_sw_updates(process_id)
        return [
            from_dict(
                data_class=UpdateProcess,
                data=process,
                config=Config(
                    type_hooks={
                        pendulum.DateTime: _parse_datetime,
                    },
                    convert_key=lambda k: k.replace("_", "-"),
                ),
            )
            for process in updates
        ]

    def _get_missing_updates_or_fixcat(self, path: str, updates: bool) -> dict[
        str,
        pendulum.Date
        | pendulum.Time
        | pendulum.DateTime
        | pendulum.Duration
        | list[MissingUpdate]
        | list[MissingFixcat],
    ]:
        resp = self.http.post(path)
        if resp.status_code == 404:
            raise ZosmfSoftwareInstanceNotFoundError(resp)
        self._raise_for_status(resp, exc_handler=ZosmfSoftwareManagementRequestError)
        status_monitor_url = resp.json()["statusurl"]
        status = self.http.get(status_monitor_url)
        while status.json()["status"] == "running":
            time.sleep(2)
            status = self.http.get(status_monitor_url)
            self._raise_for_status(
                status, exc_handler=ZosmfSoftwareManagementRequestError
            )
        if updates:
            return {
                "lastholdrecvdate": pendulum.parse(status.json()["lastholdrecvdate"]),
                "list": [
                    from_dict(
                        data_class=MissingUpdate,
                        data=missing,
                    )
                    for missing in status.json()["missingcriticalupdates"]
                ],
            }
        return {
            "lastholdrecvdate": pendulum.parse(status.json()["lastholdrecvdate"]),
            "list": [
                from_dict(data_class=MissingFixcat, data=missing)
                for missing in status.json()["missingfixcatupdates"]
            ],
        }

    def get_missing_updates_by_uuid(self, uuid: str) -> dict[
        str,
        pendulum.Date
        | pendulum.Time
        | pendulum.DateTime
        | pendulum.Duration
        | list[MissingUpdate]
        | list[MissingFixcat],
    ]:
        """Get missing critical updates for a software instance by UUID.

        Args:
            uuid: UUID of the software instance.

        Returns:
            A dictionary with ``lastholdrecvdate`` (parsed by Pendulum) and
            ``list`` (a list of ``MissingUpdate`` models) keys.

        Raises:
            ZosmfSoftwareInstanceNotFoundError: If the software instance does not exist.
            ZosmfAuthError: If a request returns HTTP 401.
            ZosmfSoftwareManagementRequestError: If a request returns another
                unsuccessful HTTP status.
            httpx2.RequestError: If a request fails before an HTTP response is
                received.
        """
        return self._get_missing_updates_or_fixcat(
            f"/zosmf/swmgmt/swi/{uuid}/missingcriticalupdates", updates=True
        )

    def get_missing_updates_by_name(self, name: str, system: str) -> dict[
        str,
        pendulum.Date
        | pendulum.Time
        | pendulum.DateTime
        | pendulum.Duration
        | list[MissingUpdate]
        | list[MissingFixcat],
    ]:
        """Get missing critical updates for a software instance by name and system.

        Args:
            name: Name of the software instance.
            system: System of the software instance.

        Returns:
            A dictionary with ``lastholdrecvdate`` (parsed by Pendulum) and
            ``list`` (a list of ``MissingUpdate`` models) keys.

        Raises:
            ZosmfSoftwareInstanceNotFoundError: If the software instance does not exist.
            ZosmfAuthError: If a request returns HTTP 401.
            ZosmfSoftwareManagementRequestError: If a request returns another
                unsuccessful HTTP status.
            httpx2.RequestError: If a request fails before an HTTP response is
                received.
        """
        return self._get_missing_updates_or_fixcat(
            f"/zosmf/swmgmt/swi/{system}/{name}/missingcriticalupdates", updates=True
        )

    def get_missing_fixcat_by_uuid(self, uuid: str) -> dict[
        str,
        pendulum.Date
        | pendulum.Time
        | pendulum.DateTime
        | pendulum.Duration
        | list[MissingUpdate]
        | list[MissingFixcat],
    ]:
        """Get updates missing the requested fix categories for an instance by UUID.

        Args:
            uuid: UUID of the software instance.

        Returns:
            A dictionary with ``lastholdrecvdate`` (parsed by Pendulum) and
            ``list`` (a list of ``MissingFixcat`` models) keys.

        Raises:
            ZosmfSoftwareInstanceNotFoundError: If the software instance does not exist.
            ZosmfAuthError: If a request returns HTTP 401.
            ZosmfSoftwareManagementRequestError: If a request returns another
                unsuccessful HTTP status.
            httpx2.RequestError: If a request fails before an HTTP response is
                received.
        """
        return self._get_missing_updates_or_fixcat(
            f"/zosmf/swmgmt/swi/{uuid}/missingfixcatupdates", updates=False
        )

    def get_missing_fixcat_by_name(self, name: str, system: str) -> dict[
        str,
        pendulum.Date
        | pendulum.Time
        | pendulum.DateTime
        | pendulum.Duration
        | list[MissingUpdate]
        | list[MissingFixcat],
    ]:
        """Get updates missing the requested fix categories by name and system.

        Args:
            name: Name of the software instance.
            system: System of the software instance.

        Returns:
            A dictionary with ``lastholdrecvdate`` (parsed by Pendulum) and
            ``list`` (a list of ``MissingFixcat`` models) keys.

        Raises:
            ZosmfSoftwareInstanceNotFoundError: If the software instance does not exist.
            ZosmfAuthError: If a request returns HTTP 401.
            ZosmfSoftwareManagementRequestError: If a request returns another
                unsuccessful HTTP status.
            httpx2.RequestError: If a request fails before an HTTP response is
                received.
        """
        return self._get_missing_updates_or_fixcat(
            f"/zosmf/swmgmt/swi/{system}/{name}/missingfixcatupdates", updates=False
        )

    def _get_sw_updates(self, process_id: int) -> list[dict[str, Any]]:
        path = f"/zosmf/swmgmt/swupdate/{process_id}"
        resp = self.http.get(path)
        self._raise_for_status(resp, exc_handler=ZosmfSoftwareManagementRequestError)
        return resp.json()["update-processes"]

    def search_sw_updates_by_uuid(
        self,
        uuid: str,
        updates: list[str] | None,
        zosmf_userid: str | None = None,
        zosmf_password: str | None = None,
        proxy_userid: str | None = None,
        proxy_password: str | None = None,
    ) -> list[SoftwareUpdate]:
        """Search for software updates in an instance identified by UUID.

        The search is submitted to z/OSMF and polled until it completes.

        Args:
            uuid: UUID of the software instance to search.
            updates: SYSMOD IDs to include in the search.
            zosmf_userid: Optional z/OSMF user ID; currently not applied here.
            zosmf_password: Optional z/OSMF password; currently not applied here.
            proxy_userid: Optional proxy user ID; currently not applied here.
            proxy_password: Optional proxy password; currently not applied here.

        Returns:
            A list of matching ``SoftwareUpdate`` objects.

        Raises:
            ZosmfAuthError: If a request returns HTTP 401.
            ZosmfSoftwareManagementRequestError: If a request returns another
                unsuccessful HTTP status.
            httpx2.RequestError: If a request fails before an HTTP response is
                received.
        """
        return self._search_sw_updates(
            f"/zosmf/swmgmt/swi/{uuid}/softwareupdatesearch", updates
        )

    def search_sw_updates_by_name(
        self,
        name: str,
        system: str,
        updates: list[str] | None,
        zosmf_userid: str | None = None,
        zosmf_password: str | None = None,
        proxy_userid: str | None = None,
        proxy_password: str | None = None,
    ) -> list[SoftwareUpdate]:
        """Search for software updates in an instance identified by name/system.

        The search is submitted to z/OSMF and polled until it completes.

        Args:
            name: Name of the software instance to search.
            system: System where the software instance is defined.
            updates: SYSMOD IDs to include in the search.
            zosmf_userid: Optional z/OSMF user ID; currently not applied here.
            zosmf_password: Optional z/OSMF password; currently not applied here.
            proxy_userid: Optional proxy user ID; currently not applied here.
            proxy_password: Optional proxy password; currently not applied here.

        Returns:
            A list of matching ``SoftwareUpdate`` objects.

        Raises:
            ZosmfAuthError: If a request returns HTTP 401.
            ZosmfSoftwareManagementRequestError: If a request returns another
                unsuccessful HTTP status.
            httpx2.RequestError: If a request fails before an HTTP response is
                received.
        """
        return self._search_sw_updates(
            f"/zosmf/swmgmt/swi/{system}/{name}/softwareupdatesearch", updates
        )

    def _search_sw_updates(
        self,
        path: str,
        updates: list[str] | None,
        zosmf_userid: str | None = None,
        zosmf_password: str | None = None,
        proxy_userid: str | None = None,
        proxy_password: str | None = None,
    ) -> list[SoftwareUpdate]:
        resp = self.http.post(path, json={"updates": updates or None})
        self._raise_for_status(resp, exc_handler=ZosmfSoftwareManagementRequestError)
        status_monitor_url = resp.json()["statusurl"]
        status = self.http.get(status_monitor_url)
        while status.json()["status"] == "running":
            time.sleep(2)
            status = self.http.get(status_monitor_url)
            self._raise_for_status(
                status, exc_handler=ZosmfSoftwareManagementRequestError
            )
        return [
            from_dict(
                data_class=SoftwareUpdate,
                data=sw_upd,
                config=Config(
                    type_hooks={
                        pendulum.DateTime: _parse_datetime,
                    }
                ),
            )
            for sw_upd in status.json().get("updates", [])
        ]

    def _start_sw_update(
        self,
        path: str,
        tgtzone: str,
        updates: list[str],
        sourceids: list[str],
        fixcats: list[str],
        zosmf_auth: tuple[str, ...],
        proxy_auth: tuple[str, ...],
        step: list[str],
        holds: list[str],
        notes: str,
        exclude_updates: list[str],
        wait: bool,
    ) -> int | list[UpdateProcess]:
        if (
            (not updates and not sourceids and not fixcats)
            or (updates and sourceids)
            or (updates and fixcats)
            or (sourceids and fixcats)
        ):
            raise ZosmfSoftwareManagementError(
                "At most one of updates, sourceids, or fixcats must be provided"
            )
        resp = self.http.post(
            path,
            json={
                "targetzone": tgtzone,
                "updates": updates or None,
                "sourceids": sourceids or None,
                "fixcats": fixcats or None,
                "suspend-steps": step,
                "resolve-holds": holds,
                "exclude-updates": exclude_updates,
                "notes": notes,
            },
        )
        self._raise_for_status(resp, exc_handler=ZosmfSoftwareManagementRequestError)
        process_id = int(resp.json()["processid"])
        if not wait:
            return process_id

        upd_processes = self.check_sw_update_status(process_id)
        while any(upd.status == "RUNNING" for upd in upd_processes):
            time.sleep(2)
            upd_processes = self.check_sw_update_status(process_id)
        return upd_processes

    def start_sw_update_by_uuid(
        self,
        uuid: str,
        tgtzone: str,
        updates: list[str] = [],
        sourceids: list[str] = [],
        fixcats: list[str] = [],
        step: list[str] = [],
        holds: list[str] = [],
        notes: str = "",
        exclude_updates: list[str] = [],
        zosmf_auth: tuple[str, ...] = (),
        proxy_auth: tuple[str, ...] = (),
        wait: bool = False,
    ) -> int | list[UpdateProcess]:
        """Start a software update for a software instance identified by its UUID.

        This submits an update operation to the specified target zone and may
        change the software instance. Exactly one of ``updates``, ``sourceids``,
        or ``fixcats`` must be non-empty. When ``wait`` is false, the request
        returns the process ID; when true, the method polls until no process is
        reported as running.

        Args:
            uuid: UUID of the software instance to update.
            tgtzone: Target zone where the update will be applied.
            updates: SYSMOD IDs to select.
            sourceids: Source IDs to select.
            fixcats: Fix categories to select.
            step: Steps to suspend during the update.
            holds: Holds to resolve during the update.
            notes: Notes for the update process.
            exclude_updates: Updates to exclude from the process.
            zosmf_auth: Reserved compatibility argument; currently not applied.
            proxy_auth: Reserved compatibility argument; currently not applied.
            wait: Whether to wait for the update process to finish.

        Returns:
            The process ID if ``wait`` is false, otherwise a list of
            ``UpdateProcess`` records.

        Raises:
            ZosmfSoftwareManagementBaseError: If none or multiple selection
                lists are non-empty.
            ZosmfAuthError: If a request returns HTTP 401.
            ZosmfSoftwareManagementError: If a request returns another
                unsuccessful HTTP status.
            httpx2.RequestError: If a request fails before an HTTP response is
                received.
        """
        return self._start_sw_update(
            f"/zosmf/swmgmt/swi/{uuid}/swupdate",
            tgtzone,
            updates,
            sourceids,
            fixcats,
            step=step,
            holds=holds,
            notes=notes,
            exclude_updates=exclude_updates,
            zosmf_auth=zosmf_auth,
            proxy_auth=proxy_auth,
            wait=wait,
        )

    def start_sw_update_by_name(
        self,
        name: str,
        system: str,
        tgtzone: str,
        updates: list[str] = [],
        sourceids: list[str] = [],
        fixcats: list[str] = [],
        step: list[str] = [],
        holds: list[str] = [],
        notes: str = "",
        exclude_updates: list[str] = [],
        zosmf_auth: tuple[str, ...] = (),
        proxy_auth: tuple[str, ...] = (),
        wait: bool = False,
    ) -> int | list[UpdateProcess]:
        """Start a software update for a software instance identified by its name and system.

        This submits an update operation to the specified target zone and may
        change the software instance. Exactly one of ``updates``, ``sourceids``,
        or ``fixcats`` must be non-empty. When ``wait`` is false, the request
        returns the process ID; when true, the method polls until no process is
        reported as running.

        Args:
            name: Name of the software instance to update.
            system: System of the software instance to update.
            tgtzone: Target zone where the update will be applied.
            updates: SYSMOD IDs to select.
            sourceids: Source IDs to select.
            fixcats: Fix categories to select.
            step: Steps to suspend during the update.
            holds: Holds to resolve during the update.
            notes: Notes for the update process.
            exclude_updates: Updates to exclude from the process.
            zosmf_auth: Reserved compatibility argument; currently not applied.
            proxy_auth: Reserved compatibility argument; currently not applied.
            wait: Whether to wait for the update process to finish.

        Returns:
            The process ID if ``wait`` is false, otherwise a list of
            ``UpdateProcess`` records.

        Raises:
            ZosmfSoftwareManagementBaseError: If none or multiple selection
                lists are non-empty.
            ZosmfAuthError: If a request returns HTTP 401.
            ZosmfSoftwareManagementError: If a request returns another
                unsuccessful HTTP status.
            httpx2.RequestError: If a request fails before an HTTP response is
                received.
        """
        return self._start_sw_update(
            f"/zosmf/swmgmt/swi/{system}/{name}/swupdate",
            tgtzone,
            updates,
            sourceids,
            fixcats,
            step=step,
            holds=holds,
            notes=notes,
            exclude_updates=exclude_updates,
            zosmf_auth=zosmf_auth,
            proxy_auth=proxy_auth,
            wait=wait,
        )

    def _cancel_sw_update(self, path: str) -> int:
        resp = self.http.post(path)
        self._raise_for_status(resp, exc_handler=ZosmfSoftwareManagementError)
        return int(resp.json()["processid"])

    def cancel_sw_update_by_process(self, processid: int) -> int:
        """Request cancellation of an update process by its process ID.

        This method submits the cancellation request and does not wait for the
        process to reach a terminal state.

        Args:
            processid: Process ID of the software update to cancel.
        Returns:
            The process ID returned by z/OSMF for the cancellation request.

        Raises:
            ZosmfAuthError: If z/OSMF returns HTTP 401.
            ZosmfSoftwareManagementError: If z/OSMF returns another
                unsuccessful HTTP status.
            httpx2.RequestError: If the request fails before an HTTP response
                is received.
        """
        return self._cancel_sw_update(f"/zosmf/swmgmt/swupdate/cancel/{processid}")

    def cancel_sw_update_by_uuid(self, uuid: str) -> int:
        """Cancel a software update for a software instance identified by its UUID.

        Cancel the software update identified by the given UUID. While GIMSMP is
        executing, the cancellation request may be not be possible.

        Args:
            uuid: UUID of the software instance to update.

        Returns:
            The process ID.

        Raises:
            ZosmfAuthError: If z/OSMF returns HTTP 401.
            ZosmfSoftwareManagementError: If z/OSMF returns another
                unsuccessful HTTP status.
            httpx2.RequestError: If the request fails before an HTTP response
                is received.
        """
        return self._cancel_sw_update(f"/zosmf/swmgmt/swi/{uuid}/swupdate/cancel")

    def cancel_sw_update_by_name(self, name: str, system: str) -> int:
        """Cancel a software update for a software instance identified by its name and system.

        Cancel the software update identified by the given name and system. While GIMSMP is
        executing, the cancellation request may be not be possible.

        Args:
            name: Name of the software instance to update.
            system: System of the software instance to update.

        Returns:
            The process ID.

        Raises:
            ZosmfAuthError: If z/OSMF returns HTTP 401.
            ZosmfSoftwareManagementError: If z/OSMF returns another
                unsuccessful HTTP status.
            httpx2.RequestError: If the request fails before an HTTP response
                is received.
        """
        return self._cancel_sw_update(
            f"/zosmf/swmgmt/swi/{system}/{name}/swupdate/cancel"
        )

    def _resume_sw_update(
        self,
        path: str,
        steps: list[str],
        holds: list[str],
        notes: str,
        exclude_updates: list[str],
        zosmf_auth: tuple[str, ...],
        proxy_auth: tuple[str, ...],
        wait: bool,
    ) -> int | list[UpdateProcess]:
        resp = self.http.post(
            path,
            json={
                "suspend-steps": steps,
                "resolve-holds": holds,
                "exclude-updates": exclude_updates,
                "notes": notes,
            },
        )
        self._raise_for_status(resp, exc_handler=ZosmfSoftwareManagementError)
        process_id = int(resp.json()["processid"])
        if not wait:
            return process_id

        upd_processes = self.check_sw_update_status(process_id)
        while any(upd.status == "RUNNING" for upd in upd_processes):
            time.sleep(2)
            upd_processes = self.check_sw_update_status(process_id)
        return upd_processes

    def resume_sw_update_by_process(
        self,
        processid: int,
        steps: list[str] = [],
        holds: list[str] = [],
        notes: str = "",
        exclude_updates: list[str] = [],
        zosmf_auth: tuple[str, ...] = (),
        proxy_auth: tuple[str, ...] = (),
        wait: bool = False,
    ) -> int | list[UpdateProcess]:
        """Resume a software update for a software instance identified by process ID.

        Resume the software update identified by the given process ID. When
        ``wait`` is false, return the process ID as soon as z/OSMF accepts the
        request. When true, poll the process until it is no longer running and
        return its update-process records.

        Args:
            processid: Process ID of the software update to resume.
            steps: Steps to suspend during the update.
            holds: Holds to resolve during the update.
            notes: Notes for the update process.
            exclude_updates: Updates to exclude from the process.
            zosmf_auth: Reserved compatibility argument; currently not applied.
            proxy_auth: Reserved compatibility argument; currently not applied.
            wait: Whether to wait for the update process to finish.

        Returns:
            The process ID if ``wait`` is false, otherwise a list of
            ``UpdateProcess`` records.

        Raises:
            ZosmfAuthError: If a request returns HTTP 401.
            ZosmfSoftwareManagementError: If a request returns another
                unsuccessful HTTP status.
            httpx2.RequestError: If a request fails before an HTTP response is
                received.
        """
        return self._resume_sw_update(
            f"/zosmf/swmgmt/swupdate/resume/{processid}",
            steps=steps,
            holds=holds,
            notes=notes,
            exclude_updates=exclude_updates,
            zosmf_auth=zosmf_auth,
            proxy_auth=proxy_auth,
            wait=wait,
        )

    def resume_sw_update_by_uuid(
        self,
        uuid: str,
        steps: list[str] = [],
        holds: list[str] = [],
        notes: str = "",
        exclude_updates: list[str] = [],
        zosmf_auth: tuple[str, ...] = (),
        proxy_auth: tuple[str, ...] = (),
        wait: bool = False,
    ) -> int | list[UpdateProcess]:
        """Resume a software update for a software instance identified by its UUID.

        Resume the software update identified by the given UUID. When ``wait``
        is false, return the process ID as soon as z/OSMF accepts the request.
        When true, poll the process until it is no longer running and return its
        update-process records.

        Args:
            uuid: UUID of the software instance to update.
            steps: Steps to suspend during the update.
            holds: Holds to resolve during the update.
            notes: Notes for the update process.
            exclude_updates: Updates to exclude from the process.
            zosmf_auth: Reserved compatibility argument; currently not applied.
            proxy_auth: Reserved compatibility argument; currently not applied.
            wait: Whether to wait for the update process to finish.

        Returns:
            The process ID if ``wait`` is false, otherwise a list of
            ``UpdateProcess`` records.

        Raises:
            ZosmfAuthError: If a request returns HTTP 401.
            ZosmfSoftwareManagementError: If a request returns another
                unsuccessful HTTP status.
            httpx2.RequestError: If a request fails before an HTTP response is
                received.
        """
        return self._resume_sw_update(
            f"/zosmf/swmgmt/swi/{uuid}/swupdate/resume",
            steps=steps,
            holds=holds,
            notes=notes,
            exclude_updates=exclude_updates,
            zosmf_auth=zosmf_auth,
            proxy_auth=proxy_auth,
            wait=wait,
        )

    def resume_sw_update_by_name(
        self,
        name: str,
        system: str,
        steps: list[str] = [],
        holds: list[str] = [],
        notes: str = "",
        exclude_updates: list[str] = [],
        zosmf_auth: tuple[str, ...] = (),
        proxy_auth: tuple[str, ...] = (),
        wait: bool = False,
    ) -> int | list[UpdateProcess]:
        """Resume a software update for a software instance identified by its name and system.

        Resume the software update identified by the given name and system. When
        ``wait`` is false, return the process ID as soon as z/OSMF accepts the
        request. When true, poll the process until it is no longer running and
        return its update-process records.

        Args:
            name: Name of the software instance to update.
            system: System of the software instance to update.
            steps: Steps to suspend during the update.
            holds: Holds to resolve during the update.
            notes: Notes for the update process.
            exclude_updates: Updates to exclude from the process.
            zosmf_auth: Reserved compatibility argument; currently not applied.
            proxy_auth: Reserved compatibility argument; currently not applied.
            wait: Whether to wait for the update process to finish.

        Returns:
            The process ID if ``wait`` is false, otherwise a list of
            ``UpdateProcess`` records.

        Raises:
            ZosmfAuthError: If a request returns HTTP 401.
            ZosmfSoftwareManagementError: If a request returns another
                unsuccessful HTTP status.
            httpx2.RequestError: If a request fails before an HTTP response is
                received.
        """
        return self._resume_sw_update(
            f"/zosmf/swmgmt/swi/{system}/{name}/swupdate/resume",
            steps=steps,
            holds=holds,
            notes=notes,
            exclude_updates=exclude_updates,
            zosmf_auth=zosmf_auth,
            proxy_auth=proxy_auth,
            wait=wait,
        )

    def check_sw_update_status(self, process_id: int) -> list[UpdateProcess]:
        """Retrieve the latest update-process records for a process ID.

        This method performs one status request; it does not poll while the
        process is running. Use :meth:`get_sw_updates` with ``wait=True`` to
        poll until the process is no longer running.

        Args:
            process_id: ID returned when the update process was started.

        Returns:
            Parsed update-process records returned for this process.

        Raises:
            ZosmfAuthError: If z/OSMF returns HTTP 401.
            ZosmfSoftwareManagementError: If z/OSMF returns another
                unsuccessful HTTP status.
            httpx2.RequestError: If the request fails before an HTTP response
                is received.
        """
        path = f"/zosmf/swmgmt/swupdate/{process_id}"
        resp = self.http.get(path)
        self._raise_for_status(resp, exc_handler=ZosmfSoftwareManagementError)
        return [
            from_dict(
                data_class=UpdateProcess,
                data=process,
                config=Config(
                    type_hooks={
                        pendulum.DateTime: _parse_datetime,
                    },
                    convert_key=lambda k: k.replace("_", "-"),
                ),
            )
            for process in resp.json()["update-processes"]
        ]

    def _copy_output_sw_update(
        self, path: str, output_dir: str
    ) -> list[dict[str, Any]]:
        resp = self.http.put(path, params={"dir": output_dir})
        self._raise_for_status(resp, exc_handler=ZosmfSoftwareManagementError)
        return resp.json()["files"]

    def copy_output_sw_update_by_uuid(
        self, uuid: str, output_dir: str
    ) -> list[dict[str, Any]]:
        """Copy output files for a software instance identified by UUID.

        Args:
            uuid: UUID of the software instance whose update output is copied.
            output_dir: Destination directory on the z/OS UNIX system.

        Returns:
            File metadata returned by z/OSMF; each entry includes the copied
            file's name/path.

        Raises:
            ZosmfAuthError: If z/OSMF returns HTTP 401.
            ZosmfSoftwareManagementError: If z/OSMF returns another
                unsuccessful HTTP status.
            httpx2.RequestError: If the request fails before an HTTP response
                is received.
        """
        return self._copy_output_sw_update(
            f"/zosmf/swmgmt/swi/{uuid}/swupdate", output_dir=output_dir
        )

    def copy_output_sw_update_by_process(
        self, process: int, output_dir: str
    ) -> list[dict[str, Any]]:
        """Copy output files for an update process.

        Args:
            process: ID of the update process whose output is copied.
            output_dir: Destination directory on the z/OS UNIX system.

        Returns:
            File metadata returned by z/OSMF; each entry includes the copied
            file's name/path.

        Raises:
            ZosmfAuthError: If z/OSMF returns HTTP 401.
            ZosmfSoftwareManagementError: If z/OSMF returns another
                unsuccessful HTTP status.
            httpx2.RequestError: If the request fails before an HTTP response
                is received.
        """
        return self._copy_output_sw_update(
            f"/zosmf/swmgmt/swupdate/{process}", output_dir=output_dir
        )

    def copy_output_sw_update_by_name(
        self, name: str, system: str, output_dir: str
    ) -> list[dict[str, Any]]:
        """Copy output files for a software instance identified by name.

        Args:
            name: Name of the software instance.
            system: System where the software instance is defined.
            output_dir: Destination directory on the z/OS UNIX system.

        Returns:
            File metadata returned by z/OSMF; each entry includes the copied
            file's name/path.

        Raises:
            ZosmfAuthError: If z/OSMF returns HTTP 401.
            ZosmfSoftwareManagementError: If z/OSMF returns another
                unsuccessful HTTP status.
            httpx2.RequestError: If the request fails before an HTTP response
                is received.
        """
        return self._copy_output_sw_update(
            f"/zosmf/swmgmt/swi/{system}/{name}/swupdate", output_dir=output_dir
        )
