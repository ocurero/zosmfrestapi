import logging
import ssl
from importlib.metadata import version
from types import TracebackType
from typing import Literal, Self

import httpx2
from zosmfrestapi.exceptions import ZosmfAuthError, ZosmfError

__version__ = version("zosmfrestapi")
logger = logging.getLogger(__name__)


class ZosmfBase:
    """Shared HTTP client and request handling for the service mixins.

    :class:`ZosmfClient` inherits the operations provided by the service mixins;
    this base class configures their shared ``httpx2.Client`` and manages its
    lifetime. Use a client as a context manager when possible so the connection
    pool is closed deterministically.
    """

    def __init__(
        self,
        server: str,
        username: str | None = None,
        password: str | None = None,
        cert: str | tuple[str, str] | None = None,
        key_password: str | None = None,
        ltpa_token: str | None = None,
        jwt_token: str | None = None,
        jwt_cookie_name: str = "jwtToken",
        proxy: str | None = None,
        proxyusername: str = "",
        proxypassword: str = "",
        insecure: bool = False,
        cafile: None | str = None,
        encoding: str | None = None,
    ) -> None:
        """Create an HTTP client for communicating with z/OSMF.

        Args:
            server: Base URL of the z/OSMF server, including its scheme and
                optional port or base path.
            username: Optional user ID for HTTP basic authentication. Basic
                authentication is configured only when both ``username`` and
                ``password`` are non-empty.
            password: Password paired with ``username`` for basic
                authentication.
            cert: Optional client certificate configuration. Pass a path to a
                PEM file containing both the certificate and private key, or
                a ``(certificate_path, private_key_path)`` tuple for separate
                files.
            key_password: Optional private key password. Pass the private key
                password if the key is password protected.
            ltpa_token: Optional LTPA token sent as the ``LtpaToken2`` cookie.
            jwt_token: Optional JWT sent as the cookie named by
                ``jwt_cookie_name``. If both token types are provided, both
                cookies are sent.
            jwt_cookie_name: Cookie name used for ``jwt_token``. Defaults to
                ``"jwtToken"``.
            proxy: Optional proxy URL used for HTTP requests.
            proxyusername: Optional proxy user ID. Used with
                ``proxypassword`` when proxy authentication is configured.
            proxypassword: Optional proxy password.
            insecure: Disable TLS certificate verification when true. This
                cannot be combined with ``cert`` or ``cafile``.
            cafile: Optional CA certificate file added to the default trust
                store. It can be combined with ``cert``.
            encoding: Reserved compatibility parameter; currently unused.

        Raises:
            ZosmfError: If ``insecure`` is combined with ``cert`` or ``cafile``.
        """
        if insecure and (cafile or cert):
            raise ZosmfError("Cannot set insecure mode when cafile or cert is provided.")

        verify: bool | ssl.SSLContext
        if insecure:
            logger.debug("Insecure mode enabled, TLS certificate verification is disabled.")
            verify = False
        else:
            ctx = ssl.create_default_context()
            if isinstance(cert, tuple):
                certfile, keyfile = cert
                ctx.load_cert_chain(certfile=certfile, keyfile=keyfile, password=key_password)
            elif cert:
                ctx.load_cert_chain(certfile=cert)
            if cafile:
                ctx.load_verify_locations(cafile=cafile)
            verify = ctx

        proxy_config: str | httpx2.Proxy | None = proxy
        if proxy:
            proxy_config = httpx2.Proxy(proxy)
            proxy_config.auth = (
                (proxyusername, proxypassword) if proxyusername or proxypassword else None
            )
        auth = (username, password) if username and password else None
        headers = {
            "X-CSRF-ZOSMF-HEADER": "zosmfrestapi",
            "User-Agent": f"zosmfrestapi/{__version__}",
        }
        if ltpa_token:
            headers["Cookie"] = f"LtpaToken2={ltpa_token}"
        if jwt_token:
            headers["Cookie"] = f"{jwt_cookie_name}={jwt_token}"
        if ltpa_token and jwt_token:
            headers["Cookie"] = f"LtpaToken2={ltpa_token}; {jwt_cookie_name}={jwt_token}"
        self.http = httpx2.Client(
            base_url=server,
            proxy=proxy_config,
            verify=verify,
            auth=auth,
            headers=headers,
        )

        self.base_url = server
        self.username = username
        self.password = password
        self.insecure = insecure
        self.cert = cert
        self.cafile = cafile
        self.ltpa_token = ltpa_token
        self.jwt_token = jwt_token
        self.jwt_cookie_name = jwt_cookie_name
        self.proxy = proxy_config
        self.proxyusername = proxyusername
        self.proxypassword = proxypassword

    def _raise_for_status(
        self,
        response: httpx2.Response,
        exc_handler: type[ZosmfError] = ZosmfError,
    ) -> None:
        """Raise a package exception for an unsuccessful HTTP response.

        HTTP 401 responses are translated to :class:`ZosmfAuthError`; other
        HTTP status errors are wrapped using ``exc_handler``.

        Args:
            response: Response returned by the shared HTTP client.
            exc_handler: Exception class used for non-authentication status
                errors. Defaults to :class:`ZosmfError`.

        Raises:
            ZosmfAuthError: If the response status is 401.
            ZosmfError: Or ``exc_handler`` for another unsuccessful status.
        """
        try:
            response.raise_for_status()
        except httpx2.HTTPStatusError as exc:
            if exc.response.status_code == 401:
                raise ZosmfAuthError(exc) from exc
            raise exc_handler(exc) from exc

    def close(self) -> None:
        """Close the shared HTTP client and release its connection resources.

        Call this when the client is no longer needed. Exiting a ``with`` block
        also calls this method.
        """
        self.http.close()

    def __enter__(self) -> Self:
        """Return this client for use in a ``with`` statement."""
        return self

    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        exception: BaseException | None,
        traceback: TracebackType | None,
    ) -> Literal[False]:
        """Close the HTTP client without suppressing an exception from the block.

        The exception arguments follow the context-manager protocol; they are
        not inspected by this implementation.
        """
        self.close()
        return False
