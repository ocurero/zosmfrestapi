from dataclasses import dataclass, field

import pendulum


@dataclass
class UpdateSelection:
    """SYSMOD updates selected for a software-update process."""

    updates: list[str] = field(default_factory=list)


@dataclass
class UpdateResult:
    """Selection and application result for one update in a process."""

    fmid: str | None = None
    selectStatus: str | None = field(default=None)
    name: str | None = None


@dataclass
class UpdateErrorResults:
    """SMP/E return code and messages associated with a failed update."""

    smpe_rc: int
    message: str
    detailedMessage: str


@dataclass
class UpdateProcess:
    """Status, selection, timing, and results for a software-update process."""

    targetzone: str
    selection: UpdateSelection
    notes: str
    processid: int
    started: pendulum.DateTime
    status: str
    step: str
    lastmodified: pendulum.DateTime | None = None
    completed: pendulum.DateTime | None = None
    error_results: UpdateErrorResults | None = None
    updates: list[UpdateResult] = field(default_factory=list)
    holds: list[str] = field(default_factory=list)


@dataclass
class SoftwareUpdateZone:
    """Installation status of a software update in one zone."""

    zone: str
    status: str
    installed: pendulum.DateTime | None


@dataclass
class SoftwareUpdate:
    """Software-update metadata and its status across zones."""

    name: str | None = None
    type: str | None = None
    fmid: str | None = None
    zones: list[SoftwareUpdateZone] = field(default_factory=list)


@dataclass
class MissingUpdateResolver:
    """Update that can resolve a hold on a missing update."""

    name: str | None = None
    received: bool | None = None


@dataclass
class MissingUpdate:
    """Critical missing update, its hold details, and resolving updates."""

    name: str | None = None
    holdclass: str | None = None
    holdsymptom: str | None = None
    heldsysmod: str | None = None
    fmid: str | None = None
    fmiddesc: str | None = None
    resolvers: list[MissingUpdateResolver] | None = field(default_factory=list)
    tgtzones: list[str] = field(default_factory=list)


@dataclass
class MissingFixcat:
    """Fix category missing from an instance and its resolving updates."""

    name: str | None = None
    fixcats: list[str] = field(default_factory=list)
    fmid: str | None = None
    fmiddesc: str | None = None
    resolvers: list[MissingUpdateResolver] | None = field(default_factory=list)
    tgtzones: list[str] = field(default_factory=list)
