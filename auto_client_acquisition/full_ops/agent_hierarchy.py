"""Full Ops agent hierarchy — the explicit governed agent pyramid.

Defines a single orchestrator ("Chief of Staff"), five directors, and a
set of operator agents under each director. Every node is registered as
an :class:`AgentCard` through the existing ``agent_registry``.

Doctrine guard: no node is registered above autonomy level L3. The MVP
ceiling is L3 (recommend) — L4 (auto-with-audit) and L5 (fully autonomous)
are never used here. Operators that only draft run at L2; operators that
run deterministic-but-recommending steps run at L3.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from auto_client_acquisition.agent_os.agent_card import AgentCard, new_card
from auto_client_acquisition.agent_os.agent_registry import (
    get_agent,
    list_agents,
    register_agent,
)
from auto_client_acquisition.agent_os.autonomy_levels import AutonomyLevel

# Hard ceiling for every node in this hierarchy (never exceed L3).
HIERARCHY_MAX_AUTONOMY_LEVEL: int = int(AutonomyLevel.L3_RECOMMEND)

_OWNER = "founder"
_KILL_SWITCH_OWNER = "founder"


@dataclass(frozen=True, slots=True)
class HierarchyNode:
    """One node in the Full Ops agent pyramid."""

    tier: str  # "orchestrator" | "director" | "operator"
    agent_id: str
    name: str
    role_ar: str
    role_en: str
    parent_id: str | None
    autonomy_level: int
    capabilities: tuple[str, ...] = field(default_factory=tuple)
    allowed_tools: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return {
            "tier": self.tier,
            "agent_id": self.agent_id,
            "name": self.name,
            "role_ar": self.role_ar,
            "role_en": self.role_en,
            "parent_id": self.parent_id,
            "autonomy_level": self.autonomy_level,
            "capabilities": list(self.capabilities),
            "allowed_tools": list(self.allowed_tools),
        }


_L2 = int(AutonomyLevel.L2_DRAFT)
_L3 = int(AutonomyLevel.L3_RECOMMEND)


# ── Orchestrator ──────────────────────────────────────────────────────

_ORCHESTRATOR = HierarchyNode(
    tier="orchestrator",
    agent_id="fo_orchestrator_chief_of_staff",
    name="Chief of Staff",
    role_ar="رئيس الأركان — ينسّق دورة العمليات الكاملة",
    role_en="Chief of Staff — coordinates the full operations cycle",
    parent_id=None,
    autonomy_level=_L3,
    capabilities=("plan_cycle", "delegate", "aggregate_report", "escalate"),
    allowed_tools=("read", "analyze", "recommend"),
)


# ── Directors ─────────────────────────────────────────────────────────

_DIRECTORS: tuple[HierarchyNode, ...] = (
    HierarchyNode(
        tier="director",
        agent_id="fo_director_sales",
        name="Sales Director",
        role_ar="مدير المبيعات — يقود قمع الاكتساب",
        role_en="Sales Director — owns the acquisition funnel",
        parent_id=_ORCHESTRATOR.agent_id,
        autonomy_level=_L3,
        capabilities=("own_pipeline", "qualify", "shape_offers"),
        allowed_tools=("read", "analyze", "recommend"),
    ),
    HierarchyNode(
        tier="director",
        agent_id="fo_director_delivery",
        name="Delivery Director",
        role_ar="مدير التسليم — يقود تنفيذ المشاريع وإثباتها",
        role_en="Delivery Director — owns sprint delivery and proof",
        parent_id=_ORCHESTRATOR.agent_id,
        autonomy_level=_L3,
        capabilities=("own_delivery", "proof_pack", "capital_assets"),
        allowed_tools=("read", "analyze", "recommend"),
    ),
    HierarchyNode(
        tier="director",
        agent_id="fo_director_content",
        name="Content Director",
        role_ar="مدير المحتوى — يقود المسوّدات والمواد",
        role_en="Content Director — owns drafts and bilingual material",
        parent_id=_ORCHESTRATOR.agent_id,
        autonomy_level=_L3,
        capabilities=("own_content", "draft_only", "bilingual"),
        allowed_tools=("read", "analyze", "draft"),
    ),
    HierarchyNode(
        tier="director",
        agent_id="fo_director_revenue",
        name="Revenue Director",
        role_ar="مدير الإيراد — يقود التسعير والقيمة",
        role_en="Revenue Director — owns scoring, value and renewals",
        parent_id=_ORCHESTRATOR.agent_id,
        autonomy_level=_L3,
        capabilities=("own_revenue", "score", "value_ledger"),
        allowed_tools=("read", "analyze", "recommend"),
    ),
    HierarchyNode(
        tier="director",
        agent_id="fo_director_governance",
        name="Governance Director",
        role_ar="مدير الحوكمة — يحرس الخطوط الحمراء",
        role_en="Governance Director — guards the non-negotiables",
        parent_id=_ORCHESTRATOR.agent_id,
        autonomy_level=_L3,
        capabilities=("own_governance", "block_unsafe", "require_approval"),
        allowed_tools=("read", "analyze", "recommend"),
    ),
)


def _operator(
    *,
    agent_id: str,
    name: str,
    role_ar: str,
    role_en: str,
    parent_id: str,
    autonomy_level: int,
    capabilities: tuple[str, ...],
    allowed_tools: tuple[str, ...],
) -> HierarchyNode:
    return HierarchyNode(
        tier="operator",
        agent_id=agent_id,
        name=name,
        role_ar=role_ar,
        role_en=role_en,
        parent_id=parent_id,
        autonomy_level=autonomy_level,
        capabilities=capabilities,
        allowed_tools=allowed_tools,
    )


# ── Operators (~21 total) ─────────────────────────────────────────────

_OPERATORS: tuple[HierarchyNode, ...] = (
    # Sales operators
    _operator(
        agent_id="fo_op_sales_intake",
        name="Lead Intake Operator",
        role_ar="مشغّل استقبال العملاء المحتملين",
        role_en="Lead intake operator",
        parent_id="fo_director_sales",
        autonomy_level=_L3,
        capabilities=("ingest_leads", "normalize"),
        allowed_tools=("read", "analyze"),
    ),
    _operator(
        agent_id="fo_op_sales_enrichment",
        name="Lead Enrichment Operator",
        role_ar="مشغّل إثراء بيانات العملاء",
        role_en="Lead enrichment operator",
        parent_id="fo_director_sales",
        autonomy_level=_L3,
        capabilities=("enrich_rows",),
        allowed_tools=("read", "analyze"),
    ),
    _operator(
        agent_id="fo_op_sales_scoring",
        name="Lead Scoring Operator",
        role_ar="مشغّل تصنيف العملاء المحتملين",
        role_en="Lead scoring operator",
        parent_id="fo_director_sales",
        autonomy_level=_L3,
        capabilities=("score_accounts",),
        allowed_tools=("read", "analyze"),
    ),
    _operator(
        agent_id="fo_op_sales_qualification",
        name="Qualification Operator",
        role_ar="مشغّل التأهيل التجاري",
        role_en="Qualification operator",
        parent_id="fo_director_sales",
        autonomy_level=_L3,
        capabilities=("qualify_leads",),
        allowed_tools=("read", "analyze", "recommend"),
    ),
    _operator(
        agent_id="fo_op_sales_proposal_draft",
        name="Proposal Draft Operator",
        role_ar="مشغّل مسوّدات العروض",
        role_en="Proposal draft operator",
        parent_id="fo_director_sales",
        autonomy_level=_L2,
        capabilities=("draft_proposals",),
        allowed_tools=("read", "draft"),
    ),
    _operator(
        agent_id="fo_op_sales_outreach_draft",
        name="Outreach Draft Operator",
        role_ar="مشغّل مسوّدات التواصل",
        role_en="Outreach draft operator",
        parent_id="fo_director_sales",
        autonomy_level=_L2,
        capabilities=("draft_outreach",),
        allowed_tools=("read", "draft"),
    ),
    _operator(
        agent_id="fo_op_sales_followup",
        name="Follow-up Planning Operator",
        role_ar="مشغّل تخطيط المتابعات",
        role_en="Follow-up planning operator",
        parent_id="fo_director_sales",
        autonomy_level=_L3,
        capabilities=("plan_followups",),
        allowed_tools=("read", "analyze", "recommend"),
    ),
    # Delivery operators
    _operator(
        agent_id="fo_op_delivery_sprint",
        name="Sprint Planning Operator",
        role_ar="مشغّل تخطيط المشاريع",
        role_en="Sprint planning operator",
        parent_id="fo_director_delivery",
        autonomy_level=_L3,
        capabilities=("plan_sprint",),
        allowed_tools=("read", "analyze", "recommend"),
    ),
    _operator(
        agent_id="fo_op_delivery_proof_pack",
        name="Proof Pack Operator",
        role_ar="مشغّل حزمة الإثبات",
        role_en="Proof pack operator",
        parent_id="fo_director_delivery",
        autonomy_level=_L3,
        capabilities=("assemble_proof_pack",),
        allowed_tools=("read", "analyze"),
    ),
    _operator(
        agent_id="fo_op_delivery_capital_asset",
        name="Capital Asset Operator",
        role_ar="مشغّل الأصول الرأسمالية",
        role_en="Capital asset operator",
        parent_id="fo_director_delivery",
        autonomy_level=_L3,
        capabilities=("register_capital_asset",),
        allowed_tools=("read", "analyze"),
    ),
    _operator(
        agent_id="fo_op_delivery_retainer",
        name="Retainer Readiness Operator",
        role_ar="مشغّل جاهزية الاشتراك الشهري",
        role_en="Retainer readiness operator",
        parent_id="fo_director_delivery",
        autonomy_level=_L3,
        capabilities=("evaluate_retainer",),
        allowed_tools=("read", "analyze", "recommend"),
    ),
    # Content operators
    _operator(
        agent_id="fo_op_content_email_draft",
        name="Email Draft Operator",
        role_ar="مشغّل مسوّدات البريد",
        role_en="Email draft operator",
        parent_id="fo_director_content",
        autonomy_level=_L2,
        capabilities=("draft_email",),
        allowed_tools=("read", "draft"),
    ),
    _operator(
        agent_id="fo_op_content_case_study",
        name="Case Study Draft Operator",
        role_ar="مشغّل مسوّدات دراسات الحالة",
        role_en="Case study draft operator",
        parent_id="fo_director_content",
        autonomy_level=_L2,
        capabilities=("draft_case_study",),
        allowed_tools=("read", "draft"),
    ),
    _operator(
        agent_id="fo_op_content_bilingual_qa",
        name="Bilingual QA Operator",
        role_ar="مشغّل مراجعة المحتوى ثنائي اللغة",
        role_en="Bilingual QA operator",
        parent_id="fo_director_content",
        autonomy_level=_L3,
        capabilities=("check_bilingual",),
        allowed_tools=("read", "analyze"),
    ),
    _operator(
        agent_id="fo_op_content_report",
        name="Report Composer Operator",
        role_ar="مشغّل تأليف التقارير",
        role_en="Report composer operator",
        parent_id="fo_director_content",
        autonomy_level=_L3,
        capabilities=("compose_report",),
        allowed_tools=("read", "analyze"),
    ),
    # Revenue operators
    _operator(
        agent_id="fo_op_revenue_account_scoring",
        name="Account Scoring Operator",
        role_ar="مشغّل تصنيف الحسابات",
        role_en="Account scoring operator",
        parent_id="fo_director_revenue",
        autonomy_level=_L3,
        capabilities=("score_account_value",),
        allowed_tools=("read", "analyze"),
    ),
    _operator(
        agent_id="fo_op_revenue_value_ledger",
        name="Value Ledger Operator",
        role_ar="مشغّل سجل القيمة",
        role_en="Value ledger operator",
        parent_id="fo_director_revenue",
        autonomy_level=_L3,
        capabilities=("record_value_event",),
        allowed_tools=("read", "analyze"),
    ),
    _operator(
        agent_id="fo_op_revenue_renewal",
        name="Renewal Scheduling Operator",
        role_ar="مشغّل جدولة التجديدات",
        role_en="Renewal scheduling operator",
        parent_id="fo_director_revenue",
        autonomy_level=_L3,
        capabilities=("schedule_renewal",),
        allowed_tools=("read", "analyze", "recommend"),
    ),
    _operator(
        agent_id="fo_op_revenue_expansion",
        name="Expansion Recommendation Operator",
        role_ar="مشغّل توصيات التوسّع",
        role_en="Expansion recommendation operator",
        parent_id="fo_director_revenue",
        autonomy_level=_L3,
        capabilities=("recommend_expansion",),
        allowed_tools=("read", "analyze", "recommend"),
    ),
    # Governance operators
    _operator(
        agent_id="fo_op_governance_policy_check",
        name="Policy Check Operator",
        role_ar="مشغّل فحص السياسات",
        role_en="Policy check operator",
        parent_id="fo_director_governance",
        autonomy_level=_L3,
        capabilities=("check_policy",),
        allowed_tools=("read", "analyze"),
    ),
    _operator(
        agent_id="fo_op_governance_approval_router",
        name="Approval Routing Operator",
        role_ar="مشغّل توجيه الموافقات",
        role_en="Approval routing operator",
        parent_id="fo_director_governance",
        autonomy_level=_L3,
        capabilities=("route_approvals",),
        allowed_tools=("read", "analyze", "recommend"),
    ),
    _operator(
        agent_id="fo_op_governance_audit",
        name="Audit Trail Operator",
        role_ar="مشغّل سجل التدقيق",
        role_en="Audit trail operator",
        parent_id="fo_director_governance",
        autonomy_level=_L3,
        capabilities=("emit_audit",),
        allowed_tools=("read", "analyze"),
    ),
)


def all_nodes() -> tuple[HierarchyNode, ...]:
    """Return every node in the pyramid (orchestrator, directors, operators)."""
    return (_ORCHESTRATOR, *_DIRECTORS, *_OPERATORS)


def _purpose(node: HierarchyNode) -> str:
    return f"Full Ops {node.tier}: {node.role_en}"


def _node_to_card(node: HierarchyNode) -> AgentCard:
    """Build a validated :class:`AgentCard` for a hierarchy node.

    Asserts the L3 ceiling defensively before delegating to ``new_card``.
    """
    if node.autonomy_level > HIERARCHY_MAX_AUTONOMY_LEVEL:
        raise ValueError(
            f"node {node.agent_id} autonomy_level {node.autonomy_level} "
            f"exceeds the L3 ceiling"
        )
    return new_card(
        agent_id=node.agent_id,
        name=node.name,
        owner=_OWNER,
        purpose=_purpose(node),
        autonomy_level=node.autonomy_level,
        allowed_tools=list(node.allowed_tools),
        kill_switch_owner=_KILL_SWITCH_OWNER,
        notes=f"parent={node.parent_id or 'none'}; tier={node.tier}",
    )


def seed_hierarchy() -> list[AgentCard]:
    """Register every hierarchy node as an :class:`AgentCard`.

    Idempotent: if a node is already registered it is returned as-is
    rather than re-registered. Returns the full set of cards.
    """
    cards: list[AgentCard] = []
    for node in all_nodes():
        existing = get_agent(node.agent_id)
        if existing is not None:
            cards.append(existing)
            continue
        card = _node_to_card(node)
        try:
            cards.append(register_agent(card))
        except ValueError:
            # Lost a race; fetch the now-registered card.
            again = get_agent(node.agent_id)
            cards.append(again if again is not None else card)
    return cards


def get_hierarchy() -> dict[str, Any]:
    """Return the pyramid as a nested tree with totals."""
    operators_by_parent: dict[str, list[dict[str, Any]]] = {}
    for op in _OPERATORS:
        operators_by_parent.setdefault(op.parent_id or "", []).append(op.to_dict())

    directors: list[dict[str, Any]] = []
    for d in _DIRECTORS:
        node = d.to_dict()
        node["operators"] = operators_by_parent.get(d.agent_id, [])
        directors.append(node)

    return {
        "orchestrator": _ORCHESTRATOR.to_dict(),
        "directors": directors,
        "totals": {
            "directors": len(_DIRECTORS),
            "operators": len(_OPERATORS),
            "max_autonomy_level": HIERARCHY_MAX_AUTONOMY_LEVEL,
        },
    }


def hierarchy_status() -> dict[str, Any]:
    """Return the pyramid annotated with the live registry status of
    each node (``proposed``/``active``/``killed``/``unregistered``)."""
    registered = {c.agent_id: c for c in list_agents()}

    def _status(agent_id: str) -> str:
        card = registered.get(agent_id)
        return card.status if card is not None else "unregistered"

    tree = get_hierarchy()
    orch = tree["orchestrator"]
    orch["status"] = _status(orch["agent_id"])
    for director in tree["directors"]:
        director["status"] = _status(director["agent_id"])
        for op in director["operators"]:
            op["status"] = _status(op["agent_id"])
    return tree


__all__ = [
    "HIERARCHY_MAX_AUTONOMY_LEVEL",
    "HierarchyNode",
    "all_nodes",
    "get_hierarchy",
    "hierarchy_status",
    "seed_hierarchy",
]
