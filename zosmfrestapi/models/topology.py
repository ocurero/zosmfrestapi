from dataclasses import dataclass, field, fields, is_dataclass
from typing import Any

import pendulum


@dataclass
class System:
    """System record returned by the z/OSMF topology API."""

    name: str = field(metadata={"json_name": "systemName"})
    nickName: str = field(metadata={"json_name": "systemNickName"})
    sysplex: str = field(metadata={"json_name": "sysplexName"})
    groups: str = field(default="", metadata={"json_name": "groupNames"})
    cpcSerial: str = ""
    zosVR: str = ""
    jesType: str = ""
    jesMemberName: str = ""
    httpProxyName: str = ""
    ftpDestinationName: str = ""
    url: str = ""
    cpcName: str = ""


@dataclass
class Group:
    """Group record and the system nicknames that belong to it."""

    name: str
    systems: str = field(metadata={"json_name": "systemNickNames"})
    description: str = ""
