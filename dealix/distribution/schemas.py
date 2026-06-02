"""Lightweight, dependency-free JSON-Schema validation for distribution records.

The repo does not ship ``jsonschema`` as a hard dependency, so this module
implements just enough of Draft 2020-12 to validate the distribution record
types: ``required`` fields, ``type`` (incl. union types), ``enum``, ``const``,
and numeric ``minimum`` / ``maximum``. If ``jsonschema`` happens to be
installed it is used for a stricter pass; otherwise the built-in checker runs.
"""

from __future__ import annotations

import json
from functools import cache, lru_cache
from pathlib import Path
from typing import Any

from dealix.distribution.paths import SCHEMAS_DIR

_JSON_TYPES: dict[str, type | tuple[type, ...]] = {
    "string": str,
    "integer": int,
    "number": (int, float),
    "boolean": bool,
    "array": list,
    "object": dict,
    "null": type(None),
}

SCHEMA_FILES = {
    "prospect": "prospect.schema.json",
    "draft": "draft.schema.json",
    "followup": "followup.schema.json",
    "proposal": "proposal.schema.json",
    "proof_pack": "proof_pack.schema.json",
    "payment_handoff": "payment_handoff.schema.json",
    "renewal": "renewal.schema.json",
    "win_loss": "win_loss.schema.json",
}


@cache
def load_schema(name: str) -> dict[str, Any]:
    """Load a schema by short name (e.g. ``"draft"``) or filename."""
    fname = SCHEMA_FILES.get(name, name)
    path = SCHEMAS_DIR / fname
    if not path.is_file():
        raise FileNotFoundError(f"schema not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def _type_ok(value: Any, type_spec: Any) -> bool:
    if isinstance(type_spec, list):
        return any(_type_ok(value, t) for t in type_spec)
    py = _JSON_TYPES.get(type_spec)
    if py is None:
        return True
    # bool is a subclass of int — keep them distinct for "integer"/"number".
    if type_spec in ("integer", "number") and isinstance(value, bool):
        return False
    return isinstance(value, py)


def _check_property(key: str, value: Any, spec: dict[str, Any]) -> list[str]:
    errs: list[str] = []
    if "type" in spec and not _type_ok(value, spec["type"]):
        errs.append(f"{key}: expected type {spec['type']!r}, got {type(value).__name__}")
    if "const" in spec and value != spec["const"]:
        errs.append(f"{key}: must equal {spec['const']!r}")
    if "enum" in spec and value not in spec["enum"]:
        errs.append(f"{key}: {value!r} not in enum {spec['enum']!r}")
    if "minimum" in spec and isinstance(value, (int, float)) and value < spec["minimum"]:
        errs.append(f"{key}: {value} < minimum {spec['minimum']}")
    if "maximum" in spec and isinstance(value, (int, float)) and value > spec["maximum"]:
        errs.append(f"{key}: {value} > maximum {spec['maximum']}")
    return errs


def validate_record(record: dict[str, Any], schema_name: str) -> list[str]:
    """Return a list of validation errors (empty list == valid)."""
    schema = load_schema(schema_name)

    # Prefer jsonschema when available (stricter), but never hard-depend on it.
    try:  # pragma: no cover - exercised only when jsonschema is installed
        import jsonschema  # type: ignore

        validator = jsonschema.Draft202012Validator(schema)
        return [e.message for e in validator.iter_errors(record)]
    except Exception:
        pass

    errs: list[str] = []
    for req in schema.get("required", []):
        if req not in record:
            errs.append(f"missing required field: {req}")
    props: dict[str, Any] = schema.get("properties", {})
    for key, value in record.items():
        spec = props.get(key)
        if isinstance(spec, dict):
            errs.extend(_check_property(key, value, spec))
    return errs


def assert_valid(record: dict[str, Any], schema_name: str) -> None:
    """Raise ``ValueError`` if the record violates its schema."""
    errs = validate_record(record, schema_name)
    if errs:
        raise ValueError(f"{schema_name} schema validation failed: {errs}")


__all__ = ["SCHEMA_FILES", "assert_valid", "load_schema", "validate_record"]
