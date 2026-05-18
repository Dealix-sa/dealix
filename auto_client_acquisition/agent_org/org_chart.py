"""Dealix Agent Organization — the org chart.

A governed pyramid of agent roles: one Chief of Staff, six Directors, and
eighteen Operators. This module is **pure data + helpers** — it declares
*who exists, what they own, and who they report to*. The daily executive
cycle that actually runs them lives in ``orchestrator.py``.

منظمة وكلاء ديلكس — الهيكل التنظيمي: رئيس أركان، ستة مدراء، ثمانية عشر
وكيلاً تنفيذياً. هرم محكوم — كل مخرج خارجي مسودة تمر على الموافقة البشرية.

Doctrine (non-negotiable):
  - No role exceeds L2 (DRAFT) autonomy for any externally-visible output.
  - Every external work item is draft-only and routed to the approval queue.
  - No scraping, no cold automation, no guaranteed-outcome language.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from auto_client_acquisition.agent_os.autonomy_levels import AutonomyLevel

# Tier constants — lower number = higher in the pyramid.
TIER_CHIEF = 0
TIER_DIRECTOR = 1
TIER_OPERATOR = 2


@dataclass(frozen=True)
class AgentRole:
    """One seat in the organization."""

    id: str
    name_ar: str
    name_en: str
    tier: int
    reports_to: str | None
    mission_ar: str
    mission_en: str
    autonomy: AutonomyLevel
    produces_external: bool
    mandate: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, object]:
        return {
            "id": self.id,
            "name_ar": self.name_ar,
            "name_en": self.name_en,
            "tier": self.tier,
            "tier_label": _TIER_LABEL[self.tier],
            "reports_to": self.reports_to,
            "mission_ar": self.mission_ar,
            "mission_en": self.mission_en,
            "autonomy": int(self.autonomy),
            "autonomy_label": self.autonomy.name,
            "produces_external": self.produces_external,
            "mandate": list(self.mandate),
        }


_TIER_LABEL: dict[int, str] = {
    TIER_CHIEF: "chief",
    TIER_DIRECTOR: "director",
    TIER_OPERATOR: "operator",
}


# ── Tier 0 — Chief of Staff ──────────────────────────────────────────
_CHIEF = AgentRole(
    id="chief_of_staff",
    name_ar="رئيس الأركان",
    name_en="Chief of Staff",
    tier=TIER_CHIEF,
    reports_to=None,
    mission_ar="يدير الدورة التنفيذية اليومية، يجمّع موجز المؤسس، ويرفع التصعيدات.",
    mission_en="Runs the daily executive cycle, assembles the founder brief, raises escalations.",
    autonomy=AutonomyLevel.L3_RECOMMEND,
    produces_external=False,
    mandate=("daily_cycle", "founder_brief", "escalation"),
)


# ── Tier 1 — Directors ───────────────────────────────────────────────
_DIRECTORS: tuple[AgentRole, ...] = (
    AgentRole(
        id="revenue_director",
        name_ar="مدير الإيراد",
        name_en="Revenue Director",
        tier=TIER_DIRECTOR,
        reports_to="chief_of_staff",
        mission_ar="يملك سلّم العروض الخمسة وخط الأنابيب من الحساب المؤهل حتى الإغلاق.",
        mission_en="Owns the 5-rung offer ladder and the pipeline from qualified account to close.",
        autonomy=AutonomyLevel.L3_RECOMMEND,
        produces_external=False,
        mandate=("pipeline_review", "revenue_plan"),
    ),
    AgentRole(
        id="delivery_director",
        name_ar="مدير التسليم",
        name_en="Delivery Director",
        tier=TIER_DIRECTOR,
        reports_to="chief_of_staff",
        mission_ar="يملك تنفيذ السبرنت وجودة التسليم وحزمة الإثبات.",
        mission_en="Owns sprint execution, delivery quality, and the Proof Pack.",
        autonomy=AutonomyLevel.L3_RECOMMEND,
        produces_external=False,
        mandate=("delivery_review", "capacity_plan"),
    ),
    AgentRole(
        id="customer_director",
        name_ar="مدير العملاء",
        name_en="Customer Director",
        tier=TIER_DIRECTOR,
        reports_to="chief_of_staff",
        mission_ar="يملك الاحتفاظ بالعملاء، صحة الحسابات، والتوسّع المحكوم بالإثبات.",
        mission_en="Owns retention, account health, and proof-gated expansion.",
        autonomy=AutonomyLevel.L3_RECOMMEND,
        produces_external=False,
        mandate=("retention_review", "expansion_plan"),
    ),
    AgentRole(
        id="growth_director",
        name_ar="مدير النمو",
        name_en="Growth Director",
        tier=TIER_DIRECTOR,
        reports_to="chief_of_staff",
        mission_ar="يملك محتوى ديلكس الخاص، محرّك السلطة، وشبكة الشركاء.",
        mission_en="Owns Dealix's own content, the authority engine, and the partner network.",
        autonomy=AutonomyLevel.L3_RECOMMEND,
        produces_external=False,
        mandate=("growth_review", "content_calendar"),
    ),
    AgentRole(
        id="governance_director",
        name_ar="مدير الحوكمة",
        name_en="Governance Director",
        tier=TIER_DIRECTOR,
        reports_to="chief_of_staff",
        mission_ar="يملك الامتثال، بوابة الموافقات، وحماية الخصوصية (PDPL).",
        mission_en="Owns compliance, the approval gate, and PDPL privacy protection.",
        autonomy=AutonomyLevel.L3_RECOMMEND,
        produces_external=False,
        mandate=("governance_review", "compliance_gate"),
    ),
    AgentRole(
        id="intelligence_director",
        name_ar="مدير الذكاء",
        name_en="Intelligence Director",
        tier=TIER_DIRECTOR,
        reports_to="chief_of_staff",
        mission_ar="يملك جودة البيانات، التسجيل، رصد السوق، وسجل الاحتكاك.",
        mission_en="Owns data quality, scoring, market radar, and the friction log.",
        autonomy=AutonomyLevel.L3_RECOMMEND,
        produces_external=False,
        mandate=("intelligence_review", "market_brief"),
    ),
)


# ── Tier 2 — Operators ───────────────────────────────────────────────
_OPERATORS: tuple[AgentRole, ...] = (
    # Revenue
    AgentRole(
        id="lead_scout",
        name_ar="كشّاف العملاء المحتملين",
        name_en="Lead Scout",
        tier=TIER_OPERATOR,
        reports_to="revenue_director",
        mission_ar="يجهّز قائمة حسابات مؤهلة بمعيار ICP — دافئة أولاً، بلا scraping.",
        mission_en="Prepares an ICP-qualified account list — warm-first, no scraping.",
        autonomy=AutonomyLevel.L1_ANALYZE,
        produces_external=False,
        mandate=("qualified_accounts",),
    ),
    AgentRole(
        id="proposal_drafter",
        name_ar="كاتب العروض",
        name_en="Proposal Drafter",
        tier=TIER_OPERATOR,
        reports_to="revenue_director",
        mission_ar="يكتب مسودات عروض من سلّم العروض — نطاق محدود، بلا وعود نتائج.",
        mission_en="Drafts proposals from the offer ladder — bounded scope, no outcome promises.",
        autonomy=AutonomyLevel.L2_DRAFT,
        produces_external=True,
        mandate=("proposal_draft",),
    ),
    AgentRole(
        id="outreach_drafter",
        name_ar="كاتب التواصل",
        name_en="Outreach Drafter",
        tier=TIER_OPERATOR,
        reports_to="revenue_director",
        mission_ar="يكتب مسودات تواصل دافئ — كل مسودة تذهب لقائمة الموافقة، لا إرسال آلي.",
        mission_en="Drafts warm outreach — every draft goes to the approval queue, never auto-sent.",
        autonomy=AutonomyLevel.L2_DRAFT,
        produces_external=True,
        mandate=("outreach_draft",),
    ),
    # Delivery
    AgentRole(
        id="sprint_planner",
        name_ar="مخطّط السبرنت",
        name_en="Sprint Planner",
        tier=TIER_OPERATOR,
        reports_to="delivery_director",
        mission_ar="يحوّل المشروع المباع إلى خطة سبرنت سبعة أيام بحدود واضحة.",
        mission_en="Turns a sold engagement into a bounded 7-day sprint plan.",
        autonomy=AutonomyLevel.L1_ANALYZE,
        produces_external=False,
        mandate=("sprint_plan",),
    ),
    AgentRole(
        id="data_quality_agent",
        name_ar="وكيل جودة البيانات",
        name_en="Data Quality Agent",
        tier=TIER_OPERATOR,
        reports_to="delivery_director",
        mission_ar="يفحص بيانات العميل ويصدر درجة جودة قبل أي تحليل.",
        mission_en="Inspects customer data and issues a quality score before any analysis.",
        autonomy=AutonomyLevel.L1_ANALYZE,
        produces_external=False,
        mandate=("data_quality_score",),
    ),
    AgentRole(
        id="proof_assembler",
        name_ar="مجمّع حزمة الإثبات",
        name_en="Proof Assembler",
        tier=TIER_OPERATOR,
        reports_to="delivery_director",
        mission_ar="يجمّع حزمة الإثبات بأربعة عشر قسماً لكل تسليم.",
        mission_en="Assembles the 14-section Proof Pack for every delivery.",
        autonomy=AutonomyLevel.L2_DRAFT,
        produces_external=True,
        mandate=("proof_pack_draft",),
    ),
    # Customer
    AgentRole(
        id="followup_sequencer",
        name_ar="مرتّب المتابعات",
        name_en="Follow-up Sequencer",
        tier=TIER_OPERATOR,
        reports_to="customer_director",
        mission_ar="يولّد مسودات متابعة D+3 / D+7 / D+14 — كلها للموافقة.",
        mission_en="Generates D+3 / D+7 / D+14 follow-up drafts — all approval-gated.",
        autonomy=AutonomyLevel.L2_DRAFT,
        produces_external=True,
        mandate=("followup_draft",),
    ),
    AgentRole(
        id="health_monitor",
        name_ar="مراقب صحة الحسابات",
        name_en="Account Health Monitor",
        tier=TIER_OPERATOR,
        reports_to="customer_director",
        mission_ar="يراقب إشارات صحة كل حساب ويصنّفها.",
        mission_en="Monitors each account's health signals and buckets them.",
        autonomy=AutonomyLevel.L1_ANALYZE,
        produces_external=False,
        mandate=("health_signal",),
    ),
    AgentRole(
        id="expansion_agent",
        name_ar="وكيل التوسّع",
        name_en="Expansion Agent",
        tier=TIER_OPERATOR,
        reports_to="customer_director",
        mission_ar="يقترح العرض التالي — محكوم بالإثبات، لا توسّع بلا إثبات موثّق.",
        mission_en="Recommends the next-best offer — proof-gated, no upsell without recorded proof.",
        autonomy=AutonomyLevel.L3_RECOMMEND,
        produces_external=False,
        mandate=("expansion_recommendation",),
    ),
    # Growth
    AgentRole(
        id="content_writer",
        name_ar="كاتب المحتوى",
        name_en="Content Writer",
        tier=TIER_OPERATOR,
        reports_to="growth_director",
        mission_ar="يكتب محتوى ديلكس الخاص — لا تواصل بارد، نشر ذاتي فقط.",
        mission_en="Writes Dealix's own content — no cold outreach, own-channel publishing only.",
        autonomy=AutonomyLevel.L2_DRAFT,
        produces_external=True,
        mandate=("content_draft",),
    ),
    AgentRole(
        id="partner_scout",
        name_ar="كشّاف الشركاء",
        name_en="Partner Scout",
        tier=TIER_OPERATOR,
        reports_to="growth_director",
        mission_ar="يجهّز قائمة شركاء وكالات محتملين لحركة الإسفين.",
        mission_en="Prepares a candidate agency-partner list for the wedge motion.",
        autonomy=AutonomyLevel.L1_ANALYZE,
        produces_external=False,
        mandate=("partner_candidates",),
    ),
    AgentRole(
        id="distribution_planner",
        name_ar="مخطّط النشر",
        name_en="Distribution Planner",
        tier=TIER_OPERATOR,
        reports_to="growth_director",
        mission_ar="يجدول نشر المحتوى المعتمد عبر قنوات ديلكس بأفضل توقيت.",
        mission_en="Schedules approved content across Dealix channels at the best times.",
        autonomy=AutonomyLevel.L2_DRAFT,
        produces_external=True,
        mandate=("distribution_schedule",),
    ),
    # Governance
    AgentRole(
        id="compliance_reviewer",
        name_ar="مراجع الامتثال",
        name_en="Compliance Reviewer",
        tier=TIER_OPERATOR,
        reports_to="governance_director",
        mission_ar="يفحص كل مخرج خارجي بحثاً عن وعود مضمونة أو لغة ممنوعة.",
        mission_en="Scans every external output for guaranteed-outcome or forbidden language.",
        autonomy=AutonomyLevel.L1_ANALYZE,
        produces_external=False,
        mandate=("compliance_finding",),
    ),
    AgentRole(
        id="approval_router",
        name_ar="موجّه الموافقات",
        name_en="Approval Router",
        tier=TIER_OPERATOR,
        reports_to="governance_director",
        mission_ar="يوجّه كل مخرج خارجي إلى قائمة موافقة المؤسس بنقرة واحدة.",
        mission_en="Routes every external output to the founder's one-click approval queue.",
        autonomy=AutonomyLevel.L1_ANALYZE,
        produces_external=False,
        mandate=("approval_routing",),
    ),
    AgentRole(
        id="pdpl_auditor",
        name_ar="مدقّق الخصوصية",
        name_en="PDPL Auditor",
        tier=TIER_OPERATOR,
        reports_to="governance_director",
        mission_ar="يدقّق التعامل مع البيانات الشخصية وفق نظام حماية البيانات.",
        mission_en="Audits personal-data handling against PDPL.",
        autonomy=AutonomyLevel.L1_ANALYZE,
        produces_external=False,
        mandate=("pdpl_finding",),
    ),
    # Intelligence
    AgentRole(
        id="market_radar",
        name_ar="رادار السوق",
        name_en="Market Radar",
        tier=TIER_OPERATOR,
        reports_to="intelligence_director",
        mission_ar="يرصد إشارات السوق والقطاعات ذات الصلة بالعملاء.",
        mission_en="Scans market and sector signals relevant to customers.",
        autonomy=AutonomyLevel.L1_ANALYZE,
        produces_external=False,
        mandate=("market_signal",),
    ),
    AgentRole(
        id="metrics_analyst",
        name_ar="محلّل المؤشرات",
        name_en="Metrics Analyst",
        tier=TIER_OPERATOR,
        reports_to="intelligence_director",
        mission_ar="يحلّل مؤشرات الإيراد والتسليم والاحتفاظ للموجز اليومي.",
        mission_en="Analyzes revenue, delivery, and retention metrics for the daily brief.",
        autonomy=AutonomyLevel.L1_ANALYZE,
        produces_external=False,
        mandate=("metrics_summary",),
    ),
    AgentRole(
        id="friction_logger",
        name_ar="مسجّل الاحتكاك",
        name_en="Friction Logger",
        tier=TIER_OPERATOR,
        reports_to="intelligence_director",
        mission_ar="يسجّل كل احتكاك تشغيلي ليُحوَّل لقرار تحسين.",
        mission_en="Logs every operational friction so it becomes an improvement decision.",
        autonomy=AutonomyLevel.L1_ANALYZE,
        produces_external=False,
        mandate=("friction_entry",),
    ),
)


ORG: tuple[AgentRole, ...] = (_CHIEF, *_DIRECTORS, *_OPERATORS)

_BY_ID: dict[str, AgentRole] = {role.id: role for role in ORG}


# ── Helpers ──────────────────────────────────────────────────────────


def all_roles() -> tuple[AgentRole, ...]:
    """Every role in the organization, chief first."""
    return ORG


def get_role(role_id: str) -> AgentRole:
    """Return one role by id. Raises KeyError if unknown."""
    return _BY_ID[role_id]


def has_role(role_id: str) -> bool:
    return role_id in _BY_ID


def chief() -> AgentRole:
    return _CHIEF


def directors() -> tuple[AgentRole, ...]:
    return _DIRECTORS


def operators() -> tuple[AgentRole, ...]:
    return _OPERATORS


def roles_by_tier(tier: int) -> tuple[AgentRole, ...]:
    return tuple(r for r in ORG if r.tier == tier)


def operators_under(director_id: str) -> tuple[AgentRole, ...]:
    """Operators that report to the given director."""
    return tuple(r for r in _OPERATORS if r.reports_to == director_id)


def external_roles() -> tuple[AgentRole, ...]:
    """Roles whose output is externally visible (draft-only, approval-gated)."""
    return tuple(r for r in ORG if r.produces_external)


def validate_org() -> list[str]:
    """Structural integrity check. Returns a list of problems (empty == healthy).

    Enforced invariants:
      - exactly one chief (tier 0) and it reports to no one;
      - every non-chief reports_to an existing role;
      - operators report to a director, directors report to the chief;
      - no cycles in the reporting chain;
      - no role exceeds L2 autonomy while producing external output
        (doctrine: external work is draft-only).
    """
    problems: list[str] = []

    chiefs = roles_by_tier(TIER_CHIEF)
    if len(chiefs) != 1:
        problems.append(f"expected exactly 1 chief, found {len(chiefs)}")
    if chiefs and chiefs[0].reports_to is not None:
        problems.append("chief must not report to anyone")

    for role in ORG:
        if role.tier == TIER_CHIEF:
            continue
        if role.reports_to is None or role.reports_to not in _BY_ID:
            problems.append(f"{role.id}: reports_to {role.reports_to!r} does not resolve")
            continue
        manager = _BY_ID[role.reports_to]
        if role.tier == TIER_DIRECTOR and manager.tier != TIER_CHIEF:
            problems.append(f"{role.id}: director must report to the chief")
        if role.tier == TIER_OPERATOR and manager.tier != TIER_DIRECTOR:
            problems.append(f"{role.id}: operator must report to a director")

    for role in ORG:
        if role.produces_external and role.autonomy > AutonomyLevel.L2_DRAFT:
            problems.append(
                f"{role.id}: external output forbidden above L2 (draft) autonomy"
            )

    # Cycle detection over the reporting chain.
    for role in ORG:
        seen: set[str] = set()
        cursor: str | None = role.id
        while cursor is not None:
            if cursor in seen:
                problems.append(f"{role.id}: reporting cycle detected")
                break
            seen.add(cursor)
            cursor = _BY_ID[cursor].reports_to if cursor in _BY_ID else None

    return problems


def org_chart_dict() -> dict[str, object]:
    """Serializable org tree — chief → directors → operators."""
    return {
        "chief": {
            **_CHIEF.to_dict(),
            "directs": [
                {
                    **d.to_dict(),
                    "directs": [op.to_dict() for op in operators_under(d.id)],
                }
                for d in _DIRECTORS
            ],
        },
        "headcount": len(ORG),
        "tiers": {"chief": 1, "directors": len(_DIRECTORS), "operators": len(_OPERATORS)},
    }


__all__ = [
    "TIER_CHIEF",
    "TIER_DIRECTOR",
    "TIER_OPERATOR",
    "AgentRole",
    "ORG",
    "all_roles",
    "get_role",
    "has_role",
    "chief",
    "directors",
    "operators",
    "roles_by_tier",
    "operators_under",
    "external_roles",
    "validate_org",
    "org_chart_dict",
]
