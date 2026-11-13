import pytest
from zosmfrestapi import ZosmfClient
from zosmfrestapi.exceptions import (
    ZosmfSoftwareInstanceNotFoundError,
    ZosmfSoftwareManagementError,
    ZosmfSoftwareManagementRequestError,
)
from zosmfrestapi.models import SoftwareInstance
from zosmfrestapi.services import software
from zosmfrestapi.testing import (
    make_csi_entry,
    make_new_swi_with_product,
    make_new_swi_with_workflow,
    make_swi,
    make_swi_datasets,
    make_swi_with_product_and_workflow,
)


@pytest.mark.vcr
def test_list_swis():
    with ZosmfClient("https://zosmf.example") as client:
        assert client.list_swis() == [
            make_swi(
                system="TSTA",
                uuid="c66bb092-cf92-4db9-96fd-2073e3b826ae",
            ),
            make_swi(
                system="TSTB",
                uuid="dabf0e67-cb96-43a5-abba-b47caa91a61d",
            ),
        ]


@pytest.mark.vcr
def test_get_swi_by_uuid(monkeypatch):
    with ZosmfClient("https://zosmf.example") as client:
        assert (
            client.get_swi_by_uuid("c66bb092-cf92-4db9-96fd-2073e3b826ae")
            == make_swi_with_product_and_workflow()
        )


@pytest.mark.vcr
def test_get_swi_by_name():
    with ZosmfClient("https://zosmf.example") as client:
        assert client.get_swi_by_name("HOOLIE", "TSTA") == make_swi_with_product_and_workflow()


@pytest.mark.vcr
def test_get_swi_raises_ZosmfSoftwareInstanceNotFoundError():
    with ZosmfClient("https://zosmf.example") as client:
        with pytest.raises(ZosmfSoftwareInstanceNotFoundError):
            client.get_swi_by_uuid("000000-0000000-000000-0000-00000")


@pytest.mark.vcr
def test_get_swi_datasets_by_uuid(monkeypatch):
    with ZosmfClient("https://zosmf.example") as client:
        monkeypatch.setattr(software.time, "sleep", lambda *_: None)

        assert (
            client.get_swi_datasets_by_uuid("c66bb092-cf92-4db9-96fd-2073e3b826ae")
            == make_swi_datasets()
        )


@pytest.mark.vcr
def test_get_swi_datasets_by_name(monkeypatch):
    with ZosmfClient("https://zosmf.example") as client:
        monkeypatch.setattr(software.time, "sleep", lambda *_: None)
        assert client.get_swi_datasets_by_name("HOOLIE", "TSTA") == make_swi_datasets()


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
        client.add_swi(make_new_swi_with_product())


@pytest.mark.vcr
def test_add_workflow_swi():
    with ZosmfClient("https://zosmf.example") as client:
        client.add_swi(make_new_swi_with_workflow())


@pytest.mark.vcr
def test_add_swi_globalzone_no_targetzones():
    with ZosmfClient("https://zosmf.example") as client:
        with pytest.raises(
            ValueError, match="Target zones must be specified when globalzone is set"
        ):
            client.add_swi(
                SoftwareInstance(name="HOOLIE", system="TSTB", globalzone="OSHOOLI.GLOBAL.CSI")
            )


@pytest.mark.vcr
def test_add_swi_no_globalzone_or_datasets():
    with ZosmfClient("https://zosmf.example") as client:
        with pytest.raises(ValueError, match="Either globalzone or datasets must be specified"):
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
            "statusurl": "https://zosmf.example/zosmf/swmgmt/"
            "statusmonitor/csiquery/1793101874908"
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
        ) == [make_csi_entry()]


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
        ) == [make_csi_entry()]


@pytest.mark.vcr
def test_get_query_csi_status(monkeypatch):
    with ZosmfClient("https://zosmf.example") as client:
        monkeypatch.setattr(software.time, "sleep", lambda *_: None)
        assert client.get_query_csi_status(
            "https://zosmf.example/zosmf/swmgmt/statusmonitor/csiquery/1793101874908"
        ) == [make_csi_entry()]


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
