"""Prospect intake — load + validate the distribution input set.

Validation reuses Revenue OS anti-waste so a blocked ingestion source
(scraping / cold_whatsapp / purchased_list / linkedin_automation) is rejected
at the door, consistent with the rest of the platform.
"""

from __future__ import annotations

from typing import Any

from auto_client_acquisition.distribution_os.models import (
    Channel,
    Prospect,
    ProspectStatus,
)
from auto_client_acquisition.distribution_os.store import prospects_path, read_json
from auto_client_acquisition.revenue_os.anti_waste import validate_pipeline_step

REQUIRED_FIELDS: tuple[str, ...] = ("id", "company", "sector", "status", "source")

_VALID_STATUSES = {s.value for s in ProspectStatus}
_VALID_CHANNELS = {c.value for c in Channel}


def validate_prospect_dict(data: dict[str, Any]) -> list[str]:
    """Return a list of validation errors for a single prospect dict (empty = ok)."""
    errors: list[str] = []
    for f in REQUIRED_FIELDS:
        if not str(data.get(f, "")).strip():
            errors.append(f"missing_required:{f}")

    status = str(data.get("status", "")).strip()
    if status and status not in _VALID_STATUSES:
        errors.append(f"invalid_status:{status}")

    channel = str(data.get("preferred_channel", "")).strip()
    if channel and channel not in _VALID_CHANNELS:
        errors.append(f"invalid_channel:{channel}")

    # Anti-waste: blocked ingestion sources are never allowed.
    source = str(data.get("source", "")).strip()
    if source:
        violations = validate_pipeline_step(
            has_decision_passport=True,
            lead_source=source,
            action_external=False,
            upsell_attempt=False,
            proof_event_count=1,
        )
        errors.extend(f"blocked_source:{v.code}" for v in violations if v.code == "blocked_source")

    return errors


def load_prospects(path: Any = None, *, strict: bool = False) -> list[Prospect]:
    """Load prospects from JSON (defaults to the configured/seed path).

    ``strict=True`` raises on any validation error; otherwise invalid rows are
    skipped (the caller can re-run validation for reporting).
    """
    src = path if path is not None else prospects_path()
    raw = read_json(src) or []
    if isinstance(raw, dict):  # allow {"prospects": [...]} envelope
        raw = raw.get("prospects", [])

    prospects: list[Prospect] = []
    for row in raw:
        errs = validate_prospect_dict(row)
        if errs:
            if strict:
                raise ValueError(f"invalid prospect {row.get('id', '?')}: {errs}")
            continue
        prospects.append(Prospect.from_dict(row))
    return prospects


__all__ = [
    "REQUIRED_FIELDS",
    "load_prospects",
    "validate_prospect_dict",
]
