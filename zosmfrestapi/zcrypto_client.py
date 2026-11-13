import platform
import secrets
import ssl
from tempfile import NamedTemporaryFile

from zosmfrestapi.client import ZosmfClient


class ZosmfZcryptoClient(ZosmfClient):
    """Create an HTTP client for communicating with z/OSMF using a
    client certificate stored in a SAF key ring.

    This class behaves like ``ZosmfClient`` but retrieves the client
    certificate and private key from a SAF key ring using ``py_zcrypto``.
    The certificate material is exported to temporary PEM files and
    configured automatically for mutual TLS (mTLS) authentication.

    Example:
        Use a client with mTLS authentication using a certificate stored
        in a SAF key ring:

            with ZosmfClient(
                "https://zosmf.example",
                keyring="USERID/SAF_key_ring_name",
                label="Certificate label",
            ) as client:
                systems = client.get_systems()

    Additional Args:
        keyring: SAF key ring name. The format can be either
            ``keyring_name`` or ``USERID/keyring_name``.

        label: Label of the certificate in the SAF key ring.

    Notes:
        The ``zcrypto`` optional dependency must be installed:

            pip install "zosmfrestapi[zcrypto]"

        All other arguments are inherited from ``ZosmfClient``.
    """

    def __init__(self, *args, **kwargs):
        if platform.system() != "OS/390":
            raise RuntimeError("The zcrypto backend is only available on z/OS.")
        import py_zcrypto  # pyright: ignore[reportMissingImports]

        from zosmfrestapi.zcrypto import _extract_key_from_pkcs12

        keyring = kwargs.pop("keyring")
        label = kwargs.pop("label")
        zcrypto_obj = py_zcrypto.zcrypto()
        zcrypto_obj.open_key_ring(keyring)
        password = secrets.token_urlsafe(32)
        with NamedTemporaryFile(mode="w") as key_pem, NamedTemporaryFile(mode="w") as cert_pem:

            key = _extract_key_from_pkcs12(
                bytes(zcrypto_obj.export_key_to_buffer(password, label)), password
            )
            cert = ssl.DER_cert_to_PEM_cert(bytes(zcrypto_obj.export_cert_to_buffer(label)))

            key_pem.write(key)
            cert_pem.write(cert)
            key_pem.flush()
            cert_pem.flush()

            super().__init__(
                *args, **kwargs, cert=(cert_pem.name, key_pem.name), key_password=password
            )
