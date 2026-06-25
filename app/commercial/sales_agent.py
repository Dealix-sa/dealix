"""Review-first Sales Agent and Company Brain pack builder.

This module is deterministic and does not call external services. It prepares
sales, discovery, negotiation, and decision material for founder review.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass(frozen=True)
class SectorPlaybook:
    sector: str
    buyer_persona: str
    pain_hypotheses: tuple[str, ...]
    recommended_offer: str
    discovery_questions: tuple[str, ...]
    negotiation_notes: tuple[str, ...]


@dataclass(frozen=True)
class SalesAgentPack:
    company_name: str
    sector: str
    city: str
    source_url: str
    buyer_persona: str
    pain_hypothesis: str
    recommended_offer: str
    draft_message_ar: str
    discovery_questions: tuple[str, ...]
    negotiation_notes: tuple[str, ...]
    company_brain_decision: str
    next_action: str
    owner_decision_required: bool = True
    communication_mode: str = "draft_only"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


PLAYBOOKS: dict[str, SectorPlaybook] = {
    "clinics": SectorPlaybook(
        sector="clinics",
        buyer_persona="owner or operations manager",
        pain_hypotheses=(
            "patient inquiries and follow-ups may be scattered across WhatsApp and calls",
            "booking follow-up may not have a daily owner or visible queue",
        ),
        recommended_offer="Follow-up Recovery OS",
        discovery_questions=(
            "How do you track inquiries that do not book immediately?",
            "Who owns follow-up after the first patient conversation?",
            "What does the owner see every morning about missed follow-ups?",
        ),
        negotiation_notes=(
            "Start with one branch or one service line.",
            "Offer a 7-day follow-up recovery sprint before larger automation.",
            "Do not promise more bookings; promise visible follow-up discipline and proof.",
        ),
    ),
    "real_estate": SectorPlaybook(
        sector="real_estate",
        buyer_persona="sales manager or owner",
        pain_hypotheses=(
            "leads may enter from several channels without one follow-up rhythm",
            "offers and viewings may not have clear next actions",
        ),
        recommended_offer="Revenue Command Room OS",
        discovery_questions=(
            "How many new leads arrive weekly and from which channels?",
            "How do you know which leads need action today?",
            "What happens after a proposal or viewing is shared?",
        ),
        negotiation_notes=(
            "Begin with one pipeline and one city or project.",
            "Sell the sprint as visibility, ownership, and follow-up discipline.",
            "Avoid guaranteed sales language; focus on measurable operating control.",
        ),
    ),
    "logistics": SectorPlaybook(
        sector="logistics",
        buyer_persona="commercial director or general manager",
        pain_hypotheses=(
            "B2B proposals may stay open without clear status or owner",
            "account opportunities may need a weekly command room",
        ),
        recommended_offer="Revenue Command Room OS",
        discovery_questions=(
            "How do you track active B2B proposals?",
            "Who owns follow-up for each account?",
            "What report shows the top opportunities this week?",
        ),
        negotiation_notes=(
            "Start with proposal tracking and weekly commercial command room.",
            "Attach the offer to account visibility, not generic automation.",
            "Keep scope narrow before adding integrations.",
        ),
    ),
    "training_centers": SectorPlaybook(
        sector="training_centers",
        buyer_persona="center manager or admissions lead",
        pain_hypotheses=(
            "registrations may need structured follow-up before cohort start",
            "inquiries may stall because pricing and schedules are not followed up",
        ),
        recommended_offer="Follow-up Recovery OS",
        discovery_questions=(
            "How do you follow up with inquiries before a course starts?",
            "Which step loses the most potential learners?",
            "How does management see registrations by cohort?",
        ),
        negotiation_notes=(
            "Start with one course category or cohort.",
            "Measure inquiries classified, follow-ups prepared, and registration status visibility.",
            "Offer monthly operating support after proof.",
        ),
    ),
    "b2b_services": SectorPlaybook(
        sector="b2b_services",
        buyer_persona="founder or sales lead",
        pain_hypotheses=(
            "pipeline may depend on memory instead of a daily operating queue",
            "proposals may lack a consistent proof and follow-up process",
        ),
        recommended_offer="Revenue Command Room OS",
        discovery_questions=(
            "How do you decide the top commercial actions every morning?",
            "Where do proposal follow-ups live today?",
            "What proof pack do you show after delivery?",
        ),
        negotiation_notes=(
            "Start with founder-led revenue command room.",
            "Offer a paid diagnostic if the client is unsure.",
            "Do not discount without reducing deliverables.",
        ),
    ),
}

DEFAULT_PLAYBOOK = PLAYBOOKS["b2b_services"]


def get_playbook(sector: str) -> SectorPlaybook:
    return PLAYBOOKS.get(sector.strip().lower(), DEFAULT_PLAYBOOK)


def build_sales_agent_pack(
    *,
    company_name: str,
    sector: str,
    city: str = "Riyadh",
    source_url: str = "manual_review_required",
) -> SalesAgentPack:
    if not company_name.strip():
        raise ValueError("company_name is required")

    playbook = get_playbook(sector)
    pain = playbook.pain_hypotheses[0]
    draft = (
        f"السلام عليكم، لاحظنا أن شركات كثيرة في قطاع {playbook.sector} تواجه تحديًا في "
        f"تحويل المتابعات والعروض إلى إجراءات يومية واضحة.\n\n"
        f"قد لا ينطبق هذا عليكم بالكامل، لكن الفرضية الأولية هي: {pain}.\n\n"
        f"في Dealix نبدأ عادةً بـ {playbook.recommended_offer} كنطاق صغير يوضح أين تتعطل المتابعة "
        f"وما القرار التجاري المطلوب اليوم، بدون تغيير أنظمتكم الحالية.\n\n"
        "إذا مناسب، نرتب مراجعة قصيرة لفهم الوضع ونحدد هل التشخيص يستحق البدء أم لا."
    )

    decision = (
        f"Review {company_name} as a {playbook.sector} target in {city}. "
        f"Validate the source, confirm the pain hypothesis, then decide whether to prepare a scoped diagnostic."
    )

    return SalesAgentPack(
        company_name=company_name.strip(),
        sector=playbook.sector,
        city=city.strip() or "Riyadh",
        source_url=source_url.strip() or "manual_review_required",
        buyer_persona=playbook.buyer_persona,
        pain_hypothesis=pain,
        recommended_offer=playbook.recommended_offer,
        draft_message_ar=draft,
        discovery_questions=playbook.discovery_questions,
        negotiation_notes=playbook.negotiation_notes,
        company_brain_decision=decision,
        next_action="founder_review",
    )
