"""Draft-first marketing agents.

Every agent's ``propose`` method takes a plain ``dict`` payload and returns a
draft object suitable for the approval flow. No external IO is performed; the
agents are rule-based and deterministic so they can run in CI without secrets.
A future PR will route prose generation through ``llm_gateway`` but the public
contract is already draft-first to keep the approval surface stable.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from dealix.revenue_marketing.schemas import (
    Audience,
    CaseStudyDraft,
    Lead,
    MarketingCampaign,
    MarketingTouch,
    MarketSignal,
    MessageVariant,
    Offer,
    compute_lead_score,
)
from dealix.revenue_marketing.store import (
    RevenueMarketingStore,
    get_revenue_marketing_store,
    uid,
)
from dealix.revenue_ops_autopilot.schemas import EvidenceEvent
from dealix.revenue_ops_autopilot.store import (
    get_autopilot_store,
)
from dealix.revenue_ops_autopilot.store import (
    uid as ev_uid,
)


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


class _BaseAgent:
    """Common base for draft-first marketing agents."""

    name: str = "base"

    def __init__(self, store: RevenueMarketingStore | None = None) -> None:
        self._store = store

    @property
    def store(self) -> RevenueMarketingStore:
        return self._store or get_revenue_marketing_store()

    def propose(self, payload: dict[str, Any]) -> dict[str, Any]:  # pragma: no cover
        raise NotImplementedError


class MarketRadarAgent(_BaseAgent):
    """Turns a payload of observed source items into draft MarketSignals."""

    name = "market_radar"

    def propose(self, payload: dict[str, Any]) -> dict[str, Any]:
        # TODO: route through llm_gateway for natural-language pain hypotheses.
        items = payload.get("items") or []
        drafts: list[dict[str, Any]] = []
        for item in items:
            signal = MarketSignal(
                id=uid("sig"),
                source=str(item.get("source") or "unknown"),
                segment=str(item.get("segment") or payload.get("segment") or "general"),
                pain_hypothesis=str(item.get("pain_hypothesis") or item.get("text") or ""),
                confidence=float(item.get("confidence") or 0.5),
                payload=dict(item),
            )
            drafts.append(signal.model_dump(mode="json"))
        return {
            "agent": self.name,
            "draft_kind": "market_signal",
            "drafts": drafts,
            "requires_approval": True,
            "external_send_blocked": True,
            "generated_at": _now_iso(),
        }


class AudienceResearchAgent(_BaseAgent):
    """Aggregates signals into a draft Audience definition."""

    name = "audience_research"

    def propose(self, payload: dict[str, Any]) -> dict[str, Any]:
        # TODO: route through llm_gateway for richer fit_criteria reasoning.
        name = str(payload.get("name") or "Untitled Audience")
        segment_tag = str(payload.get("segment_tag") or "unsegmented")
        fit_criteria = list(payload.get("fit_criteria") or [])
        pain_points = list(payload.get("pain_points") or [])
        size_estimate = payload.get("size_estimate")
        audience = Audience(
            id=uid("aud"),
            name=name,
            segment_tag=segment_tag,
            fit_criteria=fit_criteria,
            size_estimate=int(size_estimate) if size_estimate is not None else None,
            pain_points=pain_points,
        )
        return {
            "agent": self.name,
            "draft_kind": "audience",
            "draft": audience.model_dump(mode="json"),
            "requires_approval": True,
            "external_send_blocked": True,
            "generated_at": _now_iso(),
        }


class ICPBuilderAgent(_BaseAgent):
    """Builds a draft ICP from an audience id + scoring weights."""

    name = "icp_builder"

    def propose(self, payload: dict[str, Any]) -> dict[str, Any]:
        audience_id = str(payload.get("audience_id") or "")
        criteria = list(payload.get("criteria") or [])
        weights = dict(payload.get("weights") or {})
        return {
            "agent": self.name,
            "draft_kind": "icp",
            "draft": {
                "audience_id": audience_id,
                "criteria": criteria,
                "weights": weights,
                "score_formula": "weighted_sum_clamped_0_1",
            },
            "requires_approval": True,
            "external_send_blocked": True,
            "generated_at": _now_iso(),
        }


class OfferPositioningAgent(_BaseAgent):
    """Drafts an Offer record from a payload."""

    name = "offer_positioning"

    def propose(self, payload: dict[str, Any]) -> dict[str, Any]:
        offer = Offer(
            id=uid("off"),
            name_ar=str(payload.get("name_ar") or ""),
            name_en=str(payload.get("name_en") or ""),
            rung=payload.get("rung") or "entry",
            price_min_sar=float(payload.get("price_min_sar") or 0.0),
            price_max_sar=float(payload.get("price_max_sar") or 0.0),
            target_segment=str(payload.get("target_segment") or ""),
            pain_addressed=str(payload.get("pain_addressed") or ""),
            deliverables_ar=list(payload.get("deliverables_ar") or []),
            deliverables_en=list(payload.get("deliverables_en") or []),
            success_metric=str(payload.get("success_metric") or ""),
            scale_kill_rule=str(payload.get("scale_kill_rule") or ""),
        )
        return {
            "agent": self.name,
            "draft_kind": "offer",
            "draft": offer.model_dump(mode="json"),
            "requires_approval": True,
            "external_send_blocked": True,
            "generated_at": _now_iso(),
        }


class ContentStrategistAgent(_BaseAgent):
    """Outlines a campaign + content plan from an offer + audience."""

    name = "content_strategist"

    def propose(self, payload: dict[str, Any]) -> dict[str, Any]:
        offer_id = str(payload.get("offer_id") or "")
        audience_id = str(payload.get("audience_id") or "")
        channels = list(payload.get("channels") or ["linkedin", "email"])
        plan = [
            {
                "channel": ch,
                "cadence": "weekly",
                "first_angle": "money",
                "tracking": "utm_required",
            }
            for ch in channels
        ]
        return {
            "agent": self.name,
            "draft_kind": "content_plan",
            "draft": {"offer_id": offer_id, "audience_id": audience_id, "plan": plan},
            "requires_approval": True,
            "external_send_blocked": True,
            "generated_at": _now_iso(),
        }


class CopywriterAgent(_BaseAgent):
    """Drafts a bilingual MessageVariant from an angle + offer."""

    name = "copywriter"

    def propose(self, payload: dict[str, Any]) -> dict[str, Any]:
        # TODO: route through llm_gateway for prose generation.
        msg = MessageVariant(
            id=uid("msg"),
            offer_id=str(payload.get("offer_id") or ""),
            angle=str(payload.get("angle") or "money"),
            headline_ar=str(payload.get("headline_ar") or ""),
            headline_en=str(payload.get("headline_en") or ""),
            body_ar=str(payload.get("body_ar") or ""),
            body_en=str(payload.get("body_en") or ""),
            cta_ar=str(payload.get("cta_ar") or "احجز جلسة"),
            cta_en=str(payload.get("cta_en") or "Book a session"),
            status="draft",
        )
        return {
            "agent": self.name,
            "draft_kind": "message_variant",
            "draft": msg.model_dump(mode="json"),
            "requires_approval": True,
            "external_send_blocked": True,
            "generated_at": _now_iso(),
        }


class LandingPageAgent(_BaseAgent):
    """Drafts a landing-page brief from an offer."""

    name = "landing_page"

    def propose(self, payload: dict[str, Any]) -> dict[str, Any]:
        offer_id = str(payload.get("offer_id") or "")
        return {
            "agent": self.name,
            "draft_kind": "landing_page_brief",
            "draft": {
                "offer_id": offer_id,
                "sections": [
                    "hero_pain",
                    "proof_strip",
                    "outcome_promise",
                    "deliverables",
                    "cta_primary",
                    "objection_block",
                    "second_cta",
                ],
                "tracking": "utm_required",
                "cta_path": "/dealix-diagnostic",
            },
            "requires_approval": True,
            "external_send_blocked": True,
            "generated_at": _now_iso(),
        }


class CampaignPlannerAgent(_BaseAgent):
    """Drafts a MarketingCampaign object."""

    name = "campaign_planner"

    def propose(self, payload: dict[str, Any]) -> dict[str, Any]:
        camp = MarketingCampaign(
            id=uid("camp"),
            campaign_name=str(payload.get("campaign_name") or ""),
            target_segment=str(payload.get("target_segment") or ""),
            offer_id=str(payload.get("offer_id") or ""),
            channel=str(payload.get("channel") or "linkedin"),
            message_angle=str(payload.get("message_angle") or ""),
            budget_sar=float(payload.get("budget_sar") or 0.0),
            success_metric=str(payload.get("success_metric") or ""),
            scale_kill_rule=str(payload.get("scale_kill_rule") or ""),
            tracking_url_pattern=str(payload.get("tracking_url_pattern") or ""),
            status="draft",
        )
        return {
            "agent": self.name,
            "draft_kind": "campaign",
            "draft": camp.model_dump(mode="json"),
            "requires_approval": True,
            "external_send_blocked": True,
            "generated_at": _now_iso(),
        }


class LeadScoringAgent(_BaseAgent):
    """Returns the weighted score for a payload of components."""

    name = "lead_scoring"

    def propose(self, payload: dict[str, Any]) -> dict[str, Any]:
        score = compute_lead_score(
            float(payload.get("icp_fit") or 0.0),
            float(payload.get("pain") or 0.0),
            float(payload.get("ability_to_pay") or 0.0),
            float(payload.get("urgency") or 0.0),
            float(payload.get("partner_potential") or 0.0),
            float(payload.get("trust_fit") or 0.0),
        )
        lead = Lead(
            id=uid("lead"),
            source=str(payload.get("source") or "unknown"),
            campaign_id=payload.get("campaign_id"),
            segment=str(payload.get("segment") or ""),
            pain=str(payload.get("pain") or ""),
            fit_score=float(payload.get("icp_fit") or 0.0),
            pain_score=float(payload.get("pain") or 0.0),
            ability_to_pay_score=float(payload.get("ability_to_pay") or 0.0),
            urgency_score=float(payload.get("urgency") or 0.0),
            partner_potential_score=float(payload.get("partner_potential") or 0.0),
            trust_fit_score=float(payload.get("trust_fit") or 0.0),
        )
        return {
            "agent": self.name,
            "draft_kind": "lead",
            "draft": lead.model_dump(mode="json"),
            "score": score,
            "requires_approval": True,
            "external_send_blocked": True,
            "generated_at": _now_iso(),
        }


class AttributionAgent(_BaseAgent):
    """Suggests an attribution row, but does NOT persist until approved."""

    name = "attribution"

    def propose(self, payload: dict[str, Any]) -> dict[str, Any]:
        return {
            "agent": self.name,
            "draft_kind": "attribution_proposal",
            "draft": {
                "deal_id": str(payload.get("deal_id") or ""),
                "revenue_sar": float(payload.get("revenue_sar") or 0.0),
                "sources": dict(payload.get("sources") or {}),
                "attribution_type": payload.get("attribution_type") or "multi_touch",
                "payment_received": bool(payload.get("payment_received") or False),
                "signed_agreement": bool(payload.get("signed_agreement") or False),
            },
            "requires_approval": True,
            "external_send_blocked": True,
            "generated_at": _now_iso(),
        }


class ConversionOptimizerAgent(_BaseAgent):
    """Suggests CRO experiments based on a payload of touches + leads."""

    name = "conversion_optimizer"

    def propose(self, payload: dict[str, Any]) -> dict[str, Any]:
        target = str(payload.get("target") or "landing_page")
        return {
            "agent": self.name,
            "draft_kind": "cro_experiment",
            "draft": {
                "target": target,
                "hypothesis": str(payload.get("hypothesis") or ""),
                "variant_a": str(payload.get("variant_a") or "control"),
                "variant_b": str(payload.get("variant_b") or "challenger"),
                "success_metric": str(payload.get("success_metric") or "qualified_leads"),
                "min_sample_per_variant": 30,
                "lift_required": "2x",
            },
            "requires_approval": True,
            "external_send_blocked": True,
            "generated_at": _now_iso(),
        }


class CaseStudyAgent(_BaseAgent):
    """Drafts a bilingual case-study skeleton from a deal id + outcome notes."""

    name = "case_study"

    def propose(self, payload: dict[str, Any]) -> dict[str, Any]:
        deal_id = str(payload.get("deal_id") or "")
        case = CaseStudyDraft(
            id=uid("cs"),
            deal_id=deal_id,
            before_ar=str(payload.get("before_ar") or ""),
            before_en=str(payload.get("before_en") or ""),
            action_ar=str(payload.get("action_ar") or ""),
            action_en=str(payload.get("action_en") or ""),
            output_ar=str(payload.get("output_ar") or ""),
            output_en=str(payload.get("output_en") or ""),
            outcome_ar=str(payload.get("outcome_ar") or ""),
            outcome_en=str(payload.get("outcome_en") or ""),
            learning_ar=str(payload.get("learning_ar") or ""),
            learning_en=str(payload.get("learning_en") or ""),
            next_steps_ar=str(payload.get("next_steps_ar") or ""),
            next_steps_en=str(payload.get("next_steps_en") or ""),
        )
        return {
            "agent": self.name,
            "draft_kind": "case_study",
            "draft": case.model_dump(mode="json"),
            "requires_approval": True,
            "external_send_blocked": True,
            "generated_at": _now_iso(),
        }


MARKETING_AGENTS: dict[str, type[_BaseAgent]] = {
    cls.name: cls
    for cls in (
        MarketRadarAgent,
        AudienceResearchAgent,
        ICPBuilderAgent,
        OfferPositioningAgent,
        ContentStrategistAgent,
        CopywriterAgent,
        LandingPageAgent,
        CampaignPlannerAgent,
        LeadScoringAgent,
        AttributionAgent,
        ConversionOptimizerAgent,
        CaseStudyAgent,
    )
}


def propose_via_agent(
    agent_name: str,
    payload: dict[str, Any],
    *,
    store: RevenueMarketingStore | None = None,
) -> dict[str, Any]:
    """Dispatcher — runs the named agent and records an evidence event."""
    cls = MARKETING_AGENTS.get(agent_name)
    if cls is None:
        raise ValueError("agent_not_registered")
    agent = cls(store=store)
    draft = agent.propose(payload)
    try:
        get_autopilot_store().append_evidence(
            EvidenceEvent(
                id=ev_uid("ev"),
                event_type="marketing_agent_proposed",
                entity_type="revenue_marketing_agent",
                entity_id=agent_name,
                source="revenue_marketing",
                summary=f"agent={agent_name} kind={draft.get('draft_kind')}",
            ),
        )
    except Exception:
        pass
    return draft


__all__ = [
    "MARKETING_AGENTS",
    "AttributionAgent",
    "AudienceResearchAgent",
    "CampaignPlannerAgent",
    "CaseStudyAgent",
    "ContentStrategistAgent",
    "ConversionOptimizerAgent",
    "CopywriterAgent",
    "ICPBuilderAgent",
    "LandingPageAgent",
    "LeadScoringAgent",
    "MarketRadarAgent",
    "MarketingTouch",
    "OfferPositioningAgent",
    "propose_via_agent",
]
