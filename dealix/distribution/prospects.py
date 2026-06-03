"""Prospect loading + validation.

Prospects are **founder-sourced** (referral / inbound / network / event) — the
OS never scrapes. The default source is the tracked synthetic example file; in
real use the founder points ``--prospects`` at a gitignored file with real data.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from dealix.distribution.paths import PROSPECTS_EXAMPLE_JSON
from dealix.distribution.schemas import validate_record


def load_prospects(path: Path | None = None) -> list[dict[str, Any]]:
    """Load prospects from a JSON file (``{"prospects": [...]}`` or a bare list)."""
    p = path or PROSPECTS_EXAMPLE_JSON
    if not p.is_file():
        return []
    data = json.loads(p.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        items = data.get("prospects") or []
    elif isinstance(data, list):
        items = data
    else:
        items = []
    return [x for x in items if isinstance(x, dict)]


def validate_prospects(prospects: list[dict[str, Any]]) -> dict[str, Any]:
    """Validate each prospect against the schema; return a summary."""
    errors: list[dict[str, Any]] = []
    for pr in prospects:
        errs = validate_record(pr, "prospect")
        if errs:
            errors.append({"id": pr.get("id") or pr.get("company"), "errors": errs})
    return {
        "total": len(prospects),
        "valid": len(prospects) - len(errors),
        "invalid": len(errors),
        "errors": errors,
        "ok": not errors,
    }


__all__ = ["load_prospects", "validate_prospects"]
