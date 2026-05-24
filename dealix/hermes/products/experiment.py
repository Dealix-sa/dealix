"""Offer Experiment — wraps a kill/scale test plan around an offer."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class OfferExperimentPlan:
    offer: str
    audience_size: int
    target_replies: int
    target_paid: int
    kill_threshold_no_reply: int
    scale_rule: str
    kill_rule: str


class OfferExperiment:
    def plan(self, *, offer: str, audience_size: int = 50) -> OfferExperimentPlan:
        return OfferExperimentPlan(
            offer=offer,
            audience_size=audience_size,
            target_replies=max(3, audience_size // 10),
            target_paid=1,
            kill_threshold_no_reply=audience_size,
            scale_rule="2 paying customers in the pilot window",
            kill_rule=f"0 replies after {audience_size} qualified outreaches",
        )
