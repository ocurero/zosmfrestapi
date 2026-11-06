import time
from typing import Any, Iterator, Literal, overload

from dacite import from_dict

from zosmfrestapi.exceptions.workflow import (
    ZosmfWorkflowBaseError,
    ZosmfWorkflowError,
)
from zosmfrestapi.models.workflow import (
    WorkflowArchivedListItem,
    WorkflowInstance,
    WorkflowItem,
    WorkflowListItem,
)
from zosmfrestapi.utils import remap, to_dict

from . import ZosmfBase


class WorkflowServices(ZosmfBase):
    """List, inspect, create, and control z/OSMF workflow instances.

    Workflow records are converted to the dataclasses in
    :mod:`zosmfrestapi.models.workflow`. Methods that wait for a workflow return
    an iterator so callers can observe each status update while polling.
    """

    def _get_workflow(
        self, workflow_id: str, steps: bool, variables: bool
    ) -> dict[str, Any]:
        """Fetch the raw workflow response, optionally including steps/variables.

        This internal helper returns the JSON object before model conversion.
        """
        resp = self.http.get(
            f"/zosmf/workflow/rest/1.0/workflows/{workflow_id}",
            params={
                "returnData": (
                    "steps,variables"
                    if all([steps, variables])
                    else "steps" if steps else "variables" if variables else ""
                )
            },
        )
        self._raise_for_status(resp, exc_handler=ZosmfWorkflowError)
        return resp.json()

    def get_workflow(
        self, workflow_id: str, steps: bool = False, variables: bool = False
    ) -> WorkflowInstance:
        """Retrieve one workflow instance by its workflow key.

        Args:
            workflow_id: UUID/key identifying the workflow instance.
            steps: Include detailed workflow step data in the response.
            variables: Include workflow variables in the response.

        Returns:
            The parsed workflow state, including optional step and variable
            data when requested.

        Raises:
            ZosmfAuthError: If z/OSMF returns HTTP 401.
            ZosmfWorkflowError: If z/OSMF returns another unsuccessful HTTP
                status.
            httpx2.RequestError: If the request fails before an HTTP response
                is received.
        """
        return from_dict(
            WorkflowInstance,
            data=remap(
                self._get_workflow(workflow_id, steps=steps, variables=variables),
                WorkflowInstance,
            ),
        )

    def get_workflows(
        self,
        name: str | None = None,
        category: str | None = None,
        system: str | None = None,
        status: str | None = None,
        owner: str | None = None,
        vendor: str | None = None,
    ) -> list[WorkflowListItem]:
        """List workflow instances matching the supplied filters.

        Filters are combined in one z/OSMF request. ``name`` may be a regular
        expression supported by the z/OSMF workflow API.

        Args:
            name: Optional workflow name or supported regular expression.
            category: Optional workflow category.
            system: Optional system nickname.
            status: Optional status. Supported values are ``"in-progress"``,
                ``"complete"``, ``"automation-in-progress"``, and
                ``"canceled"``.
            owner: Optional workflow owner.
            vendor: Optional workflow vendor.

        Returns:
            Parsed workflow list items matching all supplied filters.

        Raises:
            ZosmfWorkflowBaseError: If ``status`` is not one of the supported
                values.
            ZosmfAuthError: If z/OSMF returns HTTP 401.
            ZosmfWorkflowError: If z/OSMF returns another unsuccessful HTTP
                status.
            httpx2.RequestError: If the request fails before an HTTP response
                is received.
        """
        if status and status not in [
            "in-progress",
            "complete",
            "automation-in-progress",
            "canceled",
        ]:
            raise ZosmfWorkflowBaseError(
                f"Invalid status '{status}'. Valid options are: 'in-progress'"
                ", 'complete', 'automation-in-progress', 'canceled'.",
            )
        resp = self.http.get(
            "/zosmf/workflow/rest/1.0/workflows",
            params={
                "workflowName": name,
                "category": category,
                "system": system,
                "statusName": status,
                "owner": owner,
                "vendor": vendor,
            },
        )
        self._raise_for_status(resp, exc_handler=ZosmfWorkflowError)
        return [
            from_dict(
                WorkflowListItem,
                data=remap(workflow, WorkflowListItem),
            )
            for workflow in resp.json()["workflows"]
        ]

    def get_archived_workflows(
        self,
    ) -> list[WorkflowArchivedListItem]:
        """List archived workflow instances.

        Returns:
            Parsed archived workflow list items.

        Raises:
            ZosmfAuthError: If z/OSMF returns HTTP 401.
            ZosmfWorkflowError: If z/OSMF returns another unsuccessful HTTP
                status.
            httpx2.RequestError: If the request fails before an HTTP response
                is received.
        """
        resp = self.http.get("/zosmf/workflow/rest/1.0/archivedworkflows")
        self._raise_for_status(resp, exc_handler=ZosmfWorkflowError)
        return [
            from_dict(
                WorkflowArchivedListItem,
                data=remap(archived_workflow, WorkflowArchivedListItem),
            )
            for archived_workflow in resp.json()["archivedWorkflows"]
        ]

    def create_workflow(self, workflow: WorkflowItem) -> WorkflowInstance:
        """Create a workflow instance from a workflow definition.

        The supplied :class:`WorkflowItem` is serialized to the request body.
        After creation, the method retrieves and returns the new instance using
        the workflow key returned by z/OSMF.

        Args:
            workflow: Definition, system, owner, and optional variables/settings
                used to create the instance.

        Returns:
            The newly created and parsed workflow instance.

        Raises:
            ZosmfAuthError: If z/OSMF returns HTTP 401.
            ZosmfWorkflowError: If creation or retrieval returns another
                unsuccessful HTTP status.
            httpx2.RequestError: If either request fails before an HTTP response
                is received.
        """
        resp = self.http.post(
            "/zosmf/workflow/rest/1.0/workflows", json=to_dict(workflow)
        )
        self._raise_for_status(resp, exc_handler=ZosmfWorkflowError)
        return self.get_workflow(resp.json()["workflowKey"])

    @overload
    def start_workflow(
        self, workflow_id: str, wait: Literal[False] = False
    ) -> Literal[True]: ...

    @overload
    def start_workflow(
        self, workflow_id: str, wait: Literal[True]
    ) -> Iterator[WorkflowInstance]: ...

    @overload
    def start_workflow(
        self, workflow_id: str, wait: bool
    ) -> Literal[True] | Iterator[WorkflowInstance]: ...

    def start_workflow(
        self, workflow_id: str, wait: bool = False
    ) -> Literal[True] | Iterator[WorkflowInstance]:
        """Start a workflow instance.

        When ``wait`` is false, this returns as soon as z/OSMF accepts the
        request. When true, it returns a lazy iterator that polls the workflow
        as the caller consumes it.

        Args:
            workflow_id: UUID of the workflow to start.
            wait: Whether to wait for the workflow to complete.

        Returns:
            ``True`` when ``wait`` is false; otherwise an iterator yielding
            :class:`WorkflowInstance` snapshots until the instance is complete
            or canceled.

        Raises:
            ZosmfAuthError: If z/OSMF returns HTTP 401.
            ZosmfWorkflowError: If the start request or a subsequent poll
                returns another unsuccessful HTTP status.
            httpx2.RequestError: If a request fails before an HTTP response is
                received.
        """
        resp = self.http.put(
            f"/zosmf/workflow/rest/1.0/workflows/{workflow_id}/operations/start",
        )
        self._raise_for_status(resp, exc_handler=ZosmfWorkflowError)
        if not wait:
            return True
        return self.wait_for_workflow(workflow_id)

    def wait_for_workflow(self, workflow_id: str) -> Iterator[WorkflowInstance]:
        """Yield workflow snapshots until the instance reaches a terminal state.

        The workflow is polled every 0.5 seconds. Iteration stops after yielding
        a snapshot whose status is ``"complete"`` or ``"canceled"``.

        Args:
            workflow_id: UUID of the workflow to wait for.

        Returns:
            An iterator of parsed workflow snapshots, including the terminal
            snapshot.

        Raises:
            ZosmfAuthError: If a poll returns HTTP 401.
            ZosmfWorkflowError: If a poll returns another unsuccessful HTTP
                status.
            httpx2.RequestError: If a poll fails before an HTTP response is
                received.
        """
        while True:
            workflow = self.get_workflow(workflow_id)
            yield workflow
            if workflow.status in ("complete", "canceled"):
                break
            time.sleep(0.5)

    def cancel_workflow(self, workflow_id: str) -> None:
        """Request cancellation of a workflow instance.

        Args:
            workflow_id: UUID of the workflow to cancel.

        Returns:
            ``None`` after z/OSMF accepts the cancellation request. This method
            does not wait for cancellation to finish.

        Raises:
            ZosmfAuthError: If z/OSMF returns HTTP 401.
            ZosmfWorkflowError: If z/OSMF returns another unsuccessful HTTP
                status.
            httpx2.RequestError: If the request fails before an HTTP response
                is received.
        """
        resp = self.http.put(
            f"/zosmf/workflow/rest/1.0/workflows/{workflow_id}/operations/cancel",
        )
        self._raise_for_status(resp, exc_handler=ZosmfWorkflowError)

    def archive_workflow(self, workflow_id: str) -> None:
        """Archive a workflow instance.

        Args:
            workflow_id: UUID of the workflow to archive.

        Returns:
            ``None`` after z/OSMF accepts the archive request.

        Raises:
            ZosmfAuthError: If z/OSMF returns HTTP 401.
            ZosmfWorkflowError: If z/OSMF returns another unsuccessful HTTP
                status.
            httpx2.RequestError: If the request fails before an HTTP response
                is received.
        """
        resp = self.http.post(
            f"/zosmf/workflow/rest/1.0/workflows/{workflow_id}/operations/archive",
        )
        self._raise_for_status(resp, exc_handler=ZosmfWorkflowError)

    def remove_workflow(self, workflow_id: str) -> None:
        """Delete an active workflow instance.

        Args:
            workflow_id: Identifier of the workflow to delete.

        Returns:
            ``None`` after z/OSMF accepts the delete request.

        Raises:
            ZosmfAuthError: If z/OSMF returns HTTP 401.
            ZosmfWorkflowError: If z/OSMF returns another unsuccessful HTTP
                status.
            httpx2.RequestError: If the request fails before an HTTP response
                is received.
        """
        resp = self.http.delete(
            f"/zosmf/workflow/rest/1.0/workflows/{workflow_id}",
        )
        self._raise_for_status(resp, exc_handler=ZosmfWorkflowError)

    def remove_archived_workflow(self, workflow_id: str) -> None:
        """Delete an archived workflow instance.

        Args:
            workflow_id: Identifier of the archived workflow to delete.

        Returns:
            ``None`` after z/OSMF accepts the delete request.

        Raises:
            ZosmfAuthError: If z/OSMF returns HTTP 401.
            ZosmfWorkflowError: If z/OSMF returns another unsuccessful HTTP
                status.
            httpx2.RequestError: If the request fails before an HTTP response
                is received.
        """
        resp = self.http.delete(
            f"/zosmf/workflow/rest/1.0/archivedworkflows/{workflow_id}",
        )
        self._raise_for_status(resp, exc_handler=ZosmfWorkflowError)
