import pendulum
import pytest

from zosmfrestapi import _utils


def test_parse_datetime_returns_datetime():
    value = "2026-10-30T12:34:56Z"

    assert _utils.parse_datetime(value) == pendulum.parse(value)


def test_parse_datetime_raises_for_non_datetime(monkeypatch):
    monkeypatch.setattr(_utils.pendulum, "parse", lambda _: None)

    with pytest.raises(TypeError, match="Expected DateTime, got <class 'NoneType'>"):
        _utils.parse_datetime("2026-10-30T12:34:56Z")
