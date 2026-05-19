"""Strategic autonomy cycle — the CEO/board-tier autonomous loop.

Sits ABOVE the Full Ops operational cycle. It aggregates company
signals, evaluates codified strategic gates, produces CEO-level
decisions, records them to the strategic decision ledger, routes
high-stakes (irreversible) decisions to the founder approval queue, and
on reversible decisions delegates execution to the Full Ops orchestrator.

Irreversible decisions (KILL / HIRE / RAISE_PRICE / CREATE_BUSINESS_UNIT
/ CREATE_VENTURE_CANDIDATE) are RECOMMENDED but NEVER auto-executed —
they remain approval-gated and are never delegated until a later cycle
observes an APPROVED approval.

Every step is friction-safe: a failure appends a warning and emits a
friction event, and never crashes the run.
"""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

from auto_client_acquisition.strategy_autonomy.board_report import (
    render_board_report_markdown,
)
from auto_client_acquisition.strategy_autonomy.decision_gates import (
    GateEvaluation,
    evaluate_strategic_gates,
)
from auto_client_acquisition.strategy_autonomy.decision_ledger import (
    StrategicDecision,
    record_decision,
)
from auto_client_acquisition.strategy_autonomy.decision_types import (
    StrategicDecisionType,
    is_irreversible,
)
from auto_client_acquisition.strategy_autonomy.signal_aggregator import (
    StrategicSignalSnapshot,
    aggregate_strategic_signals,
)
from auto_client_acquisition.strategy_autonomy.strategic_hierarchy import (
    OPERATIONAL_ORCHESTRATOR_ID,
    seed_strategic_tier,
)

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_CYCLE_DIR = _REPO_ROOT / "data" / "strategic_cycles"

_HOLD = StrategicDecisionType.HOLD.value

# Hard gates re-asserted in every strategic report (read-only UI contract).
_HARD_GATES: tuple[str, ...] = (
    "no_autonomous_irreversible_execution",
    "irreversible_decisions_require_founder_approval",
    "no_agent_above_l3",
    "doctrine_non_negotiables_enforced",
    "decisions_recorded_to_code_backed_ledger",
)


@dataclass
class StrategicCycleReport:
    """Bilingual summary of one strategic autonomy cycle."""

    cycle_id: str
    generated_at: str
    on_date: str
    cadence: str
    title_ar: str
    title_en: str
    signal_snapshot: dict[str, Any] = field(default_factory=dict)
    gate_evaluations: list[dict[str, Any]] = field(default_factory=list)
    decisions: list[dict[str, Any]] = field(default_factory=list)
    approvals_pending: dict[str, Any] = field(
        default_factory=lambda: {"count": 0, "items": []}
    )
    reconciled_decisions: dict[str, Any] = field(
        default_factory=lambda: {"approved": [], "rejected": []}
    )
    delegated_cycles: list[dict[str, Any]] = field(default_factory=list)
    next_actions: list[dict[str, str]] = field(default_factory=list)
    hard_gates: list[str] = field(default_factory=lambda: list(_HARD_GATES))
    report_paths: dict[str, str] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "cycle_id": self.cycle_id,
            "generated_at": self.generated_at,
            "on_date": self.on_date,
            "cadence": self.cadence,
            "title_ar": self.title_ar,
            "title_en": self.title_en,
            "signal_snapshot": self.signal_snapshot,
            "gate_evaluations": self.gate_evaluations,
            "decisions": self.decisions,
            "approvals_pending": self.approvals_pending,
            "reconciled_decisions": self.reconciled_decisions,
            "delegated_cycles": self.delegated_cycles,
            "next_actions": self.next_actions,
            "hard_gates": self.hard_gates,
            "report_paths": self.report_paths,
            "warnings": self.warnings,
        }


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _resolve_date(on_date: Any) -> str:
    if on_date is None:
        return date.today().isoformat()
    if isinstance(on_date, date):
        return on_date.isoformat()
    return str(on_date)


def _candidate_decisions(
    evaluations: list[GateEvaluation],
) -> list[GateEvaluation]:
    """Pick one non-HOLD gate evaluation per (decision_type, target)."""
    seen: set[tuple[str, str]] = set()
    out: list[GateEvaluation] = []
    for ev in evaluations:
        if not ev.due or ev.decision_type == _HOLD:
            continue
        key = (ev.decision_type, ev.metric)
        if key in seen:
            continue
        seen.add(key)
        out.append(ev)
    return out


def run_strategic_cycle(
    *,
    on_date: Any = None,
    customer_id: str = "dealix_strategic",
    pipeline_summary: dict[str, int] | None = None,
    cadence: str = "weekly",
    delegate_full_ops: bool = True,
) -> StrategicCycleReport:
    """Run the CEO/board-tier strategic autonomy cycle.

    Reversible decisions may delegate to the Full Ops orchestrator;
    irreversible decisions are recorded as ``pending_approval`` and routed
    to the founder approval queue — they are never auto-executed.
    """
    cycle_id = f"sac_{uuid.uuid4().hex[:12]}"
    on_date_str = _resolve_date(on_date)

    report = StrategicCycleReport(
        cycle_id=cycle_id,
        generated_at=_now_iso(),
        on_date=on_date_str,
        cadence=cadence,
        title_ar=f"دورة الاستقلالية الاستراتيجية — {on_date_str}",
        title_en=f"Strategic autonomy cycle — {on_date_str}",
    )

    def _friction(stage: str, exc: Exception) -> None:
        report.warnings.append(f"{stage}: {exc}")
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
                notes=f"strategic_cycle stage {stage} failed: {exc}",
            )
        except Exception:  # noqa: BLE001 — friction logging must never crash
            pass

    # Step 1 — seed the strategic agent tier --------------------------
    try:
        seed_strategic_tier()
    except Exception as exc:  # noqa: BLE001
        _friction("seed_strategic_tier", exc)

    # Step 1b — reconcile prior pending approvals ---------------------
    # Closes the loop: a decision recorded as ``pending_approval`` by an
    # earlier cycle is advanced to ``approved`` / ``rejected`` once the
    # founder has acted in the Approval Center. No irreversible move is
    # auto-executed — reconciliation only records the founder's verdict.
    try:
        _reconcile_pending_approvals(customer_id, report, _friction)
    except Exception as exc:  # noqa: BLE001
        _friction("reconcile_pending_approvals", exc)

    # Step 2 — aggregate strategic signals ----------------------------
    snapshot: StrategicSignalSnapshot | None = None
    try:
        snapshot = aggregate_strategic_signals(
            on_date=on_date_str,
            customer_id=customer_id,
            pipeline_summary=pipeline_summary,
            founder_hours_per_sprint=float(
                (pipeline_summary or {}).get("founder_hours_per_sprint", 0)
            ),
        )
        report.signal_snapshot = snapshot.to_dict()
        report.warnings.extend(snapshot.warnings)
    except Exception as exc:  # noqa: BLE001
        _friction("aggregate_strategic_signals", exc)

    # Step 3 — evaluate strategic gates -------------------------------
    evaluations: list[GateEvaluation] = []
    if snapshot is not None:
        try:
            evaluations = evaluate_strategic_gates(snapshot)
            report.gate_evaluations = [e.to_dict() for e in evaluations]
        except Exception as exc:  # noqa: BLE001
            _friction("evaluate_strategic_gates", exc)

    # Step 4 — produce candidate decisions (deduped) ------------------
    candidates = _candidate_decisions(evaluations)

    # Step 5 — record decisions to the code-backed ledger -------------
    recorded: list[StrategicDecision] = []
    for ev in candidates:
        irreversible = is_irreversible(ev.decision_type)
        status = "pending_approval" if irreversible else "recommended"
        try:
            decision = record_decision(
                cycle_id=cycle_id,
                decision_type=ev.decision_type,
                target=ev.metric,
                rationale_ar=(
                    f"بوابة {ev.gate_id}: {ev.title_ar} — "
                    f"درجة={ev.score} نطاق={ev.decision_band}"
                ),
                rationale_en=(
                    f"gate {ev.gate_id}: {ev.title_en} — "
                    f"score={ev.score} band={ev.decision_band}"
                ),
                score=ev.score,
                decision_band=ev.decision_band,
                gate_ref=ev.gate_id,
                evidence=list(ev.evidence),
                customer_id=customer_id,
                status=status,
            )
            recorded.append(decision)
        except Exception as exc:  # noqa: BLE001
            _friction(f"record_decision:{ev.gate_id}", exc)

    # Step 6 — route irreversible decisions to founder approval -------
    approval_items: list[dict[str, Any]] = []
    decision_dicts: list[dict[str, Any]] = []
    for decision in recorded:
        data = decision.to_dict()
        if decision.irreversible:
            approval_id = _route_approval(decision, cycle_id, customer_id, _friction)
            if approval_id:
                data["approval_id"] = approval_id
                data["status"] = "pending_approval"
                approval_items.append(
                    {
                        "approval_id": approval_id,
                        "decision_id": decision.decision_id,
                        "decision_type": decision.decision_type,
                        "summary_ar": (
                            f"قرار استراتيجي غير قابل للعكس يحتاج موافقة: "
                            f"{decision.decision_type} / {decision.target}"
                        ),
                        "summary_en": (
                            f"Irreversible strategic decision pending approval: "
                            f"{decision.decision_type} / {decision.target}"
                        ),
                    }
                )
        decision_dicts.append(data)
    report.decisions = decision_dicts
    report.approvals_pending = {
        "count": len(approval_items),
        "items": approval_items,
    }

    # Step 7 — delegate reversible decisions to Full Ops --------------
    reversible = [d for d in recorded if not d.irreversible]
    if delegate_full_ops and reversible:
        try:
            from auto_client_acquisition.full_ops.autonomous_cycle import run_cycle

            fo_report = run_cycle(on_date=on_date_str, customer_id=customer_id)
            report.delegated_cycles.append(
                {
                    "delegated_to": OPERATIONAL_ORCHESTRATOR_ID,
                    "full_ops_cycle_id": fo_report.cycle_id,
                    "triggered_by_decisions": [d.decision_id for d in reversible],
                }
            )
        except Exception as exc:  # noqa: BLE001
            _friction("delegate_full_ops", exc)

    # Step 8 — bilingual board report + persistence -------------------
    report.next_actions = _build_next_actions(
        decisions=len(recorded),
        approvals=len(approval_items),
        delegated=len(report.delegated_cycles),
        reconciled_approved=len(report.reconciled_decisions.get("approved", [])),
        warnings=len(report.warnings),
    )
    report.report_paths = _write_report(report)
    return report


def _reconcile_pending_approvals(
    customer_id: str,
    report: StrategicCycleReport,
    friction: Any,
) -> None:
    """Advance prior ``pending_approval`` decisions to the founder's verdict.

    Reads the approval store for every decision still ``pending_approval``;
    on an approved/rejected approval the decision ledger row is advanced.
    This is status reconciliation only — an irreversible move is never
    executed by code, even once approved.
    """
    from auto_client_acquisition.approval_center import get_default_approval_store
    from auto_client_acquisition.strategy_autonomy.decision_ledger import (
        query_decisions,
        update_decision_status,
    )

    store = get_default_approval_store()
    approved: list[str] = []
    rejected: list[str] = []
    for pending in query_decisions(
        status="pending_approval", customer_id=customer_id
    ):
        if not pending.approval_id:
            continue
        try:
            appr = store.get(pending.approval_id)
        except Exception as exc:  # noqa: BLE001
            friction(f"approval_lookup:{pending.decision_id}", exc)
            continue
        if appr is None:
            continue
        appr_status = str(getattr(appr.status, "value", appr.status)).lower()
        if "approv" in appr_status:
            update_decision_status(pending.decision_id, status="approved")
            approved.append(pending.decision_id)
        elif "reject" in appr_status:
            update_decision_status(pending.decision_id, status="rejected")
            rejected.append(pending.decision_id)
    report.reconciled_decisions = {"approved": approved, "rejected": rejected}


def _route_approval(
    decision: StrategicDecision,
    cycle_id: str,
    customer_id: str,
    friction: Any,
) -> str:
    """Create a founder ApprovalRequest for an irreversible decision."""
    try:
        from auto_client_acquisition.approval_center import (
            ApprovalRequest,
            get_default_approval_store,
        )

        req = ApprovalRequest(
            object_type="strategic_decision",
            object_id=decision.decision_id,
            action_type="strategic_decision",
            action_mode="approval_required",
            summary_ar=(
                f"قرار استراتيجي غير قابل للعكس: "
                f"{decision.decision_type} / {decision.target}"
            ),
            summary_en=(
                f"Irreversible strategic decision: "
                f"{decision.decision_type} / {decision.target}"
            ),
            risk_level="high",
            proof_impact=f"strategic_cycle:{cycle_id}",
            customer_id=customer_id,
        )
        stored = get_default_approval_store().create(req)
        return stored.approval_id
    except Exception as exc:  # noqa: BLE001
        friction(f"route_approval:{decision.decision_id}", exc)
        return ""


def _build_next_actions(
    *,
    decisions: int,
    approvals: int,
    delegated: int,
    reconciled_approved: int = 0,
    warnings: int = 0,
) -> list[dict[str, str]]:
    actions: list[dict[str, str]] = []
    if reconciled_approved:
        actions.append(
            {
                "ar": (
                    f"نفّذ {reconciled_approved} قرار استراتيجي وافق عليه "
                    f"المؤسس (مُرحّل من دورة سابقة)"
                ),
                "en": (
                    f"Execute {reconciled_approved} founder-approved strategic "
                    f"decision(s) carried over from an earlier cycle"
                ),
            }
        )
    if approvals:
        actions.append(
            {
                "ar": (
                    f"راجع {approvals} قرار استراتيجي غير قابل للعكس "
                    f"في مركز الموافقات"
                ),
                "en": (
                    f"Review {approvals} irreversible strategic decision(s) "
                    f"in the Approval Center"
                ),
            }
        )
    if delegated:
        actions.append(
            {
                "ar": f"تابع {delegated} دورة عمليات مفوّضة لرئيس الأركان",
                "en": f"Track {delegated} delegated Full Ops cycle(s)",
            }
        )
    if decisions and not approvals:
        actions.append(
            {
                "ar": "راجع القرارات المسجّلة في سجل القرارات الاستراتيجية",
                "en": "Review recorded decisions in the strategic decision ledger",
            }
        )
    if warnings:
        actions.append(
            {
                "ar": f"افحص {warnings} تحذير في سجل الاحتكاك",
                "en": f"Inspect {warnings} warning(s) in the friction log",
            }
        )
    if not actions:
        actions.append(
            {
                "ar": "لا إجراءات معلّقة — الدورة الاستراتيجية نظيفة",
                "en": "No pending actions — strategic cycle is clean",
            }
        )
    return actions


def _write_report(report: StrategicCycleReport) -> dict[str, str]:
    """Persist the report JSON + bilingual Markdown. Failures are non-fatal."""
    try:
        _CYCLE_DIR.mkdir(parents=True, exist_ok=True)
        json_path = _CYCLE_DIR / f"{report.on_date}.json"
        md_path = _CYCLE_DIR / f"{report.on_date}.md"
        data = report.to_dict()
        data["report_paths"] = {"json": str(json_path), "md": str(md_path)}
        json_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        md_path.write_text(
            render_board_report_markdown(
                cycle_id=report.cycle_id,
                on_date=report.on_date,
                cadence=report.cadence,
                title_ar=report.title_ar,
                title_en=report.title_en,
                signal_snapshot=report.signal_snapshot,
                gate_evaluations=report.gate_evaluations,
                decisions=report.decisions,
                approvals_pending=report.approvals_pending,
                next_actions=report.next_actions,
                hard_gates=report.hard_gates,
                warnings=report.warnings,
            ),
            encoding="utf-8",
        )
        return {"json": str(json_path), "md": str(md_path)}
    except Exception:  # noqa: BLE001 — persistence must never crash the cycle
        return {}


def latest_strategic_report() -> dict[str, Any] | None:
    """Return the newest persisted strategic cycle report, or None."""
    if not _CYCLE_DIR.exists():
        return None
    json_files = sorted(_CYCLE_DIR.glob("*.json"))
    if not json_files:
        return None
    try:
        return json.loads(json_files[-1].read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return None


__all__ = [
    "StrategicCycleReport",
    "latest_strategic_report",
    "run_strategic_cycle",
]
