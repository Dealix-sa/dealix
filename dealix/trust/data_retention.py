"""
Data retention policy.

Maps data categories to maximum retention days. Used by jobs that prune
old records and by the privacy-impact assessment template.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


_RETENTION_DAYS: dict[str, int] = {
    "lead_contact": 365,
    "call_note": 730,
    "proposal_draft": 1095,
    "payment_record": 2555,  # 7y
    "audit_log": 2555,        # 7y
    "raw_inference_log": 30,
    "ai_chat_history": 90,
}


@dataclass(frozen=True, slots=True)
class RetentionDecision:
    category: str
    keep: bool
    expires_at: datetime


def policy(category: str) -> int:
    return _RETENTION_DAYS.get(category, 90)


def evaluate(category: str, created_at: datetime, *, now: datetime | None = None) -> RetentionDecision:
    now = now or datetime.now(timezone.utc)
    horizon = timedelta(days=policy(category))
    expires_at = created_at + horizon
    return RetentionDecision(category=category, keep=now < expires_at, expires_at=expires_at)
