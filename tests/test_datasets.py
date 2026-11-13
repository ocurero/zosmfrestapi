import pytest

from zosmfrestapi import ZosmfClient
from zosmfrestapi.exceptions import ZosmfDatasetNotFoundError


@pytest.mark.vcr
def test_read_dataset():
    with ZosmfClient("https://zosmf.example") as client:
        assert client.read_dataset("USER.PDS(MEMBER)") == "HELLO WORLD\n"


@pytest.mark.vcr
def test_read_dataset_with_volser():
    with ZosmfClient("https://zosmf.example") as client:
        assert (
            client.read_dataset(
                "USER.PDS(MEMBER)",
                volser="VOL000",
            )
            == "HELLO WORLD\n"
        )


@pytest.mark.vcr
def test_read_dataset_raises_ZosmfDatasetNotFoundError():
    print(ZosmfDatasetNotFoundError)
    with ZosmfClient("https://zosmf.example") as client:
        with pytest.raises(ZosmfDatasetNotFoundError):
            client.read_dataset("USER.PDS2(MEMBER)")
