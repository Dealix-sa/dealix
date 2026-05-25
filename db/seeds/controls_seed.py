"""Hermes control library seed.

Materialises the in-memory control library (``default_library``) into a
serialisable list of dicts for database seeding. Only descriptive
metadata is captured — the executable ``fn`` lives in code.
"""

from __future__ import annotations

from typing import Any

from dealix.hermes.trust.controls import default_library


def _serialise_controls() -> list[dict[str, Any]]:
    library = default_library()
    rows: list[dict[str, Any]] = []
    for control in library.all():
        rows.append(
            {
                "control_id": control.control_id,
                "name": control.name,
                "category": control.category,
                "description": control.description,
                "default_severity": str(control.default_severity),
            }
        )
    return rows


CONTROLS: list[dict[str, Any]] = _serialise_controls()


__all__ = ["CONTROLS"]
