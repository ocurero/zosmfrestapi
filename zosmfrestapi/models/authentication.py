from dataclasses import dataclass


@dataclass
class LoginOk:
    """Successful response from the z/OSMF authentication endpoint.

    The endpoint return fields are preserved alongside any LTPA or JWT token
    cookies returned by the server.
    """

    returnCode: int
    reasonCode: int
    message: str
    ltpa_token: str | None = None
    jwt_token: str | None = None
