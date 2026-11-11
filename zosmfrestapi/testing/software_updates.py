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

from .helpers import pdt


def make_completed_sw_update_proc():
    return UpdateProcess(
        targetzone="TGT",
        selection=UpdateSelection(updates=["UO07777", "UO08888"]),
        notes="",
        processid=58,
        started=pdt("2026-10-28T13:12:56Z"),
        status="COMPLETED",
        step="COMPLETE",
        lastmodified=None,
        completed=pdt("2026-10-28T13:13:47Z"),
        error_results=None,
        updates=[
            UpdateResult(
                fmid="HOOMOC3",
                selectStatus="APPLIED",
                name="UO07777",
            ),
            UpdateResult(
                fmid="HOOMOC3",
                selectStatus="APPLIED",
                name="UO08888",
            ),
            UpdateResult(
                fmid="HOOMOC3",
                selectStatus="APPLIED",
                name="UO09999",
            ),
        ],
        holds=[],
    )


def make_running_sw_update_proc():
    return UpdateProcess(
        targetzone="TGT",
        selection=UpdateSelection(
            updates=[
                "HL00002",
            ],
        ),
        notes="",
        processid=58,
        started=pdt("2026-10-29T13:45:49Z"),
        status="RUNNING",
        step="VERIFYING_UPDATES",
        lastmodified=pdt("2026-10-29T13:46:04Z"),
        completed=None,
        error_results=None,
        updates=[],
        holds=[],
    )


def make_suspended_sw_update_proc():
    return UpdateProcess(
        targetzone="TGT",
        selection=UpdateSelection(updates=["HL00002"]),
        notes="",
        processid=58,
        started=pdt("2026-10-29T13:45:49Z"),
        status="SUSPENDED",
        step="PRE_INSTALLATION_SUMMARY",
        lastmodified=pdt("2026-10-29T13:46:24Z"),
        completed=None,
        error_results=None,
        updates=[UpdateResult(fmid="", selectStatus="SELECTED", name="HL00002")],
        holds=[],
    )


def make_canceled_sw_update_proc():
    return UpdateProcess(
        targetzone="TGT",
        selection=UpdateSelection(
            updates=[
                "UO07777",
                "UO08888",
            ],
        ),
        notes="",
        processid=58,
        started=pdt("2026-09-25T15:44:39Z"),
        completed=pdt("2026-09-25T15:44:49Z"),
        status="CANCELED",
        step="PREPARING_UPDATES",
        lastmodified=None,
        holds=[],
        updates=[],
        error_results=UpdateErrorResults(
            smpe_rc=12,
            message="SMP/E detected missing required SYSMODs. "
            "Check the Error report for the list of "
            "missing SYSMODs.<br><br>RECEIVE the missing "
            "SYSMODs into the global zone and retry the "
            "step.",
            detailedMessage="Missing SYSMODs: \n\n",
        ),
    )


def make_error_sw_update_proc():
    return UpdateProcess(
        targetzone="TGT",
        selection=UpdateSelection(updates=["UO07777", "UO08888"]),
        notes="",
        processid=58,
        started=pdt("2026-10-28T10:08:57Z"),
        status="ERROR",
        step="PREPARING_UPDATES",
        lastmodified=pdt("2026-10-28T10:08:57Z"),
        completed=None,
        error_results=UpdateErrorResults(
            smpe_rc=12,
            message="No updates to install.",
            detailedMessage="\n"
            "PAGE 0001  - NOW SET TO TARGET ZONE "
            "IPI25T   DATE 10/28/26  TIME "
            "11:08:58  SMP/E 37.41   SMPOUT   "
            "OUTPUT\n"
            "\n"
            " GIM42401I    THE FOLLOWING "
            "PARAMETERS WERE SPECIFIED ON THE "
            "EXEC STATEMENT FOR GIMSMP: "
            "'PROCESS=END'.",
        ),
        updates=[],
        holds=[],
    )


def make_missing_fixcats_list():
    return [
        MissingFixcat(
            name="DH55555",
            fixcats=["Hooli.TheBox.New.Parts"],
            fmid="HOOMOC3",
            fmiddesc="The Box III, Middle Out Compression",
            resolvers=[
                MissingUpdateResolver(
                    name="UO01111",
                    received=True,
                )
            ],
            tgtzones=["TGT"],
        ),
        MissingFixcat(
            name="DH66666",
            fixcats=["Hooli.Thebox.Exploitation"],
            fmid="HOOMOC3",
            fmiddesc="The Box III, Middle Out Compression",
            resolvers=[
                MissingUpdateResolver(
                    name="UO02222",
                    received=True,
                )
            ],
            tgtzones=["TGT"],
        ),
    ]


def make_missing_updates_list():
    return [
        MissingUpdate(
            name="DH55555",
            holdclass="HIPER",
            holdsymptom="IPL",
            heldsysmod="HOOMOC3",
            fmid="HOOMOC3",
            fmiddesc="The Box III, Middle Out Compression",
            resolvers=None,
            tgtzones=[
                "TGT",
            ],
        ),
        MissingUpdate(
            name="DH66666",
            holdclass="PE",
            holdsymptom="",
            heldsysmod="UO07777",
            fmid="HOOMOC3",
            fmiddesc="The Box III, Middle Out Compression",
            resolvers=[
                MissingUpdateResolver(
                    name="UO08888",
                    received=True,
                ),
            ],
            tgtzones=[
                "TGT",
            ],
        ),
    ]


def make_sw_update():
    return SoftwareUpdate(
        name="HL00002",
        type="PTF",
        fmid="HOOMOC3",
        zones=[
            SoftwareUpdateZone(
                zone="DLIB",
                status="Not Found",
                installed=None,
            ),
            SoftwareUpdateZone(
                zone="GLOBAL",
                status="Received",
                installed=pdt("2026-10-29T14:39:18Z"),
            ),
            SoftwareUpdateZone(
                zone="TGT",
                status="Not Found",
                installed=None,
            ),
        ],
    )


def make_copy_output():
    return [
        {"name": "/TSTA/FOOBAR/ALL_HOLDS.txt"},
        {"name": "/TSTA/FOOBAR/POST_INSTALL_HOLDS.txt"},
        {
            "name": "/TSTA/FOOBAR/smpe-output/001_PREPARING_UPDATES/"
            "2026-10-28T13-12-59.618718068-SMPRPT.txt"
        },
        {
            "name": "/TSTA/FOOBAR/smpe-output/001_PREPARING_UPDATES/"
            "2026-10-28T13-12-59.618718068-SMPHRPT.txt"
        },
        {
            "name": "/TSTA/FOOBAR/smpe-output/001_PREPARING_UPDATES/"
            "2026-10-28T13-12-59.618718068-SMPOUT.txt"
        },
        {
            "name": "/TSTA/FOOBAR/smpe-output/003_VERIFYING_UPDATES/"
            "2026-10-28T13-13-12.693149151-SMPRPT.txt"
        },
        {
            "name": "/TSTA/FOOBAR/smpe-output/003_VERIFYING_UPDATES/"
            "2026-10-28T13-13-12.693149151-SMPHRPT.txt"
        },
        {
            "name": "/TSTA/FOOBAR/smpe-output/003_VERIFYING_UPDATES/"
            "2026-10-28T13-13-12.693149151-SMPOUT.txt"
        },
        {
            "name": "/TSTA/FOOBAR/smpe-output/005_INSTALLATION/"
            "2026-10-28T13-13-46.199025023-SMPRPT.txt"
        },
        {
            "name": "/TSTA/FOOBAR/smpe-output/005_INSTALLATION/"
            "2026-10-28T13-13-46.199025023-SMPHRPT.txt"
        },
        {
            "name": "/TSTA/FOOBAR/smpe-output/005_INSTALLATION/"
            "2026-10-28T13-13-46.199025023-SMPOUT.txt"
        },
        {
            "name": "/TSTA/FOOBAR/smpe-output/005_INSTALLATION/"
            "2026-10-28T13-13-46.199025023-SYSPRINT.txt"
        },
    ]
