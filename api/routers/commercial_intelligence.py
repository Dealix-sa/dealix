"""Tenant-scoped Commercial Intelligence graph APIs.

All writes are internal records.  The router has no send, scrape, charge,
provider-dispatch, or production-mutation path.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field, HttpUrl
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError

from api.security.auth_deps import (
    get_current_user,
    require_sales_manager,
    require_tenant_admin,
)
from auto_client_acquisition.service_catalog import SERVICE_IDS
from db.models import AuditLogRecord
from db.models_commercial_intelligence import (
    CommercialFinanceCaseRecord,
    CommercialOpportunityRecord,
    CommercialOpportunitySignalRecord,
    CommercialSignalRecord,
    CommercialSourceRecord,
    DepartmentObjectiveRecord,
    StrategicRelationshipRecord,
)
from db.session import async_session_factory
from dealix.commercial_finance import (
    CommercialFinanceDecision,
    CommercialFinanceInputs,
    FinancePricingStatus,
    OfferEconomicsClass,
    evaluate_commercial_finance,
)
from dealix.commercial_intelligence import (
    CommercialSignal,
    EvidenceLevel,
    GovernedSource,
    OpportunityInputs,
    OpportunityStage,
    SourceKind,
    SourcePolicyStatus,
    highest_evidence_level,
    score_opportunity,
    score_source,
)
from dealix.commercial_persuasion import (
    DEFAULT_BUYER_ROLES,
    BuyerDecisionContext,
    BuyerRole,
    PersuasionEvidence,
    PricingDecision,
    build_buyer_decision_plan,
)

router = APIRouter(prefix="/api/v1/commercial-intelligence", tags=["Sales"])


class _StrictBody(BaseModel):
    model_config = ConfigDict(extra="forbid")


class SourceBody(_StrictBody):
    name: str = Field(min_length=1, max_length=255)
    kind: SourceKind
    source_url: HttpUrl | None = None
    policy_status: SourcePolicyStatus = SourcePolicyStatus.REVIEW_REQUIRED
    allowed_use: str = Field(min_length=1, max_length=255)
    authority_score: int = Field(default=50, ge=0, le=100)
    verifiability_score: int = Field(default=50, ge=0, le=100)
    freshness_days: int = Field(default=30, ge=1, le=3650)
    retention_days: int = Field(default=365, ge=1, le=3650)
    terms_reviewed_at: datetime | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class SignalBody(_StrictBody):
    account_id: str = Field(min_length=1, max_length=64)
    source_id: str = Field(min_length=1, max_length=64)
    signal_type: str = Field(min_length=1, max_length=64)
    claim: str = Field(min_length=1, max_length=5000)
    evidence_ref: str = Field(min_length=1, max_length=1000)
    evidence_level: EvidenceLevel
    confidence: int = Field(ge=0, le=100)
    observed_at: datetime
    expires_at: datetime | None = None
    payload: dict[str, Any] = Field(default_factory=dict)


class ObjectiveBody(_StrictBody):
    department: str = Field(min_length=1, max_length=64)
    objective: str = Field(min_length=1, max_length=5000)
    metric: str = Field(min_length=1, max_length=128)
    target_value: float | None = None
    target_unit: str | None = Field(default=None, max_length=64)
    horizon: str = Field(default="quarter", max_length=32)
    priority: int = Field(default=50, ge=0, le=100)
    evidence_required: EvidenceLevel = EvidenceLevel.L3_FIRST_PARTY
    owner_role: str = Field(default="department_owner", max_length=64)


class RelationshipBody(_StrictBody):
    account_id: str = Field(min_length=1, max_length=64)
    company_name: str = Field(min_length=1, max_length=255)
    relationship_type: str = Field(min_length=1, max_length=64)
    stage: str = Field(default="research", max_length=32)
    permission_state: str = Field(default="research_only", max_length=32)
    mutual_value: str = Field(min_length=1, max_length=5000)
    relationship_strength: int = Field(default=0, ge=0, le=100)
    owner_role: str = Field(default="partnerships", max_length=64)
    evidence_refs: list[str] = Field(default_factory=list, max_length=100)
    last_interaction_at: datetime | None = None
    next_review_at: datetime | None = None


class OpportunityBody(_StrictBody):
    account_id: str = Field(min_length=1, max_length=64)
    company_name: str = Field(min_length=1, max_length=255)
    title: str = Field(min_length=1, max_length=255)
    department_objective_id: str = Field(min_length=1, max_length=64)
    relationship_id: str | None = Field(default=None, max_length=64)
    offer_id: str = Field(min_length=1, max_length=64)
    source_signal_ids: list[str] = Field(min_length=1, max_length=100)
    strategic_fit: int = Field(ge=0, le=100)
    problem_evidence: int = Field(ge=0, le=100)
    urgency: int = Field(ge=0, le=100)
    commercial_value: int = Field(ge=0, le=100)
    next_action: str = Field(min_length=1, max_length=5000)
    proof_target: str = Field(min_length=1, max_length=5000)


class BuyerDecisionPlanBody(_StrictBody):
    buyer_roles: list[BuyerRole] = Field(default_factory=list, max_length=6)
    known_objections: list[str] = Field(default_factory=list, max_length=20)
    requested_discount_pct: float = Field(default=0, ge=0, le=100)
    non_standard_terms_requested: bool = False


class FinanceCaseBody(_StrictBody):
    offer_class: OfferEconomicsClass
    list_price_sar: Decimal = Field(gt=0, max_digits=14, decimal_places=2)
    proposed_price_sar: Decimal = Field(gt=0, max_digits=14, decimal_places=2)
    delivery_cost_sar: Decimal = Field(ge=0, max_digits=14, decimal_places=2)
    acquisition_cost_sar: Decimal = Field(ge=0, max_digits=14, decimal_places=2)
    upfront_cash_exposure_sar: Decimal = Field(
        ge=0, max_digits=14, decimal_places=2
    )
    payment_terms_days: int = Field(ge=0, le=365)
    capacity_required_pct: Decimal = Field(ge=0, le=100, max_digits=5, decimal_places=2)
    source_refs: dict[str, str] = Field(min_length=1, max_length=32)
    close_probability_low: Decimal | None = Field(default=None, ge=0, le=1)
    close_probability_base: Decimal | None = Field(default=None, ge=0, le=1)
    close_probability_high: Decimal | None = Field(default=None, ge=0, le=1)
    close_probability_source_ref: str | None = Field(default=None, max_length=1000)
    close_probability_evidence_level: EvidenceLevel | None = None
    close_probability_cohort_size: int | None = Field(default=None, ge=1)
    customer_roi_hypothesis_sar: Decimal | None = Field(
        default=None, ge=0, max_digits=14, decimal_places=2
    )
    customer_roi_source_ref: str | None = Field(default=None, max_length=1000)


class PriceApprovalBody(_StrictBody):
    confirmed_proposed_price_sar: Decimal = Field(
        gt=0, max_digits=14, decimal_places=2
    )
    approval_ref: str = Field(min_length=1, max_length=128)


def _tenant_id(current_user: Any) -> str:
    value = (
        current_user.get("tenant_id")
        if isinstance(current_user, dict)
        else getattr(current_user, "tenant_id", None)
    )
    if not value:
        raise HTTPException(403, "authenticated_tenant_required")
    return str(value)


def _user_id(current_user: Any) -> str:
    value = (
        current_user.get("id")
        if isinstance(current_user, dict)
        else getattr(current_user, "id", None)
    )
    if not value:
        raise HTTPException(403, "authenticated_user_id_required")
    clean = str(value)
    if len(clean) > 64:
        raise HTTPException(403, "authenticated_user_id_invalid")
    return clean


def _aware(value: datetime, field: str) -> datetime:
    if value.tzinfo is None:
        raise HTTPException(422, f"{field}_must_be_timezone_aware")
    return value.astimezone(UTC)


def _source_domain(record: CommercialSourceRecord) -> GovernedSource:
    return GovernedSource(
        tenant_id=record.tenant_id,
        source_id=record.id,
        name=record.name,
        kind=SourceKind(record.kind),
        policy_status=SourcePolicyStatus(record.policy_status),
        allowed_use=record.allowed_use,
        authority_score=record.authority_score,
        verifiability_score=record.verifiability_score,
        freshness_days=record.freshness_days,
        retention_days=record.retention_days,
        terms_reviewed_at=record.terms_reviewed_at,
        source_url=record.source_url,
    )


def _signal_domain(record: CommercialSignalRecord) -> CommercialSignal:
    return CommercialSignal(
        tenant_id=record.tenant_id,
        signal_id=record.id,
        account_id=record.account_id,
        source_id=record.source_id,
        signal_type=record.signal_type,
        claim=record.claim,
        evidence_ref=record.evidence_ref,
        observed_at=record.observed_at,
        confidence=record.confidence,
        evidence_level=EvidenceLevel(record.evidence_level),
        expires_at=record.expires_at,
    )


async def _commit(session: Any, *, conflict: str) -> None:
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise HTTPException(409, conflict) from exc
    except Exception as exc:
        await session.rollback()
        raise HTTPException(503, "commercial_intelligence_not_persisted") from exc


def _add_audit(
    session: Any,
    *,
    tenant_id: str,
    user_id: str,
    action: str,
    entity_id: str,
    diff: dict[str, Any],
) -> None:
    session.add(
        AuditLogRecord(
            id=f"audit_{uuid.uuid4().hex}",
            tenant_id=tenant_id,
            user_id=user_id,
            action=action,
            entity_type="commercial_finance_case",
            entity_id=entity_id,
            diff=diff,
            status="ok",
        )
    )


def _finance_case_response(record: CommercialFinanceCaseRecord) -> dict[str, Any]:
    return {
        "id": record.id,
        "opportunity_id": record.opportunity_id,
        "parent_case_id": record.parent_case_id,
        "offer_id": record.offer_id,
        "offer_class": record.offer_class,
        "pricing_status": record.pricing_status,
        "decision": record.decision,
        "currency": record.currency,
        "proposed_price_sar": str(record.proposed_price_sar),
        "gross_margin_pct": str(record.gross_margin_pct),
        "contribution_margin_pct": str(record.contribution_margin_pct),
        "readiness_score": record.readiness_score,
        "approval_required": True,
        "price_approved": record.pricing_status == FinancePricingStatus.FOUNDER_APPROVED.value,
        "approval_ref": record.approval_ref,
        "approved_at": record.approved_at,
        "assessment": record.assessment_json,
        "external_action_allowed": False,
    }


def _build_finance_inputs(
    opportunity: CommercialOpportunityRecord,
    body: FinanceCaseBody,
    *,
    pricing_status: FinancePricingStatus,
) -> CommercialFinanceInputs:
    try:
        return CommercialFinanceInputs(
            opportunity_id=opportunity.id,
            offer_id=opportunity.offer_id,
            offer_class=body.offer_class,
            list_price_sar=body.list_price_sar,
            proposed_price_sar=body.proposed_price_sar,
            delivery_cost_sar=body.delivery_cost_sar,
            acquisition_cost_sar=body.acquisition_cost_sar,
            upfront_cash_exposure_sar=body.upfront_cash_exposure_sar,
            payment_terms_days=body.payment_terms_days,
            capacity_required_pct=body.capacity_required_pct,
            source_refs=body.source_refs,
            pricing_status=pricing_status,
            close_probability_low=body.close_probability_low,
            close_probability_base=body.close_probability_base,
            close_probability_high=body.close_probability_high,
            close_probability_source_ref=body.close_probability_source_ref,
            close_probability_evidence_level=body.close_probability_evidence_level,
            close_probability_cohort_size=body.close_probability_cohort_size,
            customer_roi_hypothesis_sar=body.customer_roi_hypothesis_sar,
            customer_roi_source_ref=body.customer_roi_source_ref,
        )
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc


@router.get("/status")
async def status() -> dict[str, Any]:
    return {
        "status": "operational",
        "mode": "evidence_governed",
        "persistence": "postgres_alembic",
        "external_action_allowed": False,
        "capabilities": [
            "source_registry",
            "signal_provenance",
            "department_objectives",
            "strategic_relationships",
            "opportunity_graph",
            "source_scorecards",
            "buyer_decision_spine",
            "commercial_finance_gate",
            "append_only_price_approval",
        ],
    }


@router.post("/sources", status_code=201)
async def create_source(
    body: SourceBody,
    current_user: Any = Depends(require_tenant_admin),
) -> dict[str, Any]:
    tenant_id = _tenant_id(current_user)
    if body.terms_reviewed_at:
        _aware(body.terms_reviewed_at, "terms_reviewed_at")
    record = CommercialSourceRecord(
        id=f"cis_{uuid.uuid4().hex}",
        tenant_id=tenant_id,
        name=body.name.strip(),
        kind=body.kind.value,
        source_url=str(body.source_url) if body.source_url else None,
        policy_status=body.policy_status.value,
        allowed_use=body.allowed_use.strip(),
        authority_score=body.authority_score,
        verifiability_score=body.verifiability_score,
        freshness_days=body.freshness_days,
        retention_days=body.retention_days,
        terms_reviewed_at=body.terms_reviewed_at,
        metadata_json=body.metadata,
    )
    async with async_session_factory()() as session:
        session.add(record)
        await _commit(session, conflict="source_already_registered")
    return {"status": "created", "source_id": record.id, "external_side_effect": False}


@router.post("/signals", status_code=201)
async def create_signal(
    body: SignalBody,
    current_user: Any = Depends(require_sales_manager),
) -> dict[str, Any]:
    tenant_id = _tenant_id(current_user)
    observed_at = _aware(body.observed_at, "observed_at")
    async with async_session_factory()() as session:
        source = await session.get(CommercialSourceRecord, body.source_id)
        if source is None or source.tenant_id != tenant_id or not source.active:
            raise HTTPException(404, "tenant_source_not_found")
        if source.policy_status == SourcePolicyStatus.BLOCKED.value:
            raise HTTPException(409, "blocked_source_cannot_create_signal")
        expires_at = (
            _aware(body.expires_at, "expires_at")
            if body.expires_at
            else observed_at + timedelta(days=source.freshness_days)
        )
        if expires_at <= observed_at:
            raise HTTPException(422, "expires_at_must_follow_observed_at")
        record = CommercialSignalRecord(
            id=f"sig_{uuid.uuid4().hex}",
            tenant_id=tenant_id,
            account_id=body.account_id.strip(),
            source_id=source.id,
            signal_type=body.signal_type.strip(),
            claim=body.claim.strip(),
            evidence_ref=body.evidence_ref.strip(),
            evidence_level=body.evidence_level.value,
            confidence=body.confidence,
            observed_at=observed_at,
            expires_at=expires_at,
            status="active",
            payload_json=body.payload,
        )
        session.add(record)
        await _commit(session, conflict="signal_evidence_already_registered")
    return {"status": "created", "signal_id": record.id, "external_side_effect": False}


@router.post("/objectives", status_code=201)
async def create_objective(
    body: ObjectiveBody,
    current_user: Any = Depends(require_sales_manager),
) -> dict[str, Any]:
    tenant_id = _tenant_id(current_user)
    record = DepartmentObjectiveRecord(
        id=f"obj_{uuid.uuid4().hex}",
        tenant_id=tenant_id,
        department=body.department.strip(),
        objective=body.objective.strip(),
        metric=body.metric.strip(),
        target_value=body.target_value,
        target_unit=body.target_unit,
        horizon=body.horizon.strip(),
        priority=body.priority,
        status="active",
        evidence_required=body.evidence_required.value,
        owner_role=body.owner_role.strip(),
    )
    async with async_session_factory()() as session:
        session.add(record)
        await _commit(session, conflict="department_metric_already_registered")
    return {"status": "created", "objective_id": record.id, "external_side_effect": False}


@router.post("/relationships", status_code=201)
async def create_relationship(
    body: RelationshipBody,
    current_user: Any = Depends(require_sales_manager),
) -> dict[str, Any]:
    tenant_id = _tenant_id(current_user)
    record = StrategicRelationshipRecord(
        id=f"rel_{uuid.uuid4().hex}",
        tenant_id=tenant_id,
        account_id=body.account_id.strip(),
        company_name=body.company_name.strip(),
        relationship_type=body.relationship_type.strip(),
        stage=body.stage.strip(),
        permission_state=body.permission_state.strip(),
        mutual_value=body.mutual_value.strip(),
        relationship_strength=body.relationship_strength,
        owner_role=body.owner_role.strip(),
        evidence_refs_json=body.evidence_refs,
        last_interaction_at=body.last_interaction_at,
        next_review_at=body.next_review_at,
    )
    async with async_session_factory()() as session:
        session.add(record)
        await _commit(session, conflict="strategic_relationship_already_registered")
    return {"status": "created", "relationship_id": record.id, "external_side_effect": False}


@router.post("/opportunities", status_code=201)
async def create_opportunity(
    body: OpportunityBody,
    current_user: Any = Depends(require_sales_manager),
) -> dict[str, Any]:
    tenant_id = _tenant_id(current_user)
    if body.offer_id not in SERVICE_IDS:
        raise HTTPException(422, "offer_not_in_canonical_service_catalog")
    async with async_session_factory()() as session:
        objective = await session.get(DepartmentObjectiveRecord, body.department_objective_id)
        if objective is None or objective.tenant_id != tenant_id or objective.status != "active":
            raise HTTPException(404, "tenant_department_objective_not_found")
        relationship: StrategicRelationshipRecord | None = None
        if body.relationship_id:
            relationship = await session.get(StrategicRelationshipRecord, body.relationship_id)
            if (
                relationship is None
                or relationship.tenant_id != tenant_id
                or relationship.account_id != body.account_id
            ):
                raise HTTPException(404, "tenant_strategic_relationship_not_found")
        signal_records = (
            await session.execute(
                select(CommercialSignalRecord).where(
                    CommercialSignalRecord.tenant_id == tenant_id,
                    CommercialSignalRecord.account_id == body.account_id,
                    CommercialSignalRecord.id.in_(body.source_signal_ids),
                    CommercialSignalRecord.status == "active",
                )
            )
        ).scalars().all()
        if len(signal_records) != len(set(body.source_signal_ids)):
            raise HTTPException(422, "all_signals_must_belong_to_tenant_account")
        source_ids = {signal.source_id for signal in signal_records}
        source_records = (
            await session.execute(
                select(CommercialSourceRecord).where(
                    CommercialSourceRecord.tenant_id == tenant_id,
                    CommercialSourceRecord.id.in_(source_ids),
                    CommercialSourceRecord.active.is_(True),
                )
            )
        ).scalars().all()
        if len(source_records) != len(source_ids):
            raise HTTPException(422, "all_signals_require_active_tenant_sources")
        sources = [_source_domain(record) for record in source_records]
        source_quality = round(sum(score_source(source) for source in sources) / len(sources))
        signals = [_signal_domain(record) for record in signal_records]
        evidence_level = highest_evidence_level(signals)
        opportunity_score = score_opportunity(
            OpportunityInputs(
                strategic_fit=body.strategic_fit,
                problem_evidence=body.problem_evidence,
                urgency=body.urgency,
                relationship_strength=(
                    relationship.relationship_strength if relationship else 0
                ),
                commercial_value=body.commercial_value,
                evidence_level=evidence_level,
                source_score=source_quality,
                signal_count=len(signals),
            )
        )
        stage = (
            OpportunityStage.APPROVAL
            if opportunity_score.score >= 75
            and evidence_level
            in {
                EvidenceLevel.L3_FIRST_PARTY,
                EvidenceLevel.L4_VERIFIED,
                EvidenceLevel.L5_MEASURED_OUTCOME,
            }
            else OpportunityStage.QUALIFY
            if opportunity_score.score >= 50
            else OpportunityStage.RESEARCH
        )
        record = CommercialOpportunityRecord(
            id=f"opp_{uuid.uuid4().hex}",
            tenant_id=tenant_id,
            account_id=body.account_id.strip(),
            company_name=body.company_name.strip(),
            title=body.title.strip(),
            department_objective_id=objective.id,
            relationship_id=relationship.id if relationship else None,
            offer_id=body.offer_id,
            stage=stage.value,
            evidence_level=evidence_level.value,
            source_signal_ids_json=sorted(set(body.source_signal_ids)),
            score_components_json=opportunity_score.score_components,
            score=opportunity_score.score,
            confidence_band=opportunity_score.confidence_band,
            blockers_json=list(opportunity_score.blockers),
            next_action=body.next_action.strip(),
            proof_target=body.proof_target.strip(),
            approval_required=True,
            external_action_allowed=False,
            status="active",
        )
        session.add(record)
        session.add_all(
            CommercialOpportunitySignalRecord(
                opportunity_id=record.id,
                signal_id=signal.id,
                tenant_id=tenant_id,
            )
            for signal in signal_records
        )
        await _commit(session, conflict="commercial_opportunity_already_registered")
    return {
        "status": "created",
        "opportunity_id": record.id,
        "stage": record.stage,
        "score": record.score,
        "evidence_level": record.evidence_level,
        "blockers": record.blockers_json,
        "external_side_effect": False,
    }


@router.post("/opportunities/{opportunity_id}/finance-cases", status_code=201)
async def create_finance_case(
    opportunity_id: str,
    body: FinanceCaseBody,
    current_user: Any = Depends(require_sales_manager),
) -> dict[str, Any]:
    """Append an internal Dealix-economics case; never approve its own price."""
    tenant_id = _tenant_id(current_user)
    user_id = _user_id(current_user)
    async with async_session_factory()() as session:
        opportunity = await session.get(CommercialOpportunityRecord, opportunity_id)
        if (
            opportunity is None
            or opportunity.tenant_id != tenant_id
            or opportunity.status != "active"
        ):
            raise HTTPException(404, "tenant_commercial_opportunity_not_found")
        inputs = _build_finance_inputs(
            opportunity,
            body,
            pricing_status=FinancePricingStatus.DRAFT,
        )
        assessment = evaluate_commercial_finance(inputs)
        assessment_json = assessment.to_dict()
        record = CommercialFinanceCaseRecord(
            id=f"fin_{uuid.uuid4().hex}",
            tenant_id=tenant_id,
            opportunity_id=opportunity.id,
            parent_case_id=None,
            offer_id=opportunity.offer_id,
            offer_class=inputs.offer_class.value,
            pricing_status=FinancePricingStatus.DRAFT.value,
            decision=assessment.decision.value,
            currency=assessment.currency,
            proposed_price_sar=inputs.proposed_price_sar,
            gross_margin_pct=assessment.gross_margin_pct,
            contribution_margin_pct=assessment.contribution_margin_pct,
            readiness_score=assessment.readiness_score,
            approval_required=True,
            external_action_allowed=False,
            created_by_user_id=user_id,
            approved_by_user_id=None,
            approval_ref=None,
            approved_at=None,
            inputs_json=inputs.to_dict(),
            assessment_json=assessment_json,
        )
        session.add(record)
        _add_audit(
            session,
            tenant_id=tenant_id,
            user_id=user_id,
            action="commercial_finance.case.create",
            entity_id=record.id,
            diff={
                "opportunity_id": opportunity.id,
                "decision": assessment.decision.value,
                "pricing_status": FinancePricingStatus.DRAFT.value,
                "external_action_allowed": False,
            },
        )
        await _commit(session, conflict="commercial_finance_case_conflict")
    return {
        "status": "created",
        "finance_case": _finance_case_response(record),
        "external_side_effect": False,
    }


@router.get("/opportunities/{opportunity_id}/finance-cases")
async def list_finance_cases(
    opportunity_id: str,
    limit: int = Query(default=50, ge=1, le=200),
    current_user: Any = Depends(get_current_user),
) -> dict[str, Any]:
    tenant_id = _tenant_id(current_user)
    async with async_session_factory()() as session:
        opportunity = await session.get(CommercialOpportunityRecord, opportunity_id)
        if opportunity is None or opportunity.tenant_id != tenant_id:
            raise HTTPException(404, "tenant_commercial_opportunity_not_found")
        records = (
            await session.execute(
                select(CommercialFinanceCaseRecord)
                .where(
                    CommercialFinanceCaseRecord.tenant_id == tenant_id,
                    CommercialFinanceCaseRecord.opportunity_id == opportunity_id,
                )
                .order_by(
                    CommercialFinanceCaseRecord.created_at.desc(),
                    CommercialFinanceCaseRecord.id.desc(),
                )
                .limit(limit)
            )
        ).scalars().all()
    return {
        "count": len(records),
        "items": [_finance_case_response(record) for record in records],
        "external_action_allowed": False,
    }


@router.post(
    "/opportunities/{opportunity_id}/finance-cases/{case_id}/approve-price",
    status_code=201,
)
async def approve_finance_case_price(
    opportunity_id: str,
    case_id: str,
    body: PriceApprovalBody,
    current_user: Any = Depends(require_tenant_admin),
) -> dict[str, Any]:
    """Create an immutable approved child case after an exact-price check."""
    tenant_id = _tenant_id(current_user)
    user_id = _user_id(current_user)
    async with async_session_factory()() as session:
        opportunity = await session.get(CommercialOpportunityRecord, opportunity_id)
        if (
            opportunity is None
            or opportunity.tenant_id != tenant_id
            or opportunity.status != "active"
        ):
            raise HTTPException(404, "tenant_commercial_opportunity_not_found")
        source_case = await session.get(CommercialFinanceCaseRecord, case_id)
        if (
            source_case is None
            or source_case.tenant_id != tenant_id
            or source_case.opportunity_id != opportunity_id
        ):
            raise HTTPException(404, "tenant_commercial_finance_case_not_found")
        if (
            source_case.parent_case_id is not None
            or source_case.pricing_status != FinancePricingStatus.DRAFT.value
        ):
            raise HTTPException(409, "only_root_draft_finance_case_can_be_approved")
        if Decimal(str(source_case.proposed_price_sar)) != body.confirmed_proposed_price_sar:
            raise HTTPException(409, "confirmed_price_does_not_match_finance_case")
        if source_case.offer_id != opportunity.offer_id:
            raise HTTPException(409, "finance_case_offer_integrity_error")
        try:
            approved_inputs = CommercialFinanceInputs.from_dict(
                source_case.inputs_json,
                pricing_status=FinancePricingStatus.FOUNDER_APPROVED,
            )
            if (
                approved_inputs.opportunity_id != opportunity_id
                or approved_inputs.offer_id != opportunity.offer_id
            ):
                raise ValueError("finance case lineage does not match opportunity")
            assessment = evaluate_commercial_finance(approved_inputs)
        except (KeyError, TypeError, ValueError) as exc:
            raise HTTPException(409, "finance_case_inputs_corrupt") from exc
        if assessment.decision is not CommercialFinanceDecision.PURSUE:
            raise HTTPException(409, "finance_case_not_eligible_for_price_approval")

        approved_at = datetime.now(UTC)
        approval_ref = body.approval_ref.strip()
        record = CommercialFinanceCaseRecord(
            id=f"fin_{uuid.uuid4().hex}",
            tenant_id=tenant_id,
            opportunity_id=opportunity.id,
            parent_case_id=source_case.id,
            offer_id=opportunity.offer_id,
            offer_class=approved_inputs.offer_class.value,
            pricing_status=FinancePricingStatus.FOUNDER_APPROVED.value,
            decision=assessment.decision.value,
            currency=assessment.currency,
            proposed_price_sar=approved_inputs.proposed_price_sar,
            gross_margin_pct=assessment.gross_margin_pct,
            contribution_margin_pct=assessment.contribution_margin_pct,
            readiness_score=assessment.readiness_score,
            approval_required=True,
            external_action_allowed=False,
            created_by_user_id=user_id,
            approved_by_user_id=user_id,
            approval_ref=approval_ref,
            approved_at=approved_at,
            inputs_json=approved_inputs.to_dict(),
            assessment_json=assessment.to_dict(),
        )
        session.add(record)
        _add_audit(
            session,
            tenant_id=tenant_id,
            user_id=user_id,
            action="commercial_finance.price.approve",
            entity_id=record.id,
            diff={
                "parent_case_id": source_case.id,
                "approval_ref": approval_ref,
                "pricing_status": FinancePricingStatus.FOUNDER_APPROVED.value,
                "decision": assessment.decision.value,
                "external_action_allowed": False,
            },
        )
        await _commit(session, conflict="commercial_finance_price_approval_conflict")
    return {
        "status": "approved_record_created",
        "finance_case": _finance_case_response(record),
        "external_side_effect": False,
    }


@router.post("/opportunities/{opportunity_id}/buyer-decision-plan")
async def build_opportunity_buyer_decision_plan(
    opportunity_id: str,
    body: BuyerDecisionPlanBody,
    current_user: Any = Depends(get_current_user),
) -> dict[str, Any]:
    """Build an internal persuasion plan without price, send, or commitment."""
    tenant_id = _tenant_id(current_user)
    async with async_session_factory()() as session:
        opportunity = await session.get(CommercialOpportunityRecord, opportunity_id)
        if (
            opportunity is None
            or opportunity.tenant_id != tenant_id
            or opportunity.status != "active"
        ):
            raise HTTPException(404, "tenant_commercial_opportunity_not_found")
        objective = await session.get(
            DepartmentObjectiveRecord,
            opportunity.department_objective_id,
        )
        if objective is None or objective.tenant_id != tenant_id:
            raise HTTPException(409, "opportunity_objective_integrity_error")
        relationship = None
        if opportunity.relationship_id:
            relationship = await session.get(
                StrategicRelationshipRecord,
                opportunity.relationship_id,
            )
            if relationship is None or relationship.tenant_id != tenant_id:
                raise HTTPException(409, "opportunity_relationship_integrity_error")

        signal_records = (
            (
                await session.execute(
                    select(CommercialSignalRecord).where(
                        CommercialSignalRecord.tenant_id == tenant_id,
                        CommercialSignalRecord.id.in_(opportunity.source_signal_ids_json),
                        CommercialSignalRecord.status == "active",
                    )
                )
            )
            .scalars()
            .all()
        )
        source_ids = {record.source_id for record in signal_records}
        source_records = (
            (
                await session.execute(
                    select(CommercialSourceRecord).where(
                        CommercialSourceRecord.tenant_id == tenant_id,
                        CommercialSourceRecord.id.in_(source_ids),
                    )
                )
            )
            .scalars()
            .all()
        )
        source_policy = {
            record.id: (
                record.policy_status if record.active else SourcePolicyStatus.BLOCKED.value
            )
            for record in source_records
        }
        finance_records = (
            (
                await session.execute(
                    select(CommercialFinanceCaseRecord)
                    .where(
                        CommercialFinanceCaseRecord.tenant_id == tenant_id,
                        CommercialFinanceCaseRecord.opportunity_id == opportunity.id,
                    )
                    .order_by(
                        CommercialFinanceCaseRecord.created_at.desc(),
                        CommercialFinanceCaseRecord.id.desc(),
                    )
                    .limit(1)
                )
            )
            .scalars()
            .all()
        )
        latest_finance_case = finance_records[0] if finance_records else None

    evidence = tuple(
        PersuasionEvidence(
            claim=record.claim,
            signal_type=record.signal_type,
            evidence_ref=record.evidence_ref,
            evidence_level=EvidenceLevel(record.evidence_level),
            confidence=record.confidence,
            source_policy_status=SourcePolicyStatus(
                source_policy.get(record.source_id, SourcePolicyStatus.BLOCKED.value)
            ),
            publication_consent_ref=(
                str((record.payload_json or {}).get("publication_consent_ref"))
                if (record.payload_json or {}).get("publication_consent_ref")
                else None
            ),
            stale=bool(record.expires_at and record.expires_at <= datetime.now(UTC)),
        )
        for record in signal_records
    )
    current_signals = [
        _signal_domain(record)
        for record in signal_records
        if not record.expires_at or record.expires_at > datetime.now(UTC)
    ]
    context = BuyerDecisionContext(
        opportunity_id=opportunity.id,
        account_name=opportunity.company_name,
        opportunity_title=opportunity.title,
        offer_id=opportunity.offer_id,
        objective=objective.objective,
        metric=objective.metric,
        proof_target=opportunity.proof_target,
        evidence_level=highest_evidence_level(current_signals),
        opportunity_score=opportunity.score,
        evidence=evidence,
        buyer_roles=tuple(dict.fromkeys(body.buyer_roles)) or DEFAULT_BUYER_ROLES,
        known_objections=tuple(
            objection.strip() for objection in body.known_objections if objection.strip()
        ),
        relationship_permission_state=(
            relationship.permission_state if relationship else "research_only"
        ),
        pricing_decision=(
            PricingDecision.FOUNDER_APPROVED
            if latest_finance_case is not None
            and getattr(latest_finance_case, "pricing_status", None)
            == FinancePricingStatus.FOUNDER_APPROVED.value
            and getattr(latest_finance_case, "decision", None)
            == CommercialFinanceDecision.PURSUE.value
            else PricingDecision.CATALOG_RECONCILIATION_REQUIRED
        ),
        requested_discount_pct=body.requested_discount_pct,
        non_standard_terms_requested=body.non_standard_terms_requested,
    )
    return build_buyer_decision_plan(context).to_dict()


@router.get("/snapshot")
async def snapshot(current_user: Any = Depends(get_current_user)) -> dict[str, Any]:
    tenant_id = _tenant_id(current_user)
    models = (
        CommercialSourceRecord,
        CommercialSignalRecord,
        DepartmentObjectiveRecord,
        StrategicRelationshipRecord,
        CommercialOpportunityRecord,
        CommercialOpportunitySignalRecord,
        CommercialFinanceCaseRecord,
    )
    async with async_session_factory()() as session:
        try:
            counts = [
                int(
                    await session.scalar(
                        select(func.count()).select_from(model).where(model.tenant_id == tenant_id)
                    )
                    or 0
                )
                for model in models
            ]
            high_priority = int(
                await session.scalar(
                    select(func.count()).select_from(CommercialOpportunityRecord).where(
                        CommercialOpportunityRecord.tenant_id == tenant_id,
                        CommercialOpportunityRecord.status == "active",
                        CommercialOpportunityRecord.score >= 75,
                    )
                )
                or 0
            )
            ranked_finance_cases = (
                select(
                    CommercialFinanceCaseRecord.opportunity_id.label("opportunity_id"),
                    CommercialFinanceCaseRecord.decision.label("decision"),
                    CommercialFinanceCaseRecord.pricing_status.label("pricing_status"),
                    func.row_number()
                    .over(
                        partition_by=CommercialFinanceCaseRecord.opportunity_id,
                        order_by=(
                            CommercialFinanceCaseRecord.created_at.desc(),
                            CommercialFinanceCaseRecord.id.desc(),
                        ),
                    )
                    .label("row_number"),
                )
                .where(CommercialFinanceCaseRecord.tenant_id == tenant_id)
                .subquery()
            )
            finance_summary = (
                await session.execute(
                    select(
                        func.count().label("latest_cases"),
                        func.count()
                        .filter(
                            ranked_finance_cases.c.decision
                            == CommercialFinanceDecision.PURSUE.value
                        )
                        .label("pursue_cases"),
                        func.count()
                        .filter(
                            ranked_finance_cases.c.pricing_status
                            == FinancePricingStatus.FOUNDER_APPROVED.value
                        )
                        .label("approved_price_cases"),
                    )
                    .select_from(ranked_finance_cases)
                    .where(ranked_finance_cases.c.row_number == 1)
                )
            ).one()
        except Exception as exc:
            raise HTTPException(503, "commercial_intelligence_database_unreachable") from exc
    return {
        "status": "ok",
        "tenant_id": tenant_id,
        "counts": dict(
            zip(
                (
                    "sources",
                    "signals",
                    "objectives",
                    "relationships",
                    "opportunities",
                    "opportunity_signal_edges",
                    "finance_cases",
                ),
                counts,
            )
        ),
        "high_priority_opportunities": high_priority,
        "finance_latest": {
            "cases": int(finance_summary.latest_cases or 0),
            "pursue": int(finance_summary.pursue_cases or 0),
            "price_approved": int(finance_summary.approved_price_cases or 0),
            "latest_case_only": True,
        },
        "external_action_allowed": False,
    }


@router.get("/sources")
async def list_sources(
    limit: int = Query(default=100, ge=1, le=500),
    current_user: Any = Depends(get_current_user),
) -> dict[str, Any]:
    tenant_id = _tenant_id(current_user)
    async with async_session_factory()() as session:
        records = (
            await session.execute(
                select(CommercialSourceRecord)
                .where(CommercialSourceRecord.tenant_id == tenant_id)
                .order_by(CommercialSourceRecord.active.desc(), CommercialSourceRecord.name)
                .limit(limit)
            )
        ).scalars().all()
    return {
        "count": len(records),
        "items": [
            {
                "id": record.id,
                "name": record.name,
                "kind": record.kind,
                "source_url": record.source_url,
                "policy_status": record.policy_status,
                "allowed_use": record.allowed_use,
                "source_score": score_source(_source_domain(record)),
                "freshness_days": record.freshness_days,
                "retention_days": record.retention_days,
                "active": record.active,
            }
            for record in records
        ],
    }


@router.get("/source-scorecards")
async def source_scorecards(
    current_user: Any = Depends(get_current_user),
) -> dict[str, Any]:
    tenant_id = _tenant_id(current_user)
    now = datetime.now(UTC)
    async with async_session_factory()() as session:
        sources = (
            await session.execute(
                select(CommercialSourceRecord).where(
                    CommercialSourceRecord.tenant_id == tenant_id,
                    CommercialSourceRecord.active.is_(True),
                )
            )
        ).scalars().all()
        signals = (
            await session.execute(
                select(CommercialSignalRecord).where(
                    CommercialSignalRecord.tenant_id == tenant_id,
                    CommercialSignalRecord.status == "active",
                )
            )
        ).scalars().all()
    signal_domains = [_signal_domain(record) for record in signals]
    items = []
    for source in sources:
        source_signals = [signal for signal in signal_domains if signal.source_id == source.id]
        items.append(
            {
                "source_id": source.id,
                "name": source.name,
                "policy_status": source.policy_status,
                "source_score": score_source(_source_domain(source), now=now),
                "signals": len(source_signals),
                "stale_signals": sum(signal.is_stale(now=now) for signal in source_signals),
                "average_signal_confidence": (
                    round(sum(signal.confidence for signal in source_signals) / len(source_signals))
                    if source_signals
                    else 0
                ),
            }
        )
    return {"count": len(items), "items": sorted(items, key=lambda item: -item["source_score"])}


@router.get("/objectives")
async def list_objectives(
    current_user: Any = Depends(get_current_user),
) -> dict[str, Any]:
    tenant_id = _tenant_id(current_user)
    async with async_session_factory()() as session:
        records = (
            await session.execute(
                select(DepartmentObjectiveRecord)
                .where(DepartmentObjectiveRecord.tenant_id == tenant_id)
                .order_by(DepartmentObjectiveRecord.priority.desc())
            )
        ).scalars().all()
    return {
        "count": len(records),
        "items": [
            {
                "id": item.id,
                "department": item.department,
                "objective": item.objective,
                "metric": item.metric,
                "target_value": item.target_value,
                "target_unit": item.target_unit,
                "horizon": item.horizon,
                "priority": item.priority,
                "status": item.status,
                "evidence_required": item.evidence_required,
                "owner_role": item.owner_role,
            }
            for item in records
        ],
    }


@router.get("/relationships")
async def list_relationships(
    limit: int = Query(default=100, ge=1, le=500),
    current_user: Any = Depends(get_current_user),
) -> dict[str, Any]:
    tenant_id = _tenant_id(current_user)
    async with async_session_factory()() as session:
        records = (
            await session.execute(
                select(StrategicRelationshipRecord)
                .where(StrategicRelationshipRecord.tenant_id == tenant_id)
                .order_by(StrategicRelationshipRecord.relationship_strength.desc())
                .limit(limit)
            )
        ).scalars().all()
    return {
        "count": len(records),
        "items": [
            {
                "id": item.id,
                "account_id": item.account_id,
                "company_name": item.company_name,
                "relationship_type": item.relationship_type,
                "stage": item.stage,
                "permission_state": item.permission_state,
                "mutual_value": item.mutual_value,
                "relationship_strength": item.relationship_strength,
                "owner_role": item.owner_role,
                "next_review_at": item.next_review_at,
            }
            for item in records
        ],
    }


@router.get("/opportunities")
async def list_opportunities(
    stage: OpportunityStage | None = None,
    department_objective_id: str | None = None,
    limit: int = Query(default=100, ge=1, le=500),
    current_user: Any = Depends(get_current_user),
) -> dict[str, Any]:
    tenant_id = _tenant_id(current_user)
    async with async_session_factory()() as session:
        query = select(CommercialOpportunityRecord).where(
            CommercialOpportunityRecord.tenant_id == tenant_id,
            CommercialOpportunityRecord.status == "active",
        )
        if stage:
            query = query.where(CommercialOpportunityRecord.stage == stage.value)
        if department_objective_id:
            query = query.where(
                CommercialOpportunityRecord.department_objective_id == department_objective_id
            )
        records = (
            await session.execute(
                query.order_by(CommercialOpportunityRecord.score.desc()).limit(limit)
            )
        ).scalars().all()
        opportunity_ids = [record.id for record in records]
        latest_finance_by_opportunity: dict[str, CommercialFinanceCaseRecord] = {}
        if opportunity_ids:
            ranked_finance_ids = (
                select(
                    CommercialFinanceCaseRecord.id.label("case_id"),
                    CommercialFinanceCaseRecord.opportunity_id.label("opportunity_id"),
                    func.row_number()
                    .over(
                        partition_by=CommercialFinanceCaseRecord.opportunity_id,
                        order_by=(
                            CommercialFinanceCaseRecord.created_at.desc(),
                            CommercialFinanceCaseRecord.id.desc(),
                        ),
                    )
                    .label("row_number"),
                )
                .where(
                    CommercialFinanceCaseRecord.tenant_id == tenant_id,
                    CommercialFinanceCaseRecord.opportunity_id.in_(opportunity_ids),
                )
                .subquery()
            )
            latest_finance_records = (
                await session.execute(
                    select(CommercialFinanceCaseRecord)
                    .join(
                        ranked_finance_ids,
                        ranked_finance_ids.c.case_id == CommercialFinanceCaseRecord.id,
                    )
                    .where(ranked_finance_ids.c.row_number == 1)
                )
            ).scalars().all()
            latest_finance_by_opportunity = {
                record.opportunity_id: record for record in latest_finance_records
            }
    return {
        "count": len(records),
        "items": [
            {
                "id": item.id,
                "account_id": item.account_id,
                "company_name": item.company_name,
                "title": item.title,
                "department_objective_id": item.department_objective_id,
                "relationship_id": item.relationship_id,
                "offer_id": item.offer_id,
                "stage": item.stage,
                "evidence_level": item.evidence_level,
                "score": item.score,
                "confidence_band": item.confidence_band,
                "blockers": item.blockers_json,
                "next_action": item.next_action,
                "proof_target": item.proof_target,
                "approval_required": item.approval_required,
                "latest_finance_case": (
                    _finance_case_response(latest_finance_by_opportunity[item.id])
                    if item.id in latest_finance_by_opportunity
                    else None
                ),
                "external_action_allowed": False,
            }
            for item in records
        ],
    }


@router.get("/graph")
async def opportunity_graph(
    limit: int = Query(default=100, ge=1, le=500),
    current_user: Any = Depends(get_current_user),
) -> dict[str, Any]:
    tenant_id = _tenant_id(current_user)
    async with async_session_factory()() as session:
        objectives = (
            await session.execute(
                select(DepartmentObjectiveRecord).where(
                    DepartmentObjectiveRecord.tenant_id == tenant_id,
                    DepartmentObjectiveRecord.status == "active",
                )
            )
        ).scalars().all()
        relationships = (
            await session.execute(
                select(StrategicRelationshipRecord)
                .where(StrategicRelationshipRecord.tenant_id == tenant_id)
                .limit(limit)
            )
        ).scalars().all()
        opportunities = (
            await session.execute(
                select(CommercialOpportunityRecord)
                .where(
                    CommercialOpportunityRecord.tenant_id == tenant_id,
                    CommercialOpportunityRecord.status == "active",
                )
                .order_by(CommercialOpportunityRecord.score.desc())
                .limit(limit)
            )
        ).scalars().all()
        opportunity_ids = [item.id for item in opportunities]
        signal_edges = (
            await session.execute(
                select(CommercialOpportunitySignalRecord).where(
                    CommercialOpportunitySignalRecord.tenant_id == tenant_id,
                    CommercialOpportunitySignalRecord.opportunity_id.in_(opportunity_ids),
                )
            )
        ).scalars().all()
        signal_ids = {edge.signal_id for edge in signal_edges}
        signals = (
            await session.execute(
                select(CommercialSignalRecord).where(
                    CommercialSignalRecord.tenant_id == tenant_id,
                    CommercialSignalRecord.id.in_(signal_ids),
                )
            )
        ).scalars().all()
    nodes = [
        {"id": item.id, "type": "objective", "label": item.department, "detail": item.objective}
        for item in objectives
    ]
    nodes.extend(
        {
            "id": item.id,
            "type": "signal",
            "label": item.signal_type,
            "detail": item.claim,
            "evidence_level": item.evidence_level,
        }
        for item in signals
    )
    nodes.extend(
        {
            "id": item.id,
            "type": "relationship",
            "label": item.company_name,
            "detail": item.relationship_type,
        }
        for item in relationships
    )
    nodes.extend(
        {
            "id": item.id,
            "type": "opportunity",
            "label": item.title,
            "detail": item.stage,
            "score": item.score,
        }
        for item in opportunities
    )
    edges = []
    for item in opportunities:
        edges.append({"from": item.department_objective_id, "to": item.id, "type": "drives"})
        if item.relationship_id:
            edges.append({"from": item.relationship_id, "to": item.id, "type": "enables"})
    edges.extend(
        {"from": item.signal_id, "to": item.opportunity_id, "type": "evidences"}
        for item in signal_edges
    )
    return {
        "tenant_id": tenant_id,
        "nodes": nodes,
        "edges": edges,
        "external_action_allowed": False,
    }


__all__ = ["router"]
