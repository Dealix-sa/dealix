"""
Data retention helpers — enforces `docs/trust/DATA_RETENTION_POLICY.md`.

Provides a small, auditable utility to:
* compute deletion-eligibility for records given a category + last-touched
  timestamp
* produce a deletion report (does not delete by itself)
* be wrapped by a scheduled job in the private repo

The deletion itself is intentionally a separate operation, requiring
founder approval — see `docs/trust/DATA_RETENTION_POLICY.md` for the
workflow. This module never auto-deletes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from enum import StrEnum


class DataCategory(StrEnum):
    PUBLIC_LEAD = "public_lead"
    BUYER_CONTACT = "buyer_contact"
    CLIENT_ENGAGEMENT = "client_engagement"
    CLIENT_CONFIDENTIAL = "client_confidential"
    APPROVAL_LOG = "approval_log"
    FINANCIAL_RECORD = "financial_record"


# Retention windows (days). Aligned with `docs/trust/DATA_RETENTION_POLICY.md`.
# `None` means indefinite retention (audit trail).
_RETENTION_DAYS: dict[DataCategory, int | None] = {
    DataCategory.PUBLIC_LEAD: None,
    DataCategory.BUYER_CONTACT: 730,  # 24 months from last interaction
    DataCategory.CLIENT_ENGAGEMENT: 730,  # engagement + 24 months
    DataCategory.CLIENT_CONFIDENTIAL: 180,  # engagement + 6 months (DPA may extend)
    DataCategory.APPROVAL_LOG: 2557,  # 7 years
    DataCategory.FINANCIAL_RECORD: 3653,  # 10 years (Saudi tax)
}


@dataclass(frozen=True)
class RetentionRecord:
    record_id: str
    category: DataCategory
    last_touched_at: datetime
    dpa_override_days: int | None = None  # for Custom AI / DPA-driven schedules


@dataclass
class DeletionReport:
    generated_at: datetime
    eligible: list[RetentionRecord] = field(default_factory=list)
    not_eligible: list[RetentionRecord] = field(default_factory=list)

    def summary(self) -> dict[str, int]:
        return {
            "eligible": len(self.eligible),
            "not_eligible": len(self.not_eligible),
            "by_category": {
                cat.value: sum(1 for r in self.eligible if r.category == cat)
                for cat in DataCategory
            },
        }


def retention_days(category: DataCategory, dpa_override: int | None = None) -> int | None:
    """Effective retention window for a category, with optional DPA override."""
    if dpa_override is not None:
        return dpa_override
    return _RETENTION_DAYS[category]


def is_eligible_for_deletion(record: RetentionRecord, now: datetime | None = None) -> bool:
    """True if the record's last-touched age exceeds its retention window."""
    days = retention_days(record.category, record.dpa_override_days)
    if days is None:
        return False
    now = now or datetime.now(UTC)
    return now - record.last_touched_at > timedelta(days=days)


def build_deletion_report(
    records: list[RetentionRecord], now: datetime | None = None
) -> DeletionReport:
    """Build a deletion report — never deletes; founder approves separately."""
    now = now or datetime.now(UTC)
    report = DeletionReport(generated_at=now)
    for r in records:
        (report.eligible if is_eligible_for_deletion(r, now) else report.not_eligible).append(r)
    return report


__all__ = [
    "DataCategory",
    "DeletionReport",
    "RetentionRecord",
    "build_deletion_report",
    "is_eligible_for_deletion",
    "retention_days",
]
