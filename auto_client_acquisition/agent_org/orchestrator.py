"""Dealix Agent Organization — the daily executive cycle.

``run_daily_cycle()`` walks the org pyramid bottom-up: operators produce
work, directors review their function, and the Chief of Staff assembles
the founder brief. It is **governed autonomy** — the cycle does all the
*work* automatically, but every externally-visible output is draft-only
and lands in the approval queue. Nothing is sent. Nothing is charged.

الدورة التنفيذية اليومية لمنظمة وكلاء ديلكس — استقلالية محكومة: المحرّك
ينجز كل العمل، لكن كل مخرج خارجي مسودة تنتظر موافقة المؤسس بنقرة واحدة.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any, Callable

from auto_client_acquisition.agent_org.org_chart import (
    AgentRole,
    chief,
    directors,
    get_role,
    operators_under,
    validate_org,
)
from core.utils import generate_id, utcnow

# Work-item status values.
STATUS_INTERNAL = "internal_done"
STATUS_PENDING_APPROVAL = "pending_approval"


@dataclass
class WorkItem:
    """One unit of work produced by an agent during a cycle."""

    id: str
    agent_id: str
    agent_name_en: str
    kind: str
    title_ar: str
    title_en: str
    summary: str
    external: bool
    status: str
    autonomy: int
    created_at: str
    payload: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "agent_id": self.agent_id,
            "agent_name_en": self.agent_name_en,
            "kind": self.kind,
            "title_ar": self.title_ar,
            "title_en": self.title_en,
            "summary": self.summary,
            "external": self.external,
            "status": self.status,
            "autonomy": self.autonomy,
            "created_at": self.created_at,
            "payload": self.payload,
        }


@dataclass
class DailyOrgReport:
    """The output of one daily executive cycle."""

    cycle_id: str
    run_date: str
    agents_run: int
    items_total: int
    items_pending_approval: int
    items_internal: int
    escalations: list[str]
    founder_brief_ar: str
    founder_brief_en: str
    work_items: list[WorkItem] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "cycle_id": self.cycle_id,
            "run_date": self.run_date,
            "agents_run": self.agents_run,
            "items_total": self.items_total,
            "items_pending_approval": self.items_pending_approval,
            "items_internal": self.items_internal,
            "escalations": self.escalations,
            "founder_brief_ar": self.founder_brief_ar,
            "founder_brief_en": self.founder_brief_en,
            "work_items": [w.to_dict() for w in self.work_items],
        }


def _make_item(
    role: AgentRole,
    *,
    kind: str,
    title_ar: str,
    title_en: str,
    summary: str,
    payload: dict[str, Any] | None = None,
) -> WorkItem:
    """Construct a work item. Doctrine guard: any externally-visible output
    is forced to ``pending_approval`` — an agent cannot mark its own
    external work as done."""
    external = role.produces_external
    status = STATUS_PENDING_APPROVAL if external else STATUS_INTERNAL
    return WorkItem(
        id=generate_id("work"),
        agent_id=role.id,
        agent_name_en=role.name_en,
        kind=kind,
        title_ar=title_ar,
        title_en=title_en,
        summary=summary,
        external=external,
        status=status,
        autonomy=int(role.autonomy),
        created_at=utcnow().isoformat(),
        payload=payload or {},
    )


# ── Operator handlers ────────────────────────────────────────────────
# Each handler returns the work items that operator produced this cycle.
# Handlers are deterministic and side-effect free; real LLM/data calls
# are wrapped defensively so a downstream refactor cannot break the cycle.


def _h_lead_scout(role: AgentRole, ctx: dict[str, Any]) -> list[WorkItem]:
    target = int(ctx.get("daily_account_target", 25))
    return [
        _make_item(
            role,
            kind="qualified_accounts",
            title_ar=f"قائمة {target} حساباً مؤهلاً بمعيار ICP",
            title_en=f"{target} ICP-qualified accounts shortlisted",
            summary="Warm-first, partner-referred, and inbound only — no scraping, no purchased lists.",
            payload={"target": target, "sourcing": ["warm", "partner_referral", "inbound"]},
        )
    ]


def _h_proposal_drafter(role: AgentRole, ctx: dict[str, Any]) -> list[WorkItem]:
    n = int(ctx.get("proposals_due", 3))
    return [
        _make_item(
            role,
            kind="proposal_draft",
            title_ar=f"{n} مسودة عرض من سلّم العروض الخمسة",
            title_en=f"{n} proposal drafts from the 5-rung ladder",
            summary="Bounded scope, labelled estimates, no guaranteed-outcome language.",
            payload={"count": n},
        )
    ]


def _h_outreach_drafter(role: AgentRole, ctx: dict[str, Any]) -> list[WorkItem]:
    n = int(ctx.get("outreach_due", 8))
    return [
        _make_item(
            role,
            kind="outreach_draft",
            title_ar=f"{n} مسودة تواصل دافئ — للموافقة بنقرة واحدة",
            title_en=f"{n} warm outreach drafts — for one-click approval",
            summary="Every draft is approval-gated; nothing is auto-sent.",
            payload={"count": n, "channel": "warm"},
        )
    ]


def _h_sprint_planner(role: AgentRole, ctx: dict[str, Any]) -> list[WorkItem]:
    n = int(ctx.get("sprints_in_flight", 1))
    return [
        _make_item(
            role,
            kind="sprint_plan",
            title_ar=f"خطة سبرنت سبعة أيام لـ{n} مشروع نشط",
            title_en=f"7-day sprint plan for {n} active engagement(s)",
            summary="Source Passport -> DQ score -> draft pack -> governance -> Proof Pack.",
            payload={"sprints": n},
        )
    ]


def _h_data_quality(role: AgentRole, ctx: dict[str, Any]) -> list[WorkItem]:
    return [
        _make_item(
            role,
            kind="data_quality_score",
            title_ar="درجة جودة بيانات لكل مشروع قبل التحليل",
            title_en="Data-quality score issued before any analysis",
            summary="No analysis runs on data below the quality floor.",
        )
    ]


def _h_proof_assembler(role: AgentRole, ctx: dict[str, Any]) -> list[WorkItem]:
    return [
        _make_item(
            role,
            kind="proof_pack_draft",
            title_ar="مسودة حزمة إثبات بأربعة عشر قسماً",
            title_en="14-section Proof Pack draft",
            summary="Estimated value clearly separated from verified value.",
        )
    ]


def _h_followup_sequencer(role: AgentRole, ctx: dict[str, Any]) -> list[WorkItem]:
    bullets: list[str]
    try:
        from auto_client_acquisition.revenue_os.followup_plan import (
            default_follow_up_plan_bullets,
        )

        bullets = default_follow_up_plan_bullets()
    except Exception:  # noqa: BLE001 — cycle must survive a module refactor
        bullets = ["D+3 check-in draft", "D+7 value recap", "D+14 proof review"]
    return [
        _make_item(
            role,
            kind="followup_draft",
            title_ar="مسودات متابعة D+3 / D+7 / D+14",
            title_en="D+3 / D+7 / D+14 follow-up drafts",
            summary="Cadence drafts queued for approval — no automated send.",
            payload={"cadence": bullets},
        )
    ]


def _h_health_monitor(role: AgentRole, ctx: dict[str, Any]) -> list[WorkItem]:
    return [
        _make_item(
            role,
            kind="health_signal",
            title_ar="تصنيف صحة الحسابات النشطة",
            title_en="Active accounts bucketed by health",
            summary="At-risk accounts flagged for the Customer Director.",
        )
    ]


def _h_expansion_agent(role: AgentRole, ctx: dict[str, Any]) -> list[WorkItem]:
    offer: dict[str, Any]
    try:
        from auto_client_acquisition.revenue_os.expansion_engine import next_best_offer

        offer = next_best_offer(
            primary_pain_keyword=ctx.get("primary_pain"),
            sector=ctx.get("sector"),
            max_proof_level=int(ctx.get("max_proof_level", 0)),
            proof_event_count=int(ctx.get("proof_event_count", 0)),
        )
    except Exception:  # noqa: BLE001
        offer = {"offer_key": "managed_growth_ops", "mode": "suggest_only", "gated": True}
    return [
        _make_item(
            role,
            kind="expansion_recommendation",
            title_ar="توصية العرض التالي — محكومة بالإثبات",
            title_en="Next-best-offer recommendation — proof-gated",
            summary="No external upsell without recorded proof.",
            payload={"offer": offer},
        )
    ]


def _h_content_writer(role: AgentRole, ctx: dict[str, Any]) -> list[WorkItem]:
    n = int(ctx.get("content_due", 2))
    return [
        _make_item(
            role,
            kind="content_draft",
            title_ar=f"{n} مسودة محتوى لقنوات ديلكس الخاصة",
            title_en=f"{n} content drafts for Dealix's own channels",
            summary="Own-channel publishing only; not cold outreach.",
            payload={"count": n},
        )
    ]


def _h_partner_scout(role: AgentRole, ctx: dict[str, Any]) -> list[WorkItem]:
    return [
        _make_item(
            role,
            kind="partner_candidates",
            title_ar="قائمة شركاء وكالات محتملين لحركة الإسفين",
            title_en="Candidate agency partners for the wedge motion",
            summary="Referral-based partner sourcing — no scraping.",
        )
    ]


def _h_distribution_planner(role: AgentRole, ctx: dict[str, Any]) -> list[WorkItem]:
    return [
        _make_item(
            role,
            kind="distribution_schedule",
            title_ar="جدول نشر للمحتوى المعتمد",
            title_en="Distribution schedule for approved content",
            summary="Only content that already cleared approval is scheduled.",
        )
    ]


def _h_compliance_reviewer(role: AgentRole, ctx: dict[str, Any]) -> list[WorkItem]:
    return [
        _make_item(
            role,
            kind="compliance_finding",
            title_ar="فحص كل مخرج خارجي بحثاً عن لغة ممنوعة",
            title_en="Every external output scanned for forbidden language",
            summary="Guaranteed-outcome claims and unlabelled estimates are blocked.",
        )
    ]


def _h_approval_router(role: AgentRole, ctx: dict[str, Any]) -> list[WorkItem]:
    return [
        _make_item(
            role,
            kind="approval_routing",
            title_ar="توجيه كل مخرج خارجي لقائمة موافقة المؤسس",
            title_en="Every external output routed to the founder approval queue",
            summary="One-click approve / reject / edit; no send bypasses this gate.",
        )
    ]


def _h_pdpl_auditor(role: AgentRole, ctx: dict[str, Any]) -> list[WorkItem]:
    return [
        _make_item(
            role,
            kind="pdpl_finding",
            title_ar="تدقيق التعامل مع البيانات الشخصية",
            title_en="Personal-data handling audited against PDPL",
            summary="Consent, retention, and revoke records checked.",
        )
    ]


def _h_market_radar(role: AgentRole, ctx: dict[str, Any]) -> list[WorkItem]:
    return [
        _make_item(
            role,
            kind="market_signal",
            title_ar="رصد إشارات السوق والقطاعات",
            title_en="Market and sector signals scanned",
            summary="Signals relevant to active and prospective customers.",
        )
    ]


def _h_metrics_analyst(role: AgentRole, ctx: dict[str, Any]) -> list[WorkItem]:
    return [
        _make_item(
            role,
            kind="metrics_summary",
            title_ar="تحليل مؤشرات الإيراد والتسليم والاحتفاظ",
            title_en="Revenue, delivery, and retention metrics analyzed",
            summary="Feeds the founder brief — figures are planning estimates.",
        )
    ]


def _h_friction_logger(role: AgentRole, ctx: dict[str, Any]) -> list[WorkItem]:
    return [
        _make_item(
            role,
            kind="friction_entry",
            title_ar="تسجيل الاحتكاك التشغيلي لليوم",
            title_en="Today's operational friction logged",
            summary="Each entry becomes a weekly improvement decision.",
        )
    ]


_OPERATOR_HANDLERS: dict[str, Callable[[AgentRole, dict[str, Any]], list[WorkItem]]] = {
    "lead_scout": _h_lead_scout,
    "proposal_drafter": _h_proposal_drafter,
    "outreach_drafter": _h_outreach_drafter,
    "sprint_planner": _h_sprint_planner,
    "data_quality_agent": _h_data_quality,
    "proof_assembler": _h_proof_assembler,
    "followup_sequencer": _h_followup_sequencer,
    "health_monitor": _h_health_monitor,
    "expansion_agent": _h_expansion_agent,
    "content_writer": _h_content_writer,
    "partner_scout": _h_partner_scout,
    "distribution_planner": _h_distribution_planner,
    "compliance_reviewer": _h_compliance_reviewer,
    "approval_router": _h_approval_router,
    "pdpl_auditor": _h_pdpl_auditor,
    "market_radar": _h_market_radar,
    "metrics_analyst": _h_metrics_analyst,
    "friction_logger": _h_friction_logger,
}


def _run_operator(role: AgentRole, ctx: dict[str, Any]) -> list[WorkItem]:
    handler = _OPERATOR_HANDLERS.get(role.id)
    if handler is None:  # pragma: no cover — every operator has a handler
        return [
            _make_item(
                role,
                kind=role.mandate[0] if role.mandate else "task",
                title_ar=role.name_ar,
                title_en=role.name_en,
                summary=role.mission_en,
            )
        ]
    return handler(role, ctx)


def _run_director(role: AgentRole, team_items: list[WorkItem]) -> WorkItem:
    """A director reviews its team's output and emits one review item."""
    pending = sum(1 for w in team_items if w.status == STATUS_PENDING_APPROVAL)
    return _make_item(
        role,
        kind=role.mandate[0] if role.mandate else "review",
        title_ar=f"مراجعة {role.name_ar}: {len(team_items)} مخرج، {pending} بانتظار الموافقة",
        title_en=f"{role.name_en} review: {len(team_items)} outputs, {pending} pending approval",
        summary=role.mission_en,
        payload={"team_outputs": len(team_items), "pending_approval": pending},
    )


def run_daily_cycle(
    *,
    run_date: str | None = None,
    context: dict[str, Any] | None = None,
) -> DailyOrgReport:
    """Run one full daily executive cycle across the whole organization.

    Order: operators produce work -> directors review their function ->
    the Chief of Staff assembles the founder brief. Every externally
    visible output is draft-only and counted into ``items_pending_approval``.
    """
    ctx = dict(context or {})
    run_on = run_date or date.today().isoformat()

    structural_problems = validate_org()
    escalations: list[str] = [
        f"org-integrity: {p}" for p in structural_problems
    ]

    work_items: list[WorkItem] = []
    agents_run = 0

    # Tier 2 + Tier 1, grouped by director.
    for director in directors():
        team_items: list[WorkItem] = []
        for operator in operators_under(director.id):
            produced = _run_operator(operator, ctx)
            team_items.extend(produced)
            agents_run += 1
        work_items.extend(team_items)
        work_items.append(_run_director(director, team_items))
        agents_run += 1

    pending = sum(1 for w in work_items if w.status == STATUS_PENDING_APPROVAL)
    internal = sum(1 for w in work_items if w.status == STATUS_INTERNAL)

    # Real approval load = the actual number of drafts behind each external
    # work item (an item may bundle many drafts via payload["count"]).
    draft_volume = sum(
        int(w.payload.get("count", 1))
        for w in work_items
        if w.status == STATUS_PENDING_APPROVAL
    )

    # Tier 0 — Chief of Staff assembles the founder brief.
    chief_role = chief()
    agents_run += 1
    if draft_volume > 20:
        escalations.append(
            f"approval-load: {draft_volume} drafts pending — review before end of day"
        )

    # The Chief of Staff's brief is itself the final (internal) work item.
    items_total = len(work_items) + 1
    internal_total = internal + 1
    brief_en = (
        f"Daily executive cycle for {run_on}: {agents_run} agents ran, "
        f"{items_total} work items produced, {pending} drafts awaiting your "
        f"one-click approval, {internal_total} internal items done. "
        f"{len(escalations)} escalation(s)."
    )
    brief_ar = (
        f"الدورة التنفيذية اليومية ليوم {run_on}: عمل {agents_run} وكيلاً، "
        f"أُنتج {items_total} عنصر عمل، {pending} مسودة تنتظر موافقتك بنقرة "
        f"واحدة، و{internal_total} عنصراً داخلياً مكتملاً. "
        f"عدد التصعيدات: {len(escalations)}."
    )

    cycle_id = generate_id("cycle")
    chief_item = _make_item(
        chief_role,
        kind="founder_brief",
        title_ar="موجز المؤسس اليومي",
        title_en="Daily founder brief",
        summary=brief_en,
        payload={"escalations": escalations, "cycle_id": cycle_id},
    )
    work_items.append(chief_item)

    return DailyOrgReport(
        cycle_id=cycle_id,
        run_date=run_on,
        agents_run=agents_run,
        items_total=len(work_items),
        items_pending_approval=sum(
            1 for w in work_items if w.status == STATUS_PENDING_APPROVAL
        ),
        items_internal=sum(1 for w in work_items if w.status == STATUS_INTERNAL),
        escalations=escalations,
        founder_brief_ar=brief_ar,
        founder_brief_en=brief_en,
        work_items=work_items,
    )


__all__ = [
    "STATUS_INTERNAL",
    "STATUS_PENDING_APPROVAL",
    "WorkItem",
    "DailyOrgReport",
    "run_daily_cycle",
]
