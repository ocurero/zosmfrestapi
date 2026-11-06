import pytest

from tests.helpers import pdt
from zosmfrestapi.services import software_updates
from zosmfrestapi import (
    MissingFixcat,
    MissingUpdate,
    MissingUpdateResolver,
    SoftwareUpdate,
    SoftwareUpdateZone,
    UpdateErrorResults,
    UpdateProcess,
    UpdateResult,
    UpdateSelection,
    ZosmfClient,
    ZosmfSoftwareInstanceNotFoundError,
    ZosmfSoftwareManagementError,
)


@pytest.mark.vcr
def test_list_sw_updates_by_uuid():
    with ZosmfClient("https://zosmf.example") as client:
        assert client.list_sw_updates_by_uuid(
            "ab7a70d9-02bf-4a70-9623-961d014bdec1"
        ) == [
            UpdateProcess(
                targetzone="TGT",
                selection=UpdateSelection(updates=["UO07777", "UO08888"]),
                notes="",
                processid=36,
                started=pdt("2026-09-25T15:47:03Z"),
                completed=pdt("2026-09-25T15:48:03Z"),
                status="COMPLETED",
                step="COMPLETE",
                lastmodified=None,
                holds=[],
                updates=[
                    UpdateResult(
                        fmid="HOOMOC3", selectStatus="APPLIED", name="UO06666"
                    ),
                    UpdateResult(
                        fmid="HOOMOC3", selectStatus="APPLIED", name="UO07777"
                    ),
                    UpdateResult(
                        fmid="HOOMOC3", selectStatus="APPLIED", name="UO08888"
                    ),
                    UpdateResult(
                        fmid="HOOMOC3", selectStatus="APPLIED", name="UO09999"
                    ),
                ],
                error_results=None,
            ),
            UpdateProcess(
                targetzone="TGT",
                selection=UpdateSelection(
                    updates=[
                        "UO07777",
                        "UO08888",
                    ],
                ),
                notes="",
                processid=34,
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
            ),
        ]


@pytest.mark.vcr
def test_list_sw_updates_by_name():
    with ZosmfClient("https://zosmf.example") as client:
        assert client.list_sw_updates_by_name(system="TSTA", name="HOOLIE") == [
            UpdateProcess(
                targetzone="TGT",
                selection=UpdateSelection(updates=["UO07777", "UO08888"]),
                notes="",
                processid=36,
                started=pdt("2026-09-25T15:47:03Z"),
                completed=pdt("2026-09-25T15:48:03Z"),
                status="COMPLETED",
                step="COMPLETE",
                lastmodified=None,
                holds=[],
                updates=[
                    UpdateResult(
                        fmid="HOOMOC3", selectStatus="APPLIED", name="UO06666"
                    ),
                    UpdateResult(
                        fmid="HOOMOC3", selectStatus="APPLIED", name="UO07777"
                    ),
                    UpdateResult(
                        fmid="HOOMOC3", selectStatus="APPLIED", name="UO08888"
                    ),
                    UpdateResult(
                        fmid="HOOMOC3", selectStatus="APPLIED", name="UO09999"
                    ),
                ],
                error_results=None,
            ),
            UpdateProcess(
                targetzone="TGT",
                selection=UpdateSelection(
                    updates=[
                        "UO07777",
                        "UO08888",
                    ],
                ),
                notes="",
                processid=34,
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
            ),
        ]


@pytest.mark.vcr
def test_list_sw_updates_by_name_empty():
    with ZosmfClient("https://zosmf.example") as client:
        assert client.list_sw_updates_by_name(system="TSTC", name="HOOLIE") == []


@pytest.mark.vcr
def test_get_sw_updates_nowait():
    with ZosmfClient("https://zosmf.example") as client:
        assert client.get_sw_updates(process_id=34, wait=False) == [
            UpdateProcess(
                targetzone="TGT",
                selection=UpdateSelection(
                    updates=[
                        "UO07777",
                        "UO08888",
                    ],
                ),
                notes="",
                processid=34,
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
        ]


@pytest.mark.vcr
def test_get_sw_updates_wait(monkeypatch):
    with ZosmfClient("https://zosmf.example") as client:
        monkeypatch.setattr(software_updates.time, "sleep", lambda *_: None)
        assert client.get_sw_updates(process_id=34, wait=True) == [
            UpdateProcess(
                targetzone="TGT",
                selection=UpdateSelection(
                    updates=[
                        "UO07777",
                        "UO08888",
                    ],
                ),
                notes="",
                processid=34,
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
        ]


@pytest.mark.vcr
def test_get_missing_fixcat_by_uuid(monkeypatch):
    with ZosmfClient("https://zosmf.example") as client:
        monkeypatch.setattr(software_updates.time, "sleep", lambda *_: None)

        assert client.get_missing_fixcat_by_uuid(
            uuid="ab7a70d9-02bf-4a70-9623-961d014bdec1"
        ) == {
            "lastholdrecvdate": pdt("2026-10-27T05:12:26Z"),
            "list": [
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
            ],
        }


@pytest.mark.vcr
def test_get_missing_fixcat_by_name(monkeypatch):
    with ZosmfClient("https://zosmf.example") as client:
        monkeypatch.setattr(software_updates.time, "sleep", lambda *_: None)

        assert client.get_missing_fixcat_by_name(name="HOOLIE", system="TSTA") == {
            "lastholdrecvdate": pdt("2026-10-27T05:12:26Z"),
            "list": [
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
            ],
        }


@pytest.mark.vcr
def test_get_missing_updates_by_uuid(monkeypatch):
    with ZosmfClient("https://zosmf.example") as client:
        monkeypatch.setattr(software_updates.time, "sleep", lambda *_: None)

        assert client.get_missing_updates_by_uuid(
            uuid="ab7a70d9-02bf-4a70-9623-961d014bdec1"
        ) == {
            "lastholdrecvdate": pdt("2026-10-28T05:12:35Z"),
            "list": [
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
            ],
        }


@pytest.mark.vcr
def test_get_missing_updates_by_name(monkeypatch):
    with ZosmfClient("https://zosmf.example") as client:
        monkeypatch.setattr(software_updates.time, "sleep", lambda *_: None)

        assert client.get_missing_updates_by_name(name="HOOLIE", system="TSTA") == {
            "lastholdrecvdate": pdt("2026-10-28T05:12:35Z"),
            "list": [
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
            ],
        }


@pytest.mark.vcr
def test_get_missing_updates_raises_mal():
    with ZosmfClient("https://zosmf.example") as client:
        with pytest.raises(ZosmfSoftwareInstanceNotFoundError):
            client.get_missing_updates_by_name(name="HOOLIE", system="TSTC")


@pytest.mark.vcr
def test_search_sw_updates_by_uuid(monkeypatch):
    with ZosmfClient("https://zosmf.example") as client:
        monkeypatch.setattr(software_updates.time, "sleep", lambda *_: None)

        assert client.search_sw_updates_by_uuid(
            uuid="c66bb092-cf92-4db9-96fd-2073e3b826ae", updates=["HL00002"]
        ) == [
            SoftwareUpdate(
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
        ]


@pytest.mark.vcr
def test_search_sw_updates_by_name(monkeypatch):
    with ZosmfClient("https://zosmf.example") as client:
        monkeypatch.setattr(software_updates.time, "sleep", lambda *_: None)

        assert client.search_sw_updates_by_name(
            name="HOOLIE", system="TSTA", updates=["UO07777"]
        ) == [
            SoftwareUpdate(
                name="UO07777",
                type="PTF",
                fmid="HOOMOC3",
                zones=[
                    SoftwareUpdateZone(
                        zone="DLI",
                        status="Not Found",
                        installed=None,
                    ),
                    SoftwareUpdateZone(
                        zone="GLOBAL",
                        status="Received",
                        installed=pdt("2026-05-15T09:55:08Z"),
                    ),
                    SoftwareUpdateZone(
                        zone="TGT",
                        status="Applied",
                        installed=pdt("2026-10-27T17:52:42Z"),
                    ),
                ],
            )
        ]


@pytest.mark.vcr
def test_start_sw_update_by_uuid_nowait():
    with ZosmfClient("https://zosmf.example") as client:
        assert (
            client.start_sw_update_by_uuid(
                uuid="ab7a70d9-02bf-4a70-9623-961d014bdec1",
                updates=["UO07777"],
                tgtzone="IPI25T",
                wait=False,
            )
            == 58
        )


@pytest.mark.vcr
def test_start_sw_update_by_name_nowait():
    with ZosmfClient("https://zosmf.example") as client:
        assert (
            client.start_sw_update_by_name(
                name="HOOLIE",
                system="TSTA",
                updates=["UO07777"],
                tgtzone="IPI25T",
                wait=False,
            )
            == 58
        )


@pytest.mark.vcr
def test_start_sw_update_by_uuid_wait(monkeypatch):
    with ZosmfClient("https://zosmf.example") as client:
        monkeypatch.setattr(software_updates.time, "sleep", lambda *_: None)

        assert client.start_sw_update_by_uuid(
            uuid="ab7a70d9-02bf-4a70-9623-961d014bdec1",
            updates=["UO07777", "UO08888"],
            tgtzone="TGT",
            wait=True,
        ) == [
            UpdateProcess(
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
        ]


@pytest.mark.vcr
def test_start_sw_update_by_name_wait(monkeypatch):
    with ZosmfClient("https://zosmf.example") as client:
        monkeypatch.setattr(software_updates.time, "sleep", lambda *_: None)

        assert client.start_sw_update_by_name(
            name="HOOLIE",
            system="TSTA",
            updates=["UO07777", "UO08888"],
            tgtzone="TGT",
            wait=True,
        ) == [
            UpdateProcess(
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
        ]


@pytest.mark.vcr
def test_cancel_sw_update_by_uuid():
    with ZosmfClient("https://zosmf.example") as client:
        assert (
            client.cancel_sw_update_by_uuid(
                uuid="c66bb092-cf92-4db9-96fd-2073e3b826ae",
            )
            == 58
        )


@pytest.mark.vcr
def test_cancel_sw_update_by_name():
    with ZosmfClient("https://zosmf.example") as client:
        assert (
            client.cancel_sw_update_by_name(
                name="HOOLIE",
                system="TSTA",
            )
            == 58
        )


@pytest.mark.vcr
def test_cancel_sw_update_by_process():
    with ZosmfClient("https://zosmf.example") as client:
        assert (
            client.cancel_sw_update_by_process(
                processid=58,
            )
            == 58
        )


@pytest.mark.vcr
def test_resume_sw_update_by_uuid_nowait():
    with ZosmfClient("https://zosmf.example") as client:
        assert (
            client.resume_sw_update_by_uuid(
                uuid="c66bb092-cf92-4db9-96fd-2073e3b826ae", wait=False
            )
            == 58
        )


@pytest.mark.vcr
def test_resume_sw_update_by_uuid_wait(monkeypatch):
    with ZosmfClient("https://zosmf.example") as client:
        monkeypatch.setattr(software_updates.time, "sleep", lambda *_: None)
        assert client.resume_sw_update_by_uuid(
            uuid="c66bb092-cf92-4db9-96fd-2073e3b826ae",
            steps=["PRE_INSTALLATION_SUMMARY"],
            wait=True,
        ) == [
            UpdateProcess(
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
                updates=[
                    UpdateResult(fmid="", selectStatus="SELECTED", name="HL00002")
                ],
                holds=[],
            )
        ]


@pytest.mark.vcr
def test_resume_sw_update_by_name_nowait():
    with ZosmfClient("https://zosmf.example") as client:
        assert (
            client.resume_sw_update_by_name(
                name="HOOLIE",
                system="TSTA",
                wait=False,
            )
            == 58
        )


@pytest.mark.vcr
def test_resume_sw_update_by_name_wait(monkeypatch):
    with ZosmfClient("https://zosmf.example") as client:
        monkeypatch.setattr(software_updates.time, "sleep", lambda *_: None)
        assert client.resume_sw_update_by_name(
            name="HOOLIE",
            system="TSTA",
            steps=["PRE_INSTALLATION_SUMMARY"],
            wait=True,
        ) == [
            UpdateProcess(
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
                updates=[
                    UpdateResult(fmid="", selectStatus="SELECTED", name="HL00002")
                ],
                holds=[],
            )
        ]


@pytest.mark.vcr
def test_resume_sw_update_by_process_nowait():
    with ZosmfClient("https://zosmf.example") as client:
        assert client.resume_sw_update_by_process(processid=58, wait=False) == 58


@pytest.mark.vcr
def test_resume_sw_update_by_process_wait(monkeypatch):
    with ZosmfClient("https://zosmf.example") as client:
        monkeypatch.setattr(software_updates.time, "sleep", lambda *_: None)
        assert client.resume_sw_update_by_process(
            processid=58,
            steps=["PRE_INSTALLATION_SUMMARY"],
            wait=True,
        ) == [
            UpdateProcess(
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
                updates=[
                    UpdateResult(fmid="", selectStatus="SELECTED", name="HL00002")
                ],
                holds=[],
            )
        ]


@pytest.mark.vcr
def test_copy_output_sw_update_by_uuid():
    with ZosmfClient("https://zosmf.example") as client:
        assert client.copy_output_sw_update_by_uuid(
            uuid="ab7a70d9-02bf-4a70-9623-961d014bdec1",
            output_dir="/TSTA/FOOBAR/",
        ) == [
            {"name": "/TSTA/FOOBAR/ALL_HOLDS.txt"},
            {"name": "/TSTA/FOOBAR/POST_INSTALL_HOLDS.txt"},
            {
                "name": "/TSTA/FOOBAR/smpe-output/001_PREPARING_UPDATES/2026-10-28T13-12-59.618718068-SMPRPT.txt"
            },
            {
                "name": "/TSTA/FOOBAR/smpe-output/001_PREPARING_UPDATES/2026-10-28T13-12-59.618718068-SMPHRPT.txt"
            },
            {
                "name": "/TSTA/FOOBAR/smpe-output/001_PREPARING_UPDATES/2026-10-28T13-12-59.618718068-SMPOUT.txt"
            },
            {
                "name": "/TSTA/FOOBAR/smpe-output/003_VERIFYING_UPDATES/2026-10-28T13-13-12.693149151-SMPRPT.txt"
            },
            {
                "name": "/TSTA/FOOBAR/smpe-output/003_VERIFYING_UPDATES/2026-10-28T13-13-12.693149151-SMPHRPT.txt"
            },
            {
                "name": "/TSTA/FOOBAR/smpe-output/003_VERIFYING_UPDATES/2026-10-28T13-13-12.693149151-SMPOUT.txt"
            },
            {
                "name": "/TSTA/FOOBAR/smpe-output/005_INSTALLATION/2026-10-28T13-13-46.199025023-SMPRPT.txt"
            },
            {
                "name": "/TSTA/FOOBAR/smpe-output/005_INSTALLATION/2026-10-28T13-13-46.199025023-SMPHRPT.txt"
            },
            {
                "name": "/TSTA/FOOBAR/smpe-output/005_INSTALLATION/2026-10-28T13-13-46.199025023-SMPOUT.txt"
            },
            {
                "name": "/TSTA/FOOBAR/smpe-output/005_INSTALLATION/2026-10-28T13-13-46.199025023-SYSPRINT.txt"
            },
        ]


@pytest.mark.vcr
def test_copy_output_sw_update_by_name():
    with ZosmfClient("https://zosmf.example") as client:
        assert client.copy_output_sw_update_by_name(
            name="TSTA",
            system="HOOLIE",
            output_dir="/TSTA/FOOBAR/",
        ) == [
            {"name": "/TSTA/FOOBAR/ALL_HOLDS.txt"},
            {"name": "/TSTA/FOOBAR/POST_INSTALL_HOLDS.txt"},
            {
                "name": "/TSTA/FOOBAR/smpe-output/001_PREPARING_UPDATES/2026-10-28T13-12-59.618718068-SMPRPT.txt"
            },
            {
                "name": "/TSTA/FOOBAR/smpe-output/001_PREPARING_UPDATES/2026-10-28T13-12-59.618718068-SMPHRPT.txt"
            },
            {
                "name": "/TSTA/FOOBAR/smpe-output/001_PREPARING_UPDATES/2026-10-28T13-12-59.618718068-SMPOUT.txt"
            },
            {
                "name": "/TSTA/FOOBAR/smpe-output/003_VERIFYING_UPDATES/2026-10-28T13-13-12.693149151-SMPRPT.txt"
            },
            {
                "name": "/TSTA/FOOBAR/smpe-output/003_VERIFYING_UPDATES/2026-10-28T13-13-12.693149151-SMPHRPT.txt"
            },
            {
                "name": "/TSTA/FOOBAR/smpe-output/003_VERIFYING_UPDATES/2026-10-28T13-13-12.693149151-SMPOUT.txt"
            },
            {
                "name": "/TSTA/FOOBAR/smpe-output/005_INSTALLATION/2026-10-28T13-13-46.199025023-SMPRPT.txt"
            },
            {
                "name": "/TSTA/FOOBAR/smpe-output/005_INSTALLATION/2026-10-28T13-13-46.199025023-SMPHRPT.txt"
            },
            {
                "name": "/TSTA/FOOBAR/smpe-output/005_INSTALLATION/2026-10-28T13-13-46.199025023-SMPOUT.txt"
            },
            {
                "name": "/TSTA/FOOBAR/smpe-output/005_INSTALLATION/2026-10-28T13-13-46.199025023-SYSPRINT.txt"
            },
        ]


@pytest.mark.vcr
def test_copy_output_sw_update_by_process():
    with ZosmfClient("https://zosmf.example") as client:
        assert client.copy_output_sw_update_by_process(
            process=58,
            output_dir="/TSTA/FOOBAR/",
        ) == [
            {"name": "/TSTA/FOOBAR/ALL_HOLDS.txt"},
            {"name": "/TSTA/FOOBAR/POST_INSTALL_HOLDS.txt"},
            {
                "name": "/TSTA/FOOBAR/smpe-output/001_PREPARING_UPDATES/2026-10-28T13-12-59.618718068-SMPRPT.txt"
            },
            {
                "name": "/TSTA/FOOBAR/smpe-output/001_PREPARING_UPDATES/2026-10-28T13-12-59.618718068-SMPHRPT.txt"
            },
            {
                "name": "/TSTA/FOOBAR/smpe-output/001_PREPARING_UPDATES/2026-10-28T13-12-59.618718068-SMPOUT.txt"
            },
            {
                "name": "/TSTA/FOOBAR/smpe-output/003_VERIFYING_UPDATES/2026-10-28T13-13-12.693149151-SMPRPT.txt"
            },
            {
                "name": "/TSTA/FOOBAR/smpe-output/003_VERIFYING_UPDATES/2026-10-28T13-13-12.693149151-SMPHRPT.txt"
            },
            {
                "name": "/TSTA/FOOBAR/smpe-output/003_VERIFYING_UPDATES/2026-10-28T13-13-12.693149151-SMPOUT.txt"
            },
            {
                "name": "/TSTA/FOOBAR/smpe-output/005_INSTALLATION/2026-10-28T13-13-46.199025023-SMPRPT.txt"
            },
            {
                "name": "/TSTA/FOOBAR/smpe-output/005_INSTALLATION/2026-10-28T13-13-46.199025023-SMPHRPT.txt"
            },
            {
                "name": "/TSTA/FOOBAR/smpe-output/005_INSTALLATION/2026-10-28T13-13-46.199025023-SMPOUT.txt"
            },
            {
                "name": "/TSTA/FOOBAR/smpe-output/005_INSTALLATION/2026-10-28T13-13-46.199025023-SYSPRINT.txt"
            },
        ]


@pytest.mark.vcr
def test_start_sw_update_with_error(monkeypatch):
    with ZosmfClient("https://zosmf.example") as client:
        monkeypatch.setattr(software_updates.time, "sleep", lambda *_: None)

        assert client.start_sw_update_by_uuid(
            uuid="ab7a70d9-02bf-4a70-9623-961d014bdec1",
            updates=["UO07777", "UO08888"],
            tgtzone="TGT",
            wait=True,
        ) == [
            UpdateProcess(
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
        ]


@pytest.mark.vcr
def test_start_sw_update_raises():
    with ZosmfClient("https://zosmf.example") as client:

        with pytest.raises(
            ZosmfSoftwareManagementError,
            match="At most one of updates, sourceids, or fixcats must be provided",
        ):
            client.start_sw_update_by_uuid(
                uuid="ab7a70d9-02bf-4a70-9623-961d014bdec1",
                updates=["UO07777", "UO08888"],
                fixcats=["Hooli.TheBox.New.Parts"],
                tgtzone="TGT",
                wait=True,
            )
