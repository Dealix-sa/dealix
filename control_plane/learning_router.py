"""LearningRouter: convert weekly inputs into a learning decision.

Inputs are loose dicts (DMs, replies, calls, proposals, payments, delivery
feedback, QA failures, trust escalations, product bugs). Output is one of:
BUILD, FIX, KILL, DEFER. Every week must produce at least one decision.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class LearningDecision(str, Enum):
    BUILD = "BUILD"
    FIX = "FIX"
    KILL = "KILL"
    DEFER = "DEFER"


@dataclass
class LearningOutcome:
    decision: LearningDecision
    area: str
    rationale: str


class LearningRouter:
    """Map weekly inputs into one or more learning outcomes."""

    def route(self, inputs: Dict[str, int]) -> List[LearningOutcome]:
        outcomes: List[LearningOutcome] = []

        replies = int(inputs.get("replies", 0))
        dms = int(inputs.get("dms", 0))
        if dms >= 25 and replies <= 1:
            outcomes.append(
                LearningOutcome(
                    decision=LearningDecision.FIX,
                    area="messaging",
                    rationale="High volume, low reply rate — rewrite message templates.",
                )
            )

        calls = int(inputs.get("calls", 0))
        proposals_won = int(inputs.get("proposals_won", 0))
        proposals_sent = int(inputs.get("proposals_sent", 0))
        if proposals_sent >= 2 and proposals_won == 0:
            outcomes.append(
                LearningOutcome(
                    decision=LearningDecision.FIX,
                    area="pricing_or_scope",
                    rationale="Proposals sent but none won — review pricing and scope.",
                )
            )

        if calls >= 3 and proposals_sent == 0:
            outcomes.append(
                LearningOutcome(
                    decision=LearningDecision.FIX,
                    area="proposal_cadence",
                    rationale="Calls happening but no proposals — close the loop faster.",
                )
            )

        qa_failures = int(inputs.get("qa_failures", 0))
        if qa_failures >= 2:
            outcomes.append(
                LearningOutcome(
                    decision=LearningDecision.FIX,
                    area="delivery_quality",
                    rationale="Repeated QA failures — update delivery playbook.",
                )
            )

        trust_escalations = int(inputs.get("trust_escalations", 0))
        if trust_escalations >= 1:
            outcomes.append(
                LearningOutcome(
                    decision=LearningDecision.FIX,
                    area="trust_policy",
                    rationale="Trust escalation occurred — tighten policy and routes.",
                )
            )

        product_bugs = int(inputs.get("product_bugs", 0))
        if product_bugs >= 3:
            outcomes.append(
                LearningOutcome(
                    decision=LearningDecision.FIX,
                    area="product_quality",
                    rationale="Bug rate elevated — pause new build, stabilize.",
                )
            )

        feedback_pos = int(inputs.get("feedback_positive", 0))
        if feedback_pos >= 2:
            outcomes.append(
                LearningOutcome(
                    decision=LearningDecision.BUILD,
                    area="offer_expansion",
                    rationale="Positive feedback signal — consider next-rung offer.",
                )
            )

        if not outcomes:
            outcomes.append(
                LearningOutcome(
                    decision=LearningDecision.DEFER,
                    area="general",
                    rationale="No strong signal this week — collect more data before deciding.",
                )
            )

        return outcomes
