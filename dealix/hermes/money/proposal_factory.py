"""Proposal Factory — turn an opportunity into a structured proposal.

The factory renders a proposal from a small set of named templates.
Every draft is passed through `trust_check` and tagged with a
sovereignty level. We never auto-send; the orchestrator queues it for
founder approval.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from dealix.hermes.core.schemas import (
    Decision,
    DecisionVerdict,
    Opportunity,
    TrustCheckOutcome,
    TrustCheckResult,
)
from dealix.hermes.sovereignty import SovereigntyLevel
from dealix.hermes.trust.guardrails import TrustContext, trust_check

# Canonical templates. Keep prose short — the factory composes them
# with opportunity data at render time. New templates go here.
TEMPLATES: dict[str, dict[str, Any]] = {
    "revenue_hunter_pilot": {
        "title": "Revenue Hunter Pilot",
        "default_price_sar": 999.0,
        "duration_days": 7,
        "deliverables": [
            "Ranked target list (≥20 accounts)",
            "Pain hypothesis per account",
            "Drafted outreach for top 10",
            "Founder-reviewed follow-up plan",
        ],
        "exclusions": ["No external sending without founder approval"],
        "assumptions": ["Client provides target sector and ICP"],
        "risks": ["Outreach reply rate depends on client brand"],
    },
    "ai_trust_kit": {
        "title": "AI Trust Kit",
        "default_price_sar": 2499.0,
        "duration_days": 14,
        "deliverables": [
            "AI usage policy aligned to ISO/IEC 42001",
            "Governance map (NIST AI RMF: Govern/Map/Measure/Manage)",
            "Tool allowlist + manifest pinning",
            "Audit-ready evidence pack",
        ],
        "exclusions": ["Not a legal opinion"],
        "assumptions": ["Client provides current AI tool inventory"],
        "risks": ["External certification is out of scope"],
    },
    "agency_white_label_kit": {
        "title": "Agency White-label Kit",
        "default_price_sar": 4999.0,
        "duration_days": 21,
        "deliverables": [
            "Branded Revenue Hunter workflow",
            "Founder-co-signed proposal templates",
            "Partner pricing card",
            "Monthly outcome ledger",
        ],
        "exclusions": ["Agency owns client relationship"],
        "assumptions": ["Agency signs partner code of conduct"],
        "risks": ["Brand drift if guardrails are bypassed"],
    },
    "founder_os_setup": {
        "title": "Founder OS Setup",
        "default_price_sar": 1499.0,
        "duration_days": 5,
        "deliverables": [
            "Sovereign Console install",
            "Money + Trust + Outcome engines wired",
            "Weekly review checklist",
        ],
        "exclusions": [],
        "assumptions": ["Founder is the single point of decision"],
        "risks": ["Console value depends on founder review cadence"],
    },
    "market_radar_report": {
        "title": "Market Radar Report",
        "default_price_sar": 1500.0,
        "duration_days": 7,
        "deliverables": [
            "Top 20 accounts for a chosen sector",
            "Pain map + offer fit",
            "12 outreach drafts ready for founder approval",
        ],
        "exclusions": [],
        "assumptions": ["Sector + region supplied"],
        "risks": ["Public data quality varies"],
    },
}


@dataclass
class ProposalRequest:
    template: str
    opportunity: Opportunity
    client_name: str
    contact: str | None = None
    custom_price_sar: float | None = None
    custom_scope: list[str] = field(default_factory=list)
    notes: str | None = None


@dataclass
class Proposal:
    id: str
    template: str
    title: str
    client_name: str
    price_sar: float
    duration_days: int
    sections: dict[str, Any]
    sovereignty_level: SovereigntyLevel
    trust_check: TrustCheckResult
    decision: Decision

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "template": self.template,
            "title": self.title,
            "client_name": self.client_name,
            "price_sar": self.price_sar,
            "duration_days": self.duration_days,
            "sections": self.sections,
            "sovereignty_level": self.sovereignty_level.name,
            "trust_check": self.trust_check.model_dump(mode="json"),
            "decision": self.decision.model_dump(mode="json"),
        }


def list_templates() -> list[dict[str, Any]]:
    return [{"key": k, **v} for k, v in TEMPLATES.items()]


def render_proposal(req: ProposalRequest) -> Proposal:
    """Render a proposal draft for founder review.

    Always returns a Proposal — including when the trust check denies it,
    so the founder can read the violations and edit before retrying.
    """
    if req.template not in TEMPLATES:
        raise KeyError(f"unknown proposal template: {req.template}")

    t = TEMPLATES[req.template]
    price = req.custom_price_sar or t["default_price_sar"]
    scope = req.custom_scope or t["deliverables"]

    sections = {
        "context": (
            f"Prepared for {req.client_name} on behalf of "
            f"{req.opportunity.sector or 'their team'}."
        ),
        "problem": req.opportunity.pain_hypothesis
        or "Revenue leak between lead → proposal → follow-up.",
        "desired_outcome": (
            "A short, founder-reviewed sprint that converts the opportunity "
            "into measurable next steps without committing to long contracts."
        ),
        "scope": scope,
        "deliverables": t["deliverables"],
        "timeline_days": t["duration_days"],
        "price_sar": price,
        "assumptions": t["assumptions"],
        "exclusions": t["exclusions"],
        "risks": t["risks"],
        "next_step": "Founder confirms scope, then we send a signed PDF.",
        "notes": req.notes,
    }

    check = trust_check(
        TrustContext(
            target_id=req.opportunity.id,
            target_kind="proposal",
            payload={"price_sar": price, **dict(sections)},
            action="send_external_proposal",
        )
    )

    verdict = (
        DecisionVerdict.ESCALATE
        if check.outcome != TrustCheckOutcome.DENY
        else DecisionVerdict.DEFER
    )
    decision = Decision(
        opportunity_id=req.opportunity.id,
        verdict=verdict,
        rationale=(
            "External proposal — sovereign approval required before send."
            if verdict == DecisionVerdict.ESCALATE
            else f"Blocked by trust check: {', '.join(check.violations)}"
        ),
        next_action="founder review",
        sovereignty_level=SovereigntyLevel.L4_EXTERNAL_APPROVAL,
        requires_approval=True,
        approval_status="pending"
        if verdict == DecisionVerdict.ESCALATE
        else "n/a",
    )

    return Proposal(
        id=f"prop_{req.opportunity.id[-8:]}_{req.template}",
        template=req.template,
        title=t["title"],
        client_name=req.client_name,
        price_sar=price,
        duration_days=t["duration_days"],
        sections=sections,
        sovereignty_level=SovereigntyLevel.L4_EXTERNAL_APPROVAL,
        trust_check=check,
        decision=decision,
    )
