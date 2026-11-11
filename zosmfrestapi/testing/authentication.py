from unittest.mock import ANY

from zosmfrestapi.models.authentication import LoginOk

ltpa_token = "x2q29998U26AwfYy4vc0GlK5zItaZkkXEbGQ/...<REDACTED>.../NiM1t3FQpvWRbzTsmyr2"

jwt_token = (
    "eyJraWQiOiJBTk9OWU1JWkVEX0tJRCIsInR5cCI6IkpXVCIsImFsZyI6IlJTMjU2In0.eyJ0b2tlbl90"
    "eXBlIjoiQmVhcmVyIiwic3ViIjoiPFVTRVI+IiwidXBuIjoiPFVTRVI+IiwiZ3JvdXBzIjpbIkdST1VQX"
    "0EiLCJHUk9VUF9CIiwiR1JPVVBfQyJdLCJyZWFsbSI6IjxSRUFMTT4iLCJpc3MiOiI8SVNTVUVSPiIsImV"
    "4cCI6MTIzNDU2Nzg5MCwiaWF0IjoxMjM0NTYwMDAwfQ.<SIGNATURE_REDACTED>"
)


def make_loginok():
    return LoginOk(
        returnCode=0,
        reasonCode=0,
        message="Success.",
        ltpa_token=ANY,
        jwt_token=ANY,
    )


def make_loginok_ltpa():
    return LoginOk(
        returnCode=0,
        reasonCode=0,
        message="Success.",
        ltpa_token=ltpa_token,
        jwt_token=ANY,
    )


def make_loginok_jwt():
    return LoginOk(
        returnCode=0, reasonCode=0, message="Success.", ltpa_token=None, jwt_token=jwt_token
    )


def make_loginok_ltpa_jwt():
    return LoginOk(
        returnCode=0,
        reasonCode=0,
        message="Success.",
        ltpa_token=ltpa_token,
        jwt_token=jwt_token,
    )
