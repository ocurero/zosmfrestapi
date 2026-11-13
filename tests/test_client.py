from unittest.mock import patch

import pytest
from httpx2 import Proxy
from zosmfrestapi import ZosmfClient
from zosmfrestapi.exceptions import ZosmfError


def test_insecure():
    client = ZosmfClient("https://zosmf.example", insecure=True)
    assert client.insecure is True


def test_proxy():
    client = ZosmfClient("https://zosmf.example", proxy="http://proxy.example:8080")
    assert isinstance(client.proxy, Proxy)
    assert client.proxy.url == "http://proxy.example:8080"


def test_proxy_with_auth():
    client = ZosmfClient(
        "https://zosmf.example",
        proxy="http://proxy.example:8080",
        proxyusername="demouser",
        proxypassword="demopass",
    )
    assert isinstance(client.proxy, Proxy)
    assert client.proxy.auth == ("demouser", "demopass")


def test_insecure_and_cert_raises_ZosmfError():
    with pytest.raises(
        ZosmfError, match="Cannot set insecure mode when cafile or cert is provided."
    ):
        ZosmfClient("https://zosmf.example", insecure=True, cert="/path/to/cert.pem")


def test_loads_separate_cert_and_key():
    with patch("ssl.SSLContext.load_cert_chain") as load_cert_chain:
        with ZosmfClient(
            "https://zosmf.example",
            cert=("/path/to/cert.pem", "/path/to/key.pem"),
        ):
            pass

    load_cert_chain.assert_called_once_with(
        certfile="/path/to/cert.pem",
        keyfile="/path/to/key.pem",
        password=None,
    )


def test_insecure_and_cafile_raises_ZosmfError():
    with pytest.raises(
        ZosmfError, match="Cannot set insecure mode when cafile or cert is provided."
    ):
        ZosmfClient(
            "https://zosmf.example",
            insecure=True,
            cafile="/path/to/cafile",
        )
