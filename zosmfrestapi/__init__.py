"""Synchronous Python client for the z/OSMF REST API.

The package root re-exports :class:`ZosmfClient`, :class:`ZosmfZcryptoClient`,
response models, and public exceptions. Create one client per server/configuration and
use it as a context manager to close the shared HTTP session when finished.
"""

from zosmfrestapi.client import ZosmfClient
from zosmfrestapi.exceptions import ZosmfAuthError, ZosmfError
from zosmfrestapi.exceptions.authentication import ZosmfLoginError
from zosmfrestapi.exceptions.dataset import ZosmfDatasetNotFoundError
from zosmfrestapi.exceptions.software import (
    ZosmfSoftwareInstanceNotFoundError,
    ZosmfSoftwareManagementError,
    ZosmfSoftwareManagementRequestError,
)
from zosmfrestapi.exceptions.workflow import ZosmfWorkflowBaseError, ZosmfWorkflowError
from zosmfrestapi.models.authentication import LoginOk
from zosmfrestapi.models.software import (
    CsiEntry,
    DataSet,
    Feature,
    Fmid,
    NonSmpeManagedDataset,
    Product,
    SmpeManagedDataset,
    SmpeManagedDatasetZoneDddef,
    SmpeManagedUnixDataset,
    SoftwareInstance,
    SoftwareInstanceWorkflow,
    WorkflowLocation,
)
from zosmfrestapi.models.software_updates import (
    MissingFixcat,
    MissingUpdate,
    MissingUpdateResolver,
    SoftwareUpdate,
    SoftwareUpdateZone,
    UpdateErrorResults,
    UpdateProcess,
    UpdateResult,
    UpdateSelection,
)
from zosmfrestapi.models.topology import Group, System
from zosmfrestapi.models.workflow import (
    WorkflowArchivedListItem,
    WorkflowInstance,
    WorkflowItem,
    WorkflowListItem,
)
from zosmfrestapi.zcrypto_client import ZosmfZcryptoClient

__all__ = [
    "ZosmfClient",
    "ZosmfZcryptoClient",
    "LoginOk",
    "ZosmfDatasetNotFoundError",
    "ZosmfError",
    "ZosmfAuthError",
    "ZosmfLoginError",
    "System",
    "Group",
    "CsiEntry",
    "DataSet",
    "Feature",
    "Fmid",
    "NonSmpeManagedDataset",
    "Product",
    "SmpeManagedDataset",
    "SmpeManagedDatasetZoneDddef",
    "SmpeManagedUnixDataset",
    "SoftwareInstance",
    "SoftwareInstanceWorkflow",
    "WorkflowLocation",
    "ZosmfSoftwareManagementError",
    "ZosmfSoftwareInstanceNotFoundError",
    "ZosmfSoftwareManagementRequestError",
    "MissingFixcat",
    "MissingUpdate",
    "MissingUpdateResolver",
    "SoftwareUpdate",
    "SoftwareUpdateZone",
    "UpdateErrorResults",
    "UpdateProcess",
    "UpdateResult",
    "UpdateSelection",
    "WorkflowArchivedListItem",
    "WorkflowInstance",
    "WorkflowItem",
    "WorkflowListItem",
    "ZosmfWorkflowBaseError",
    "ZosmfWorkflowError",
]
