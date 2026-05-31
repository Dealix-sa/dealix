"""Trust plane router — registries, checks, evidence, audit."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from api.routers.hermes._dependencies import get_hermes
from dealix.hermes.orchestrator import HermesOrchestrator
from dealix.hermes.trust.agent_registry import AgentCard
from dealix.hermes.trust.evidence import EvidenceItem, EvidencePack
from dealix.hermes.trust.tool_registry import ToolCard


router = APIRouter(prefix="/api/v1/hermes/trust", tags=["hermes-trust"])


@router.post("/agents/register")
def register_agent(card: AgentCard, orch: HermesOrchestrator = Depends(get_hermes)):
    return orch.agent_registry.register(card)


@router.get("/agents")
def list_agents(orch: HermesOrchestrator = Depends(get_hermes)):
    return orch.agent_registry.list()


@router.post("/tools/register")
def register_tool(card: ToolCard, orch: HermesOrchestrator = Depends(get_hermes)):
    return orch.tool_registry.register(card)


@router.get("/tools")
def list_tools(orch: HermesOrchestrator = Depends(get_hermes)):
    return orch.tool_registry.list()


class TrustCheckRequest(BaseModel):
    agent_id: str
    proposed_text: str = ""
    context: dict = Field(default_factory=dict)


@router.post("/check")
def trust_check(body: TrustCheckRequest, orch: HermesOrchestrator = Depends(get_hermes)):
    result = orch.trust_check.check(
        agent_id=body.agent_id,
        proposed_text=body.proposed_text,
        context=body.context,
    )
    return {
        "passed": result.passed,
        "blocking_reasons": list(result.reasons),
        "policy_verdict": result.policy_evaluation.verdict.value if result.policy_evaluation else None,
    }


class EvidencePackRequest(BaseModel):
    subject_id: str
    subject_type: str
    items: list[EvidenceItem]
    model_used: str = "unspecified"
    bilingual_memo_ar: str = ""
    bilingual_memo_en: str = ""


@router.post("/evidence-pack")
def create_evidence_pack(body: EvidencePackRequest, orch: HermesOrchestrator = Depends(get_hermes)):
    pack = EvidencePack(
        subject_id=body.subject_id,
        subject_type=body.subject_type,
        items=body.items,
        model_used=body.model_used,
        bilingual_memo_ar=body.bilingual_memo_ar,
        bilingual_memo_en=body.bilingual_memo_en,
    )
    return orch.evidence_packs.save(pack)


@router.get("/audit")
def audit(actor: str | None = None, subject_id: str | None = None, orch: HermesOrchestrator = Depends(get_hermes)):
    return orch.audit_log.search(actor=actor, subject_id=subject_id)


@router.get("/risks")
def risks(orch: HermesOrchestrator = Depends(get_hermes)):
    return orch.risk_register.open_risks()


@router.get("/incidents")
def incidents(orch: HermesOrchestrator = Depends(get_hermes)):
    return orch.incident_register.open_incidents()


class MCPReviewRequest(BaseModel):
    manifest: dict
    descriptors: list[dict] = Field(default_factory=list)


@router.post("/mcp-review")
def mcp_review(body: MCPReviewRequest):
    from dealix.hermes.mcp.descriptor_scan import scan_tool_descriptor
    from dealix.hermes.mcp.manifest_review import review_manifest

    manifest_result = review_manifest(body.manifest)
    descriptor_results = [scan_tool_descriptor(d) for d in body.descriptors]
    return {
        "manifest_passed": manifest_result.passed,
        "manifest_reasons": list(manifest_result.reasons),
        "manifest_hash": manifest_result.manifest_hash,
        "descriptor_findings": [list(d.findings) for d in descriptor_results],
        "all_passed": manifest_result.passed and all(d.passed for d in descriptor_results),
    }
