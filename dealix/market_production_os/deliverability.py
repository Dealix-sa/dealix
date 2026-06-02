"""Sending-domain health evaluation.

Bulk senders to Gmail must set SPF + DKIM + DMARC, offer one-click
unsubscribe, and keep spam rate < 0.3% (Google Email sender guidelines).
Cold outreach must run on a dedicated domain, never the primary brand domain.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

# weighted health components -> points
_WEIGHTS: dict[str, int] = {
    "spf": 15,
    "dkim": 15,
    "dmarc": 15,
    "dedicated_domain": 15,
    "custom_tracking_domain": 10,
    "postmaster_connected": 10,
    "bounce_handling": 10,
    "unsubscribe_endpoint": 10,
}
# hard requirements for any send
_REQUIRED: tuple[str, ...] = (
    "spf",
    "dkim",
    "dmarc",
    "dedicated_domain",
    "unsubscribe_endpoint",
    "bounce_handling",
)


@dataclass(frozen=True, slots=True)
class DeliverabilityResult:
    ready: bool
    health_score: int
    reasons: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "ready": self.ready,
            "health_score": self.health_score,
            "reasons": list(self.reasons),
        }


def evaluate_account(account: dict[str, Any]) -> DeliverabilityResult:
    reasons: list[str] = []
    score = 0
    for key, weight in _WEIGHTS.items():
        if account.get(key):
            score += weight
        else:
            reasons.append(f"missing:{key}")

    if account.get("dmarc") and account.get("dmarc_policy") in ("none", "absent"):
        reasons.append("dmarc_policy_not_enforced")

    warmup = account.get("warmup_status", "cold")
    if warmup == "cold":
        reasons.append("domain_not_warmed")

    ready = all(account.get(k) for k in _REQUIRED) and warmup != "cold"
    return DeliverabilityResult(ready=ready, health_score=min(score, 100), reasons=tuple(reasons))


def ready_to_send(account: dict[str, Any]) -> bool:
    return evaluate_account(account).ready
