"""Weekly financial autonomy cycle.

Aggregates the metrics snapshot, detects anomalies vs the prior cycle,
evaluates threshold rules, routes every high-stakes signal to the
founder approval queue, persists the report, and returns a bilingual
:class:`FinancialCycleReport`.

Hard gates re-asserted on every report:
- ``no_live_send`` — nothing is ever sent to a customer.
- ``no_live_charge`` — nothing is ever charged.
- ``no_auto_refund`` — refunds always require an explicit founder
  approval; the cycle only flags candidates.
- ``approval_required_for_financial_decisions`` — every high-stakes
  financial signal becomes a pending approval.
- ``no_fake_revenue`` — every metric is sourced from the payments
  ledger or a documented estimate.
"""
from __future__ import annotations

import json
import logging
import os
import uuid
from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

from auto_client_acquisition.financial_autonomy.anomaly_detector import (
    Anomaly,
    detect_anomalies,
)
from auto_client_acquisition.financial_autonomy.financial_report import (
    render_financial_report_markdown,
)
from auto_client_acquisition.financial_autonomy.metrics_aggregator import (
    FinancialMetricsSnapshot,
    aggregate_financial_metrics,
)
from auto_client_acquisition.financial_autonomy.threshold_rules import (
    ThresholdViolation,
    evaluate_thresholds,
)

log = logging.getLogger(__name__)


_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_DEFAULT_DIR = _REPO_ROOT / "data" / "financial_cycles"


def _cycle_dir() -> Path:
    """Return the persisted cycles directory, honoring the env override."""
    env = os.environ.get("DEALIX_FINANCIAL_CYCLES_PATH")
    if env:
        return Path(env)
    return _DEFAULT_DIR


_HARD_GATES: tuple[str, ...] = (
    "no_live_send",
    "no_live_charge",
    "no_auto_refund",
    "approval_required_for_financial_decisions",
    "no_fake_revenue",
)


@dataclass
class FinancialCycleReport:
    """Bilingual report for a single financial cycle run."""

    cycle_id: str
    generated_at: str
    period_end: str
    cadence: str
    title_ar: str
    title_en: str
    metrics: dict[str, Any] = field(default_factory=dict)
    unit_economics: dict[str, Any] = field(default_factory=dict)
    anomalies: list[dict[str, Any]] = field(default_factory=list)
    threshold_violations: list[dict[str, Any]] = field(default_factory=list)
    approvals_pending: dict[str, Any] = field(
        default_factory=lambda: {"count": 0, "items": []}
    )
    hard_gates: list[str] = field(default_factory=lambda: list(_HARD_GATES))
    warnings: list[str] = field(default_factory=list)
    report_paths: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "cycle_id": self.cycle_id,
            "generated_at": self.generated_at,
            "period_end": self.period_end,
            "cadence": self.cadence,
            "title_ar": self.title_ar,
            "title_en": self.title_en,
            "metrics": dict(self.metrics),
            "unit_economics": dict(self.unit_economics),
            "anomalies": list(self.anomalies),
            "threshold_violations": list(self.threshold_violations),
            "approvals_pending": dict(self.approvals_pending),
            "hard_gates": list(self.hard_gates),
            "warnings": list(self.warnings),
            "report_paths": dict(self.report_paths),
        }


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _resolve_period_end(period_end: Any) -> str:
    if period_end is None:
        return date.today().isoformat()
    if isinstance(period_end, date):
        return period_end.isoformat()
    return str(period_end)


def _emit_friction(
    *,
    customer_id: str,
    cycle_id: str,
    stage: str,
    exc: Exception,
    warnings: list[str],
) -> None:
    warnings.append(f"{stage}: {exc}")
    try:
        from auto_client_acquisition.friction_log import emit as friction_emit
        from auto_client_acquisition.friction_log.schemas import (
            FrictionKind,
            FrictionSeverity,
        )

        friction_emit(
            customer_id=customer_id,
            kind=FrictionKind.SCHEMA_FAILURE,
            severity=FrictionSeverity.MED,
            workflow_id=cycle_id,
            notes=f"financial_cycle stage {stage} failed: {exc}",
        )
    except Exception:  # noqa: BLE001 — friction logging must never crash
        pass


def _load_previous_snapshot(period_end: str) -> dict[str, Any] | None:
    """Return the newest persisted snapshot strictly before ``period_end``."""
    cycle_dir = _cycle_dir()
    if not cycle_dir.exists():
        return None
    candidates = sorted(cycle_dir.glob("*.json"))
    if not candidates:
        return None
    target = None
    for path in candidates:
        stem = path.stem
        if stem >= period_end:
            continue
        target = path
    if target is None:
        return None
    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        log.debug("previous snapshot load failed: %s", exc)
        return None
    return data.get("metrics") if isinstance(data, dict) else None


def _append_event(payload: dict[str, Any], warnings: list[str]) -> None:
    """Append a financial-event record to ``data/financial_cycles/events.jsonl``.

    Friction-safe: failures degrade to a warning and never crash.
    """
    try:
        cycle_dir = _cycle_dir()
        cycle_dir.mkdir(parents=True, exist_ok=True)
        events_path = cycle_dir / "events.jsonl"
        with events_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")
    except Exception as exc:  # noqa: BLE001
        warnings.append(f"events_jsonl_write_failed:{exc}")


def _write_report(report: FinancialCycleReport, warnings: list[str]) -> dict[str, str]:
    """Persist the report JSON + bilingual Markdown. Failures are non-fatal."""
    try:
        cycle_dir = _cycle_dir()
        cycle_dir.mkdir(parents=True, exist_ok=True)
        json_path = cycle_dir / f"{report.period_end}.json"
        md_path = cycle_dir / f"{report.period_end}.md"
        payload = report.to_dict()
        payload["report_paths"] = {"json": str(json_path), "md": str(md_path)}
        json_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        md_path.write_text(
            render_financial_report_markdown(payload), encoding="utf-8"
        )
        return {"json": str(json_path), "md": str(md_path)}
    except Exception as exc:  # noqa: BLE001
        warnings.append(f"report_persist_failed:{exc}")
        return {}


def _approval_for_anomaly(
    *,
    cycle_id: str,
    customer_id: str,
    anomaly: Anomaly,
) -> Any:
    from auto_client_acquisition.approval_center import (
        get_default_approval_store,
        render_approval_card,
    )
    from auto_client_acquisition.approval_center.schemas import ApprovalRequest

    req = ApprovalRequest(
        object_type="financial_decision",
        object_id=f"{cycle_id}:{anomaly.kind}",
        action_type="follow_up_task",
        action_mode="approval_required",
        channel="financial",
        summary_ar=f"شذوذ مالي ({anomaly.kind}): {anomaly.evidence_ar}",
        summary_en=f"Financial anomaly ({anomaly.kind}): {anomaly.evidence_en}",
        risk_level=_severity_to_risk(anomaly.severity),
        proof_impact=f"financial_cycle:{cycle_id}",
        customer_id=customer_id,
    )
    stored = get_default_approval_store().create(req)
    return render_approval_card(stored)


def _approval_for_violation(
    *,
    cycle_id: str,
    customer_id: str,
    violation: ThresholdViolation,
) -> Any:
    from auto_client_acquisition.approval_center import (
        get_default_approval_store,
        render_approval_card,
    )
    from auto_client_acquisition.approval_center.schemas import ApprovalRequest

    rule = violation.rule
    req = ApprovalRequest(
        object_type="financial_decision",
        object_id=f"{cycle_id}:{rule.rule_id}",
        action_type="follow_up_task",
        action_mode="approval_required",
        channel="financial",
        summary_ar=(
            f"{rule.title_ar} — {rule.reason_ar} "
            f"(القياس={violation.observed_value})"
        ),
        summary_en=(
            f"{rule.title_en} — {rule.reason_en} "
            f"(observed={violation.observed_value})"
        ),
        risk_level=_severity_to_risk(rule.severity),
        proof_impact=f"financial_cycle:{cycle_id}",
        customer_id=customer_id,
    )
    stored = get_default_approval_store().create(req)
    return render_approval_card(stored)


def _severity_to_risk(severity: str) -> str:
    """Map a rule/anomaly severity to an approval risk level."""
    if severity == "critical":
        return "high"
    if severity == "high":
        return "high"
    if severity == "medium":
        return "medium"
    return "low"


def run_financial_cycle(
    *,
    period_end: Any = None,
    cadence: str = "weekly",
    customer_id: str = "dealix_financial",
) -> FinancialCycleReport:
    """Run the weekly autonomous financial cycle.

    Deterministic-to-the-gate: never sends, never charges, never refunds.
    Every high-severity anomaly and every threshold violation whose
    action is ``approval_required`` or ``escalate_board`` becomes a
    pending :class:`ApprovalRequest` for the founder.
    """
    cycle_id = f"fc_{uuid.uuid4().hex[:12]}"
    period_end_str = _resolve_period_end(period_end)
    warnings: list[str] = []

    report = FinancialCycleReport(
        cycle_id=cycle_id,
        generated_at=_now_iso(),
        period_end=period_end_str,
        cadence=cadence,
        title_ar=f"دورة الاستقلالية المالية — {period_end_str}",
        title_en=f"Financial autonomy cycle — {period_end_str}",
    )

    # Step 1 — aggregate the current snapshot --------------------------
    snapshot: FinancialMetricsSnapshot | None = None
    try:
        snapshot = aggregate_financial_metrics(period_end=period_end_str)
    except Exception as exc:  # noqa: BLE001
        _emit_friction(
            customer_id=customer_id,
            cycle_id=cycle_id,
            stage="aggregate_financial_metrics",
            exc=exc,
            warnings=warnings,
        )

    if snapshot is None:
        report.warnings = warnings
        report.report_paths = _write_report(report, warnings)
        return report

    metrics_dict = snapshot.to_dict()
    report.metrics = metrics_dict
    report.unit_economics = {
        "gross_margin_pct": snapshot.gross_margin_pct,
        "ltv_sar": snapshot.ltv_sar,
        "cac_payback_months": snapshot.cac_payback_months,
        "runway_months": snapshot.runway_months,
        "estimates_flagged": list(snapshot.estimates_flagged),
    }
    # Propagate aggregator warnings to the cycle warnings list.
    warnings.extend(snapshot.warnings)

    # Step 2 — load previous snapshot for anomaly detection -----------
    previous: dict[str, Any] | None = None
    try:
        previous = _load_previous_snapshot(period_end_str)
    except Exception as exc:  # noqa: BLE001
        _emit_friction(
            customer_id=customer_id,
            cycle_id=cycle_id,
            stage="load_previous_snapshot",
            exc=exc,
            warnings=warnings,
        )

    # Step 3 — detect anomalies ---------------------------------------
    anomalies: list[Anomaly] = []
    try:
        anomalies = detect_anomalies(snapshot, previous)
    except Exception as exc:  # noqa: BLE001
        _emit_friction(
            customer_id=customer_id,
            cycle_id=cycle_id,
            stage="detect_anomalies",
            exc=exc,
            warnings=warnings,
        )
    report.anomalies = [a.to_dict() for a in anomalies]

    # Step 4 — evaluate threshold rules -------------------------------
    violations: list[ThresholdViolation] = []
    try:
        violations = evaluate_thresholds(snapshot)
    except Exception as exc:  # noqa: BLE001
        _emit_friction(
            customer_id=customer_id,
            cycle_id=cycle_id,
            stage="evaluate_thresholds",
            exc=exc,
            warnings=warnings,
        )
    report.threshold_violations = [v.to_dict() for v in violations]

    # Step 5 — route high-stakes signals to the approval queue --------
    cards: list[dict[str, Any]] = []
    for anomaly in anomalies:
        if anomaly.severity not in ("high", "critical"):
            continue
        try:
            cards.append(
                _approval_for_anomaly(
                    cycle_id=cycle_id,
                    customer_id=customer_id,
                    anomaly=anomaly,
                )
            )
        except Exception as exc:  # noqa: BLE001
            _emit_friction(
                customer_id=customer_id,
                cycle_id=cycle_id,
                stage="approval_for_anomaly",
                exc=exc,
                warnings=warnings,
            )

    for violation in violations:
        if violation.action_on_violation not in ("approval_required", "escalate_board"):
            continue
        try:
            cards.append(
                _approval_for_violation(
                    cycle_id=cycle_id,
                    customer_id=customer_id,
                    violation=violation,
                )
            )
        except Exception as exc:  # noqa: BLE001
            _emit_friction(
                customer_id=customer_id,
                cycle_id=cycle_id,
                stage="approval_for_violation",
                exc=exc,
                warnings=warnings,
            )

    report.approvals_pending = {"count": len(cards), "items": cards}

    # Step 6 — append a financial event ------------------------------
    _append_event(
        {
            "event_id": cycle_id,
            "event_type": "financial_cycle_run",
            "period_end": period_end_str,
            "cadence": cadence,
            "mrr_sar": snapshot.mrr_sar,
            "arr_sar": snapshot.arr_sar,
            "runway_months": snapshot.runway_months,
            "anomalies": len(anomalies),
            "violations": len(violations),
            "approvals_pending": len(cards),
            "generated_at": report.generated_at,
        },
        warnings,
    )

    # Step 7 — persist the bilingual report --------------------------
    report.warnings = warnings
    report.report_paths = _write_report(report, warnings)
    return report


def latest_financial_report() -> dict[str, Any] | None:
    """Return the newest persisted financial cycle report, or ``None``."""
    cycle_dir = _cycle_dir()
    if not cycle_dir.exists():
        return None
    candidates = sorted(p for p in cycle_dir.glob("*.json") if p.name != "events.jsonl")
    if not candidates:
        return None
    newest = candidates[-1]
    try:
        return json.loads(newest.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return None


__all__ = [
    "FinancialCycleReport",
    "latest_financial_report",
    "run_financial_cycle",
]
