"""Company-wide workload routing for the canonical Dealix operating system.

This module is deliberately a *feature layer*, not another runtime.  It maps a
business burden to the existing service catalog and Full-Ops queue while
keeping external actions approval-first.
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import asdict, dataclass
from typing import Any, Literal

from auto_client_acquisition.full_ops import WorkItem

CompanyDomain = Literal[
    "executive_strategy",
    "growth",
    "sales",
    "marketing_brand",
    "customer_support",
    "customer_success",
    "delivery_pmo",
    "operations",
    "finance",
    "data_intelligence",
    "compliance_risk",
    "people_ops",
    "procurement_vendor",
    "product",
    "knowledge",
    "partnerships",
]


@dataclass(frozen=True)
class Capability:
    domain: CompanyDomain
    name_ar: str
    name_en: str
    os_type: str
    owner_role: str
    keywords: tuple[str, ...]
    service_ids: tuple[str, ...]
    agents: tuple[str, ...]
    integrations: tuple[str, ...]
    artifacts: tuple[str, ...]
    proof_metrics: tuple[str, ...]


_CAPABILITIES: tuple[Capability, ...] = (
    Capability(
        "executive_strategy",
        "الاستراتيجية والقيادة",
        "Executive strategy",
        "executive",
        "executive_owner",
        (
            "strategy", "executive", "board", "decision", "okr", "استراتيجية",
            "تنفيذي", "إدارة", "قرار", "اهداف", "أهداف",
        ),
        (
            "ai_command_center_os", "executive_reporting_os",
            "executive_command_center_7500",
        ),
        ("company_brain", "strategy_agent", "decision_agent"),
        ("erp", "crm", "project_management", "bi"),
        ("decision_passport", "operating_plan", "executive_brief"),
        ("decision_cycle_time", "plan_completion_rate", "hours_saved"),
    ),
    Capability(
        "growth", "النمو", "Growth", "growth", "growth_owner",
        (
            "growth", "acquisition", "funnel", "experiment", "conversion", "نمو",
            "استحواذ", "قمع", "تحويل", "تجربة",
        ),
        ("growth_engine_os", "growth_ops_monthly_2999", "revenue_proof_sprint_499"),
        ("market_intelligence_agent", "growth_agent", "experiment_agent"),
        ("analytics", "crm", "website", "ads"),
        ("growth_diagnostic", "experiment_backlog", "weekly_growth_pack"),
        ("qualified_pipeline", "conversion_rate", "experiment_velocity"),
    ),
    Capability(
        "sales", "المبيعات", "Sales", "sales", "sales_owner",
        (
            "sales", "lead", "pipeline", "proposal", "deal", "negotiation",
            "meeting", "مبيعات", "عميل محتمل", "صفقة", "عرض", "تفاوض", "موعد",
        ),
        ("revenue_proof_sprint_499", "growth_engine_os", "data_to_revenue_pack_1500"),
        ("research_agent", "qualification_agent", "proposal_agent", "deal_coach"),
        ("crm", "email", "calendar", "whatsapp_business"),
        ("account_dossier", "qualification_brief", "proposal_draft", "meeting_brief"),
        ("qualified_opportunities", "reply_rate", "meeting_rate", "sales_cycle_days"),
    ),
    Capability(
        "marketing_brand",
        "التسويق والعلامة",
        "Marketing and brand",
        "growth",
        "marketing_owner",
        (
            "marketing", "campaign", "content", "brand", "seo", "social", "تسويق",
            "حملة", "محتوى", "علامة", "هوية", "منصات",
        ),
        ("brand_intelligence_os", "growth_engine_os"),
        ("brand_agent", "content_agent", "campaign_agent"),
        ("website", "analytics", "cms", "approved_social_channels"),
        ("brand_diagnostic", "content_plan", "campaign_draft_pack"),
        ("content_conversion", "brand_consistency", "marketing_sourced_pipeline"),
    ),
    Capability(
        "customer_support",
        "خدمة العملاء",
        "Customer support",
        "support",
        "support_owner",
        (
            "support", "ticket", "sla", "complaint", "inbox", "دعم", "تذكرة",
            "شكوى", "خدمة عملاء", "استفسار",
        ),
        ("support_os_addon_1500", "client_experience_os"),
        ("triage_agent", "reply_draft_agent", "escalation_agent"),
        ("helpdesk", "email", "whatsapp_business", "knowledge_base"),
        ("ticket_classification", "reply_draft", "root_cause_map", "sla_alert"),
        ("first_response_time", "resolution_time", "reopen_rate", "csat"),
    ),
    Capability(
        "customer_success",
        "نجاح العملاء",
        "Customer success",
        "customer_success",
        "customer_success_owner",
        (
            "customer success", "renewal", "churn", "adoption", "health score",
            "نجاح العملاء", "تجديد", "تسرب", "تبني", "رضا",
        ),
        ("client_experience_os", "executive_command_center_7500"),
        ("health_agent", "adoption_agent", "renewal_agent"),
        ("crm", "product_analytics", "support", "billing"),
        ("health_score", "success_plan", "renewal_risk_brief"),
        ("retention", "adoption", "expansion", "time_to_value"),
    ),
    Capability(
        "delivery_pmo",
        "التسليم وإدارة المشاريع",
        "Delivery and PMO",
        "delivery",
        "delivery_owner",
        (
            "delivery", "project", "milestone", "scope", "pmo", "implementation",
            "تسليم", "مشروع", "مرحلة", "نطاق", "تنفيذ",
        ),
        ("operations_automation_os", "custom_enterprise_system"),
        ("project_planner", "dependency_agent", "delivery_risk_agent"),
        ("project_management", "documents", "calendar", "erp"),
        ("delivery_plan", "dependency_map", "risk_register", "status_pack"),
        ("on_time_delivery", "scope_variance", "cycle_time", "rework_rate"),
    ),
    Capability(
        "operations",
        "العمليات والأتمتة",
        "Operations and automation",
        "delivery",
        "operations_owner",
        (
            "operations", "workflow", "process", "automation", "back office",
            "تشغيل", "عمليات", "إجراء", "أتمتة", "عبء", "روتيني",
        ),
        ("operations_automation_os", "ai_agent_workforce_os", "custom_enterprise_system"),
        ("process_miner", "workflow_designer", "automation_agent", "qa_agent"),
        ("erp", "project_management", "documents", "approved_connectors"),
        ("process_map", "automation_blueprint", "runbook", "exception_queue"),
        ("hours_saved", "cycle_time", "error_rate", "automation_success_rate"),
    ),
    Capability(
        "finance",
        "المالية والتحصيل",
        "Finance and collections",
        "executive",
        "finance_owner",
        (
            "finance", "invoice", "cash", "budget", "collection", "payment",
            "refund", "مالية", "فاتورة", "ميزانية", "تحصيل", "دفع", "استرداد",
        ),
        ("executive_reporting_os", "operations_automation_os", "custom_enterprise_system"),
        ("finance_ops_agent", "collections_draft_agent", "variance_agent"),
        ("accounting", "billing", "erp", "bank_feed_read_only"),
        ("cash_brief", "invoice_exception_queue", "variance_report"),
        ("days_sales_outstanding", "collection_rate", "forecast_accuracy", "close_cycle_days"),
    ),
    Capability(
        "data_intelligence",
        "البيانات والذكاء",
        "Data and intelligence",
        "executive",
        "data_owner",
        (
            "data", "dashboard", "analytics", "forecast", "report", "بيانات",
            "لوحة", "تحليل", "توقع", "تقرير",
        ),
        ("data_to_revenue_pack_1500", "ai_command_center_os", "executive_reporting_os"),
        ("data_quality_agent", "insight_agent", "forecast_agent"),
        ("warehouse", "crm", "erp", "bi"),
        ("data_quality_report", "metric_dictionary", "decision_dashboard"),
        ("data_freshness", "completeness", "forecast_error", "decision_adoption"),
    ),
    Capability(
        "compliance_risk",
        "الامتثال والمخاطر",
        "Compliance and risk",
        "compliance",
        "compliance_owner",
        (
            "compliance", "privacy", "pdpl", "risk", "audit", "legal", "security",
            "امتثال", "خصوصية", "مخاطر", "تدقيق", "قانون", "أمن",
        ),
        ("trust_governance_os", "custom_enterprise_system"),
        ("policy_agent", "risk_agent", "evidence_agent", "incident_coordinator"),
        ("identity", "audit_log", "data_catalog", "security_monitoring"),
        ("control_map", "risk_register", "evidence_pack", "incident_brief"),
        ("control_coverage", "open_risks", "incident_response_time", "audit_findings"),
    ),
    Capability(
        "people_ops",
        "عمليات الموارد البشرية",
        "People operations",
        "executive",
        "people_owner",
        (
            "people", "hr", "hiring", "employee", "performance", "training",
            "موارد بشرية", "توظيف", "موظف", "أداء", "تدريب", "فصل",
        ),
        ("ai_agent_workforce_os", "operations_automation_os", "custom_enterprise_system"),
        ("workforce_planner", "onboarding_agent", "learning_agent"),
        ("hris", "documents", "calendar", "identity"),
        ("workforce_plan", "onboarding_pack", "training_path", "decision_brief"),
        ("time_to_productivity", "training_completion", "retention", "manager_hours_saved"),
    ),
    Capability(
        "procurement_vendor",
        "المشتريات والموردون",
        "Procurement and vendors",
        "delivery",
        "procurement_owner",
        (
            "procurement", "vendor", "supplier", "purchase", "rfp", "مشتريات",
            "مورد", "شراء", "مناقصة", "عقد",
        ),
        ("operations_automation_os", "custom_enterprise_system"),
        ("requirements_agent", "vendor_comparison_agent", "contract_risk_agent"),
        ("erp", "documents", "vendor_portal", "approval_system"),
        ("requirements_pack", "vendor_scorecard", "approval_brief"),
        ("procurement_cycle_time", "cost_variance", "vendor_sla", "approved_savings"),
    ),
    Capability(
        "product", "المنتج", "Product", "delivery", "product_owner",
        (
            "product", "feature", "roadmap", "research", "ux", "منتج", "ميزة",
            "خارطة", "بحث مستخدم", "تجربة مستخدم",
        ),
        ("ai_command_center_os", "custom_enterprise_system"),
        ("research_synthesizer", "product_strategy_agent", "spec_agent"),
        ("product_analytics", "support", "project_management", "research_repository"),
        ("opportunity_brief", "prioritized_roadmap", "product_spec"),
        ("feature_adoption", "time_to_learn", "delivery_lead_time", "outcome_attainment"),
    ),
    Capability(
        "knowledge",
        "المعرفة والسياسات",
        "Knowledge and policy",
        "executive",
        "knowledge_owner",
        (
            "knowledge", "policy", "sop", "document", "search", "معرفة", "سياسة",
            "دليل", "مستند", "بحث",
        ),
        ("ai_agent_workforce_os", "ai_command_center_os"),
        ("knowledge_curator", "retrieval_agent", "policy_draft_agent"),
        ("documents", "knowledge_base", "identity", "search"),
        ("knowledge_map", "source_grounded_answer", "policy_draft"),
        ("answer_groundedness", "search_success", "knowledge_freshness", "repeat_question_rate"),
    ),
    Capability(
        "partnerships",
        "الشراكات والقنوات",
        "Partnerships and channels",
        "partnership",
        "partnership_owner",
        (
            "partner", "partnership", "channel", "alliance", "referral", "شريك",
            "شراكة", "قناة", "تحالف", "إحالة",
        ),
        ("agency_partner_os", "growth_engine_os"),
        ("partner_research_agent", "partner_fit_agent", "partner_pack_agent"),
        ("crm", "documents", "email", "partner_portal"),
        ("partner_dossier", "joint_value_map", "partner_proposal_draft"),
        ("partner_sourced_pipeline", "activation_rate", "joint_wins", "partner_retention"),
    ),
)

_HIGH_RISK_TERMS = (
    "contract", "legal", "lawsuit", "discount", "price", "payment", "refund", "hire",
    "fire", "terminate", "security incident", "breach", "delete", "production",
    "personal data", "sensitive", "عقد", "قانون", "خصم", "سعر", "دفع", "استرداد",
    "توظيف", "فصل", "حادث أمني", "اختراق", "حذف", "إنتاج", "بيانات شخصية",
    "حساسة",
)
_EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
_PHONE_RE = re.compile(
    r"(?<!\w)(?:(?:\+?966|00966|0)[\s-]*)?5\d(?:[\s-]?\d){7}(?!\w)"
)


@dataclass(frozen=True)
class CompanyWorkloadRequest:
    tenant_id: str
    customer_id: str | None
    title: str
    description: str
    objective: str = ""
    urgency: Literal["low", "normal", "high", "critical"] = "normal"
    sensitivity: Literal["public", "internal", "confidential", "restricted"] = "internal"
    external_action_requested: bool = False
    requested_channel: str | None = None
    recipient_opted_in: bool | None = None
    evidence_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class WorkloadRoute:
    schema_version: int
    route_id: str
    tenant_id: str
    customer_id: str | None
    urgency: str
    evidence_ids: tuple[str, ...]
    sanitized_title: str
    sanitized_description: str
    pii_redacted: bool
    primary_domain: CompanyDomain
    supporting_domains: tuple[CompanyDomain, ...]
    matched_capabilities: tuple[dict[str, Any], ...]
    recommended_service_ids: tuple[str, ...]
    assigned_agents: tuple[str, ...]
    required_integrations: tuple[str, ...]
    execution_plan: tuple[dict[str, str], ...]
    artifacts: tuple[str, ...]
    proof_contract: tuple[str, ...]
    risk_level: Literal["low", "medium", "high", "critical"]
    risk_flags: tuple[str, ...]
    autonomy_level: Literal["L2_DRAFT", "L3_INTERNAL_EXECUTE", "L5_BLOCKED"]
    action_mode: str
    queue_status: str
    owner_role: str
    human_decision: dict[str, Any] | None
    missing_inputs: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_work_item(self) -> WorkItem:
        priority = {"critical": "p0", "high": "p1", "normal": "p2", "low": "p3"}
        # Route IDs are stable and the queue is idempotent; no raw contact data is stored.
        return WorkItem(
            id=self.route_id,
            tenant_id=self.tenant_id,
            customer_id=self.customer_id,
            os_type=_CAPABILITY_BY_DOMAIN[self.primary_domain].os_type,
            title_ar=self.sanitized_title[:140],
            title_en=self.sanitized_title[:140],
            description_ar=self.sanitized_description[:500],
            description_en=self.sanitized_description[:500],
            priority=priority[self.urgency],
            status=self.queue_status,
            action_mode=self.action_mode,
            owner_role=self.owner_role,
            source="company_os_workload_router",
            evidence_ids=list(self.evidence_ids),
            risk_flags=list(self.risk_flags),
            next_action_ar=self.execution_plan[0]["instruction_ar"],
            next_action_en=self.execution_plan[0]["instruction_en"],
        )

_CAPABILITY_BY_DOMAIN = {c.domain: c for c in _CAPABILITIES}


def _unique(values: list[str] | tuple[str, ...]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(values))


def _sanitize(value: str) -> tuple[str, bool]:
    redacted = False
    cleaned, count = _EMAIL_RE.subn("[REDACTED_EMAIL]", value)
    redacted = redacted or count > 0
    cleaned, count = _PHONE_RE.subn("[REDACTED_PHONE]", cleaned)
    return cleaned.strip(), redacted or count > 0


def capability_map() -> tuple[dict[str, Any], ...]:
    """Return the product capability registry without runtime side effects."""
    return tuple(
        {
            "domain": c.domain,
            "name_ar": c.name_ar,
            "name_en": c.name_en,
            "os_type": c.os_type,
            "owner_role": c.owner_role,
            "service_ids": c.service_ids,
            "agents": c.agents,
            "integrations": c.integrations,
            "artifacts": c.artifacts,
            "proof_metrics": c.proof_metrics,
        }
        for c in _CAPABILITIES
    )


def _execution_plan(action_mode: str) -> tuple[dict[str, str], ...]:
    approval_ar = "اطلب قرار المالك قبل أي أثر خارجي أو قرار غير قابل للعكس"
    approval_en = "Request owner approval before any external or irreversible action"
    if action_mode == "blocked":
        approval_ar = "أوقف المسار المخالف، واجمع موافقة صحيحة أو استخدم قناة يدوية مسموحة"
        approval_en = (
            "Stop the disallowed path; obtain valid consent or use an allowed manual channel"
        )
    return (
        {
            "stage": "diagnose",
            "instruction_ar": "اجمع الأدلة وخط الأساس وحدد السبب الجذري",
            "instruction_en": "Collect evidence and baseline; identify the root cause",
        },
        {
            "stage": "design",
            "instruction_ar": "صمم الحل وسير العمل وعقد النتيجة",
            "instruction_en": "Design the solution, workflow, and outcome contract",
        },
        {
            "stage": "draft_or_internal_execute",
            "instruction_ar": "أنشئ المخرجات ونفّذ فقط التغييرات الداخلية القابلة للعكس",
            "instruction_en": "Create artifacts and execute only reversible internal changes",
        },
        {
            "stage": "approval",
            "instruction_ar": approval_ar,
            "instruction_en": approval_en,
        },
        {
            "stage": "connector_handoff",
            "instruction_ar": "مرر العمل للموصل المصرح به مع سجل تدقيق",
            "instruction_en": "Hand off through an authorized connector with an audit record",
        },
        {
            "stage": "measure",
            "instruction_ar": "قارن النتيجة بخط الأساس وسجل دليلًا حقيقيًا",
            "instruction_en": "Compare outcome with baseline and record real evidence",
        },
        {
            "stage": "learn",
            "instruction_ar": "صنف الفشل وحدّث الذاكرة واقترح التجربة التالية",
            "instruction_en": "Classify failures, update memory, and propose the next experiment",
        },
    )


def route_company_workload(request: CompanyWorkloadRequest) -> WorkloadRoute:
    """Classify one company burden and produce a governed execution route."""
    if not request.tenant_id.strip():
        raise ValueError("tenant_id is required")
    if not request.title.strip():
        raise ValueError("title is required")

    title, title_redacted = _sanitize(request.title)
    description, description_redacted = _sanitize(request.description)
    objective, objective_redacted = _sanitize(request.objective)
    haystack = f"{title} {description} {objective}".casefold()

    scores = []
    for capability in _CAPABILITIES:
        score = sum(1 for keyword in capability.keywords if keyword.casefold() in haystack)
        scores.append((score, capability.domain))
    scores.sort(key=lambda pair: (-pair[0], pair[1]))
    matched = [domain for score, domain in scores if score > 0]
    if not matched:
        matched = ["operations"]
    primary = matched[0]
    supporting = tuple(matched[1:4])
    selected = [_CAPABILITY_BY_DOMAIN[domain] for domain in (primary, *supporting)]

    risk_flags: list[str] = []
    if request.sensitivity in ("confidential", "restricted"):
        risk_flags.append(f"sensitivity:{request.sensitivity}")
    if any(term.casefold() in haystack for term in _HIGH_RISK_TERMS):
        risk_flags.append("high_impact_decision")
    if title_redacted or description_redacted or objective_redacted:
        risk_flags.append("possible_pii_redacted")

    channel = (request.requested_channel or "").strip().casefold()
    action_mode = "draft_only"
    queue_status = "triaged"
    autonomy_level: Literal[
        "L2_DRAFT", "L3_INTERNAL_EXECUTE", "L5_BLOCKED"
    ] = "L3_INTERNAL_EXECUTE"
    if channel in ("linkedin", "linkedin_automation") and request.external_action_requested:
        risk_flags.append("linkedin_automation_disallowed")
        action_mode, queue_status, autonomy_level = "blocked", "blocked", "L5_BLOCKED"
    elif (
        channel in ("whatsapp", "whatsapp_business")
        and request.external_action_requested
        and request.recipient_opted_in is not True
    ):
        risk_flags.append("whatsapp_opt_in_not_proven")
        action_mode, queue_status, autonomy_level = "blocked", "blocked", "L5_BLOCKED"
    elif request.external_action_requested or risk_flags:
        action_mode, queue_status, autonomy_level = (
            "approval_required", "needs_approval", "L2_DRAFT"
        )

    if request.urgency == "critical" and action_mode != "blocked":
        risk_flags.append("critical_urgency")
        action_mode, queue_status, autonomy_level = (
            "approval_required", "escalated", "L2_DRAFT"
        )

    if action_mode == "blocked" or request.urgency == "critical":
        risk_level = "critical"
    elif "high_impact_decision" in risk_flags or request.sensitivity == "restricted":
        risk_level = "high"
    elif request.external_action_requested or risk_flags:
        risk_level = "medium"
    else:
        risk_level = "low"

    human_decision = None
    if action_mode in ("approval_required", "blocked"):
        human_decision = {
            "required": True,
            "owner_role": selected[0].owner_role,
            "question_ar": "هل تعتمد المسار المقترح بعد مراجعة الأدلة والمخاطر؟",
            "question_en": "Do you approve the proposed route after reviewing evidence and risks?",
            "options": ("approve_once", "request_changes", "reject"),
            "reason": risk_flags or ["external_action_requested"],
        }

    missing_inputs: list[str] = []
    if not request.customer_id:
        missing_inputs.append("customer_id")
    if not request.evidence_ids:
        missing_inputs.append("baseline_evidence")
    if request.external_action_requested and not channel:
        missing_inputs.append("requested_channel")
    if channel in ("whatsapp", "whatsapp_business") and request.recipient_opted_in is not True:
        missing_inputs.append("whatsapp_opt_in_evidence")

    digest = hashlib.sha256(
        f"{request.tenant_id}|{request.customer_id or ''}|{primary}|{title}".encode()
    ).hexdigest()[:16]
    route_id = f"wi_{digest}"
    return WorkloadRoute(
        schema_version=1,
        route_id=route_id,
        tenant_id=request.tenant_id,
        customer_id=request.customer_id,
        urgency=request.urgency,
        evidence_ids=tuple(request.evidence_ids),
        sanitized_title=title,
        sanitized_description=description,
        pii_redacted=title_redacted or description_redacted or objective_redacted,
        primary_domain=primary,
        supporting_domains=supporting,
        matched_capabilities=tuple(
            {
                "domain": c.domain,
                "name_ar": c.name_ar,
                "name_en": c.name_en,
                "os_type": c.os_type,
            }
            for c in selected
        ),
        recommended_service_ids=_unique(
            [service_id for c in selected for service_id in c.service_ids]
        ),
        assigned_agents=_unique([agent for c in selected for agent in c.agents]),
        required_integrations=_unique(
            [integration for c in selected for integration in c.integrations]
        ),
        execution_plan=_execution_plan(action_mode),
        artifacts=_unique([artifact for c in selected for artifact in c.artifacts]),
        proof_contract=_unique([metric for c in selected for metric in c.proof_metrics]),
        risk_level=risk_level,
        risk_flags=tuple(risk_flags),
        autonomy_level=autonomy_level,
        action_mode=action_mode,
        queue_status=queue_status,
        owner_role=selected[0].owner_role,
        human_decision=human_decision,
        missing_inputs=tuple(missing_inputs),
    )
