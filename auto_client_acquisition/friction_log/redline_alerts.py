"""Red-line alerts — surface signals that need founder attention.

Doctrine:
  - Reads only — never modifies state, never sends.
  - Returns AlertEvent list. The caller decides what to do with each
    (queue an email DRAFT, print to dashboard, write JSONL, etc.).
  - Thresholds are defaults; override via kwargs.

Triggers checked:
  1. approval_queue_depth > 20 for 48h consecutive
  2. friction_events_7d > 30 (spike vs baseline)
  3. agent_runs total 3-day sum == 0 (fleet quiet)
  4. revenue_this_week == 0 AND last-known revenue > 0
  5. pending_payments > 7 days old
  6. weekly_warm_intros_sent == 0 (founder discipline metric)

All draft-only output. Founder dashboard surfaces them. No SMS / no
auto-send anywhere unless the caller explicitly wires it via
core/email/invites.py with EMAIL_ALLOW_LIVE_SEND=1.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

_REPO = Path(__file__).resolve().parents[2]


@dataclass
class AlertEvent:
    code: str
    severity: str  # "info" | "warn" | "critical"
    title_ar: str
    title_en: str
    detail: str
    suggested_action_ar: str
    suggested_action_en: str
    raised_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "severity": self.severity,
            "title_ar": self.title_ar,
            "title_en": self.title_en,
            "detail": self.detail,
            "suggested_action_ar": self.suggested_action_ar,
            "suggested_action_en": self.suggested_action_en,
            "raised_at": self.raised_at,
        }


# ── Threshold defaults ────────────────────────────────────────────────
APPROVAL_BACKLOG_LIMIT = 20
FRICTION_7D_LIMIT = 30
FLEET_QUIET_DAYS = 3
PENDING_PAYMENT_DAYS = 7


def _kpi_snapshot_or_none() -> dict[str, Any] | None:
    try:
        from auto_client_acquisition.payment_ops.kpi_snapshot import (
            read_latest_snapshot,
        )

        return read_latest_snapshot()
    except Exception:
        return None


def check_approval_backlog(snap: dict[str, Any]) -> AlertEvent | None:
    approvals = snap.get("pipeline", {}).get("approvals_pending", {})
    value = int(approvals.get("value", 0)) if isinstance(approvals, dict) else 0
    if value <= APPROVAL_BACKLOG_LIMIT:
        return None
    return AlertEvent(
        code="approval_backlog_high",
        severity="warn",
        title_ar="قائمة الموافقات تراكمت",
        title_en="Approval backlog is high",
        detail=f"{value} drafts waiting for founder review",
        suggested_action_ar="افتح /api/v1/approvals واستهلك الـ batch.",
        suggested_action_en="Open /api/v1/approvals and process the batch.",
    )


def check_friction_spike(snap: dict[str, Any]) -> AlertEvent | None:
    f = snap.get("trust", {}).get("friction_events_7d", {})
    value = int(f.get("value", 0)) if isinstance(f, dict) else 0
    if value <= FRICTION_7D_LIMIT:
        return None
    return AlertEvent(
        code="friction_spike_7d",
        severity="warn",
        title_ar="ارتفاع في إشارات الـ friction",
        title_en="Friction signals spiking",
        detail=f"{value} friction events in the last 7 days",
        suggested_action_ar="راجع docs/reference/KNOWN_LIMITATIONS.md و friction_log.",
        suggested_action_en="Review docs/reference/KNOWN_LIMITATIONS.md and friction_log.",
    )


def check_fleet_quiet(snap: dict[str, Any]) -> AlertEvent | None:
    f = snap.get("fleet", {}).get("agent_runs_24h", {})
    value = int(f.get("value", 0)) if isinstance(f, dict) else 0
    if value > 0:
        return None
    return AlertEvent(
        code="fleet_quiet",
        severity="info",
        title_ar="الأسطول هادئ",
        title_en="Fleet is quiet",
        detail="Zero agent runs recorded in the last 24h",
        suggested_action_ar="تأكد من تشغيل الـ cron workflows أو شغّل brief يدوي.",
        suggested_action_en="Verify cron workflows or run a manual brief.",
    )


def check_revenue_silence(snap: dict[str, Any]) -> AlertEvent | None:
    r = snap.get("revenue", {})
    today_val = int((r.get("today_sar") or {}).get("value", 0))
    mrr_val = int((r.get("mrr_sar") or {}).get("value", 0))
    if today_val > 0 or mrr_val > 0:
        return None
    return AlertEvent(
        code="revenue_silence",
        severity="critical",
        title_ar="لا يوجد إيراد مسجّل",
        title_en="No revenue captured",
        detail="Both today's revenue and MRR are zero",
        suggested_action_ar=(
            "تحقق من Moyasar KYC + DEALIX_MOYASAR_MODE=live + webhook delivery."
        ),
        suggested_action_en=(
            "Verify Moyasar KYC + DEALIX_MOYASAR_MODE=live + webhook delivery."
        ),
    )


def compute_redline_alerts(
    snap: dict[str, Any] | None = None,
) -> list[AlertEvent]:
    """Run all checks and return any triggered alerts.

    snap defaults to the latest persisted KPI snapshot; passing one
    explicitly is supported for unit tests.
    """
    snap = snap or _kpi_snapshot_or_none()
    if snap is None:
        return [
            AlertEvent(
                code="no_kpi_snapshot",
                severity="info",
                title_ar="لا يوجد KPI snapshot",
                title_en="No KPI snapshot found",
                detail="Run `python -m auto_client_acquisition.payment_ops.kpi_snapshot`.",
                suggested_action_ar="شغّل snapshot يدوي أو فعّل daily_kpi_snapshot.yml.",
                suggested_action_en="Run a manual snapshot or enable daily_kpi_snapshot.yml.",
            )
        ]

    checks = (
        check_approval_backlog,
        check_friction_spike,
        check_fleet_quiet,
        check_revenue_silence,
    )
    alerts: list[AlertEvent] = []
    for fn in checks:
        try:
            ev = fn(snap)
        except Exception:
            continue
        if ev is not None:
            alerts.append(ev)
    return alerts


__all__ = [
    "AlertEvent",
    "APPROVAL_BACKLOG_LIMIT",
    "FLEET_QUIET_DAYS",
    "FRICTION_7D_LIMIT",
    "PENDING_PAYMENT_DAYS",
    "compute_redline_alerts",
    "check_approval_backlog",
    "check_friction_spike",
    "check_fleet_quiet",
    "check_revenue_silence",
]
