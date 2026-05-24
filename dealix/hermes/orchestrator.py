"""
Hermes Orchestrator — wires the canonical loop:

    Signal → Opportunity → Decision → Execution → Trust → Outcome → Asset

Each method is deterministic and side-effect-free except for explicit
store calls. The orchestrator never sends external messages, never moves
money, and never bypasses sovereignty.
"""

from __future__ import annotations

from dealix.hermes.core.schemas import (
    HermesAsset,
    HermesDecisionMemo,
    HermesExecutionPlan,
    HermesOpportunity,
    HermesOutcome,
    HermesSignal,
)
from dealix.hermes.core.scoring import opportunity_score, should_execute_now
from dealix.hermes.sovereignty import SovereigntyLevel, classify_action
from dealix.hermes.trust.guardrails import TrustCheckRequest, trust_check


class HermesOrchestrator:
    # ── 1. Signal → Opportunity ────────────────────────────────────
    def signal_to_opportunity(self, signal: HermesSignal) -> HermesOpportunity:
        """Deterministic v0.1 mapping. LLM-assisted enrichment lands later."""
        opportunity_type = self._infer_opportunity_type(signal.signal_type)
        return HermesOpportunity(
            opportunity_type=opportunity_type,
            title=f"Opportunity from: {signal.title}",
            description=signal.content,
            target_entity=None,
            estimated_value_sar=None,
            cash_speed_score=3,
            strategic_score=3,
            difficulty_score=3,
            risk_score=2,
            repeatability_score=3,
            data_moat_score=3,
            sovereignty_level=SovereigntyLevel.S1_INTERNAL.value,
            recommended_action="Create decision memo",
            recommended_agent="opportunity_mapper",
        )

    @staticmethod
    def _infer_opportunity_type(signal_type: str) -> str:
        mapping = {
            "customer": "customer",
            "partner": "partner",
            "product": "product",
            "training": "training",
            "report": "report",
            "api": "api",
            "venture": "venture",
            "risk": "risk_reduction",
            "finance": "personal_wealth",
            "legal": "governance",
            "personal": "personal_wealth",
            "market": "product",
            "technical": "product",
        }
        return mapping.get(signal_type, "product")

    # ── 2. Opportunity → Evaluation ────────────────────────────────
    def evaluate_opportunity(self, opportunity: HermesOpportunity) -> dict:
        score = opportunity_score(opportunity)
        return {
            "score": score,
            "execute_now": should_execute_now(opportunity),
            "recommended_action": opportunity.recommended_action,
        }

    # ── 3. Opportunity → Decision Memo ─────────────────────────────
    def create_decision_memo(self, opportunity: HermesOpportunity) -> HermesDecisionMemo:
        execute_now = should_execute_now(opportunity)
        approval_required = opportunity.sovereignty_level not in {
            SovereigntyLevel.S0_AUTO_SAFE.value,
            SovereigntyLevel.S1_INTERNAL.value,
        }
        return HermesDecisionMemo(
            decision_title=f"Decision: {opportunity.title}",
            context=opportunity.description,
            options=["execute_now", "defer", "kill"],
            recommendation="execute_now" if execute_now else "defer",
            expected_impact=f"Potential value: {opportunity.estimated_value_sar or 'unknown'} SAR",
            risks=[f"Risk score: {opportunity.risk_score}"],
            sovereignty_level=opportunity.sovereignty_level,
            approval_required=approval_required,
            next_steps=[opportunity.recommended_action],
        )

    # ── 4. Decision → Execution Plan ───────────────────────────────
    def plan_execution(self, memo: HermesDecisionMemo, action_type: str) -> HermesExecutionPlan:
        sovereign = classify_action(action_type)
        return HermesExecutionPlan(
            action_type=action_type,
            agent_id="hermes_orchestrator",
            permission_level=sovereign.level.value,
            steps=[
                "draft",
                "trust_check",
                "approval_if_needed",
                "execute_or_hold",
                "log_outcome",
            ],
            expected_result="Action prepared safely",
            requires_approval=sovereign.requires_sami_approval,
        )

    # ── 5. Trust check ─────────────────────────────────────────────
    def check_trust(self, content: str, action_type: str) -> dict:
        result = trust_check(
            TrustCheckRequest(
                content=content,
                action_type=action_type,
                target_audience="external" if action_type.startswith("external_") else "internal",
                contains_external_commitment=action_type.startswith("external_"),
            )
        )
        return result.model_dump()

    # ── 6. Outcome → Asset ─────────────────────────────────────────
    def outcome_to_asset(self, outcome: HermesOutcome) -> HermesAsset | None:
        if outcome.status in {"won", "asset_created"} or outcome.learning:
            return HermesAsset(
                asset_type="playbook",
                title=f"Asset from outcome: {outcome.outcome_type}",
                description=outcome.learning or outcome.actual_result or "Reusable learning",
                reusable=True,
            )
        return None
