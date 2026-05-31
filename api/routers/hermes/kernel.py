"""Kernel router — the seven lifecycle endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from api.routers.hermes._dependencies import get_hermes
from dealix.hermes.kernel.schemas import (
    AssetType,
    OpportunityType,
    OutcomeStatus,
    SignalSensitivity,
    SignalSource,
    SignalType,
    SovereigntyLevel,
)
from dealix.hermes.kernel.signals import capture_signal
from dealix.hermes.orchestrator import HermesOrchestrator


router = APIRouter(prefix="/api/v1/hermes", tags=["hermes-kernel"])


class CaptureSignalRequest(BaseModel):
    source: SignalSource
    signal_type: SignalType
    title: str
    content: str
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    sensitivity: SignalSensitivity = SignalSensitivity.internal
    workspace_id: str = "dealix_internal"
    owner: str = "Sami"


@router.post("/signals/capture")
def capture(body: CaptureSignalRequest, orch: HermesOrchestrator = Depends(get_hermes)):
    s = capture_signal(
        store=orch.kernel.signals,
        source=body.source,
        signal_type=body.signal_type,
        title=body.title,
        content=body.content,
        confidence=body.confidence,
        sensitivity=body.sensitivity,
        workspace_id=body.workspace_id,
        owner=body.owner,
    )
    return s


class ScoreOpportunityRequest(BaseModel):
    signal_id: str
    opportunity_type: OpportunityType
    title: str
    estimated_value_sar: float = 0.0
    cash_speed_score: int = 0
    strategic_score: int = 0
    repeatability_score: int = 0
    data_moat_score: int = 0
    difficulty_score: int = 0
    risk_score: int = 0
    sovereignty_level: SovereigntyLevel = SovereigntyLevel.S1_INTERNAL


@router.post("/opportunities/score")
def score_opportunity(body: ScoreOpportunityRequest, orch: HermesOrchestrator = Depends(get_hermes)):
    try:
        signal = orch.kernel.signals.get(body.signal_id)
    except KeyError as exc:
        raise HTTPException(404, str(exc)) from exc
    return orch.kernel.opportunities.create_from_signal(
        signal,
        opportunity_type=body.opportunity_type,
        title=body.title,
        estimated_value_sar=body.estimated_value_sar,
        scores={
            "cash_speed_score": body.cash_speed_score,
            "strategic_score": body.strategic_score,
            "repeatability_score": body.repeatability_score,
            "data_moat_score": body.data_moat_score,
            "difficulty_score": body.difficulty_score,
            "risk_score": body.risk_score,
        },
        sovereignty_level=body.sovereignty_level,
    )


class CreateDecisionRequest(BaseModel):
    opportunity_id: str
    memo: str
    rationale: str = ""
    expected_outcome: str = ""
    risks: list[str] = Field(default_factory=list)


@router.post("/decisions/create")
def create_decision(body: CreateDecisionRequest, orch: HermesOrchestrator = Depends(get_hermes)):
    try:
        opp = orch.kernel.opportunities.get(body.opportunity_id)
    except KeyError as exc:
        raise HTTPException(404, str(exc)) from exc
    return orch.kernel.decisions.create_memo(
        opp,
        memo=body.memo,
        rationale=body.rationale,
        risks=body.risks,
        expected_outcome=body.expected_outcome,
    )


class PlanExecutionRequest(BaseModel):
    decision_id: str
    agent_id: str
    tools: list[str] = Field(default_factory=list)
    payload: dict = Field(default_factory=dict)


@router.post("/executions/plan")
def plan_execution(body: PlanExecutionRequest, orch: HermesOrchestrator = Depends(get_hermes)):
    try:
        d = orch.kernel.decisions.get(body.decision_id)
    except KeyError as exc:
        raise HTTPException(404, str(exc)) from exc
    if not orch.agent_registry.exists(body.agent_id):
        raise HTTPException(400, f"agent {body.agent_id} is not registered")
    return orch.kernel.executions.plan(d, agent_id=body.agent_id, tools=body.tools, payload=body.payload)


class LogOutcomeRequest(BaseModel):
    execution_id: str
    status: OutcomeStatus
    actual_result: str
    revenue_sar: float = 0.0
    cost_sar: float = 0.0
    learning: str = ""
    asset_review_required: bool = False


@router.post("/outcomes/log")
def log_outcome(body: LogOutcomeRequest, orch: HermesOrchestrator = Depends(get_hermes)):
    try:
        e = orch.kernel.executions.get(body.execution_id)
    except KeyError as exc:
        raise HTTPException(404, str(exc)) from exc
    return orch.kernel.outcomes.log(
        e,
        status=body.status,
        actual_result=body.actual_result,
        revenue_sar=body.revenue_sar,
        cost_sar=body.cost_sar,
        learning=body.learning,
        asset_review_required=body.asset_review_required,
    )


class BuildAssetRequest(BaseModel):
    outcome_id: str
    asset_type: AssetType
    title: str
    description: str = ""
    moat_score: float = 0.0


@router.post("/assets/build")
def build_asset(body: BuildAssetRequest, orch: HermesOrchestrator = Depends(get_hermes)):
    try:
        out = orch.kernel.outcomes.get(body.outcome_id)
    except KeyError as exc:
        raise HTTPException(404, str(exc)) from exc
    try:
        return orch.kernel.assets.create_from_outcome(
            out,
            asset_type=body.asset_type,
            title=body.title,
            description=body.description,
            moat_score=body.moat_score,
        )
    except ValueError as exc:
        raise HTTPException(409, str(exc)) from exc


@router.get("/events")
def list_events(orch: HermesOrchestrator = Depends(get_hermes)):
    return orch.kernel.all_events()
