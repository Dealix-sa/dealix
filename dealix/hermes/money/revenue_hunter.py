"""Revenue Hunter — turn signals into ranked, monetisable opportunities.

The Hunter does NOT send anything. It produces ranked leads, scored
opportunities, and drafted outreach. Anything that touches the outside
world is queued for founder approval through the orchestrator.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from dealix.hermes.core.schemas import (
    MoneyAction,
    MoneyActionSource,
    Opportunity,
    Signal,
    SignalSource,
)
from dealix.hermes.core.scoring import money_priority_score, rank_money_actions
from dealix.hermes.money.opportunity_cash_score import hydrate
from dealix.hermes.sovereignty import SovereigntyLevel
from dealix.hermes.trust.guardrails import TrustContext, trust_check


@dataclass
class HunterRequest:
    sector: str
    region: str = "SA"
    icp: str | None = None
    offer: str = "Revenue Hunter Pilot"
    price_sar: float = 999.0
    message_style: str = "direct"
    leads: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class RankedLead:
    company_name: str
    fit_score: int
    pain_hypothesis: str
    recommended_message: str
    expected_value_sar: float
    next_action: str
    sovereignty_level: SovereigntyLevel
    blocked_reason: str | None = None


@dataclass
class HunterResult:
    sector: str
    offer: str
    ranked_leads: list[RankedLead]
    opportunities: list[Opportunity]
    money_actions: list[MoneyAction]

    def to_dict(self) -> dict[str, Any]:
        return {
            "sector": self.sector,
            "offer": self.offer,
            "ranked_leads": [
                {
                    "company_name": lead.company_name,
                    "fit_score": lead.fit_score,
                    "pain_hypothesis": lead.pain_hypothesis,
                    "recommended_message": lead.recommended_message,
                    "expected_value_sar": lead.expected_value_sar,
                    "next_action": lead.next_action,
                    "sovereignty_level": lead.sovereignty_level.name,
                    "blocked_reason": lead.blocked_reason,
                }
                for lead in self.ranked_leads
            ],
            "opportunities": [o.model_dump(mode="json") for o in self.opportunities],
            "money_actions": [a.model_dump(mode="json") for a in self.money_actions],
        }


def _fit_score(lead: dict[str, Any], icp: str | None) -> int:
    score = 50
    if lead.get("has_b2b_clients"):
        score += 15
    if lead.get("active_marketing"):
        score += 10
    if lead.get("recent_funding"):
        score += 10
    if icp and lead.get("icp_tag") == icp:
        score += 15
    if lead.get("blocked"):
        score = max(0, score - 40)
    return max(0, min(100, score))


def _pain_hypothesis(lead: dict[str, Any], sector: str) -> str:
    if lead.get("known_pain"):
        return str(lead["known_pain"])
    if sector == "agencies":
        return "Has B2B clients but no AI-powered revenue service."
    if sector == "consultants":
        return "Manual proposal work eats billable hours."
    return f"Typical {sector} revenue leak around lead → proposal → follow-up."


def _draft_message(lead: dict[str, Any], offer: str, style: str) -> str:
    name = lead.get("company_name", "there")
    if style == "warm":
        return (
            f"Hi {name} team, we've been helping firms like yours productise "
            f"revenue with {offer}. Worth 15 minutes to compare notes this week?"
        )
    return (
        f"{name} — quick one. We package {offer} for firms in your space, "
        "outcome-priced, no long contract. Open to a 15-minute call?"
    )


def run_hunter(req: HunterRequest) -> HunterResult:
    """Score, draft, and rank leads. Pure function — safe to test."""
    ranked: list[RankedLead] = []
    opps: list[Opportunity] = []
    actions: list[MoneyAction] = []

    for lead in req.leads:
        fit = _fit_score(lead, req.icp)
        pain = _pain_hypothesis(lead, req.sector)
        message = _draft_message(lead, req.offer, req.message_style)

        signal = Signal(
            source=SignalSource.OUTBOUND_RESEARCH,
            sector=req.sector,
            region=req.region,
            payload=lead,
        )
        opp = Opportunity(
            signal_id=signal.id,
            title=f"{req.offer} → {lead.get('company_name', 'lead')}",
            sector=req.sector,
            buyer_persona=lead.get("buyer_persona"),
            pain_hypothesis=pain,
            recommended_offer=req.offer,
            estimated_value_sar=req.price_sar,
            sovereignty_level=SovereigntyLevel.L2_INTERNAL_TASK,
        )
        opp = hydrate(opp, signal)
        opps.append(opp)

        # Guardrail: any draft message that overclaims is blocked before
        # ever being surfaced to the founder.
        check = trust_check(
            TrustContext(
                target_id=opp.id,
                target_kind="message",
                text=message,
                payload={"price_sar": req.price_sar},
            )
        )

        blocked_reason: str | None = None
        next_action = "manual outreach"
        if check.outcome.value == "deny":
            blocked_reason = "; ".join(check.violations)
            next_action = "rewrite message — guardrail violation"
        elif check.outcome.value == "escalate":
            next_action = "founder approval before send"

        action = MoneyAction(
            title=f"Outreach: {lead.get('company_name', 'lead')}",
            source=MoneyActionSource.DIRECT_CLIENT,
            estimated_value_sar=req.price_sar,
            cash_speed_score=opp.cash_speed_score,
            close_probability=opp.close_probability,
            strategic_value_score=opp.strategic_value_score,
            risk_score=opp.risk_score,
            next_action=next_action,
            sovereignty_level=SovereigntyLevel.L2_INTERNAL_TASK,
            opportunity_id=opp.id,
        )
        action.money_priority_score = money_priority_score(action)
        actions.append(action)

        ranked.append(
            RankedLead(
                company_name=lead.get("company_name", "unknown"),
                fit_score=fit,
                pain_hypothesis=pain,
                recommended_message=message,
                expected_value_sar=req.price_sar,
                next_action=next_action,
                sovereignty_level=SovereigntyLevel.L2_INTERNAL_TASK,
                blocked_reason=blocked_reason,
            )
        )

    ranked.sort(key=lambda lead: lead.fit_score, reverse=True)
    actions = rank_money_actions(actions)

    return HunterResult(
        sector=req.sector,
        offer=req.offer,
        ranked_leads=ranked,
        opportunities=opps,
        money_actions=actions,
    )
