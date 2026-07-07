"""Generate OutreachDraft records from scored companies. Never sends.

Drafts are always created ``pending`` and carry risk notes. A draft is only
generated for companies that are a plausible fit (``score_class`` != not_fit)
unless ``force`` is set.
"""

from __future__ import annotations

from dealix.opportunity_graph.drafting.message_templates import (
    SEGMENT_DEFAULTS,
    render_message,
)
from dealix.opportunity_graph.schemas import Channel, Language, OpportunityCompany, OutreachDraft
from dealix.opportunity_graph.store import uid

# Phrases we refuse to emit — belt-and-braces guard against fake/pushy claims.
_FORBIDDEN = (
    "guaranteed",
    "مضمون",
    "as we discussed",
    "as agreed",
    "per our last call",
    "risk-free",
)


def _risk_notes(company: OpportunityCompany) -> str:
    notes: list[str] = []
    if not company.consent_to_contact:
        notes.append("No stored consent — founder confirms channel appropriateness before send.")
    if company.trust_risk_score >= 6:
        notes.append("Elevated trust-risk score — review sector sensitivity before outreach.")
    if company.company_type == "government_related":
        notes.append("Government-related — use formal, compliant channel only.")
    return " ".join(notes)


def _safety_check(text: str) -> None:
    lowered = text.lower()
    for phrase in _FORBIDDEN:
        if phrase in lowered:
            raise ValueError(f"Draft contains forbidden phrase: {phrase!r}")


def generate_draft_for_company(
    company: OpportunityCompany,
    *,
    channel: Channel | None = None,
    language: Language | None = None,
    force: bool = False,
) -> OutreachDraft | None:
    if company.score_class == "not_fit" and not force:
        return None

    default_channel, default_language = SEGMENT_DEFAULTS.get(
        company.segment, ("linkedin", "ar")
    )
    channel = channel or default_channel
    language = language or default_language

    text = render_message(
        segment=company.segment,
        language=language,
        channel=channel,
        company=company.name,
        persona=company.buyer_persona,
        signal=company.saudi_signal or company.signal_type,
        pain=company.pain_hypothesis,
    )
    _safety_check(text)

    return OutreachDraft(
        id=uid("draft"),
        company_id=company.id,
        persona=company.buyer_persona,
        channel=channel,
        language=language,
        draft_text=text,
        personalization_notes=(
            f"segment={company.segment}; score={company.total_score} "
            f"({company.score_class}); signal={company.saudi_signal or company.signal_type}"
        ),
        risk_notes=_risk_notes(company),
        approval_status="pending",
    )
