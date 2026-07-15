"""Company targeting, agent capability evaluation, and negotiation planning APIs."""
from __future__ import annotations

import hashlib
import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import delete, func, select

from api.security.auth_deps import get_current_user
from db.models_company_targeting import (
    AgentCapabilityEvaluationRecord,
    CommercialCampaignItemRecord,
    CommercialCampaignPlanRecord,
    CompanyDirectoryEntryRecord,
)
from db.session import async_session_factory
from dealix.company_os.capability_evaluation import (
    benchmark_scenarios,
    evaluate_employee_output,
)
from dealix.company_os.campaign_planner import (
    ContactPermission,
    build_campaign_plan,
)
from dealix.company_os.company_directory import DirectoryCandidate
from dealix.company_os.negotiation_engine import (
    NegotiationContext,
    build_negotiation_plan,
)

router = APIRouter(prefix="/api/v1/company-targeting", tags=["Sales"])


class EvaluateCapabilityBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    capability: str = Field(default="commercial_generalist", max_length=64)
    output: dict[str, Any]


class PersistCapabilityEvaluationBody(EvaluateCapabilityBody):
    agent_name: str = Field(min_length=1, max_length=64)
    scenario_id: str = Field(min_length=1, max_length=128)
    run_id: str | None = Field(default=None, max_length=64)
    model_name: str | None = Field(default=None, max_length=128)
    prompt_version: str | None = Field(default=None, max_length=64)


class NegotiationBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    account_name: str = Field(min_length=1, max_length=255)
    offer_id: str = Field(min_length=1, max_length=64)
    customer_problem: str = Field(min_length=1, max_length=2_000)
    customer_priorities: list[str] = Field(default_factory=list, max_length=20)
    known_objections: list[str] = Field(default_factory=list, max_length=20)
    list_price_sar: float | None = Field(default=None, ge=0)
    approved_floor_sar: float | None = Field(default=None, ge=0)
    max_discount_without_approval_pct: float = Field(default=0, ge=0, le=100)
    requested_discount_pct: float = Field(default=0, ge=0, le=100)
    non_standard_terms_requested: bool = False
    evidence_refs: list[str] = Field(default_factory=list, max_length=100)


class PermissionBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    relationship_status: str = "unknown"
    channel: str = "research_only"
    consent_status: str = "unknown"
    opt_out: bool = False
    evidence_id: str | None = None


class CampaignPreviewBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    campaign_name: str = Field(default="controlled_research_cohort", max_length=255)
    offer_id: str | None = Field(default=None, max_length=64)
    experiment_hypothesis: str = Field(
        default="اختبار ملاءمة المشكلة والعرض قبل أي إرسال خارجي.",
        max_length=2_000,
    )
    success_metric: str = Field(default="approved_draft_rate", max_length=128)
    candidate_ids: list[str] = Field(default_factory=list, max_length=100)
    permissions: dict[str, PermissionBody] = Field(default_factory=dict)
    max_items: int = Field(default=25, ge=1, le=100)


def _to_candidate(record: CompanyDirectoryEntryRecord) -> DirectoryCandidate:
    return DirectoryCandidate(
        id=record.id.removeprefix(f"{record.tenant_id}_"),
        company_name=record.company_name,
        normalized_name=record.normalized_name,
        city=record.city or "",
        activity=record.activity or "",
        has_valid_email=record.has_valid_email,
        has_valid_phone=record.has_valid_phone,
        email_masked=record.email_masked,
        phone_masked=record.phone_masked,
        email_hmac=record.email_hmac,
        phone_hmac=record.phone_hmac,
        source_sheet=record.source_sheet,
        source_row_number=record.source_row_number,
        source_fingerprint=record.source_fingerprint,
        data_quality_score=record.data_quality_score,
        fit_score=record.fit_score,
        research_priority_score=record.research_priority_score,
        priority=record.priority,
        recommended_offer_id=record.recommended_offer_id,
        value_angle_ar=record.value_angle_ar,
        relationship_status=record.relationship_status,
        consent_status=record.consent_status,
        targeting_status=record.targeting_status,
        suppression_reasons=tuple(record.suppression_reasons_json or []),
    )


def _authenticated_tenant_id(current_user: Any) -> str:
    tenant_id = getattr(current_user, "tenant_id", None)
    if not tenant_id:
        raise HTTPException(403, "authenticated_tenant_required")
    return str(tenant_id)


@router.get("/status")
async def targeting_status() -> dict[str, Any]:
    return {
        "status": "operational",
        "database": "persistent_staging",
        "raw_directory_contacts_stored": False,
        "external_send": False,
        "capability_eval_gate": "score>=85_and_no_critical_failures",
        "campaign_mode": "draft_only",
    }


@router.get("/capability-benchmark")
async def capability_benchmark() -> dict[str, Any]:
    scenarios = benchmark_scenarios()
    return {"count": len(scenarios), "scenarios": scenarios}


@router.post("/evaluate-capability")
async def evaluate_capability(body: EvaluateCapabilityBody) -> dict[str, Any]:
    evaluation = evaluate_employee_output(body.output, capability=body.capability)
    return {
        "evaluation": evaluation.to_dict(),
        "production_eligible": evaluation.passed,
    }


@router.post("/evaluation-runs")
async def persist_capability_evaluation(
    body: PersistCapabilityEvaluationBody,
    current_user: Any = Depends(get_current_user),
) -> dict[str, Any]:
    tenant_id = _authenticated_tenant_id(current_user)
    evaluation = evaluate_employee_output(body.output, capability=body.capability)
    record_id = f"ace_{uuid.uuid4().hex}"
    run_id = body.run_id or f"run_{uuid.uuid4().hex[:24]}"
    record = AgentCapabilityEvaluationRecord(
        id=record_id,
        tenant_id=tenant_id,
        run_id=run_id,
        agent_name=body.agent_name,
        capability=body.capability,
        scenario_id=body.scenario_id,
        evaluator_version=evaluation.evaluator_version,
        model_name=body.model_name,
        prompt_version=body.prompt_version,
        dimension_scores_json=evaluation.dimension_scores,
        total_score=evaluation.total_score,
        passed=evaluation.passed,
        critical_failures_json=list(evaluation.critical_failures),
        evidence_json=list(body.output.get("source_refs") or []),
    )
    async with async_session_factory()() as session:
        try:
            session.add(record)
            await session.commit()
        except Exception as exc:
            await session.rollback()
            raise HTTPException(503, "capability_evaluation_not_persisted") from exc
    return {
        "status": "recorded",
        "record_id": record_id,
        "run_id": run_id,
        "evaluation": evaluation.to_dict(),
        "production_eligible": evaluation.passed,
    }


@router.post("/negotiate")
async def negotiate(body: NegotiationBody) -> dict[str, Any]:
    if (
        body.list_price_sar is not None
        and body.approved_floor_sar is not None
        and body.approved_floor_sar > body.list_price_sar
    ):
        raise HTTPException(400, "approved_floor_cannot_exceed_list_price")
    plan = build_negotiation_plan(
        NegotiationContext(
            account_name=body.account_name,
            offer_id=body.offer_id,
            customer_problem=body.customer_problem,
            customer_priorities=tuple(body.customer_priorities),
            known_objections=tuple(body.known_objections),
            list_price_sar=body.list_price_sar,
            approved_floor_sar=body.approved_floor_sar,
            max_discount_without_approval_pct=body.max_discount_without_approval_pct,
            requested_discount_pct=body.requested_discount_pct,
            non_standard_terms_requested=body.non_standard_terms_requested,
            evidence_refs=tuple(body.evidence_refs),
        )
    )
    return {
        "mode": "advisory_draft",
        "external_commitment": False,
        "plan": plan.to_dict(),
    }


@router.get("/summary")
async def directory_summary(
    current_user: Any = Depends(get_current_user),
) -> dict[str, Any]:
    tenant_id = _authenticated_tenant_id(current_user)
    async with async_session_factory()() as session:
        try:
            total = await session.scalar(
                select(func.count()).select_from(CompanyDirectoryEntryRecord).where(
                    CompanyDirectoryEntryRecord.tenant_id == tenant_id
                )
            )
            ready = await session.scalar(
                select(func.count()).select_from(CompanyDirectoryEntryRecord).where(
                    CompanyDirectoryEntryRecord.tenant_id == tenant_id,
                    CompanyDirectoryEntryRecord.targeting_status == "ready_to_draft",
                )
            )
        except Exception as exc:
            return {
                "status": "database_unreachable",
                "tenant_id": tenant_id,
                "error_type": type(exc).__name__,
            }
    return {
        "status": "ok",
        "tenant_id": tenant_id,
        "total_companies": int(total or 0),
        "ready_to_draft": int(ready or 0),
        "research_only": int(total or 0) - int(ready or 0),
    }


@router.get("/candidates")
async def list_target_candidates(
    city: str | None = None,
    offer_id: str | None = None,
    limit: int = Query(default=50, ge=1, le=500),
    current_user: Any = Depends(get_current_user),
) -> dict[str, Any]:
    tenant_id = _authenticated_tenant_id(current_user)
    async with async_session_factory()() as session:
        try:
            query = select(CompanyDirectoryEntryRecord).where(
                CompanyDirectoryEntryRecord.tenant_id == tenant_id
            )
            if city:
                query = query.where(CompanyDirectoryEntryRecord.city == city)
            if offer_id:
                query = query.where(
                    CompanyDirectoryEntryRecord.recommended_offer_id == offer_id
                )
            query = query.order_by(
                CompanyDirectoryEntryRecord.research_priority_score.desc()
            ).limit(limit)
            records = (await session.execute(query)).scalars().all()
        except Exception as exc:
            return {
                "status": "database_unreachable",
                "tenant_id": tenant_id,
                "error_type": type(exc).__name__,
                "items": [],
            }
    return {
        "status": "ok",
        "count": len(records),
        "items": [
            {
                "id": record.id,
                "company_name": record.company_name,
                "city": record.city,
                "activity": record.activity,
                "priority": record.priority,
                "research_priority_score": record.research_priority_score,
                "recommended_offer_id": record.recommended_offer_id,
                "value_angle_ar": record.value_angle_ar,
                "targeting_status": record.targeting_status,
                "suppression_reasons": record.suppression_reasons_json,
                "has_valid_email": record.has_valid_email,
                "has_valid_phone": record.has_valid_phone,
            }
            for record in records
        ],
    }


@router.post("/campaign/preview")
async def preview_campaign(
    body: CampaignPreviewBody,
    current_user: Any = Depends(get_current_user),
) -> dict[str, Any]:
    tenant_id = _authenticated_tenant_id(current_user)
    async with async_session_factory()() as session:
        try:
            query = select(CompanyDirectoryEntryRecord).where(
                CompanyDirectoryEntryRecord.tenant_id == tenant_id
            )
            if body.candidate_ids:
                query = query.where(
                    CompanyDirectoryEntryRecord.id.in_(body.candidate_ids)
                )
            if body.offer_id:
                query = query.where(
                    CompanyDirectoryEntryRecord.recommended_offer_id == body.offer_id
                )
            query = query.order_by(
                CompanyDirectoryEntryRecord.research_priority_score.desc()
            ).limit(body.max_items)
            records = (await session.execute(query)).scalars().all()
        except Exception as exc:
            return {
                "status": "database_unreachable",
                "external_side_effect": False,
                "error_type": type(exc).__name__,
            }
    permissions = {
        candidate_id.removeprefix(f"{tenant_id}_"): ContactPermission(
            relationship_status=value.relationship_status,
            channel=value.channel,
            consent_status=value.consent_status,
            opt_out=value.opt_out,
            evidence_id=value.evidence_id,
        )
        for candidate_id, value in body.permissions.items()
    }
    candidates = [_to_candidate(record) for record in records]
    plan = build_campaign_plan(
        candidates,
        permissions=permissions,
        max_items=body.max_items,
    )
    if not plan.items:
        raise HTTPException(404, "no_candidates_for_campaign_preview")
    plan_record_id = "ccp_" + hashlib.sha256(
        f"{tenant_id}|{plan.id}".encode("utf-8")
    ).hexdigest()[:32]
    directory_ids = {
        candidate.id: record.id for candidate, record in zip(candidates, records)
    }
    async with async_session_factory()() as session:
        try:
            plan_record = await session.get(
                CommercialCampaignPlanRecord,
                plan_record_id,
            )
            plan_values = {
                "tenant_id": tenant_id,
                "name": body.campaign_name,
                "offer_id": body.offer_id or "mixed_research_offers",
                "mode": plan.mode,
                "status": "planned",
                "segment_filter_json": {
                    "candidate_ids": body.candidate_ids,
                    "offer_id": body.offer_id,
                },
                "audience_count": plan.audience_count,
                "experiment_hypothesis": body.experiment_hypothesis,
                "success_metric": body.success_metric,
                "guardrails_json": list(plan.guardrails),
                "approval_id": None,
            }
            if plan_record is None:
                session.add(
                    CommercialCampaignPlanRecord(
                        id=plan_record_id,
                        **plan_values,
                    )
                )
            else:
                for key, value in plan_values.items():
                    setattr(plan_record, key, value)
            await session.execute(
                delete(CommercialCampaignItemRecord).where(
                    CommercialCampaignItemRecord.campaign_id == plan_record_id
                )
            )
            for item in plan.items:
                item_id = "cci_" + hashlib.sha256(
                    f"{tenant_id}|{item.id}".encode("utf-8")
                ).hexdigest()[:32]
                session.add(
                    CommercialCampaignItemRecord(
                        id=item_id,
                        tenant_id=tenant_id,
                        campaign_id=plan_record_id,
                        directory_entry_id=directory_ids[item.company_id],
                        channel=item.channel,
                        status=item.status,
                        qualification_json={
                            "questions_ar": list(item.qualification_questions_ar)
                        },
                        value_case_json={
                            "offer_id": item.offer_id,
                            "value_angle_ar": item.value_angle_ar,
                        },
                        objections_json=[],
                        negotiation_policy_json={
                            "approval_required": item.approval_required,
                            "external_action_permitted": False,
                        },
                        draft_json={
                            "preview_ar": item.draft_preview_ar,
                            "why_now": item.why_now,
                            "blockers": list(item.blockers),
                        },
                    )
                )
            await session.commit()
        except Exception as exc:
            await session.rollback()
            raise HTTPException(503, "campaign_preview_not_persisted") from exc
    return {
        "status": "planned",
        "external_side_effect": False,
        "campaign_record_id": plan_record_id,
        "plan": plan.to_dict(),
    }
