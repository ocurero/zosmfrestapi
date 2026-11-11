import pytest
from zosmfrestapi import ZosmfClient
from zosmfrestapi.testing import make_group, make_system


@pytest.mark.vcr
def test_get_groups():
    with ZosmfClient("https://zosmf.example") as client:
        assert client.get_groups() == {
            "GROUP0": make_group(name="GROUP0", systems=["TESTA", "TESTB"]),
            "IYUCLOUD": make_group(name="IYUCLOUD", systems=["TESTA", "TESTB", "TESTC"]),
        }


@pytest.mark.vcr
def test_get_systems():
    with ZosmfClient("https://zosmf.example") as client:
        assert client.get_systems() == {
            "TSTA": make_system(name="A", groups=["GROUP0", "IYUCLOUD"]),
            "TSTB": make_system(name="B", groups=["IYUCLOUD"]),
        }
