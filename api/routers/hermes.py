"""
Hermes Universal Kernel — public-shape API.

Exposes the canonical loop (signal → opportunity → decision → execution
→ trust → outcome → asset) plus the sovereign brief. No external side
effects: every "send" is a draft awaiting Sami's approval.
"""

from __future__ import annotations

from fastapi import APIRouter

from dealix.hermes.agents.founder_brief import FounderBrief, build_brief
from dealix.hermes.core.schemas import (
    HermesOpportunity,
    HermesOutcome,
    HermesSignal,
)
from dealix.hermes.money.dashboard import MoneyDashboard, render as render_dashboard
from dealix.hermes.orchestrator import HermesOrchestrator
from dealix.hermes.sovereignty import SovereigntyDecision, classify_action
from dealix.hermes.trust.guardrails import (
    TrustCheckRequest,
    TrustCheckResult,
    trust_check,
)
from dealix.hermes.trust.mcp_security import (
    MCPReviewResult,
    MCPServerReview,
    review_mcp_server,
)

router = APIRouter(prefix="/api/v1/hermes", tags=["Hermes"])
_orchestrator = HermesOrchestrator()


@router.post("/signals/capture")
async def capture_signal(signal: HermesSignal) -> dict:
    opportunity = _orchestrator.signal_to_opportunity(signal)
    return {
        "signal": signal.model_dump(),
        "opportunity": opportunity.model_dump(),
        "evaluation": _orchestrator.evaluate_opportunity(opportunity),
    }


@router.post("/opportunities/score")
async def score_opportunity(opportunity: HermesOpportunity) -> dict:
    return _orchestrator.evaluate_opportunity(opportunity)


@router.post("/decisions/create")
async def create_decision(opportunity: HermesOpportunity) -> dict:
    return _orchestrator.create_decision_memo(opportunity).model_dump()


@router.post("/executions/plan")
async def plan_execution(action_type: str, opportunity: HermesOpportunity) -> dict:
    memo = _orchestrator.create_decision_memo(opportunity)
    plan = _orchestrator.plan_execution(memo, action_type)
    return plan.model_dump()


@router.post("/trust/check", response_model=TrustCheckResult)
async def run_trust_check(request: TrustCheckRequest) -> TrustCheckResult:
    return trust_check(request)


@router.post("/sovereignty/check", response_model=SovereigntyDecision)
async def sovereignty_check(
    action_type: str,
    contains_sensitive_data: bool = False,
) -> SovereigntyDecision:
    return classify_action(action_type, contains_sensitive_data)


@router.post("/mcp/review", response_model=MCPReviewResult)
async def mcp_review(review: MCPServerReview) -> MCPReviewResult:
    return review_mcp_server(review)


@router.post("/outcomes/log")
async def log_outcome(outcome: HermesOutcome) -> dict:
    asset = _orchestrator.outcome_to_asset(outcome)
    return {
        "outcome": outcome.model_dump(),
        "asset_created": asset.model_dump() if asset else None,
    }


@router.get("/sovereign/brief", response_model=FounderBrief)
async def sovereign_brief() -> FounderBrief:
    return build_brief()


@router.get("/money/dashboard", response_model=MoneyDashboard)
async def money_dashboard() -> MoneyDashboard:
    return render_dashboard()
