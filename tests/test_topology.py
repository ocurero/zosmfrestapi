import pytest

from zosmfrestapi import (
    System,
    ZosmfClient,
    Group,
)


@pytest.mark.vcr
def test_get_groups():
    with ZosmfClient("https://zosmf.example") as client:
        assert client.get_groups() == {
            "GROUP0": Group(
                name="GROUP0", description="A simple group", systems="TESTA,TESTB"
            ),
            "IYUCLOUD": Group(
                name="IYUCLOUD", description="", systems="TESTA,TESTB,TESTC"
            ),
        }


@pytest.mark.vcr
def test_get_systems():
    with ZosmfClient("https://zosmf.example") as client:
        assert client.get_systems() == {
            "TSTA": System(
                name="TSTA",
                nickName="TESTA",
                sysplex="TST01",
                groups="GROUP0,IYUCLOUD",
                jesType="JES2",
                jesMemberName="TSTA",
                url="https://zosmf.example/zosmf/",
            ),
            "TSTB": System(
                name="TSTB",
                nickName="TESTB",
                sysplex="TST01",
                groups="IYUCLOUD",
                jesType="JES2",
                jesMemberName="TSTB",
            ),
        }
