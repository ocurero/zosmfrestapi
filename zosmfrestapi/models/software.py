from dataclasses import dataclass, field
from typing import Any

import pendulum


@dataclass
class DataSet:
    """Reference to a data set and, optionally, the volume that contains it."""

    dsname: str | None = None
    volume: str | None = None


@dataclass
class SmpeManagedDatasetZoneDddef:
    """DDDEF names associated with an SMP/E zone."""

    zone: str | None = None
    dddefs: list[str] = field(default_factory=list)


@dataclass
class SmpeManagedDataset:
    """Inventory details for an SMP/E-managed MVS data set."""

    dsname: str | None = None
    volumes: list[str] | None = field(default_factory=list)
    dstype: str | None = None
    recfm: str | None = None
    lrecl: str | None = None
    blksize: str | None = None
    tracks: str | None = None
    used: str | None = None
    extents: str | None = None
    dscategory: list[str] = field(default_factory=list)
    zones: list[str] = field(default_factory=list)
    zonedddefs: list[SmpeManagedDatasetZoneDddef] | None = field(default_factory=list)
    msgs: Any = None


@dataclass
class SmpeManagedUnixDataset:
    """Inventory details for an SMP/E-managed UNIX file-system data set."""

    dsname: str | None = None
    unixdirs: list[str] | None = field(default_factory=list)
    volumes: list[str] | None = field(default_factory=list)
    dstype: str | None = None
    recfm: str | None = None
    lrecl: str | None = None
    blksize: str | None = None
    tracks: str | None = None
    used: str | None = None
    extents: str | None = None
    dscategory: list[str] | None = field(default_factory=list)
    zones: list[str] | None = field(default_factory=list)
    zonedddefs: list[SmpeManagedDatasetZoneDddef] | None = field(default_factory=list)
    msgs: list[str] | None = field(default_factory=list)


@dataclass
class NonSmpeManagedDataset:
    """Inventory details for a data set not managed by SMP/E."""

    dsname: str | None = None
    volumes: list[str] | None = field(default_factory=list)
    dstype: str | None = None
    recfm: str | None = None
    lrecl: str | None = None
    blksize: str | None = None
    tracks: str | None = None
    used: str | None = None
    extents: str | None = None
    dscategory: list[str] | None = field(default_factory=list)
    unixdirs: list[str] | None = field(default_factory=list)
    msgs: list[str] | None = field(default_factory=list)


@dataclass
class CsiSubEntry:
    """Arbitrary values returned for one CSI subentry."""

    values: dict[str, Any]


@dataclass
class CsiEntry:
    """CSI entry identity and its returned subentry values."""

    entryname: str | None = None
    entrytype: str | None = None
    zonename: str | None = None
    subentries: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class Fmid:
    """Function modification identifier and its description/target zones."""

    fmid: str | None = None
    description: str | None = None
    targetzones: list[str] | None = field(default_factory=list)


@dataclass
class Feature:
    """Software product feature and the FMIDs that implement it."""

    feature: str | None = None
    fmids: list[Fmid] = field(default_factory=list)


@dataclass
class Product:
    """SMP/E-managed product metadata and service lifecycle dates."""

    prodname: str | None = None
    productid: str | None = None
    release: str | None = None
    vendor: str | None = None
    generalavailability: pendulum.DateTime | None = None
    endofservice: pendulum.DateTime | None = None
    url: str | None = None
    productinfofileversion: str | None = None
    features: list[Feature] = field(default_factory=list)


@dataclass
class NonSmpeProduct:
    """Product metadata for a product not managed by SMP/E."""

    prodname: str | None = None
    productid: str | None = None
    release: str | None = None
    vendor: str | None = None
    url: str | None = None
    features: list[str] = field(default_factory=list)
    generalavailability: pendulum.DateTime | None = None
    endofservice: pendulum.DateTime | None = None


@dataclass
class WorkflowLocation:
    """Location details for a workflow associated with a software instance."""

    smptype: str | None = None
    smpname: str | None = None
    dsname: str | None = None
    path: str | None = None


@dataclass
class SoftwareInstanceWorkflow:
    """Workflow definition associated with a software instance."""

    name: str | None = None
    description: str | None = None
    location: WorkflowLocation = field(default_factory=WorkflowLocation)
    performonhostsystem: bool | None = None


@dataclass
class DataSetProperty:
    """Property values for a data set DDDEF in a software instance."""

    dddefname: str | None = None
    zone: str | None = None
    dsname: str | None = None
    volume: str | None = None
    dstype: str | None = None
    properties: list[dict[str, str]] = field(default_factory=list)


@dataclass
class DataSetPropertyLabel:
    """Display label associated with a data set property name."""

    propertyname: str | None = None
    label: str | None = None


@dataclass
class ProductProperty:
    """Property values associated with a product and release."""

    prodid: str | None = None
    release: str | None = None
    prodname: str | None = None
    properties: list[dict[str, str]] = field(default_factory=list)


@dataclass
class SoftwareInstance:
    """A z/OSMF software instance and its associated inventory.

    Construction requires either a global zone with at least one target zone,
    or data-set references when no global zone is configured.

    Raises:
        ValueError: If neither a global zone nor data sets are provided, or if
            a global zone is provided without target zones.
    """

    name: str
    system: str
    description: str | None = ""
    uuid: str | None = field(default="", metadata={"json_name": "swiuuid"})
    globalzone: str | None = None
    targetzones: list[str] = field(default_factory=list)
    categories: list[str] = field(default_factory=list)
    productinforetrieved: pendulum.DateTime | None = None
    lastmodified: pendulum.DateTime | None = None
    modifiedby: str | None = None
    created: pendulum.DateTime | None = None
    createdby: str | None = None
    locked: pendulum.DateTime | None = None
    lockedby: str | None = None
    datasets: list[DataSet] = field(default_factory=list)
    products: list[Product] = field(default_factory=list)
    nonsmpeproducts: list[NonSmpeProduct] = field(default_factory=list)
    workflows: list[SoftwareInstanceWorkflow] = field(default_factory=list)
    datasetproperties: list[DataSetProperty] = field(default_factory=list)
    datasetpropertylabels: list[DataSetPropertyLabel] = field(default_factory=list)
    productproperties: list[ProductProperty] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.globalzone and not self.datasets:
            raise ValueError("Either globalzone or datasets must be specified")
        elif self.globalzone and not self.targetzones:
            raise ValueError("Target zones must be specified when globalzone is set")
