"""WhatsApp Client OS — flow map.

WhatsApp is a controlled set of business flows, not open chat. Each flow has
a trigger, allowed inputs, an exit condition, a human-handoff condition, and a
next flow. ``flows.py`` is the single source of truth; the YAML view in the
docs is generated from :func:`flows_as_data`.
"""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.whatsapp_client_os.schemas import FlowId, Intent


@dataclass(frozen=True, slots=True)
class Flow:
    id: str
    title_ar: str
    title_en: str
    trigger_intent: str
    allowed_inputs: tuple[str, ...]
    exit_condition: str
    handoff_condition: str
    next_flow: str  # FlowId value or "" for terminal


_FLOWS: tuple[Flow, ...] = (
    Flow(
        FlowId.NEW_CLIENT_WELCOME.value,
        "ترحيب عميل جديد",
        "New Client Welcome",
        Intent.WELCOME.value,
        ("menu_number", "free_text"),
        "menu_choice_made",
        "explicit_human_request",
        FlowId.READINESS_SCAN.value,
    ),
    Flow(
        FlowId.READINESS_SCAN.value,
        "فحص الجاهزية",
        "Readiness Scan",
        Intent.START_SCAN.value,
        ("option_choice",),
        "all_axes_answered",
        "sensitive_data_or_low_confidence",
        FlowId.SERVICE_RECOMMENDATION.value,
    ),
    Flow(
        FlowId.SERVICE_RECOMMENDATION.value,
        "توصية الخدمة",
        "Service Recommendation",
        Intent.RECOMMEND_ME.value,
        ("option_choice",),
        "recommendation_shown",
        "pricing_commitment",
        FlowId.PROPOSAL_REVIEW.value,
    ),
    Flow(
        FlowId.PERMISSION_COLLECTION.value,
        "جمع الصلاحيات",
        "Permission Collection",
        Intent.GIVE_PERMISSION.value,
        ("option_choice",),
        "portal_link_issued",
        "secret_in_text",
        FlowId.ONBOARDING.value,
    ),
    Flow(
        FlowId.DRAFT_REVIEW.value,
        "مراجعة المسودات",
        "Draft Review",
        Intent.REVIEW_DRAFT.value,
        ("approve", "edit", "reject"),
        "draft_approved_or_rejected",
        "dissatisfied",
        "",
    ),
    Flow(
        FlowId.PROPOSAL_REVIEW.value,
        "مراجعة العرض",
        "Proposal Review",
        Intent.REVIEW_PROPOSAL.value,
        ("option_choice",),
        "proposal_decision_made",
        "pricing_commitment",
        FlowId.PAYMENT_HANDOFF.value,
    ),
    Flow(
        FlowId.PROOF_PACK_DELIVERY.value,
        "تسليم حزمة الإثبات",
        "Proof Pack Delivery",
        Intent.PROOF_PACK.value,
        ("option_choice",),
        "proof_pack_opened",
        "dissatisfied",
        FlowId.RENEWAL_UPSELL.value,
    ),
    Flow(
        FlowId.PAYMENT_HANDOFF.value,
        "تحويل الدفع",
        "Payment Handoff",
        Intent.START_PAYMENT.value,
        ("option_choice",),
        "secure_link_issued",
        "billing_question",
        FlowId.ONBOARDING.value,
    ),
    Flow(
        FlowId.ONBOARDING.value,
        "بدء التشغيل",
        "Onboarding",
        Intent.GIVE_PERMISSION.value,
        ("option_choice",),
        "onboarding_checklist_started",
        "low_confidence",
        FlowId.WEEKLY_REPORT.value,
    ),
    Flow(
        FlowId.WEEKLY_REPORT.value,
        "التقرير الأسبوعي",
        "Weekly Report",
        Intent.UNKNOWN.value,
        ("option_choice",),
        "report_delivered",
        "dissatisfied",
        FlowId.RENEWAL_UPSELL.value,
    ),
    Flow(
        FlowId.SUPPORT_HANDOFF.value,
        "الدعم والتصعيد",
        "Support / Human Handoff",
        Intent.REQUEST_SUPPORT.value,
        ("option_choice", "free_text"),
        "ticket_categorized",
        "billing_or_urgent_complaint",
        "",
    ),
    Flow(
        FlowId.RENEWAL_UPSELL.value,
        "التجديد والترقية",
        "Renewal / Upsell",
        Intent.RENEWAL.value,
        ("option_choice",),
        "renewal_decision_made",
        "pricing_commitment",
        "",
    ),
)

FLOWS: dict[str, Flow] = {f.id: f for f in _FLOWS}

_INTENT_TO_FLOW: dict[str, str] = {
    Intent.WELCOME.value: FlowId.NEW_CLIENT_WELCOME.value,
    Intent.START_SCAN.value: FlowId.READINESS_SCAN.value,
    Intent.RECOMMEND_ME.value: FlowId.SERVICE_RECOMMENDATION.value,
    Intent.VIEW_SERVICES.value: FlowId.SERVICE_RECOMMENDATION.value,
    Intent.BUILD_FOLLOWUP.value: FlowId.DRAFT_REVIEW.value,
    Intent.REVIEW_DRAFT.value: FlowId.DRAFT_REVIEW.value,
    Intent.REVIEW_PROPOSAL.value: FlowId.PROPOSAL_REVIEW.value,
    Intent.PROOF_PACK.value: FlowId.PROOF_PACK_DELIVERY.value,
    Intent.GIVE_PERMISSION.value: FlowId.PERMISSION_COLLECTION.value,
    Intent.START_PAYMENT.value: FlowId.PAYMENT_HANDOFF.value,
    Intent.RENEWAL.value: FlowId.RENEWAL_UPSELL.value,
    Intent.REQUEST_SUPPORT.value: FlowId.SUPPORT_HANDOFF.value,
    Intent.REQUEST_HUMAN.value: FlowId.SUPPORT_HANDOFF.value,
}


def flow_for_intent(intent: Intent | str) -> str:
    value = intent.value if isinstance(intent, Intent) else str(intent)
    return _INTENT_TO_FLOW.get(value, FlowId.NEW_CLIENT_WELCOME.value)


def next_flow(flow: FlowId | str) -> str:
    value = flow.value if isinstance(flow, FlowId) else str(flow)
    f = FLOWS.get(value)
    return f.next_flow if f else ""


def flows_as_data() -> list[dict[str, object]]:
    """Serializable view of the flow map (used to render the docs YAML)."""
    return [
        {
            "id": f.id,
            "title_ar": f.title_ar,
            "title_en": f.title_en,
            "trigger_intent": f.trigger_intent,
            "allowed_inputs": list(f.allowed_inputs),
            "exit_condition": f.exit_condition,
            "handoff_condition": f.handoff_condition,
            "next_flow": f.next_flow,
        }
        for f in _FLOWS
    ]


__all__ = ["FLOWS", "Flow", "flow_for_intent", "flows_as_data", "next_flow"]
