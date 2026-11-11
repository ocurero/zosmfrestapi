# pyright: reportMissingImports=false


import cryptography
from cryptography.hazmat.primitives import serialization

USE_MODERN_CRYPTOGRAPHY = cryptography.__version__ != "3.3.2"


def _extract_key_from_pkcs12(
    p12_data: bytes,
    password: str,
):
    if USE_MODERN_CRYPTOGRAPHY:
        # Use cryptography.pkcs12.load_key_and_certificates() whenever
        # a modern cryptography release is available.
        #
        from cryptography.hazmat.primitives.serialization import pkcs12

        private_key, _, _ = pkcs12.load_key_and_certificates(
            p12_data,
            password.encode(),
        )
        if private_key is None:
            raise ValueError("PKCS#12 does not contain a private key")

        return private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(password.encode()),
        ).decode("utf-8")

    else:  # pragma: no cover
        # Fallback to OpenSSL.crypto.load_pkcs12() on legacy z/OS
        # environments where only older cryptography versions are
        # available.
        #
        # This fallback exists for two reasons:
        #   - Older z/OS environments could not easily use modern
        #     cryptography releases due to the Rust dependency.
        #   - cryptography 3.3.2 showed extremely poor PKCS#12
        #     performance on z/OS (~15 seconds versus <1 second
        #     with PyOpenSSL).
        #
        # Note that OpenSSL.crypto.load_pkcs12() was removed from
        # PyOpenSSL 23.3.0 (2023-10-25). This code path is therefore
        # intended solely for legacy environments.
        from OpenSSL import crypto

        return crypto.dump_privatekey(
            crypto.FILETYPE_PEM,
            crypto.load_pkcs12(p12_data, password.encode()).get_privatekey(),
            cipher="aes-256-cbc",
            passphrase=password.encode(),
        ).decode("utf-8")
