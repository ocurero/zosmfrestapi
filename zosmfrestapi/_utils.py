from dataclasses import fields, is_dataclass
from typing import Any

import pendulum


def parse_datetime(value: str) -> pendulum.DateTime:
    """Parse a string and require a Pendulum ``DateTime`` result.

    Args:
        value: Date/time string accepted by :func:`pendulum.parse`.

    Returns:
        The parsed timezone-aware or naive Pendulum ``DateTime`` value.

    Raises:
        TypeError: If Pendulum parses the input as a date, time, duration, or
            another non-``DateTime`` value.
    """
    result = pendulum.parse(value)

    if not isinstance(result, pendulum.DateTime):
        raise TypeError(f"Expected DateTime, got {type(result)}")

    return result


def remap(data: dict[str, Any], cls: type[Any]) -> dict[str, Any]:
    """Translate JSON field aliases to the names used by a dataclass.

    Dataclass fields with ``metadata={"json_name": ...}`` are mapped from
    their external JSON key back to the Python field name. Other keys and
    values are preserved.

    Args:
        data: Mapping-like dictionary received from an API response.
        cls: Dataclass type whose field metadata defines the aliases.

    Returns:
        A new dictionary with aliased keys remapped; ``data`` is not modified.
    """
    aliases = {
        f.metadata["json_name"]: f.name for f in fields(cls) if "json_name" in f.metadata
    }

    return {aliases.get(k, k): v for k, v in data.items()}


def to_dict(obj: object) -> Any:
    """Recursively convert dataclasses and containers to JSON payload values.

    Dataclass fields are converted to dictionaries, respecting each field's
    ``json_name`` metadata. Lists and dictionaries are converted recursively;
    other values are returned unchanged.

    Args:
        obj: Dataclass instance, list, dictionary, or scalar value to convert.

    Returns:
        The recursively converted value. Leaves are preserved, so callers
        should supply JSON-compatible scalar values when using the result as an
        HTTP JSON body.
    """
    if is_dataclass(obj):
        return {
            f.metadata.get("json_name", f.name): to_dict(getattr(obj, f.name))
            for f in fields(obj)
        }

    if isinstance(obj, list):
        return [to_dict(item) for item in obj]

    if isinstance(obj, dict):
        return {key: to_dict(value) for key, value in obj.items()}

    return obj
