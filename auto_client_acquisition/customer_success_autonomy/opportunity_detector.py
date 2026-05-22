"""Deterministic opportunity detector for the CS autonomy cycle.

Given one ``CustomerSignalSnapshot``, returns the list of retention
opportunities the founder should act on. Pure function — no I/O.

Five opportunity kinds are detected:
  * renewal_due           — a renewal schedule is past or near its next attempt
  * expansion_ready       — expansion readiness + healthy/expansion_ready health
  * churn_intervention    — churn bucket is critical
  * nps_detractor_follow_up — most recent NPS < 7
  * adoption_friction     — adoption score < 55 AND health bucket at_risk/critical

Every opportunity carries a bilingual recommended_action and a
``requires_external_send`` flag — callers route those that need a customer
touch through the founder approval queue.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any

from auto_client_acquisition.customer_success_autonomy.signal_aggregator import (
    CustomerSignalSnapshot,
)

Urgency = str  # "low" | "normal" | "urgent"

_HEALTHY_BUCKETS: frozenset[str] = frozenset({"expansion_ready", "healthy"})
_AT_RISK_BUCKETS: frozenset[str] = frozenset({"at_risk", "critical"})


@dataclass
class Opportunity:
    """One retention opportunity surfaced by the detector."""

    type: str
    customer_id: str
    urgency: Urgency = "normal"
    recommended_action_ar: str = ""
    recommended_action_en: str = ""
    evidence: tuple[str, ...] = field(default_factory=tuple)
    requires_external_send: bool = False
    payload: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["evidence"] = list(self.evidence)
        return data


def _renewal_is_due(renewal: dict[str, Any]) -> bool:
    if not renewal.get("has_schedule"):
        return False
    status = str(renewal.get("status", "")).lower()
    if status not in {"scheduled", "awaiting_founder", ""}:
        return False
    next_at = str(renewal.get("next_attempt_at", "")).strip()
    if not next_at:
        return True  # scheduled but no date — treat as due now
    try:
        when = datetime.fromisoformat(next_at.replace("Z", "+00:00"))
    except ValueError:
        return True
    if when.tzinfo is None:
        when = when.replace(tzinfo=timezone.utc)
    return when <= datetime.now(timezone.utc)


def detect_opportunities(snapshot: CustomerSignalSnapshot) -> list[Opportunity]:
    """Return a deduplicated list of opportunities for one customer."""
    out: list[Opportunity] = []
    seen: set[str] = set()

    def _add(opp: Opportunity) -> None:
        if opp.type in seen:
            return
        seen.add(opp.type)
        out.append(opp)

    cid = snapshot.customer_id
    health_bucket = str((snapshot.health or {}).get("bucket", "")).lower()
    churn_bucket = str((snapshot.churn or {}).get("bucket", "")).lower()
    adoption_score = float((snapshot.adoption or {}).get("score", 0.0))
    expansion_ready = bool((snapshot.expansion or {}).get("ready", False))

    # --- renewal_due ---------------------------------------------------
    if _renewal_is_due(snapshot.renewal_status):
        renewal = snapshot.renewal_status
        _add(
            Opportunity(
                type="renewal_due",
                customer_id=cid,
                urgency="normal",
                recommended_action_ar="جدّد الاشتراك مع العميل وتأكّد من سلامة الدفعة.",
                recommended_action_en="Confirm renewal with the customer and verify the payment.",
                evidence=(
                    f"schedule:{renewal.get('schedule_id', '')}",
                    f"amount_sar:{renewal.get('amount_sar', 0)}",
                ),
                requires_external_send=True,
                payload={"renewal_status": renewal},
            )
        )

    # --- expansion_ready ----------------------------------------------
    if expansion_ready and health_bucket in _HEALTHY_BUCKETS:
        _add(
            Opportunity(
                type="expansion_ready",
                customer_id=cid,
                urgency="normal",
                recommended_action_ar="اقترح ترقية أو خدمة إضافية مبنية على نتائج مثبتة.",
                recommended_action_en="Propose an upgrade or add-on grounded in proven results.",
                evidence=(
                    f"health:{health_bucket}",
                    f"expansion_score:{(snapshot.expansion or {}).get('score', 0)}",
                ),
                requires_external_send=True,
                payload={"expansion": snapshot.expansion},
            )
        )

    # --- churn_intervention -------------------------------------------
    if churn_bucket == "critical":
        _add(
            Opportunity(
                type="churn_intervention",
                customer_id=cid,
                urgency="urgent",
                recommended_action_ar="تدخّل المؤسس شخصياً اليوم — مكالمة لفهم السبب وعرض حل.",
                recommended_action_en="Founder personal outreach today — call to understand and offer a remedy.",
                evidence=(f"churn_bucket:{churn_bucket}",)
                + tuple(
                    f"signal:{s}" for s in (snapshot.churn or {}).get("signals_active", [])
                ),
                requires_external_send=True,
                payload={"churn": snapshot.churn},
            )
        )

    # --- nps_detractor_follow_up --------------------------------------
    nps = snapshot.recent_nps_score
    if isinstance(nps, int) and nps < 7:
        _add(
            Opportunity(
                type="nps_detractor_follow_up",
                customer_id=cid,
                urgency="urgent" if nps <= 4 else "normal",
                recommended_action_ar="اتصل بالعميل خلال 24 ساعة — لا تبيع، اسمع.",
                recommended_action_en="Reach out within 24 hours — do not pitch, listen.",
                evidence=(
                    f"nps:{nps}",
                    f"milestone:{snapshot.recent_nps_milestone or ''}",
                ),
                requires_external_send=True,
                payload={"nps_score": nps, "milestone": snapshot.recent_nps_milestone},
            )
        )

    # --- adoption_friction --------------------------------------------
    if adoption_score < 55 and health_bucket in _AT_RISK_BUCKETS:
        _add(
            Opportunity(
                type="adoption_friction",
                customer_id=cid,
                urgency="normal",
                recommended_action_ar="جلسة تمكين قصيرة لإزالة عوائق التبنّي قبل تجديد الاشتراك.",
                recommended_action_en="Run a short enablement session to clear adoption blockers before renewal.",
                evidence=(
                    f"adoption_score:{adoption_score}",
                    f"health:{health_bucket}",
                ),
                requires_external_send=False,
                payload={"adoption": snapshot.adoption},
            )
        )

    return out


__all__ = [
    "Opportunity",
    "detect_opportunities",
]
