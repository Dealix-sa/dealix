"""Seed lead validation for the Commercial Launch OS.

Validates a JSONL lead file without requiring real data to exist. Used by
scripts/commercial_seed_leads_validate.py and tests.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from dealix.commercial_launch.engine import ROOT, load_config

VALID_COUNTRIES = {"SA", "AE", "QA", "KW", "BH", "OM"}


@dataclass
class LeadValidationResult:
    path: str
    total: int = 0
    valid: int = 0
    errors: list[dict[str, Any]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    file_exists: bool = True

    @property
    def passed(self) -> bool:
        # An empty / missing lead file is allowed (placeholder mode), but any
        # malformed row that IS present is an error.
        return len(self.errors) == 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "file_exists": self.file_exists,
            "total": self.total,
            "valid": self.valid,
            "passed": self.passed,
            "errors": self.errors,
            "warnings": self.warnings,
        }


def validate_lead_file(path: Path, config: dict[str, Any] | None = None) -> LeadValidationResult:
    cfg = config or load_config()
    valid_verticals = {v["id"] for v in cfg["verticals"]["verticals"]}
    result = LeadValidationResult(path=str(path))

    if not path.exists():
        result.file_exists = False
        result.warnings.append(
            "Lead file does not exist. The generator will run in placeholder mode "
            "(research_required drafts). This is allowed but not send-ready."
        )
        return result

    for idx, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        raw = raw.strip()
        if not raw or raw.startswith("#"):
            continue
        result.total += 1
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError as exc:
            result.errors.append({"line": idx, "error": f"invalid_json: {exc}"})
            continue
        row_errors = []
        if not (obj.get("company_name") or obj.get("company")):
            row_errors.append("missing_company_name")
        vert = obj.get("vertical")
        if not vert:
            row_errors.append("missing_vertical")
        elif vert not in valid_verticals:
            row_errors.append(f"unknown_vertical:{vert}")
        country = obj.get("country", "SA")
        if country not in VALID_COUNTRIES:
            result.warnings.append(f"line {idx}: unusual country '{country}'")
        # Personal-email scraping guard: flag obviously personal addresses.
        email = (obj.get("email") or "").lower()
        if any(dom in email for dom in ("@gmail.", "@hotmail.", "@yahoo.", "@outlook.")):
            result.warnings.append(f"line {idx}: personal email domain — prefer a business address, do not scrape")
        if row_errors:
            result.errors.append({"line": idx, "errors": row_errors})
        else:
            result.valid += 1

    if result.total == 0:
        result.warnings.append("Lead file is empty — placeholder mode will be used.")
    return result


def default_lead_path() -> Path:
    real = ROOT / "data" / "commercial_seed_leads.jsonl"
    if real.exists():
        return real
    return ROOT / "data" / "commercial_seed_leads.example.jsonl"
