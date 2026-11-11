import logging

from zosmfrestapi.exceptions import ZosmfAuthError
from zosmfrestapi.exceptions.authentication import ZosmfLoginError
from zosmfrestapi.models.authentication import LoginOk

from . import ZosmfBase

logger = logging.getLogger(__name__)


class AuthenticationServices(ZosmfBase):
    """Authentication operations for the shared z/OSMF client.

    The configured credentials and tokens are sent by the shared HTTP client.
    The client certificate, basic authentication, and token cookies are all
    configured during :class:`ZosmfBase` initialization.
    """

    def authenticate(self) -> LoginOk | None:
        """Authenticate against the z/OSMF authentication endpoint.

        This method posts to ``/zosmf/services/authenticate`` using the
        authentication configured when the client was created. It does not
        perform a separate credential negotiation or clear the configured
        token cookies.

        Returns:
            A ``LoginOk`` containing the response return/reason codes and
            message, plus any LTPA or JWT tokens returned as response cookies.

        Raises:
            ZosmfLoginError: If z/OSMF responds with HTTP 401.
            ZosmfAuthError: If another unsuccessful HTTP status is returned.
            httpx2.RequestError: If the request fails before an HTTP response
            is received.
        """
        logger.debug("Authenticating with z/OSMF using all available methods")
        resp = self.http.post("/zosmf/services/authenticate")
        if resp.status_code == 200:
            logger.debug("Authentication succeeded with z/OSMF")
            return LoginOk(
                **resp.json(),
                ltpa_token=resp.cookies.get("LtpaToken2", self.ltpa_token),
                jwt_token=resp.cookies.get(self.jwt_cookie_name, self.jwt_token),
            )
        elif resp.status_code == 401:
            logger.debug("Authentication failed with z/OSMF")
            raise ZosmfLoginError(resp)
        logger.debug("Unexpected authentication failure with z/OSMF")
        self._raise_for_status(resp, exc_handler=ZosmfAuthError)
        raise AssertionError("Unreachable")  # pragma: no cover
