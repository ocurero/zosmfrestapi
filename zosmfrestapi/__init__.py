"""Synchronous Python client for the z/OSMF REST API.

The package root re-exports :class:`ZosmfClient` and :class:`ZosmfZcryptoClient`.
Create one client per server/configuration and use it as a context manager to close
the shared HTTP session when finished.
"""

from zosmfrestapi.client import ZosmfClient
from zosmfrestapi.zcrypto_client import ZosmfZcryptoClient

__all__ = ["ZosmfClient", "ZosmfZcryptoClient"]
