from dataclasses import dataclass, field, fields, is_dataclass
from typing import Any

import pendulum


@dataclass
class WorkflowAutomationStatus:
    """Automation progress and current-step details for a workflow."""

    startUser: str | None = None
    startedTime: int | str | None = None
    stoppedTime: int | str | None = None
    currentStepName: str | None = None
    currentStepNumber: str | None = None
    currentStepTitle: str | None = None
    messageID: str | None = None
    messageText: str | None = None


@dataclass
class WorkflowInstance:
    """Current state and optional detailed data for a workflow instance."""

    name: str = field(metadata={"json_name": "workflowName"})
    owner: str
    system: str
    scope: str = ""
    percentComplete: int | None = None
    workflowDefinitionFileMD5Value: str | None = None
    workflowArchiveSAFID: str | None = None
    jobStatement: str | list[str] | None = None
    globalVariableGroup: str | None = None
    jobsOutputDirectory: str | None = None
    status: str | None = field(default="", metadata={"json_name": "statusName"})
    vendor: str | None = None
    deleteCompletedJobs: bool | None = None
    autoDeleteOnCompletion: bool | None = None
    isInstanceVariableWithoutPrefix: bool | None = None
    workflowVersion: str | None = None
    steps: list[dict[str, Any]] = field(default_factory=list)
    access: str | None = None
    productVersion: str | None = None
    productID: str | None = None
    variables: list[dict[str, Any]] = field(default_factory=list)
    category: str | None = None
    workflowDescription: str | None = None
    workflowID: str | None = None
    accountInfo: str | None = None
    automationStatus: WorkflowAutomationStatus | None = None
    containsParallelSteps: bool | None = None
    isCallable: bool | None = None
    workflowKey: str | None = None
    productName: str | None = None


@dataclass
class WorkflowListItem:
    """Summary record returned when listing active workflow instances."""

    instanceURI: str | None = None
    owner: str | None = None
    vendor: str | None = None
    workflowDefinitionFileMD5Value: str | None = None
    workflowDescription: str | None = None
    workflowID: str | None = None
    workflowKey: str | None = None
    workflowName: str | None = None
    workflowVersion: str | None = None


@dataclass
class WorkflowArchivedListItem:
    """Summary record returned when listing archived workflow instances."""

    archivedInstanceURI: str | None = None
    workflowKey: str | None = None
    workflowName: str | None = None


@dataclass
class WorkflowVariableItem:
    """Name and value of a workflow input variable."""

    name: str | None = None
    value: str | None = None


@dataclass
class WorkflowItem:
    """Request data used to create a z/OSMF workflow instance."""

    name: str = field(metadata={"json_name": "workflowName"})
    definition: str = field(metadata={"json_name": "workflowDefinitionFile"})
    system: str
    owner: str
    system_definition: str | None = field(
        default=None,
        metadata={
            "json_name": "workflowDefinitionFileSystem",
        },
    )
    variableInputFile: str | None = None
    variables: list[WorkflowVariableItem] = field(default_factory=list)
    resolveGlobalConflictByUsing: str | None = None
    workflowArchiveSAFID: str | None = None
    comments: str | None = None
    assignToOwner: bool | None = None
    accessType: str | None = None
    accountInfo: str | None = None
    jobStatement: str | list[str] | None = None
    deleteCompletedJobs: bool | None = None
    autoDeleteOnCompletion: bool | None = None
    jobsOutputDirectory: str | None = None
    targetSystemuid: str | None = None
    targetSystempwd: str | None = field(default=None, repr=False)
