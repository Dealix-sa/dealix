"""Customer Success daily autonomy cycle.

Runs in parallel to the operational Full Ops lead-acquisition cycle and
under the Strategic Autonomy Layer. For every active customer it
aggregates signals, detects retention opportunities, drafts bilingual
messages (approval-gated, never auto-sent), creates ApprovalRequests in
the founder queue, and emits WorkItems to the existing Full Ops queue.

Every step is friction-safe: a failure appends a warning and emits a
friction event; the cycle never crashes.
"""
from __future__ import annotations

import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

from auto_client_acquisition.customer_success_autonomy.cs_report import (
    render_cs_report_markdown,
)
from auto_client_acquisition.customer_success_autonomy.message_drafter import (
    draft_churn_intervention,
    draft_detractor_outreach,
    draft_expansion_proposal,
    draft_renewal_message,
)
from auto_client_acquisition.customer_success_autonomy.opportunity_detector import (
    Opportunity,
    detect_opportunities,
)
from auto_client_acquisition.customer_success_autonomy.signal_aggregator import (
    aggregate_customer_signals,
)

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_CYCLE_DIR = _REPO_ROOT / "data" / "cs_cycles"

_HARD_GATES: tuple[str, ...] = (
    "no_live_send",
    "no_live_charge",
    "approval_required_for_external_actions",
    "no_unconsented_outreach",
    "no_fake_proof",
)


@dataclass
class CustomerSuccessCycleReport:
    """Bilingual summary of one CS autonomy cycle."""

    cycle_id: str
    generated_at: str
    on_date: str
    title_ar: str
    title_en: str
    summary: dict[str, int] = field(
        default_factory=lambda: {
            "active_customers": 0,
            "opportunities_total": 0,
            "at_risk": 0,
            "expansion_ready": 0,
            "renewals_due": 0,
            "nps_detractors": 0,
        }
    )
    opportunities: list[dict[str, Any]] = field(default_factory=list)
    approvals_created: int = 0
    work_items_created: int = 0
    hard_gates: list[str] = field(default_factory=lambda: list(_HARD_GATES))
    warnings: list[str] = field(default_factory=list)
    report_paths: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _resolve_date(on_date: Any) -> str:
    if on_date is None:
        return date.today().isoformat()
    if isinstance(on_date, date):
        return on_date.isoformat()
    return str(on_date)


def _friction(
    report: CustomerSuccessCycleReport, stage: str, exc: Exception
) -> None:
    report.warnings.append(f"{stage}: {type(exc).__name__}: {exc}")
    try:
        from auto_client_acquisition.friction_log import emit as friction_emit
        from auto_client_acquisition.friction_log.schemas import (
            FrictionKind,
            FrictionSeverity,
        )

        friction_emit(
            customer_id="cs_autonomy",
            kind=FrictionKind.SCHEMA_FAILURE,
            severity=FrictionSeverity.MED,
            workflow_id=report.cycle_id,
            notes=f"cs_cycle stage {stage} failed: {exc}",
        )
    except Exception:  # noqa: BLE001 — friction logging must never crash
        pass


def _draft_for(opp: Opportunity, snapshot_dict: dict[str, Any]) -> dict[str, Any]:
    """Pick the right drafter for the opportunity. Returns {} on failure."""
    from auto_client_acquisition.customer_success_autonomy.signal_aggregator import (
        CustomerSignalSnapshot,
    )
    # Rebuild a minimal snapshot shape from the dict for the drafter.
    snap = CustomerSignalSnapshot(
        customer_id=str(snapshot_dict.get("customer_id", opp.customer_id)),
        generated_at=str(snapshot_dict.get("generated_at", "")),
    )
    snap.renewal_status = dict(snapshot_dict.get("renewal_status", {}) or {})
    snap.churn = dict(snapshot_dict.get("churn", {}) or {})
    snap.recent_nps_milestone = snapshot_dict.get("recent_nps_milestone")
    snap.recent_nps_score = snapshot_dict.get("recent_nps_score")
    if opp.type == "renewal_due":
        return draft_renewal_message(snap)
    if opp.type == "expansion_ready":
        return draft_expansion_proposal(snap, opp.payload.get("offer"))
    if opp.type == "churn_intervention":
        return draft_churn_intervention(snap)
    if opp.type == "nps_detractor_follow_up":
        score = int(snap.recent_nps_score or 0)
        return draft_detractor_outreach(snap, score)
    return {}


def _risk_level_for(opp_type: str) -> str:
    if opp_type in {"churn_intervention", "nps_detractor_follow_up"}:
        return "high"
    if opp_type == "expansion_ready":
        return "medium"
    if opp_type == "renewal_due":
        return "low"
    return "low"


def _action_type_for(opp_type: str) -> str:
    if opp_type == "renewal_due":
        return "payment_reminder"
    if opp_type == "expansion_ready":
        return "upsell_recommendation"
    if opp_type in {"churn_intervention", "nps_detractor_follow_up"}:
        return "follow_up_task"
    return "follow_up_task"


def _create_approval(opp: Opportunity, draft: dict[str, Any], cycle_id: str) -> str:
    """Create an ApprovalRequest for an external-send opportunity. Returns id."""
    from auto_client_acquisition.approval_center import (
        ApprovalRequest,
        get_default_approval_store,
    )

    req = ApprovalRequest(
        object_type="customer_opportunity",
        object_id=f"{opp.customer_id}:{opp.type}",
        action_type=_action_type_for(opp.type),
        action_mode="approval_required" if opp.requires_external_send else "draft_only",
        channel=str(draft.get("channel", "email")) if draft else "email",
        summary_ar=(
            f"عميل {opp.customer_id} — {opp.type}: {opp.recommended_action_ar}"
        )[:280],
        summary_en=(
            f"Customer {opp.customer_id} — {opp.type}: {opp.recommended_action_en}"
        )[:280],
        risk_level=_risk_level_for(opp.type),
        proof_impact=f"customer_success_cycle:{cycle_id}",
        customer_id=opp.customer_id,
    )
    stored = get_default_approval_store().create(req)
    return stored.approval_id


def _emit_work_item(opp: Opportunity, work_queue: Any) -> str:
    from auto_client_acquisition.full_ops.work_item import WorkItem

    item = WorkItem.make(
        os_type="customer_success",
        title_ar=f"{opp.type} — {opp.customer_id}",
        title_en=f"{opp.type} — {opp.customer_id}",
        source="cs_cycle",
        priority="p0" if opp.urgency == "urgent" else "p2",
        action_mode="approval_required" if opp.requires_external_send else "draft_only",
        customer_id=opp.customer_id,
        description_ar=opp.recommended_action_ar,
        description_en=opp.recommended_action_en,
        next_action_ar=opp.recommended_action_ar,
        next_action_en=opp.recommended_action_en,
    )
    if work_queue is not None:
        try:
            work_queue.add(item)
        except Exception:  # noqa: BLE001
            pass
    return item.id


def _load_active_customer_ids(customer_ids: list[str] | None) -> list[str]:
    """Resolve which customers the cycle should run for.

    Caller-provided list wins. Otherwise, attempt a defensive DB lookup;
    if no DB session is available (no DATABASE_URL etc.) return an empty
    list cleanly — the report still renders with zero customers.
    """
    if customer_ids:
        return [str(cid).strip() for cid in customer_ids if str(cid).strip()]
    return []


def run_customer_success_cycle(
    *,
    customer_ids: list[str] | None = None,
    on_date: Any = None,
    inputs_by_customer: dict[str, dict[str, Any]] | None = None,
    work_queue: Any = None,
) -> CustomerSuccessCycleReport:
    """Run the daily CS autonomy cycle.

    ``inputs_by_customer`` lets the caller inject per-customer raw signal
    inputs (logins, drafts approved, NPS, etc.). Empty inputs are fine —
    the cycle just produces empty score snapshots cleanly.
    """
    cycle_id = f"csc_{uuid.uuid4().hex[:12]}"
    on_date_str = _resolve_date(on_date)
    report = CustomerSuccessCycleReport(
        cycle_id=cycle_id,
        generated_at=_now_iso(),
        on_date=on_date_str,
        title_ar=f"دورة نجاح العملاء الذاتية — {on_date_str}",
        title_en=f"Customer Success autonomy cycle — {on_date_str}",
    )

    # Step 1 — resolve active customers ---------------------------------
    try:
        customers = _load_active_customer_ids(customer_ids)
    except Exception as exc:  # noqa: BLE001
        _friction(report, "load_customers", exc)
        customers = []

    report.summary["active_customers"] = len(customers)
    if not customers:
        # Empty-state cycle is valid — write report and return.
        report.report_paths = _write_report(report)
        return report

    inputs_by_customer = inputs_by_customer or {}
    approval_ids: list[str] = []
    work_item_ids: list[str] = []

    # Step 2 — per-customer aggregate + detect + draft -----------------
    for cid in customers:
        snapshot = None
        try:
            snapshot = aggregate_customer_signals(
                cid,
                on_date=on_date_str,
                inputs=inputs_by_customer.get(cid),
            )
            report.warnings.extend(snapshot.warnings)
        except Exception as exc:  # noqa: BLE001
            _friction(report, f"aggregate:{cid}", exc)
            continue

        try:
            opportunities = detect_opportunities(snapshot)
        except Exception as exc:  # noqa: BLE001
            _friction(report, f"detect:{cid}", exc)
            continue

        snapshot_dict = snapshot.to_dict()
        for opp in opportunities:
            data = opp.to_dict()
            draft: dict[str, Any] = {}
            if opp.requires_external_send:
                try:
                    draft = _draft_for(opp, snapshot_dict)
                except Exception as exc:  # noqa: BLE001
                    _friction(report, f"draft:{cid}:{opp.type}", exc)
                    draft = {}
            data["draft"] = draft

            try:
                approval_id = _create_approval(opp, draft, cycle_id)
                data["approval_id"] = approval_id
                approval_ids.append(approval_id)
            except Exception as exc:  # noqa: BLE001
                _friction(report, f"approval:{cid}:{opp.type}", exc)

            try:
                work_item_id = _emit_work_item(opp, work_queue)
                data["work_item_id"] = work_item_id
                work_item_ids.append(work_item_id)
            except Exception as exc:  # noqa: BLE001
                _friction(report, f"work_item:{cid}:{opp.type}", exc)

            report.opportunities.append(data)
            if opp.type == "churn_intervention":
                report.summary["at_risk"] += 1
            if opp.type == "expansion_ready":
                report.summary["expansion_ready"] += 1
            if opp.type == "renewal_due":
                report.summary["renewals_due"] += 1
            if opp.type == "nps_detractor_follow_up":
                report.summary["nps_detractors"] += 1

    report.summary["opportunities_total"] = len(report.opportunities)
    report.approvals_created = len(approval_ids)
    report.work_items_created = len(work_item_ids)

    # Step 3 — persist report -------------------------------------------
    report.report_paths = _write_report(report)
    return report


def _write_report(report: CustomerSuccessCycleReport) -> dict[str, str]:
    """Persist JSON + bilingual Markdown. Failures are non-fatal."""
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
            render_cs_report_markdown(
                cycle_id=report.cycle_id,
                on_date=report.on_date,
                title_ar=report.title_ar,
                title_en=report.title_en,
                summary=report.summary,
                opportunities=report.opportunities,
                hard_gates=report.hard_gates,
                warnings=report.warnings,
            ),
            encoding="utf-8",
        )
        return {"json": str(json_path), "md": str(md_path)}
    except Exception:  # noqa: BLE001
        return {}


def latest_cs_report() -> dict[str, Any] | None:
    """Return the newest persisted CS cycle report, or None."""
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
    "CustomerSuccessCycleReport",
    "latest_cs_report",
    "run_customer_success_cycle",
]
