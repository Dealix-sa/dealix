"""
Retention — every dataset declares how long it lives. Records past their
expiry are tombstoned and excluded from any context packet.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from typing import Any

from dealix.hermes.data.classification import DataClassification


@dataclass
class RetentionPolicy:
    dataset: str
    classification: DataClassification
    retain_days: int
    purge_after_days: int

    def expiry(self, created_at: datetime) -> datetime:
        return created_at + timedelta(days=self.retain_days)

    def purge_deadline(self, created_at: datetime) -> datetime:
        return created_at + timedelta(days=self.purge_after_days)


DEFAULT_POLICIES: dict[str, RetentionPolicy] = {
    "audit_log": RetentionPolicy("audit_log", DataClassification.CONFIDENTIAL, 365, 1825),
    "outcome_records": RetentionPolicy("outcome_records", DataClassification.INTERNAL, 730, 1825),
    "lead_data": RetentionPolicy("lead_data", DataClassification.REGULATED, 180, 365),
    "customer_deliverables": RetentionPolicy("customer_deliverables", DataClassification.CONFIDENTIAL, 1095, 1825),
    "sovereign_memory": RetentionPolicy("sovereign_memory", DataClassification.SOVEREIGN, 36500, 36500),
}


@dataclass
class RetentionResult:
    kept: list[dict[str, Any]] = field(default_factory=list)
    expired: list[dict[str, Any]] = field(default_factory=list)
    purged: list[dict[str, Any]] = field(default_factory=list)


def apply_retention(
    records: list[dict[str, Any]],
    *,
    dataset: str,
    now: datetime | None = None,
) -> RetentionResult:
    policy = DEFAULT_POLICIES.get(dataset)
    if policy is None:
        raise KeyError(f"no retention policy for dataset {dataset!r}")
    now = now or datetime.now(UTC)
    result = RetentionResult()
    for r in records:
        created = r.get("created_at")
        if isinstance(created, str):
            created = datetime.fromisoformat(created)
        if not isinstance(created, datetime):
            result.kept.append(r)
            continue
        if now >= policy.purge_deadline(created):
            result.purged.append(r)
        elif now >= policy.expiry(created):
            result.expired.append(r)
        else:
            result.kept.append(r)
    return result
