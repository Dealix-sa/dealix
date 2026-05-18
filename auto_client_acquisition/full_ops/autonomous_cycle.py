"""Unified daily autonomous Full Ops cycle.

Chains intake -> enrich -> score -> qualify -> draft -> proof -> approval
-> work-items into a single deterministic-to-the-gate run. Every external
action becomes a pending :class:`ApprovalRequest`; nothing is ever sent
or charged. Step failures emit a friction event and never crash the run.

Non-negotiables honored:
- no live send / no live charge — every external action is draft_only and
  queued as a pending approval for the founder
- no scraping — leads come only from the passed list or the founder's
  existing lead inbox
- no cold outreach / no LinkedIn automation — drafts only, approval-gated
- no fake proof — proof events are recorded at the ``estimated`` tier
"""
from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

from auto_client_acquisition.approval_center import (
    get_default_approval_store,
    render_approval_card,
)
from auto_client_acquisition.approval_center.schemas import ApprovalRequest
from auto_client_acquisition.friction_log import emit as friction_emit
from auto_client_acquisition.friction_log.schemas import FrictionKind, FrictionSeverity
from auto_client_acquisition.full_ops.prioritizer import prioritize
from auto_client_acquisition.full_ops.work_item import WorkItem
from auto_client_acquisition.full_ops.work_queue import WorkQueue, get_default_queue
from auto_client_acquisition.revenue_os.scoring import score_account_row
from auto_client_acquisition.sales_os.qualification import qualify
from auto_client_acquisition.sales_os.proposal_renderer import (
    ProposalContext,
    render_proposal,
)

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_CYCLE_DIR = _REPO_ROOT / "data" / "full_ops_cycles"

# Hard gates re-asserted in every report (read-only contract for the UI).
_HARD_GATES: tuple[str, ...] = (
    "no_live_send",
    "no_live_charge",
    "no_scraping",
    "no_cold_outreach",
    "no_linkedin_automation",
    "no_fake_proof",
    "approval_required_for_external_actions",
)

# Score threshold above which a lead row is forwarded to qualification.
_QUALIFY_SCORE_FLOOR = 40


@dataclass
class CycleReport:
    """Bilingual summary of a single Full Ops autonomous cycle."""

    cycle_id: str
    generated_at: str
    on_date: str
    title_ar: str
    title_en: str
    stages: dict[str, Any] = field(default_factory=dict)
    approvals_pending: dict[str, Any] = field(default_factory=dict)
    work_items: dict[str, Any] = field(default_factory=dict)
    next_actions: list[dict[str, str]] = field(default_factory=list)
    hard_gates: list[str] = field(default_factory=lambda: list(_HARD_GATES))
    report_paths: dict[str, str] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "cycle_id": self.cycle_id,
            "generated_at": self.generated_at,
            "on_date": self.on_date,
            "title_ar": self.title_ar,
            "title_en": self.title_en,
            "stages": self.stages,
            "approvals_pending": self.approvals_pending,
            "work_items": self.work_items,
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


def _safe(obj: Any, attr: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(attr, default)
    return getattr(obj, attr, default)


def _lead_to_row(lead: Any, index: int) -> dict[str, Any]:
    """Project a lead (dict or LeadCandidate) into a scoring row."""
    name = _safe(lead, "company_name") or _safe(lead, "name") or f"lead_{index}"
    return {
        "company_name": str(name),
        "sector": str(_safe(lead, "sector", "") or ""),
        "city": str(_safe(lead, "city", "") or ""),
        "source": str(_safe(lead, "source", "warm_intro") or "warm_intro"),
        "relationship_status": str(_safe(lead, "relationship_status", "") or ""),
        "notes": str(_safe(lead, "notes", "") or ""),
        "employee_count": _safe(lead, "employee_count"),
        "last_contact_days": _safe(lead, "last_contact_days"),
    }


def _load_inbox_leads() -> list[dict[str, Any]]:
    """Pull leads from the founder's existing lead inbox (inbound only)."""
    try:
        from scripts.dealix_daily_lead_prep import load_candidates_from_lead_inbox
    except Exception:
        return []
    try:
        candidates = load_candidates_from_lead_inbox(limit=100)
    except Exception:
        return []
    rows: list[dict[str, Any]] = []
    for cand in candidates:
        rows.append(
            {
                "company_name": getattr(cand, "name", ""),
                "name": getattr(cand, "name", ""),
                "sector": getattr(cand, "sector", ""),
                "city": getattr(cand, "city", ""),
                "source": getattr(cand, "source", "warm_intro"),
                "notes": getattr(cand, "notes", ""),
            }
        )
    return rows


def _enrich_row(row: dict[str, Any]) -> dict[str, Any]:
    """Deterministic, no-network enrichment: fill safe defaults only."""
    enriched = dict(row)
    if not str(enriched.get("source") or "").strip():
        enriched["source"] = "warm_intro"
    if not str(enriched.get("city") or "").strip():
        enriched["city"] = "unknown"
    if not str(enriched.get("sector") or "").strip():
        enriched["sector"] = "unknown"
    return enriched


def _build_outreach_draft(company_name: str, qual: Any) -> str:
    """Compose a draft proposal for a qualified lead (draft_only, never sent)."""
    handle = company_name.strip().lower().replace(" ", "_") or "prospect"
    ctx = ProposalContext(
        customer_name=company_name or "Prospect",
        customer_handle=handle,
        sector=str(_safe(qual, "recommended_offer", "")) or "general",
        city="unknown",
        engagement_id=f"fo_{uuid.uuid4().hex[:8]}",
    )
    return render_proposal(ctx)


def run_cycle(
    *,
    leads: list[dict[str, Any]] | None = None,
    on_date: Any = None,
    customer_id: str = "dealix_full_ops",
    work_queue: WorkQueue | None = None,
) -> CycleReport:
    """Run the unified daily autonomous Full Ops cycle.

    Everything is deterministic up to an approval gate. For every external
    action a pending :class:`ApprovalRequest` is created; nothing is ever
    sent or charged. Step failures emit a friction event and are recorded
    in ``warnings`` instead of crashing the run.
    """
    cycle_id = f"foc_{uuid.uuid4().hex[:12]}"
    on_date_str = _resolve_date(on_date)
    queue = work_queue if work_queue is not None else get_default_queue()
    store = get_default_approval_store()

    report = CycleReport(
        cycle_id=cycle_id,
        generated_at=_now_iso(),
        on_date=on_date_str,
        title_ar=f"دورة العمليات الكاملة المؤتمتة — {on_date_str}",
        title_en=f"Autonomous Full Ops cycle — {on_date_str}",
    )

    def _friction(stage: str, exc: Exception) -> None:
        report.warnings.append(f"{stage}: {exc}")
        try:
            friction_emit(
                customer_id=customer_id,
                kind=FrictionKind.SCHEMA_FAILURE,
                severity=FrictionSeverity.MED,
                workflow_id=cycle_id,
                notes=f"full_ops_cycle stage {stage} failed: {exc}",
            )
        except Exception:  # noqa: BLE001 — friction logging must never crash
            pass

    # (a) intake -----------------------------------------------------
    intake_leads: list[dict[str, Any]] = []
    try:
        if leads is not None:
            intake_leads = [dict(lead) for lead in leads]
        else:
            intake_leads = _load_inbox_leads()
    except Exception as exc:  # noqa: BLE001
        _friction("intake", exc)

    rows = [_lead_to_row(lead, i) for i, lead in enumerate(intake_leads)]

    # (b) enrich -----------------------------------------------------
    enriched: list[dict[str, Any]] = []
    for row in rows:
        try:
            enriched.append(_enrich_row(row))
        except Exception as exc:  # noqa: BLE001
            _friction("enrich", exc)

    # (c) score ------------------------------------------------------
    scored: list[dict[str, Any]] = []
    for row in enriched:
        try:
            result = score_account_row(row)
            scored.append({"row": row, "score": int(result.get("score", 0))})
        except Exception as exc:  # noqa: BLE001
            _friction("score", exc)

    # (d) qualify ----------------------------------------------------
    qualified: list[dict[str, Any]] = []
    verdict_counts = {"accept": 0, "diagnostic": 0, "reject": 0}
    for item in scored:
        row = item["row"]
        score = item["score"]
        if score < _QUALIFY_SCORE_FLOOR:
            verdict_counts["reject"] += 1
            continue
        try:
            qual = qualify(
                pain_clear=score >= 60,
                owner_present=True,
                data_available=score >= 50,
                accepts_governance=True,
                has_budget=score >= 70,
                wants_safe_methods=True,
                proof_path_visible=score >= 55,
                retainer_path_visible=score >= 80,
                raw_request_text=str(row.get("notes", "")),
                sector=str(row.get("sector", "")),
                city=str(row.get("city", "")),
            )
        except Exception as exc:  # noqa: BLE001
            _friction("qualify", exc)
            continue
        decision = qual.decision
        if decision == "accept":
            verdict_counts["accept"] += 1
            qualified.append({"row": row, "score": score, "qual": qual})
        elif decision in ("diagnostic_only", "reframe"):
            verdict_counts["diagnostic"] += 1
            qualified.append({"row": row, "score": score, "qual": qual})
        else:
            verdict_counts["reject"] += 1

    # (e) outreach drafts (draft_only) -------------------------------
    drafts: list[dict[str, Any]] = []
    for item in qualified:
        row = item["row"]
        try:
            draft_text = _build_outreach_draft(str(row.get("company_name", "")), item["qual"])
            drafts.append(
                {
                    "company_name": row.get("company_name", ""),
                    "decision": item["qual"].decision,
                    "draft_chars": len(draft_text),
                }
            )
        except Exception as exc:  # noqa: BLE001
            _friction("draft", exc)

    # (f) proof events ----------------------------------------------
    proof_event_ids: list[str] = []
    try:
        from auto_client_acquisition.value_os import add_event as value_add_event

        for item in qualified:
            try:
                event = value_add_event(
                    customer_id=customer_id,
                    kind="full_ops_qualified_lead",
                    amount=0.0,
                    tier="estimated",
                    notes=f"cycle {cycle_id} qualified {item['row'].get('company_name', '')}",
                )
                proof_event_ids.append(event.event_id)
            except Exception as exc:  # noqa: BLE001
                _friction("proof_event", exc)
    except Exception as exc:  # noqa: BLE001
        _friction("proof_event_import", exc)

    # (g) approvals — one pending request per external draft --------
    approval_cards: list[dict[str, Any]] = []
    for draft in drafts:
        try:
            company = str(draft["company_name"])
            req = ApprovalRequest(
                object_type="outreach_draft",
                object_id=f"{cycle_id}:{company}",
                action_type="draft_email",
                action_mode="approval_required",
                channel="email",
                summary_ar=f"مسودة تواصل تحتاج موافقة: {company}",
                summary_en=f"Outreach draft pending approval: {company}",
                risk_level="low",
                proof_impact=f"full_ops_cycle:{cycle_id}",
                customer_id=customer_id,
            )
            stored = store.create(req)
            approval_cards.append(render_approval_card(stored))
        except Exception as exc:  # noqa: BLE001
            _friction("approval", exc)

    # (h) work items -------------------------------------------------
    work_items: list[WorkItem] = []
    for draft in drafts:
        try:
            company = str(draft["company_name"])
            item = WorkItem.make(
                os_type="sales",
                title_ar=f"مراجعة مسودة تواصل: {company}",
                title_en=f"Review outreach draft: {company}",
                source=f"full_ops_cycle:{cycle_id}",
                priority="p1",
                status="needs_approval",
                action_mode="approval_required",
                next_action_ar="راجع المسودة واعتمدها أو ارفضها",
                next_action_en="Review the draft and approve or reject it",
            )
            queue.add(item)
            work_items.append(item)
        except Exception as exc:  # noqa: BLE001
            _friction("work_item", exc)

    # one orchestration work item for the cycle itself
    try:
        cycle_item = WorkItem.make(
            os_type="executive",
            title_ar=f"دورة Full Ops {on_date_str}",
            title_en=f"Full Ops cycle {on_date_str}",
            source=f"full_ops_cycle:{cycle_id}",
            priority="p2",
            status="triaged",
            action_mode="suggest_only",
        )
        queue.add(cycle_item)
        work_items.append(cycle_item)
    except Exception as exc:  # noqa: BLE001
        _friction("work_item_cycle", exc)

    by_priority: dict[str, int] = {}
    for it in work_items:
        by_priority[it.priority] = by_priority.get(it.priority, 0) + 1
    top = prioritize(work_items)[:5]

    # (i) assemble report -------------------------------------------
    report.stages = {
        "intake": len(intake_leads),
        "enriched": len(enriched),
        "scored": len(scored),
        "qualified": {
            "accept": verdict_counts["accept"],
            "diagnostic": verdict_counts["diagnostic"],
            "reject": verdict_counts["reject"],
        },
        "drafts": len(drafts),
        "proof_events": len(proof_event_ids),
    }
    report.approvals_pending = {
        "count": len(approval_cards),
        "items": approval_cards,
    }
    report.work_items = {
        "count": len(work_items),
        "by_priority": by_priority,
        "top": [it.model_dump(mode="json") for it in top],
    }
    report.next_actions = _build_next_actions(
        drafts=len(drafts),
        approvals=len(approval_cards),
        warnings=len(report.warnings),
    )

    report.report_paths = _write_report(report)
    return report


def _build_next_actions(
    *, drafts: int, approvals: int, warnings: int
) -> list[dict[str, str]]:
    actions: list[dict[str, str]] = []
    if approvals:
        actions.append(
            {
                "ar": f"راجع {approvals} موافقة معلّقة في مركز الموافقات",
                "en": f"Review {approvals} pending approval(s) in the Approval Center",
            }
        )
    if drafts:
        actions.append(
            {
                "ar": "اعتمد المسوّدات الجاهزة قبل أي إرسال",
                "en": "Approve ready drafts before any send",
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
                "ar": "لا إجراءات معلّقة — الدورة نظيفة",
                "en": "No pending actions — cycle is clean",
            }
        )
    return actions


def _write_report(report: CycleReport) -> dict[str, str]:
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
        md_path.write_text(_render_markdown(report), encoding="utf-8")
        return {"json": str(json_path), "md": str(md_path)}
    except Exception:  # noqa: BLE001 — persistence must never crash the cycle
        return {}


def _render_markdown(report: CycleReport) -> str:
    stages = report.stages
    qualified = stages.get("qualified", {})
    lines: list[str] = [
        f"# {report.title_en}",
        "",
        f"- Cycle: `{report.cycle_id}`",
        f"- Date: {report.on_date}",
        f"- Generated: {report.generated_at}",
        "",
        "## Stages",
        f"- Intake: {stages.get('intake', 0)}",
        f"- Enriched: {stages.get('enriched', 0)}",
        f"- Scored: {stages.get('scored', 0)}",
        f"- Qualified: accept={qualified.get('accept', 0)} "
        f"diagnostic={qualified.get('diagnostic', 0)} "
        f"reject={qualified.get('reject', 0)}",
        f"- Drafts: {stages.get('drafts', 0)}",
        f"- Proof events: {stages.get('proof_events', 0)}",
        "",
        f"## Approvals pending: {report.approvals_pending.get('count', 0)}",
        f"## Work items: {report.work_items.get('count', 0)}",
        "",
        "## Next actions",
    ]
    lines += [f"- {a['en']}" for a in report.next_actions]
    lines += [
        "",
        "## Hard gates",
    ]
    lines += [f"- {g}" for g in report.hard_gates]
    lines += [
        "",
        "---",
        "",
        f"# {report.title_ar}",
        "",
        "## المراحل",
        f"- استقبال: {stages.get('intake', 0)}",
        f"- إثراء: {stages.get('enriched', 0)}",
        f"- تصنيف: {stages.get('scored', 0)}",
        f"- تأهيل: قبول={qualified.get('accept', 0)} "
        f"تشخيص={qualified.get('diagnostic', 0)} "
        f"رفض={qualified.get('reject', 0)}",
        f"- مسوّدات: {stages.get('drafts', 0)}",
        f"- أحداث إثبات: {stages.get('proof_events', 0)}",
        "",
        f"## موافقات معلّقة: {report.approvals_pending.get('count', 0)}",
        f"## عناصر عمل: {report.work_items.get('count', 0)}",
        "",
        "## الإجراءات التالية",
    ]
    lines += [f"- {a['ar']}" for a in report.next_actions]
    lines.append("")
    return "\n".join(lines)


def latest_report() -> dict[str, Any] | None:
    """Return the newest persisted cycle report, or None if none exist."""
    if not _CYCLE_DIR.exists():
        return None
    json_files = sorted(_CYCLE_DIR.glob("*.json"))
    if not json_files:
        return None
    newest = json_files[-1]
    try:
        return json.loads(newest.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return None


__all__ = ["CycleReport", "latest_report", "run_cycle"]
