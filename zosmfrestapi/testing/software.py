from zosmfrestapi.models.software import (
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
)

from .helpers import pdt


def make_swi(
    system="TSTA",
    description="Product A",
    uuid="c66bb092-cf92-4db9-96fd-2073e3b826ae",
    products=[],
    workflows=[],
):
    return SoftwareInstance(
        name="HOOLIE",
        system=system,
        description=description,
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
        uuid=uuid,
        workflows=workflows,
        products=products,
    )


def make_swi_with_product_and_workflow():
    return make_swi(
        products=[make_product()],
        workflows=[
            make_sw_workflow(),
            make_sw_workflow(
                name="Configuration",
                description="Configure the software in your ServerPac order.",
                location="OSHOOLI.WORKFLOW(HOOLSETU)",
            ),
            make_sw_workflow(
                name="Verify_1",
                description="Installation verification for your ServerPac order.",
                location="OSHOOLI.WORKFLOW(HOOLIVP)",
            ),
        ],
    )


def make_new_swi(products=[], workflows=[]):
    return SoftwareInstance(
        name="HOOLIE2",
        system="TSTA",
        globalzone="OSHOOLI.GLOBAL.CSI",
        targetzones=["TGT"],
        products=products,
        workflows=workflows,
    )


def make_new_swi_with_product():
    return make_new_swi(products=[make_product()])


def make_new_swi_with_workflow():
    return make_new_swi(workflows=[make_sw_workflow()])


def make_product():
    return Product(
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


def make_sw_workflow(
    name="About your order",
    description="Information about your ServerPac order.",
    location="OSHOOLI.WORKFLOW(HOOLWELC)",
):
    return SoftwareInstanceWorkflow(
        name=name,
        description=description,
        location=WorkflowLocation(
            smptype=None,
            smpname=None,
            dsname=location,
            path=None,
        ),
        performonhostsystem=True,
    )


def make_swi_datasets():
    return {
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
                zonedddefs=[SmpeManagedDatasetZoneDddef(zone="DLIB", dddefs=["AHOOLBIN"])],
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
                zonedddefs=[SmpeManagedDatasetZoneDddef(zone="DLIB", dddefs=["AHOOLMOD"])],
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
                zonedddefs=[SmpeManagedDatasetZoneDddef(zone="TGT", dddefs=["SHOOLMOD"])],
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
                zonedddefs=[SmpeManagedDatasetZoneDddef(zone="TGT", dddefs=["SMPSCDS"])],
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
                zonedddefs=[SmpeManagedDatasetZoneDddef(zone="TGT", dddefs=["SHOOLDIR"])],
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


def make_csi_entry():
    return CsiEntry(
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
    )
