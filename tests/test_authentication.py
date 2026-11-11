from unittest.mock import ANY, patch

import pytest
from zosmfrestapi import LoginOk, ZosmfAuthError, ZosmfClient, ZosmfLoginError
from zosmfrestapi.testing import (
    make_loginok,
    make_loginok_jwt,
    make_loginok_ltpa,
    make_loginok_ltpa_jwt,
)
from zosmfrestapi.testing.authentication import jwt_token, ltpa_token


@pytest.mark.vcr()
def test_unauthenticated_raises_ZosmfAuthError():
    client = ZosmfClient("https://zosmf.example")
    with pytest.raises(ZosmfAuthError):
        client.read_dataset("MY.DATASET")


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
            assert login == make_loginok()

        load_cert_chain.assert_called_once_with(certfile="/path/to/cert.pem")


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
    """Test authentication using an LTPA token.
    A JWT token will be returned if JWT tokens are enabled by z/OSMF."""
    with ZosmfClient(
        "https://zosmf.example",
        ltpa_token=ltpa_token,
    ) as client:
        assert client.authenticate() == make_loginok_ltpa()


@pytest.mark.vcr(
    before_record_response=lambda response: response,
)
def test_authenticate_jwt_token():
    """Test authentication using a JWT token.
    A LTPA2 token is not returned by z/OSMF if JWT tokens are enabled by z/OSMF."""
    with ZosmfClient("https://zosmf.example", jwt_token=jwt_token) as client:
        assert client.authenticate() == make_loginok_jwt()


@pytest.mark.vcr(
    before_record_response=lambda response: response,
)
def test_authenticate_ltpa_jwt_tokens():
    with ZosmfClient(
        "https://zosmf.example", ltpa_token=ltpa_token, jwt_token=jwt_token
    ) as client:
        assert client.authenticate() == make_loginok_ltpa_jwt()


@pytest.mark.vcr(
    before_record_response=lambda response: response,
)
def test_authenticate_user_pass():
    with ZosmfClient(
        "https://zosmf.example",
        username="demouser",
        password="DEMOPASS",
    ) as client:
        assert client.authenticate() == make_loginok_ltpa_jwt()


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
