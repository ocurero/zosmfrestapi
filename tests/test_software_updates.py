import pytest
from zosmfrestapi import (
    ZosmfClient,
    ZosmfSoftwareInstanceNotFoundError,
    ZosmfSoftwareManagementError,
)
from zosmfrestapi.services import software_updates
from zosmfrestapi.testing import (
    make_completed_sw_update_proc,
    make_copy_output,
    make_error_sw_update_proc,
    make_missing_fixcats_list,
    make_missing_updates_list,
    make_suspended_sw_update_proc,
    make_sw_update,
)
from zosmfrestapi.testing.software_updates import (
    make_canceled_sw_update_proc,
    make_running_sw_update_proc,
)

from tests.helpers import pdt


@pytest.mark.vcr
def test_list_sw_updates_by_uuid():
    with ZosmfClient("https://zosmf.example") as client:
        assert client.list_sw_updates_by_uuid("ab7a70d9-02bf-4a70-9623-961d014bdec1") == [
            make_completed_sw_update_proc(),
            make_canceled_sw_update_proc(),
        ]


@pytest.mark.vcr
def test_list_sw_updates_by_name():
    with ZosmfClient("https://zosmf.example") as client:
        assert client.list_sw_updates_by_name(system="TSTA", name="HOOLIE") == [
            make_completed_sw_update_proc(),
            make_canceled_sw_update_proc(),
        ]


@pytest.mark.vcr
def test_list_sw_updates_by_name_empty():
    with ZosmfClient("https://zosmf.example") as client:
        assert client.list_sw_updates_by_name(system="TSTC", name="HOOLIE") == []


@pytest.mark.vcr
def test_get_sw_updates_nowait():
    with ZosmfClient("https://zosmf.example") as client:
        assert client.get_sw_updates(process_id=58, wait=False) == [
            make_running_sw_update_proc()
        ]


@pytest.mark.vcr
def test_get_sw_updates_wait(monkeypatch):
    with ZosmfClient("https://zosmf.example") as client:
        monkeypatch.setattr(software_updates.time, "sleep", lambda *_: None)
        assert client.get_sw_updates(process_id=58, wait=True) == [
            make_canceled_sw_update_proc()
        ]


@pytest.mark.vcr
def test_get_missing_fixcat_by_uuid(monkeypatch):
    with ZosmfClient("https://zosmf.example") as client:
        monkeypatch.setattr(software_updates.time, "sleep", lambda *_: None)

        assert client.get_missing_fixcat_by_uuid(
            uuid="ab7a70d9-02bf-4a70-9623-961d014bdec1"
        ) == {
            "lastholdrecvdate": pdt("2026-10-27T05:12:26Z"),
            "list": make_missing_fixcats_list(),
        }


@pytest.mark.vcr
def test_get_missing_fixcat_by_name(monkeypatch):
    with ZosmfClient("https://zosmf.example") as client:
        monkeypatch.setattr(software_updates.time, "sleep", lambda *_: None)

        assert client.get_missing_fixcat_by_name(name="HOOLIE", system="TSTA") == {
            "lastholdrecvdate": pdt("2026-10-27T05:12:26Z"),
            "list": make_missing_fixcats_list(),
        }


@pytest.mark.vcr
def test_get_missing_updates_by_uuid(monkeypatch):
    with ZosmfClient("https://zosmf.example") as client:
        monkeypatch.setattr(software_updates.time, "sleep", lambda *_: None)

        assert client.get_missing_updates_by_uuid(
            uuid="ab7a70d9-02bf-4a70-9623-961d014bdec1"
        ) == {
            "lastholdrecvdate": pdt("2026-10-28T05:12:35Z"),
            "list": make_missing_updates_list(),
        }


@pytest.mark.vcr
def test_get_missing_updates_by_name(monkeypatch):
    with ZosmfClient("https://zosmf.example") as client:
        monkeypatch.setattr(software_updates.time, "sleep", lambda *_: None)

        assert client.get_missing_updates_by_name(name="HOOLIE", system="TSTA") == {
            "lastholdrecvdate": pdt("2026-10-28T05:12:35Z"),
            "list": make_missing_updates_list(),
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
        ) == [make_sw_update()]


@pytest.mark.vcr
def test_search_sw_updates_by_name(monkeypatch):
    with ZosmfClient("https://zosmf.example") as client:
        monkeypatch.setattr(software_updates.time, "sleep", lambda *_: None)

        assert client.search_sw_updates_by_name(
            name="HOOLIE", system="TSTA", updates=["UO07777"]
        ) == [make_sw_update()]


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
        ) == [make_completed_sw_update_proc()]


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
        ) == [make_completed_sw_update_proc()]


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
        ) == [make_suspended_sw_update_proc()]


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
        ) == [make_suspended_sw_update_proc()]


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
        ) == [make_suspended_sw_update_proc()]


@pytest.mark.vcr
def test_copy_output_sw_update_by_uuid():
    with ZosmfClient("https://zosmf.example") as client:
        assert (
            client.copy_output_sw_update_by_uuid(
                uuid="ab7a70d9-02bf-4a70-9623-961d014bdec1",
                output_dir="/TSTA/FOOBAR/",
            )
            == make_copy_output()
        )


@pytest.mark.vcr
def test_copy_output_sw_update_by_name():
    with ZosmfClient("https://zosmf.example") as client:
        assert (
            client.copy_output_sw_update_by_name(
                name="TSTA",
                system="HOOLIE",
                output_dir="/TSTA/FOOBAR/",
            )
            == make_copy_output()
        )


@pytest.mark.vcr
def test_copy_output_sw_update_by_process():
    with ZosmfClient("https://zosmf.example") as client:
        assert (
            client.copy_output_sw_update_by_process(
                process=58,
                output_dir="/TSTA/FOOBAR/",
            )
            == make_copy_output()
        )


@pytest.mark.vcr
def test_start_sw_update_with_error(monkeypatch):
    with ZosmfClient("https://zosmf.example") as client:
        monkeypatch.setattr(software_updates.time, "sleep", lambda *_: None)

        assert client.start_sw_update_by_uuid(
            uuid="ab7a70d9-02bf-4a70-9623-961d014bdec1",
            updates=["UO07777", "UO08888"],
            tgtzone="TGT",
            wait=True,
        ) == [make_error_sw_update_proc()]


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
