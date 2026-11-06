import uuid

import pytest

from tests.helpers import pdt
from zosmfrestapi.services import software
from zosmfrestapi import (
    CsiEntry,
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
    ZosmfClient,
    ZosmfSoftwareManagementError,
    ZosmfSoftwareInstanceNotFoundError,
    ZosmfSoftwareManagementRequestError,
)


@pytest.mark.vcr
def test_list_swis():
    with ZosmfClient("https://zosmf.example") as client:
        assert client.list_swis() == [
            SoftwareInstance(
                name="HOOLIE",
                system="TSTA",
                description="Product A",
                globalzone="OSHOOLI.GLOBAL.CSI",
                targetzones=["TGT"],
                categories=["FOO"],
                productinforetrieved=pdt("2026-10-22T16:13:00Z"),
                lastmodified=pdt("2026-10-02T10:35:38Z"),
                modifiedby="FOOBAR",
                created=pdt("2026-10-02T10:35:38Z"),
                createdby="FOOO",
                locked=None,
                lockedby=None,
                uuid="c66bb092-cf92-4db9-96fd-2073e3b826ae",
            ),
            SoftwareInstance(
                name="HOOLIE",
                system="TSTB",
                description="Product A",
                globalzone="OSHOOLI.GLOBAL.CSI",
                targetzones=["TGT"],
                categories=["FOO"],
                productinforetrieved=pdt("2026-10-22T16:13:00Z"),
                lastmodified=pdt("2026-10-02T10:35:38Z"),
                modifiedby="FOOBAR",
                created=pdt("2026-10-02T10:35:38Z"),
                createdby="FOOO",
                locked=None,
                lockedby=None,
                uuid="dabf0e67-cb96-43a5-abba-b47caa91a61d",
            ),
        ]


@pytest.mark.vcr
def test_get_swi_by_uuid(monkeypatch):
    with ZosmfClient("https://zosmf.example") as client:
        assert client.get_swi_by_uuid(
            "c66bb092-cf92-4db9-96fd-2073e3b826ae"
        ) == SoftwareInstance(
            name="HOOLIE",
            system="TSTA",
            description="Product A",
            globalzone="OSHOOLI.GLOBAL.CSI",
            targetzones=["TGT"],
            categories=["FOO"],
            productinforetrieved=pdt("2026-10-22T16:13:00Z"),
            products=[
                Product(
                    prodname="The Box III, Gavin Belson Signature Edition",
                    productid="1122-345",
                    release="01.03.00",
                    vendor="Hooli Software",
                    url="http://hooli.xyz",
                    features=[
                        Feature(
                            feature="The Box III, Middle Out Compression",
                            fmids=[
                                Fmid(
                                    fmid="HOOMOC3",
                                    description="The Box III, Middle Out Compression",
                                    targetzones=[
                                        "TGT",
                                    ],
                                ),
                            ],
                        ),
                    ],
                )
            ],
            workflows=[
                SoftwareInstanceWorkflow(
                    name="About your order",
                    description="Information about your ServerPac order.",
                    location=WorkflowLocation(
                        smptype=None,
                        smpname=None,
                        dsname="OSHOOLI.WORKFLOW(HOOLWELC)",
                        path=None,
                    ),
                    performonhostsystem=True,
                ),
                SoftwareInstanceWorkflow(
                    name="Configuration",
                    description="Configure the software in your ServerPac order.",
                    location=WorkflowLocation(
                        smptype=None,
                        smpname=None,
                        dsname="OSHOOLI.WORKFLOW(HOOLSETU)",
                        path=None,
                    ),
                    performonhostsystem=True,
                ),
                SoftwareInstanceWorkflow(
                    name="Verify_1",
                    description="Installation verification for your ServerPac order.",
                    location=WorkflowLocation(
                        smptype=None,
                        smpname=None,
                        dsname="OSHOOLI.WORKFLOW(HOOLIVP)",
                        path=None,
                    ),
                    performonhostsystem=True,
                ),
            ],
            lastmodified=pdt("2026-10-02T10:35:38Z"),
            modifiedby="FOOBAR",
            created=pdt("2026-10-02T10:35:38Z"),
            createdby="FOOO",
            locked=None,
            lockedby=None,
            uuid="c66bb092-cf92-4db9-96fd-2073e3b826ae",
        )


@pytest.mark.vcr
def test_get_swi_by_name():
    with ZosmfClient("https://zosmf.example") as client:
        assert client.get_swi_by_name("HOOLIE", "TSTA") == SoftwareInstance(
            name="HOOLIE",
            system="TSTA",
            description="Product A",
            globalzone="OSHOOLI.GLOBAL.CSI",
            targetzones=["TGT"],
            categories=["FOO"],
            productinforetrieved=pdt("2026-10-22T16:13:00Z"),
            products=[
                Product(
                    prodname="The Box III, Gavin Belson Signature Edition",
                    productid="1122-345",
                    release="01.03.00",
                    vendor="Hooli Software",
                    url="http://hooli.xyz",
                    features=[
                        Feature(
                            feature="The Box III, Middle Out Compression",
                            fmids=[
                                Fmid(
                                    fmid="HOOMOC3",
                                    description="The Box III, Middle Out Compression",
                                    targetzones=[
                                        "TGT",
                                    ],
                                ),
                            ],
                        ),
                    ],
                )
            ],
            workflows=[
                SoftwareInstanceWorkflow(
                    name="About your order",
                    description="Information about your ServerPac order.",
                    location=WorkflowLocation(
                        smptype=None,
                        smpname=None,
                        dsname="OSHOOLI.WORKFLOW(HOOLWELC)",
                        path=None,
                    ),
                    performonhostsystem=True,
                ),
                SoftwareInstanceWorkflow(
                    name="Configuration",
                    description="Configure the software in your ServerPac order.",
                    location=WorkflowLocation(
                        smptype=None,
                        smpname=None,
                        dsname="OSHOOLI.WORKFLOW(HOOLSETU)",
                        path=None,
                    ),
                    performonhostsystem=True,
                ),
                SoftwareInstanceWorkflow(
                    name="Verify_1",
                    description="Installation verification for your ServerPac order.",
                    location=WorkflowLocation(
                        smptype=None,
                        smpname=None,
                        dsname="OSHOOLI.WORKFLOW(HOOLIVP)",
                        path=None,
                    ),
                    performonhostsystem=True,
                ),
            ],
            lastmodified=pdt("2026-10-02T10:35:38Z"),
            modifiedby="FOOBAR",
            created=pdt("2026-10-02T10:35:38Z"),
            createdby="FOOO",
            locked=None,
            lockedby=None,
            uuid="c66bb092-cf92-4db9-96fd-2073e3b826ae",
        )


@pytest.mark.vcr
def test_get_swi_raises_ZosmfSoftwareInstanceNotFoundError():
    with ZosmfClient("https://zosmf.example") as client:
        with pytest.raises(ZosmfSoftwareInstanceNotFoundError):
            client.get_swi_by_uuid("000000-0000000-000000-0000-00000")


@pytest.mark.vcr
def test_get_swi_datasets_by_uuid(monkeypatch):
    with ZosmfClient("https://zosmf.example") as client:
        monkeypatch.setattr(software.time, "sleep", lambda *_: None)

        assert client.get_swi_datasets_by_uuid(
            "c66bb092-cf92-4db9-96fd-2073e3b826ae"
        ) == {
            "smpemanageddatasets": [
                SmpeManagedDataset(
                    dsname="OSHOOLI.AHOOLBIN",
                    volumes=["FOOVOL"],
                    dstype="PDS",
                    recfm="FB",
                    lrecl="80",
                    blksize="27920",
                    tracks="1",
                    used="100",
                    extents="1",
                    dscategory=["DLIB"],
                    zones=["DLIB"],
                    zonedddefs=[
                        SmpeManagedDatasetZoneDddef(zone="DLIB", dddefs=["AHOOLBIN"])
                    ],
                    msgs=None,
                ),
                SmpeManagedDataset(
                    dsname="OSHOOLI.AHOOLMOD",
                    volumes=["FOOVOL"],
                    dstype="PDS",
                    recfm="U",
                    lrecl="0",
                    blksize="32760",
                    tracks="1",
                    used="100",
                    extents="1",
                    dscategory=["DLIB"],
                    zones=["DLIB"],
                    zonedddefs=[
                        SmpeManagedDatasetZoneDddef(zone="DLIB", dddefs=["AHOOLMOD"])
                    ],
                    msgs=None,
                ),
                SmpeManagedDataset(
                    dsname="OSHOOLI.GLOBAL.CSI",
                    volumes=["FOOVOL"],
                    dstype="VSAM",
                    recfm=None,
                    lrecl=None,
                    blksize=None,
                    tracks="2",
                    used=None,
                    extents=None,
                    dscategory=["SMP/E", "DLIB", "TARGET", "GLOBAL"],
                    zones=["GLOBAL", "TGT", "DLIB"],
                    zonedddefs=None,
                    msgs=None,
                ),
                SmpeManagedDataset(
                    dsname="OSHOOLI.SHOOLMOD",
                    volumes=["FOOVOL"],
                    dstype="PDS",
                    recfm="U",
                    lrecl="0",
                    blksize="32760",
                    tracks="1",
                    used="100",
                    extents="1",
                    dscategory=["TARGET"],
                    zones=["TGT"],
                    zonedddefs=[
                        SmpeManagedDatasetZoneDddef(zone="TGT", dddefs=["SHOOLMOD"])
                    ],
                    msgs=None,
                ),
                SmpeManagedDataset(
                    dsname="OSHOOLI.SMPLOG",
                    volumes=["FOOVOL"],
                    dstype="SEQ",
                    recfm="VB",
                    lrecl="512",
                    blksize="5120",
                    tracks="1",
                    used="100",
                    extents="1",
                    dscategory=["SMP/E", "DLIB", "TARGET", "GLOBAL"],
                    zones=["DLIB", "GLOBAL", "TGT"],
                    zonedddefs=[
                        SmpeManagedDatasetZoneDddef(zone="DLIB", dddefs=["SMPLOG"]),
                        SmpeManagedDatasetZoneDddef(zone="GLOBAL", dddefs=["SMPLOG"]),
                        SmpeManagedDatasetZoneDddef(zone="TGT", dddefs=["SMPLOG"]),
                    ],
                    msgs=None,
                ),
                SmpeManagedDataset(
                    dsname="OSHOOLI.SMPPTS",
                    volumes=["FOOVOL"],
                    dstype="PDS",
                    recfm="FB",
                    lrecl="80",
                    blksize="27920",
                    tracks="1",
                    used="100",
                    extents="1",
                    dscategory=["SMP/E", "DLIB", "TARGET", "GLOBAL"],
                    zones=["DLIB", "GLOBAL", "TGT"],
                    zonedddefs=[
                        SmpeManagedDatasetZoneDddef(zone="DLIB", dddefs=["SMPPTS"]),
                        SmpeManagedDatasetZoneDddef(zone="GLOBAL", dddefs=["SMPPTS"]),
                        SmpeManagedDatasetZoneDddef(zone="TGT", dddefs=["SMPPTS"]),
                    ],
                    msgs=None,
                ),
                SmpeManagedDataset(
                    dsname="OSHOOLI.SMPSCDS",
                    volumes=["FOOVOL"],
                    dstype="PDS",
                    recfm="FB",
                    lrecl="80",
                    blksize="27920",
                    tracks="1",
                    used="100",
                    extents="1",
                    dscategory=["SMP/E", "TARGET"],
                    zones=["TGT"],
                    zonedddefs=[
                        SmpeManagedDatasetZoneDddef(zone="TGT", dddefs=["SMPSCDS"])
                    ],
                    msgs=None,
                ),
            ],
            "smpemanagedunixdatasets": [
                SmpeManagedUnixDataset(
                    dsname="OSHOOLI.ZFS",
                    unixdirs=["/u/FOO/hooli/usr/lpp/hooli/"],
                    volumes=["FOOVOL"],
                    dstype="ZFS",
                    recfm=None,
                    lrecl=None,
                    blksize=None,
                    tracks="15",
                    used=None,
                    extents=None,
                    dscategory=["TARGET"],
                    zones=["TGT"],
                    zonedddefs=[
                        SmpeManagedDatasetZoneDddef(zone="TGT", dddefs=["SHOOLDIR"])
                    ],
                    msgs=None,
                )
            ],
            "nonsmpemanageddatasets": [
                NonSmpeManagedDataset(
                    dsname="OSHOOLI.WORKFLOW",
                    volumes=["FOOVOL"],
                    dstype="PDSE",
                    recfm="VB",
                    lrecl="256",
                    blksize="32760",
                    tracks="1",
                    used="100",
                    extents="1",
                    dscategory=["WORKFLOW"],
                    unixdirs=None,
                    msgs=None,
                )
            ],
        }


@pytest.mark.vcr
def test_get_swi_datasets_by_name(monkeypatch):
    with ZosmfClient("https://zosmf.example") as client:
        monkeypatch.setattr(software.time, "sleep", lambda *_: None)
        assert client.get_swi_datasets_by_name("HOOLIE", "TSTA") == {
            "smpemanageddatasets": [
                SmpeManagedDataset(
                    dsname="OSHOOLI.AHOOLBIN",
                    volumes=["FOOVOL"],
                    dstype="PDS",
                    recfm="FB",
                    lrecl="80",
                    blksize="27920",
                    tracks="1",
                    used="100",
                    extents="1",
                    dscategory=["DLIB"],
                    zones=["DLIB"],
                    zonedddefs=[
                        SmpeManagedDatasetZoneDddef(zone="DLIB", dddefs=["AHOOLBIN"])
                    ],
                    msgs=None,
                ),
                SmpeManagedDataset(
                    dsname="OSHOOLI.AHOOLMOD",
                    volumes=["FOOVOL"],
                    dstype="PDS",
                    recfm="U",
                    lrecl="0",
                    blksize="32760",
                    tracks="1",
                    used="100",
                    extents="1",
                    dscategory=["DLIB"],
                    zones=["DLIB"],
                    zonedddefs=[
                        SmpeManagedDatasetZoneDddef(zone="DLIB", dddefs=["AHOOLMOD"])
                    ],
                    msgs=None,
                ),
                SmpeManagedDataset(
                    dsname="OSHOOLI.GLOBAL.CSI",
                    volumes=["FOOVOL"],
                    dstype="VSAM",
                    recfm=None,
                    lrecl=None,
                    blksize=None,
                    tracks="2",
                    used=None,
                    extents=None,
                    dscategory=["SMP/E", "DLIB", "TARGET", "GLOBAL"],
                    zones=["GLOBAL", "TGT", "DLIB"],
                    zonedddefs=None,
                    msgs=None,
                ),
                SmpeManagedDataset(
                    dsname="OSHOOLI.SHOOLMOD",
                    volumes=["FOOVOL"],
                    dstype="PDS",
                    recfm="U",
                    lrecl="0",
                    blksize="32760",
                    tracks="1",
                    used="100",
                    extents="1",
                    dscategory=["TARGET"],
                    zones=["TGT"],
                    zonedddefs=[
                        SmpeManagedDatasetZoneDddef(zone="TGT", dddefs=["SHOOLMOD"])
                    ],
                    msgs=None,
                ),
                SmpeManagedDataset(
                    dsname="OSHOOLI.SMPLOG",
                    volumes=["FOOVOL"],
                    dstype="SEQ",
                    recfm="VB",
                    lrecl="512",
                    blksize="5120",
                    tracks="1",
                    used="100",
                    extents="1",
                    dscategory=["SMP/E", "DLIB", "TARGET", "GLOBAL"],
                    zones=["DLIB", "GLOBAL", "TGT"],
                    zonedddefs=[
                        SmpeManagedDatasetZoneDddef(zone="DLIB", dddefs=["SMPLOG"]),
                        SmpeManagedDatasetZoneDddef(zone="GLOBAL", dddefs=["SMPLOG"]),
                        SmpeManagedDatasetZoneDddef(zone="TGT", dddefs=["SMPLOG"]),
                    ],
                    msgs=None,
                ),
                SmpeManagedDataset(
                    dsname="OSHOOLI.SMPPTS",
                    volumes=["FOOVOL"],
                    dstype="PDS",
                    recfm="FB",
                    lrecl="80",
                    blksize="27920",
                    tracks="1",
                    used="100",
                    extents="1",
                    dscategory=["SMP/E", "DLIB", "TARGET", "GLOBAL"],
                    zones=["DLIB", "GLOBAL", "TGT"],
                    zonedddefs=[
                        SmpeManagedDatasetZoneDddef(zone="DLIB", dddefs=["SMPPTS"]),
                        SmpeManagedDatasetZoneDddef(zone="GLOBAL", dddefs=["SMPPTS"]),
                        SmpeManagedDatasetZoneDddef(zone="TGT", dddefs=["SMPPTS"]),
                    ],
                    msgs=None,
                ),
                SmpeManagedDataset(
                    dsname="OSHOOLI.SMPSCDS",
                    volumes=["FOOVOL"],
                    dstype="PDS",
                    recfm="FB",
                    lrecl="80",
                    blksize="27920",
                    tracks="1",
                    used="100",
                    extents="1",
                    dscategory=["SMP/E", "TARGET"],
                    zones=["TGT"],
                    zonedddefs=[
                        SmpeManagedDatasetZoneDddef(zone="TGT", dddefs=["SMPSCDS"])
                    ],
                    msgs=None,
                ),
            ],
            "smpemanagedunixdatasets": [
                SmpeManagedUnixDataset(
                    dsname="OSHOOLI.ZFS",
                    unixdirs=["/u/FOO/hooli/usr/lpp/hooli/"],
                    volumes=["FOOVOL"],
                    dstype="ZFS",
                    recfm=None,
                    lrecl=None,
                    blksize=None,
                    tracks="15",
                    used=None,
                    extents=None,
                    dscategory=["TARGET"],
                    zones=["TGT"],
                    zonedddefs=[
                        SmpeManagedDatasetZoneDddef(zone="TGT", dddefs=["SHOOLDIR"])
                    ],
                    msgs=None,
                )
            ],
            "nonsmpemanageddatasets": [
                NonSmpeManagedDataset(
                    dsname="OSHOOLI.WORKFLOW",
                    volumes=["FOOVOL"],
                    dstype="PDSE",
                    recfm="VB",
                    lrecl="256",
                    blksize="32760",
                    tracks="1",
                    used="100",
                    extents="1",
                    dscategory=["WORKFLOW"],
                    unixdirs=None,
                    msgs=None,
                )
            ],
        }


@pytest.mark.vcr
def test_get_swi_datasets_by_name_raises_ZosmfSoftwareInstanceNotFoundError():
    with ZosmfClient("https://zosmf.example") as client:
        with pytest.raises(ZosmfSoftwareInstanceNotFoundError):
            client.get_swi_datasets_by_name("HOOLIE", "TSTC")


@pytest.mark.vcr
def test_get_swi_datasets_by_name_raises_ZosmfSoftwareInstanceNotFoundError_str():
    with ZosmfClient("https://zosmf.example") as client:
        try:
            client.get_swi_datasets_by_name("HOOLIE", "TSTC")
        except ZosmfSoftwareInstanceNotFoundError as e:
            assert str(e) == (
                'A software instance with the name "HOOLIE" on system "TSTC" '
                "does not exist.  Specify an existing software instance and retry the request."
            )


@pytest.mark.vcr
def test_add_simple_swi():
    with ZosmfClient("https://zosmf.example") as client:
        client.add_swi(
            SoftwareInstance(
                name="HOOLIE2",
                system="TSTA",
                globalzone="OSHOOLI.GLOBAL.CSI",
                targetzones=["TGT"],
            )
        )


@pytest.mark.vcr
def test_add_product_swi():
    with ZosmfClient("https://zosmf.example") as client:
        client.add_swi(
            SoftwareInstance(
                name="HOOLIE2",
                system="TSTA",
                globalzone="OSHOOLI.GLOBAL.CSI",
                targetzones=["TGT"],
                products=[
                    Product(
                        prodname="The Box III, Gavin Belson Signature Edition",
                        productid="1122-345",
                        release="01.03.00",
                        vendor="Hooli Software",
                        url="http://hooli.xyz",
                        features=[
                            Feature(
                                feature="The Box III, Middle Out Compression",
                                fmids=[
                                    Fmid(
                                        fmid="HOOMOC3",
                                        description="The Box III, Middle Out Compression",
                                        targetzones=[
                                            "TGT",
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    )
                ],
            )
        )


@pytest.mark.vcr
def test_add_workflow_swi():
    with ZosmfClient("https://zosmf.example") as client:
        client.add_swi(
            SoftwareInstance(
                name="HOOLIE2",
                system="TSTA",
                globalzone="OSHOOLI.GLOBAL.CSI",
                targetzones=["TGT"],
                workflows=[
                    SoftwareInstanceWorkflow(
                        name="About your order",
                        description="Information about your ServerPac order.",
                        location=WorkflowLocation(
                            smptype=None,
                            smpname=None,
                            dsname="OSHOOLI.WORKFLOW(HOOLWELC)",
                            path=None,
                        ),
                        performonhostsystem=True,
                    )
                ],
            )
        )


@pytest.mark.vcr
def test_add_swi_globalzone_no_targetzones():
    with ZosmfClient("https://zosmf.example") as client:
        with pytest.raises(
            ValueError, match="Target zones must be specified when globalzone is set"
        ):
            client.add_swi(
                SoftwareInstance(
                    name="HOOLIE", system="TSTB", globalzone="OSHOOLI.GLOBAL.CSI"
                )
            )


@pytest.mark.vcr
def test_add_swi_no_globalzone_or_datasets():
    with ZosmfClient("https://zosmf.example") as client:
        with pytest.raises(
            ValueError, match="Either globalzone or datasets must be specified"
        ):
            client.add_swi(SoftwareInstance(name="HOOLIE", system="TSTB"))


@pytest.mark.vcr
def test_remove_swi_by_uuid():
    with ZosmfClient("https://zosmf.example") as client:
        client.remove_sw_instance_by_uuid("ab7a70d9-02bf-4a70-9623-961d014bdec1")


@pytest.mark.vcr
def test_remove_swi_by_name():
    with ZosmfClient("https://zosmf.example") as client:
        client.remove_sw_instance_by_name(system="TSTB", name="HOOLIE2")


@pytest.mark.vcr
def test_remove_swi_by_name_raises_ZosmfSoftwareInstanceNotFoundError():
    with ZosmfClient("https://zosmf.example") as client:
        with pytest.raises(ZosmfSoftwareInstanceNotFoundError):
            client.remove_sw_instance_by_name(system="TSTC", name="HOOLIE2")


@pytest.mark.vcr
def test_query_csi_nowait():
    with ZosmfClient("https://zosmf.example") as client:
        assert client.query_csi_by_uuid(
            uuid="ab7a70d9-02bf-4a70-9623-961d014bdec1",
            zones=["GLOBAL"],
            entries=["SYSMOD"],
            filter="ENAME='HL00006'",
            wait=False,
        ) == {
            "statusurl": "https://zosmf.example/zosmf/swmgmt/statusmonitor/csiquery/1793101874908"
        }


@pytest.mark.vcr
def test_query_csi_by_uuid(monkeypatch):
    with ZosmfClient("https://zosmf.example") as client:
        monkeypatch.setattr(software.time, "sleep", lambda *_: None)
        assert client.query_csi_by_uuid(
            uuid="ab7a70d9-02bf-4a70-9623-961d014bdec1",
            zones=["GLOBAL"],
            entries=["SYSMOD"],
            filter="ENAME='HL00006'",
        ) == [
            CsiEntry(
                entryname="HL00006",
                entrytype="SYSMOD",
                zonename="GLOBAL",
                subentries=[
                    {
                        "BYPASS": [
                            "NO",
                        ],
                        "VER": None,
                    },
                    {
                        "DELLMOD": [
                            "NO",
                        ],
                        "VER": None,
                    },
                    {
                        "ELEMMOV": [
                            "NO",
                        ],
                        "VER": None,
                    },
                    {
                        "ERROR": [
                            "NO",
                        ],
                        "VER": None,
                    },
                    {
                        "FMID": [
                            "HOOMOC3",
                        ],
                        "VER": "1",
                    },
                    {
                        "SREL": [
                            "Z038",
                        ],
                        "VER": "1",
                    },
                    {
                        "SUPING": [
                            "HL00001",
                            "HL00002",
                            "HL00003",
                            "HL00004",
                            "HL00005",
                        ],
                        "VER": "1",
                    },
                    {
                        "HFS": [
                            "HOOLMOC",
                        ],
                        "VER": None,
                    },
                    {
                        "HOLDDATA": [
                            "SYSTEM(INT),DOC,HL00006",
                        ],
                        "VER": None,
                    },
                    {
                        "JCLIN": [
                            "NO",
                        ],
                        "VER": None,
                    },
                    {
                        "PROGRAM": [
                            "HOOLMOC",
                        ],
                        "VER": None,
                    },
                    {
                        "RECDATE": [
                            "20304",
                        ],
                        "VER": None,
                    },
                    {
                        "RECTIME": [
                            "13:44:10",
                        ],
                        "VER": None,
                    },
                    {
                        "REGEN": [
                            "NO",
                        ],
                        "VER": None,
                    },
                    {
                        "RENLMOD": [
                            "NO",
                        ],
                        "VER": None,
                    },
                    {
                        "RESTORE": [
                            "NO",
                        ],
                        "VER": None,
                    },
                    {
                        "SMODTYPE": [
                            "PTF",
                        ],
                        "VER": None,
                    },
                ],
            ),
        ]


@pytest.mark.vcr
def test_query_csi_by_name(monkeypatch):
    with ZosmfClient("https://zosmf.example") as client:
        monkeypatch.setattr(software.time, "sleep", lambda *_: None)
        assert client.query_csi_by_name(
            name="HOOLIE",
            system="TSTA",
            zones=["GLOBAL"],
            entries=["SYSMOD"],
            filter="ENAME='HL00006'",
        ) == [
            CsiEntry(
                entryname="HL00006",
                entrytype="SYSMOD",
                zonename="GLOBAL",
                subentries=[
                    {
                        "BYPASS": [
                            "NO",
                        ],
                        "VER": None,
                    },
                    {
                        "DELLMOD": [
                            "NO",
                        ],
                        "VER": None,
                    },
                    {
                        "ELEMMOV": [
                            "NO",
                        ],
                        "VER": None,
                    },
                    {
                        "ERROR": [
                            "NO",
                        ],
                        "VER": None,
                    },
                    {
                        "FMID": [
                            "HOOMOC3",
                        ],
                        "VER": "1",
                    },
                    {
                        "SREL": [
                            "Z038",
                        ],
                        "VER": "1",
                    },
                    {
                        "SUPING": [
                            "HL00001",
                            "HL00002",
                            "HL00003",
                            "HL00004",
                            "HL00005",
                        ],
                        "VER": "1",
                    },
                    {
                        "HFS": [
                            "HOOLMOC",
                        ],
                        "VER": None,
                    },
                    {
                        "HOLDDATA": [
                            "SYSTEM(INT),DOC,HL00006",
                        ],
                        "VER": None,
                    },
                    {
                        "JCLIN": [
                            "NO",
                        ],
                        "VER": None,
                    },
                    {
                        "PROGRAM": [
                            "HOOLMOC",
                        ],
                        "VER": None,
                    },
                    {
                        "RECDATE": [
                            "20304",
                        ],
                        "VER": None,
                    },
                    {
                        "RECTIME": [
                            "13:44:10",
                        ],
                        "VER": None,
                    },
                    {
                        "REGEN": [
                            "NO",
                        ],
                        "VER": None,
                    },
                    {
                        "RENLMOD": [
                            "NO",
                        ],
                        "VER": None,
                    },
                    {
                        "RESTORE": [
                            "NO",
                        ],
                        "VER": None,
                    },
                    {
                        "SMODTYPE": [
                            "PTF",
                        ],
                        "VER": None,
                    },
                ],
            ),
        ]


@pytest.mark.vcr
def test_get_query_csi_status(monkeypatch):
    with ZosmfClient("https://zosmf.example") as client:
        monkeypatch.setattr(software.time, "sleep", lambda *_: None)
        assert client.get_query_csi_status(
            "https://zosmf.example/zosmf/swmgmt/statusmonitor/csiquery/1793101874908"
        ) == [
            CsiEntry(
                entryname="HL00006",
                entrytype="SYSMOD",
                zonename="GLOBAL",
                subentries=[
                    {
                        "BYPASS": [
                            "NO",
                        ],
                        "VER": None,
                    },
                    {
                        "DELLMOD": [
                            "NO",
                        ],
                        "VER": None,
                    },
                    {
                        "ELEMMOV": [
                            "NO",
                        ],
                        "VER": None,
                    },
                    {
                        "ERROR": [
                            "NO",
                        ],
                        "VER": None,
                    },
                    {
                        "FMID": [
                            "HOOMOC3",
                        ],
                        "VER": "1",
                    },
                    {
                        "SREL": [
                            "Z038",
                        ],
                        "VER": "1",
                    },
                    {
                        "SUPING": [
                            "HL00001",
                            "HL00002",
                            "HL00003",
                            "HL00004",
                            "HL00005",
                        ],
                        "VER": "1",
                    },
                    {
                        "HFS": [
                            "HOOLMOC",
                        ],
                        "VER": None,
                    },
                    {
                        "HOLDDATA": [
                            "SYSTEM(INT),DOC,HL00006",
                        ],
                        "VER": None,
                    },
                    {
                        "JCLIN": [
                            "NO",
                        ],
                        "VER": None,
                    },
                    {
                        "PROGRAM": [
                            "HOOLMOC",
                        ],
                        "VER": None,
                    },
                    {
                        "RECDATE": [
                            "20304",
                        ],
                        "VER": None,
                    },
                    {
                        "RECTIME": [
                            "13:44:10",
                        ],
                        "VER": None,
                    },
                    {
                        "REGEN": [
                            "NO",
                        ],
                        "VER": None,
                    },
                    {
                        "RENLMOD": [
                            "NO",
                        ],
                        "VER": None,
                    },
                    {
                        "RESTORE": [
                            "NO",
                        ],
                        "VER": None,
                    },
                    {
                        "SMODTYPE": [
                            "PTF",
                        ],
                        "VER": None,
                    },
                ],
            ),
        ]


@pytest.mark.vcr
def test_query_csi_raises_entry_error():
    with ZosmfClient("https://zosmf.example") as client:
        with pytest.raises(
            ZosmfSoftwareManagementError,
            match="'*' cannot be combined with other entry types.",
        ):
            client.query_csi_by_name(
                name="HOOLIE",
                system="TSTA",
                zones=["GLOBAL"],
                entries=["*", "SYSMOD"],
                filter="ENAME='HL00006'",
            )


@pytest.mark.vcr
def test_query_csi_raises_subentry_error():
    with ZosmfClient("https://zosmf.example") as client:
        with pytest.raises(
            ZosmfSoftwareManagementError,
            match="'*' cannot be combined with other subentry types.",
        ):
            client.query_csi_by_name(
                name="HOOLIE",
                system="TSTA",
                zones=["GLOBAL"],
                entries=["SYSMOD"],
                subentries=["*", "MODVER"],
                filter="ENAME='HL00006'",
            )


@pytest.mark.vcr
def test_add_swi_raises_ZosmfSoftwareManagementRequestError():
    with ZosmfClient("https://zosmf.example") as client:
        with pytest.raises(ZosmfSoftwareManagementRequestError):
            client.add_swi(
                SoftwareInstance(
                    name="HOOLIE",
                    system="TSTB",
                    globalzone="OSHOOLI.GLOBAL.CSI",
                    targetzones=["TGT"],
                )
            )
