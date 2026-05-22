"""Customer Success signal aggregator.

For one customer, pulls every relevant retention signal from the
existing modules into a single ``CustomerSignalSnapshot``. Every external
call is wrapped friction-safe: a failure appends a warning and falls back
to a safe default; the aggregator never crashes.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class CustomerSignalSnapshot:
    """All retention-relevant signals for one customer at one moment."""

    customer_id: str
    generated_at: str
    health: dict[str, Any] = field(default_factory=dict)
    churn: dict[str, Any] = field(default_factory=dict)
    adoption: dict[str, Any] = field(default_factory=dict)
    expansion: dict[str, Any] = field(default_factory=dict)
    proof_maturity: dict[str, Any] = field(default_factory=dict)
    value_summary: dict[str, Any] = field(default_factory=dict)
    recent_nps_score: int | None = None
    recent_nps_milestone: str | None = None
    last_payment_at: str | None = None
    renewal_status: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _safe(snapshot: CustomerSignalSnapshot, stage: str, fn: Any) -> Any:
    """Run a callable; append a warning + return None on any exception."""
    try:
        return fn()
    except Exception as exc:  # noqa: BLE001 — friction-safe by design
        snapshot.warnings.append(f"{stage}: {type(exc).__name__}: {exc}")
        return None


def aggregate_customer_signals(
    customer_id: str,
    *,
    on_date: Any = None,
    inputs: dict[str, Any] | None = None,
) -> CustomerSignalSnapshot:
    """Return a snapshot of every retention signal for ``customer_id``.

    ``inputs`` lets the caller inject per-customer raw numbers (logins,
    drafts approved, support tickets, etc.). When omitted, defaults to
    zeros and the snapshot reflects an empty-data customer cleanly.
    """
    snapshot = CustomerSignalSnapshot(
        customer_id=customer_id,
        generated_at=_now_iso(),
    )
    raw = inputs or {}

    # --- Health score -------------------------------------------------
    def _health() -> Any:
        from auto_client_acquisition.customer_success.health_score import (
            compute_health,
        )
        return compute_health(
            customer_id=customer_id,
            logins_last_30d=int(raw.get("logins_last_30d", 0)),
            drafts_approved_last_30d=int(raw.get("drafts_approved_last_30d", 0)),
            replies_acted_on_last_30d=int(raw.get("replies_acted_on_last_30d", 0)),
            demos_booked_last_30d=int(raw.get("demos_booked_last_30d", 0)),
            deals_stage_progressed_last_30d=int(
                raw.get("deals_stage_progressed_last_30d", 0)
            ),
            paid_customers_last_30d=int(raw.get("paid_customers_last_30d", 0)),
            pipeline_value_sar=float(raw.get("pipeline_value_sar", 0)),
            channels_enabled=int(raw.get("channels_enabled", 0)),
            integrations_connected=int(raw.get("integrations_connected", 0)),
            sectors_targeted=int(raw.get("sectors_targeted", 0)),
            total_drafts_lifetime=int(raw.get("total_drafts_lifetime", 0)),
            nps=raw.get("nps"),
            support_tickets_open=int(raw.get("support_tickets_open", 0)),
            days_since_last_login=int(raw.get("days_since_last_login", 0)),
            billing_failures=int(raw.get("billing_failures", 0)),
        )

    health_obj = _safe(snapshot, "health", _health)
    if health_obj is not None:
        snapshot.health = health_obj.to_dict()

    # --- Churn risk ---------------------------------------------------
    def _churn() -> Any:
        from auto_client_acquisition.customer_success.churn_risk import (
            compute_churn_risk,
        )
        return compute_churn_risk(
            customer_id=customer_id,
            engagement_drop_pct=float(raw.get("engagement_drop_pct", 0.0)),
            support_escalations_last_30d=int(raw.get("support_escalations_last_30d", 0)),
            payment_late_count=int(raw.get("payment_late_count", 0)),
            nps_below_7=bool(raw.get("nps_below_7", False)),
            decision_maker_left=bool(raw.get("decision_maker_left", False)),
        )

    churn_obj = _safe(snapshot, "churn", _churn)
    if churn_obj is not None:
        snapshot.churn = churn_obj.to_dict()

    # --- Adoption -----------------------------------------------------
    def _adoption() -> Any:
        from auto_client_acquisition.adoption_os.adoption_score import compute
        return compute(
            customer_id=customer_id,
            channels_enabled=int(raw.get("channels_enabled", 0)),
            integrations_connected=int(raw.get("integrations_connected", 0)),
            sectors_targeted=int(raw.get("sectors_targeted", 0)),
            total_drafts_lifetime=int(raw.get("total_drafts_lifetime", 0)),
            logins_last_30d=int(raw.get("logins_last_30d", 0)),
            drafts_approved_last_30d=int(raw.get("drafts_approved_last_30d", 0)),
            replies_acted_on_last_30d=int(raw.get("replies_acted_on_last_30d", 0)),
        )

    adoption_obj = _safe(snapshot, "adoption", _adoption)
    if adoption_obj is not None:
        snapshot.adoption = adoption_obj.to_dict()

    # --- Expansion readiness ------------------------------------------
    def _expansion() -> Any:
        from auto_client_acquisition.expansion_engine.readiness_score import (
            compute_readiness_score,
        )
        bucket = (snapshot.health or {}).get("bucket", "unknown")
        return compute_readiness_score(
            proof_event_count=int(raw.get("proof_event_count", 0)),
            max_evidence_level=int(raw.get("max_evidence_level", 0)),
            customer_approved_proof_count=int(
                raw.get("customer_approved_proof_count", 0)
            ),
            public_proof_count=int(raw.get("public_proof_count", 0)),
            payment_history_paid_count=int(raw.get("payment_history_paid_count", 0)),
            delivery_sessions_complete_count=int(
                raw.get("delivery_sessions_complete_count", 0)
            ),
            support_tickets_open=int(raw.get("support_tickets_open", 0)),
            support_tickets_critical=int(raw.get("support_tickets_critical", 0)),
            days_since_last_engagement=int(raw.get("days_since_last_engagement", 30)),
            customer_health_bucket=str(bucket),
            budget_tier_match_score=float(raw.get("budget_tier_match_score", 0.5)),
            remaining_pain_score=float(raw.get("remaining_pain_score", 0.5)),
        )

    expansion_obj = _safe(snapshot, "expansion", _expansion)
    if expansion_obj is not None:
        if hasattr(expansion_obj, "to_dict"):
            snapshot.expansion = expansion_obj.to_dict()
        else:
            snapshot.expansion = {
                "score": getattr(expansion_obj, "score", 0.0),
                "ready": getattr(expansion_obj, "ready", False),
                "blockers": list(getattr(expansion_obj, "blockers", []) or []),
            }

    # --- Proof maturity ----------------------------------------------
    def _proof() -> Any:
        from auto_client_acquisition.customer_success.proof_maturity import (
            compute_proof_maturity,
        )
        return compute_proof_maturity(
            customer_id=customer_id,
            proof_events_total=int(raw.get("proof_event_count", 0)),
            customer_approved_proof_count=int(
                raw.get("customer_approved_proof_count", 0)
            ),
            max_evidence_level=int(raw.get("max_evidence_level", 0)),
            public_proof_count=int(raw.get("public_proof_count", 0)),
        )

    proof_obj = _safe(snapshot, "proof_maturity", _proof)
    if proof_obj is not None and hasattr(proof_obj, "to_dict"):
        snapshot.proof_maturity = proof_obj.to_dict()

    # --- Value summary -------------------------------------------------
    def _value() -> Any:
        from auto_client_acquisition.value_os import value_ledger
        return value_ledger.summarize(customer_id=customer_id, period_days=90)

    value_obj = _safe(snapshot, "value_summary", _value)
    if isinstance(value_obj, dict):
        snapshot.value_summary = value_obj

    # --- Renewal status -----------------------------------------------
    def _renewal() -> Any:
        from auto_client_acquisition.payment_ops import renewal_scheduler
        rows = renewal_scheduler.list_by_customer(customer_id) or []
        if not rows:
            return {"has_schedule": False}
        latest = rows[-1]
        return {
            "has_schedule": True,
            "schedule_id": getattr(latest, "schedule_id", ""),
            "status": str(getattr(latest, "status", "")),
            "next_attempt_at": str(getattr(latest, "next_attempt_at", "")),
            "amount_sar": float(getattr(latest, "amount_sar", 0.0)),
            "cycle_count": int(getattr(latest, "cycle_count", 0)),
        }

    renewal_dict = _safe(snapshot, "renewal_status", _renewal)
    if isinstance(renewal_dict, dict):
        snapshot.renewal_status = renewal_dict

    # --- NPS + last payment (callers may supply via inputs) -----------
    nps_score = raw.get("recent_nps_score")
    if nps_score is not None:
        snapshot.recent_nps_score = int(nps_score)
        snapshot.recent_nps_milestone = str(raw.get("recent_nps_milestone", ""))
        # Reflect nps_below_7 into churn signal note if not already set.
    snapshot.last_payment_at = (
        str(raw["last_payment_at"]) if raw.get("last_payment_at") is not None else None
    )

    return snapshot


__all__ = [
    "CustomerSignalSnapshot",
    "aggregate_customer_signals",
]
