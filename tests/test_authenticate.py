from unittest.mock import ANY, patch

from httpx2 import Proxy
import pytest

from zosmfrestapi import (
    LoginOk,
    ZosmfAuthError,
    ZosmfClient,
    ZosmfError,
    ZosmfLoginError,
)


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


@pytest.mark.vcr()
def test_unauthenticated_raises_ZosmfAuthError():
    client = ZosmfClient("https://zosmf.example")
    with pytest.raises(ZosmfAuthError):
        client.read_dataset("MY.DATASET")


def test_insecure_and_cert_raises_ZosmfError():
    with pytest.raises(
        ZosmfError, match="Cannot set insecure mode when cafile or cert is provided."
    ):
        client = ZosmfClient(
            "https://zosmf.example", insecure=True, cert="/path/to/cert.pem"
        )


@pytest.mark.vcr(
    before_record_response=lambda response: response,
)
def test_authenticate_cert():
    with patch("ssl.SSLContext.load_cert_chain") as load_cert_chain:
        with ZosmfClient(
            "https://zosmf.example",
            cert="/path/to/cert.pem",
        ) as client:
            login = client.authenticate()
            assert login == LoginOk(
                returnCode=0,
                reasonCode=0,
                message="Success.",
                ltpa_token=ANY,
                jwt_token=ANY,
            )

        load_cert_chain.assert_called_once_with(certfile="/path/to/cert.pem")


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
    )


@pytest.mark.vcr(
    before_record_response=lambda response: response,
)
def test_authenticate_cafile():
    with patch("ssl.SSLContext.load_verify_locations") as load_verify_locations:
        with ZosmfClient("https://zosmf.example", cafile="/path/to/ca.pem") as client:
            login = client.authenticate()
            assert login == LoginOk(
                returnCode=0,
                reasonCode=0,
                message="Success.",
                ltpa_token=ANY,
                jwt_token=ANY,
            )

        load_verify_locations.assert_called_with(cafile="/path/to/ca.pem")


@pytest.mark.vcr(
    before_record_response=lambda response: response,
)
def test_authenticate_ltpa_token():
    """Test authentication using an LTPA token. A JWT token will be returned if JWT tokens are enabled by z/OSMF."""
    with ZosmfClient(
        "https://zosmf.example",
        ltpa_token="x2q29998U26AwfYy4vc0GlK5zItaZkkXEbGQ/...<REDACTED>.../NiM1t3FQpvWRbzTsmyr2",
    ) as client:
        assert client.authenticate() == LoginOk(
            returnCode=0,
            reasonCode=0,
            message="Success.",
            ltpa_token="x2q29998U26AwfYy4vc0GlK5zItaZkkXEbGQ/...<REDACTED>.../NiM1t3FQpvWRbzTsmyr2",
            jwt_token=ANY,
        )


@pytest.mark.vcr(
    before_record_response=lambda response: response,
)
def test_authenticate_jwt_token():
    """Test authentication using a JWT token. A LTPA2 token is not returned by z/OSMF if JWT tokens are enabled by z/OSMF."""
    with ZosmfClient(
        "https://zosmf.example",
        jwt_token="eyJraWQiOiJBTk9OWU1JWkVEX0tJRCIsInR5cCI6IkpXVCIsImFsZyI6IlJTMjU2In0.eyJ0b2tlbl90eXBlIjoiQmVhcmVyIiwic3Vi"
        "IjoiPFVTRVI+IiwidXBuIjoiPFVTRVI+IiwiZ3JvdXBzIjpbIkdST1VQX0EiLCJHUk9VUF9CIiwiR1JPVVBfQyJdLCJyZWFsbSI6IjxS"
        "RUFMTT4iLCJpc3MiOiI8SVNTVUVSPiIsImV4cCI6MTIzNDU2Nzg5MCwiaWF0IjoxMjM0NTYwMDAwfQ.<SIGNATURE_REDACTED>",
    ) as client:
        assert client.authenticate() == LoginOk(
            returnCode=0,
            reasonCode=0,
            message="Success.",
            ltpa_token=None,
            jwt_token="eyJraWQiOiJBTk9OWU1JWkVEX0tJRCIsInR5cCI6IkpXVCIsImFsZyI6IlJTMjU2In0.eyJ0b2tlbl90eXBlIjoiQmVhcmVyIiwic3Vi"
            "IjoiPFVTRVI+IiwidXBuIjoiPFVTRVI+IiwiZ3JvdXBzIjpbIkdST1VQX0EiLCJHUk9VUF9CIiwiR1JPVVBfQyJdLCJyZWFsbSI6IjxS"
            "RUFMTT4iLCJpc3MiOiI8SVNTVUVSPiIsImV4cCI6MTIzNDU2Nzg5MCwiaWF0IjoxMjM0NTYwMDAwfQ.<SIGNATURE_REDACTED>",
        )


@pytest.mark.vcr(
    before_record_response=lambda response: response,
)
def test_authenticate_ltpa_jwt_tokens():
    with ZosmfClient(
        "https://zosmf.example",
        ltpa_token="x2q29998U26AwfYy4vc0GlK5zItaZkkXEbGQ/...<REDACTED>.../NiM1t3FQpvWRbzTsmyr2",
        jwt_token="eyJraWQiOiJBTk9OWU1JWkVEX0tJRCIsInR5cCI6IkpXVCIsImFsZyI6IlJTMjU2In0.eyJ0b2tlbl90eXBlIjoiQmVhcmVyIiwic3Vi"
        "IjoiPFVTRVI+IiwidXBuIjoiPFVTRVI+IiwiZ3JvdXBzIjpbIkdST1VQX0EiLCJHUk9VUF9CIiwiR1JPVVBfQyJdLCJyZWFsbSI6IjxS"
        "RUFMTT4iLCJpc3MiOiI8SVNTVUVSPiIsImV4cCI6MTIzNDU2Nzg5MCwiaWF0IjoxMjM0NTYwMDAwfQ.<SIGNATURE_REDACTED>",
    ) as client:
        assert client.authenticate() == LoginOk(
            returnCode=0,
            reasonCode=0,
            message="Success.",
            ltpa_token="x2q29998U26AwfYy4vc0GlK5zItaZkkXEbGQ/...<REDACTED>.../NiM1t3FQpvWRbzTsmyr2",
            jwt_token="eyJraWQiOiJBTk9OWU1JWkVEX0tJRCIsInR5cCI6IkpXVCIsImFsZyI6IlJTMjU2In0.eyJ0b2tlbl90eXBlIjoiQmVhcmVyIiwic3Vi"
            "IjoiPFVTRVI+IiwidXBuIjoiPFVTRVI+IiwiZ3JvdXBzIjpbIkdST1VQX0EiLCJHUk9VUF9CIiwiR1JPVVBfQyJdLCJyZWFsbSI6IjxS"
            "RUFMTT4iLCJpc3MiOiI8SVNTVUVSPiIsImV4cCI6MTIzNDU2Nzg5MCwiaWF0IjoxMjM0NTYwMDAwfQ.<SIGNATURE_REDACTED>",
        )


@pytest.mark.vcr(
    before_record_response=lambda response: response,
)
def test_authenticate_user_pass():
    with ZosmfClient(
        "https://zosmf.example",
        username="demouser",
        password="DEMOPASS",
    ) as client:
        assert client.authenticate() == LoginOk(
            returnCode=0,
            reasonCode=0,
            message="Success.",
            ltpa_token="x2q29998U26AwfYy4vc0GlK5zItaZkkXEbGQ/...<REDACTED>.../NiM1t3FQpvWRbzTsmyr2",
            jwt_token="eyJraWQiOiJBTk9OWU1JWkVEX0tJRCIsInR5cCI6IkpXVCIsImFsZyI6IlJTMjU2In0.eyJ0b2tlbl90eXBlIjoiQmVhcmVyIiwic3Vi"
            "IjoiPFVTRVI+IiwidXBuIjoiPFVTRVI+IiwiZ3JvdXBzIjpbIkdST1VQX0EiLCJHUk9VUF9CIiwiR1JPVVBfQyJdLCJyZWFsbSI6IjxS"
            "RUFMTT4iLCJpc3MiOiI8SVNTVUVSPiIsImV4cCI6MTIzNDU2Nzg5MCwiaWF0IjoxMjM0NTYwMDAwfQ.<SIGNATURE_REDACTED>",
        )


@pytest.mark.vcr(
    before_record_response=lambda response: response,
)
def test_authentication_failure():
    with ZosmfClient(
        "https://zosmf.example",
        username="demouser",
        password="DEMOPASS",
    ) as client:
        with pytest.raises(ZosmfLoginError):
            client.authenticate()


@pytest.mark.vcr(
    before_record_response=lambda response: response,
)
def test_authentication_error():
    with ZosmfClient(
        "https://zosmf.example",
        username="demouser",
        password="DEMOPASS",
    ) as client:
        with pytest.raises(ZosmfAuthError):
            client.authenticate()


def test_insecure_and_cafile_raises_ZosmfError():
    with pytest.raises(
        ZosmfError, match="Cannot set insecure mode when cafile or cert is provided."
    ):
        client = ZosmfClient(
            "https://zosmf.example",
            insecure=True,
            cafile="/path/to/cafile",
        )
