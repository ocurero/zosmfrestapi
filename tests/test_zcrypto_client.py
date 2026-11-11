from unittest.mock import MagicMock, patch

import pendulum
import pytest
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import BestAvailableEncryption, pkcs12
from cryptography.x509.oid import NameOID

from zosmfrestapi.zcrypto import _extract_key_from_pkcs12


@pytest.fixture
def zcrypto_client():
    with (
        patch("platform.system", return_value="OS/390"),
        patch.dict(
            "sys.modules",
            {"py_zcrypto": MagicMock()},
        ),
    ):
        from zosmfrestapi import ZosmfZcryptoClient

        yield ZosmfZcryptoClient


@patch("ssl.SSLContext.load_cert_chain")
@patch("zosmfrestapi.zcrypto_client._extract_key_from_pkcs12")
def test_ZosmfZCryptoClient(mock_extract, mock_load_cert_chain, zcrypto_client):

    mock_extract.return_value = """
    -----BEGIN PRIVATE KEY-----
    dummy
    -----END PRIVATE KEY-----
    """
    with zcrypto_client("https://zosmf.example", keyring="keyring_name", label="RACF label"):
        pass


def test_extract_key_from_pkcs12_modern():

    password = "secret"

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    subject = issuer = x509.Name(
        [
            x509.NameAttribute(
                NameOID.COMMON_NAME,
                "pytest",
            ),
        ]
    )

    certificate = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(pendulum.now())
        .not_valid_after(pendulum.now().add(days=1))
        .sign(private_key, hashes.SHA256())
    )

    p12_data = pkcs12.serialize_key_and_certificates(
        b"alias",
        private_key,
        certificate,
        None,
        BestAvailableEncryption(password.encode()),
    )

    pem = _extract_key_from_pkcs12(
        p12_data,
        password,
    )

    assert "BEGIN ENCRYPTED PRIVATE KEY" in pem


def test_fails_when_not_zos():
    from zosmfrestapi import ZosmfZcryptoClient

    with pytest.raises(RuntimeError, match="The zcrypto backend is only available on z/OS."):
        with ZosmfZcryptoClient():
            pass


@patch("cryptography.hazmat.primitives.serialization.pkcs12.load_key_and_certificates")
def test_extract_key_from_pkcs12_without_private_key(mock_load):
    mock_load.return_value = (
        None,  # private_key
        object(),  # certificate
        [],  # additional_certs
    )

    with pytest.raises(
        ValueError,
        match="PKCS#12 does not contain a private key",
    ):
        _extract_key_from_pkcs12(
            b"dummy",
            "secret",
        )


def test_ZosmfZCryptoClient_missing_options(zcrypto_client):
    import sys

    print(sys.modules["py_zcrypto"])
    with pytest.raises(KeyError):
        with zcrypto_client():
            pass
