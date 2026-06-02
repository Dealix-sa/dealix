"""Staged sending ramp + suppression filtering.

250 drafts/day is allowed. 250 sends/day is NOT until the domain is healthy
and the ramp has progressed. Hard ceilings: bounce rate < 3%, spam complaint
rate < 0.3% (Google sender guidelines) — breaching either drops the allowed
send count to zero.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from dealix.market_production_os.deliverability import ready_to_send

# phase -> (label, max sends per day)
RAMP_PHASES: dict[int, tuple[str, int]] = {
    0: ("test", 20),
    1: ("week2", 50),
    2: ("week3", 150),
    3: ("week4", 250),
}

MAX_BOUNCE_RATE = 0.03
MAX_SPAM_RATE = 0.003  # 0.3%


@dataclass(frozen=True, slots=True)
class RampDecision:
    allowed: int
    phase: int
    reasons: tuple[str, ...] = ()


def phase_cap(phase: int) -> int:
    return RAMP_PHASES.get(phase, RAMP_PHASES[0])[1]


def allowed_sends(
    phase: int,
    account: dict[str, Any],
    *,
    bounce_rate: float = 0.0,
    spam_rate: float = 0.0,
) -> int:
    """How many sends are permitted right now for this account + phase."""
    if not ready_to_send(account):
        return 0
    if bounce_rate >= MAX_BOUNCE_RATE:
        return 0
    if spam_rate >= MAX_SPAM_RATE:
        return 0
    cap = phase_cap(phase)
    remaining = max(0, int(account.get("daily_cap", 0)) - int(account.get("sent_today", 0)))
    return max(0, min(cap, remaining))


def ramp_decision(
    phase: int,
    account: dict[str, Any],
    *,
    bounce_rate: float = 0.0,
    spam_rate: float = 0.0,
) -> RampDecision:
    reasons: list[str] = []
    if not ready_to_send(account):
        reasons.append("account_not_ready")
    if bounce_rate >= MAX_BOUNCE_RATE:
        reasons.append("bounce_rate_ceiling")
    if spam_rate >= MAX_SPAM_RATE:
        reasons.append("spam_rate_ceiling")
    allowed = allowed_sends(phase, account, bounce_rate=bounce_rate, spam_rate=spam_rate)
    return RampDecision(allowed=allowed, phase=phase, reasons=tuple(reasons))


def can_advance_phase(
    current_phase: int,
    *,
    bounce_rate: float = 0.0,
    spam_rate: float = 0.0,
) -> bool:
    if current_phase >= 3:
        return False
    if bounce_rate >= MAX_BOUNCE_RATE:
        return False
    if spam_rate >= MAX_SPAM_RATE:
        return False
    return True


def filter_suppressed(recipient_hashes: Iterable[str], suppressed: Iterable[str]) -> list[str]:
    blocked = set(suppressed)
    return [h for h in recipient_hashes if h not in blocked]


def plan_batch(
    *,
    batch_id: str,
    date: str,
    account: dict[str, Any],
    phase: int,
    draft_ids: list[str],
    bounce_rate: float = 0.0,
    spam_rate: float = 0.0,
) -> dict[str, Any]:
    cap = allowed_sends(phase, account, bounce_rate=bounce_rate, spam_rate=spam_rate)
    planned = min(len(draft_ids), cap)
    return {
        "schema_version": "1.0",
        "batch_id": batch_id,
        "date": date,
        "ramp_phase": phase,
        "account_id": account.get("account_id", ""),
        "draft_ids": list(draft_ids[:planned]),
        "planned_count": planned,
        "cap": cap,
        "approved_by": "",
        "status": "planned",
    }
