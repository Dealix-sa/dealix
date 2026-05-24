"""AI Stack orchestrator — sequence L1..L11 with evidence + governance.

The orchestrator is a deterministic function: given an :class:`AIStackInput`,
it walks each layer in declared order, captures evidence, and returns a
single :class:`AIStackResult`. Short-circuits on hard governance blocks and
doctrine violations.

The orchestrator NEVER:

* Sends external messages (no WhatsApp, no LinkedIn, no Gmail).
* Records a billing event (capital_os will only persist on
  ``invoice_paid`` signal — handled outside the stack).
* Mutates ``model_router`` weights or ``agent_mesh`` registry — only
  approved proposals from the self-evolving repo can do that.

These guarantees match the eleven non-negotiables in
``dealix/commercial_ops/doctrine.py``.
"""

from __future__ import annotations

import threading
import time
import uuid
from collections.abc import Mapping
from datetime import UTC, datetime, timezone
from typing import Any

from auto_client_acquisition.agent_os.agent_card import AgentCard, AgentStatus, new_card
from auto_client_acquisition.agent_os.agent_mesh import AgentMesh, MeshTrace
from auto_client_acquisition.agent_os.autonomy_levels import AutonomyLevel
from auto_client_acquisition.agent_os.task_router import (
    AGENT_ICP,
    AGENT_PAIN,
    AGENT_PROPOSAL,
    AGENT_QUALIFICATION,
    AGENT_RETAINER_RECOMMEND,
    AGENT_SECTOR_INTEL,
    plan_for_offer,
)
from auto_client_acquisition.ai.model_router import ModelTask, get_model_route
from auto_client_acquisition.ai_stack_os.schemas import (
    AIStackInput,
    AIStackResult,
    LayerResult,
    LayerStatus,
    Offer,
)
from auto_client_acquisition.data_os.data_quality_score import account_row_completeness
from auto_client_acquisition.data_os.source_passport import validate as validate_passport
from auto_client_acquisition.governance_os.runtime_decision import decide as governance_decide
from auto_client_acquisition.intelligence_os.embedder import Embedder
from auto_client_acquisition.intelligence_os.rag_pipeline import RAGPipeline
from auto_client_acquisition.intelligence_os.vector_store import InMemoryVectorStore
from auto_client_acquisition.proof_os.decision_passport import (
    Confidence,
    DecisionPassport,
    Reversibility,
    Sensitivity,
    issue_passport,
)
from auto_client_acquisition.proof_os.evidence_chain import EvidenceChain, new_chain
from auto_client_acquisition.proof_os.proof_pack import (
    ProofPackV2,
    new_proof_pack,
    render_markdown,
)
from auto_client_acquisition.proof_os.proof_score import composite_proof_score
from auto_client_acquisition.self_evolving_os.feedback_ingestion import (
    OutcomeKind,
    from_doctrine_violation,
    from_governance_block,
    make_feedback_event,
)
from auto_client_acquisition.self_evolving_os.learning_store import (
    InMemoryLearningStore,
    record_feedback,
)
from auto_client_acquisition.sovereignty_os.source_passport_standard import (
    SourcePassport,
    source_passport_valid_for_ai,
)

# Doctrine sentinel phrases that should never reach a customer-facing artifact.
# The orchestrator scans the assembled proof pack body for these and blocks if
# any appear — a redundant safety net under governance_os.
_DOCTRINE_VIOLATION_TOKENS: tuple[str, ...] = (
    "100% guaranteed",
    "100٪ مضمون",
    "نضمن نتائج",
    "نضمن مبيعات",
    "guaranteed revenue",
    "guaranteed sales",
)


def _now() -> datetime:
    return datetime.now(UTC)


def _now_iso() -> str:
    return _now().isoformat()


def _coerce_passport(input_passport: Any) -> SourcePassport:
    """Convert the Pydantic passport into the canonical institutional record."""
    return SourcePassport(
        source_id=input_passport.source_id,
        source_type=input_passport.source_type,
        owner=input_passport.owner,
        allowed_use=frozenset(input_passport.allowed_use),
        contains_pii=input_passport.contains_pii,
        sensitivity=input_passport.sensitivity,
        retention_policy=input_passport.retention_policy,
        ai_access_allowed=input_passport.ai_access_allowed,
        external_use_allowed=input_passport.external_use_allowed,
    )


def _scan_doctrine(body: str) -> tuple[bool, str | None]:
    low = body.lower()
    for token in _DOCTRINE_VIOLATION_TOKENS:
        if token.lower() in low:
            return False, token
    return True, None


_DQ_REQUIRED_KEYS: tuple[str, ...] = (
    "company_name",
    "sector",
    "challenge_ar",
    "source",
)


def _summarize_dq(record: Mapping[str, Any]) -> tuple[int, dict[str, Any]]:
    """Compute a single-record data-quality snapshot for the AI Stack intake.

    The single-record DQ uses :func:`account_row_completeness` against the
    intake's required keys plus a bilingual bonus for ``challenge_en``.
    """
    completeness = account_row_completeness(dict(record), _DQ_REQUIRED_KEYS)
    bilingual_bonus = 0.1 if str(record.get("challenge_en") or "").strip() else 0.0
    raw = min(1.0, completeness + bilingual_bonus)
    score = round(raw * 100)
    return score, {
        "required_keys": list(_DQ_REQUIRED_KEYS),
        "completeness": round(completeness, 3),
        "bilingual_bonus": bilingual_bonus,
    }


def _default_agent_handlers() -> dict[str, Any]:
    """Lightweight deterministic handlers used when no LLM provider is wired.

    These handlers produce plausible bilingual artifacts so the AI Stack
    can run end-to-end without an LLM key (useful for tests, demos, and
    the free diagnostic). Production wiring overrides each handler with
    an LLM-backed implementation via :class:`AgentMesh.register`.
    """

    def icp_handler(payload: Mapping[str, Any]) -> dict[str, Any]:
        company = payload.get("company_name", "")
        sector = payload.get("sector", "general")
        band = "A" if sector and "tech" in str(sector).lower() else "B"
        return {
            "summary": f"ICP fit band={band} for {company}",
            "fit_band": band,
            "score": 78 if band == "A" else 64,
            "ar": f"تصنيف العميل {company}: نطاق ملاءمة {band}",
            "en": f"ICP fit band for {company}: {band}",
        }

    def pain_handler(payload: Mapping[str, Any]) -> dict[str, Any]:
        challenge_ar = str(payload.get("challenge_ar", "")).strip()
        challenge_en = str(payload.get("challenge_en", "")).strip() or challenge_ar
        return {
            "summary": "extracted top pain signals",
            "pains_ar": [challenge_ar] if challenge_ar else [],
            "pains_en": [challenge_en] if challenge_en else [],
            "ar": f"المشكلة الرئيسية: {challenge_ar or 'غير محددة'}",
            "en": f"Main pain: {challenge_en or 'unspecified'}",
        }

    def sector_handler(payload: Mapping[str, Any]) -> dict[str, Any]:
        sector = str(payload.get("sector", "general"))
        return {
            "summary": f"sector signal for {sector}",
            "ar": f"إشارة قطاع {sector}: بحاجة لتدقيق",
            "en": f"Sector signal for {sector}: needs verification",
        }

    def qualification_handler(payload: Mapping[str, Any]) -> dict[str, Any]:
        return {
            "summary": "qualification baseline computed",
            "bant_score": 65,
            "ar": "تأهيل أولي: متوسط — يحتاج مكالمة استكشافية",
            "en": "Qualification: medium — needs discovery call",
        }

    def proposal_handler(payload: Mapping[str, Any]) -> dict[str, Any]:
        tier = str(payload.get("offer_tier", "free_diagnostic"))
        company = str(payload.get("company_name", ""))
        return {
            "summary": f"draft proposal for {company} on tier {tier}",
            "ar": (
                f"مقترح مبدئي للعميل {company} على الباقة {tier}: "
                "يشمل تشخيصاً قصيراً وخارطة طريق مدتها 7 أيام."
            ),
            "en": (
                f"Initial draft for {company} on the {tier} tier: includes a "
                "short diagnostic and a 7-day roadmap."
            ),
            "next_step": "draft_for_founder_review",
            "approval_required": True,
        }

    def retainer_handler(payload: Mapping[str, Any]) -> dict[str, Any]:
        tier = str(payload.get("offer_tier", "free_diagnostic"))
        recommendation = "managed_ops" if tier == "data_pack_1500" else tier
        return {
            "summary": f"retainer recommendation: {recommendation}",
            "ar": f"التوصية: ترقية الباقة إلى {recommendation} بعد إثبات القيمة الشهرية.",
            "en": f"Recommendation: upgrade to {recommendation} after monthly value proof.",
            "recommended_tier": recommendation,
        }

    return {
        AGENT_ICP: icp_handler,
        AGENT_PAIN: pain_handler,
        AGENT_SECTOR_INTEL: sector_handler,
        AGENT_QUALIFICATION: qualification_handler,
        AGENT_PROPOSAL: proposal_handler,
        AGENT_RETAINER_RECOMMEND: retainer_handler,
    }


def _default_mesh() -> AgentMesh:
    """Build a default mesh with deterministic handlers for every required agent."""
    mesh = AgentMesh()
    handlers = _default_agent_handlers()
    for agent_id, handler in handlers.items():
        card = new_card(
            agent_id=agent_id,
            name=agent_id.replace("_", " ").title(),
            owner="ai_stack_orchestrator",
            purpose=f"Default deterministic handler for {agent_id}",
            autonomy_level=AutonomyLevel.L3_RECOMMEND,
        )
        # Default registry promotes cards to ACTIVE so the runner allows them
        # under the agent_card_valid invariants.
        active_card = AgentCard(
            agent_id=card.agent_id,
            name=card.name,
            owner=card.owner,
            purpose=card.purpose,
            autonomy_level=card.autonomy_level,
            status=AgentStatus.ACTIVE.value,
            allowed_tools=card.allowed_tools,
            kill_switch_owner=card.kill_switch_owner,
            notes=card.notes,
            created_at=card.created_at,
            killed_reason=card.killed_reason,
        )
        mesh.register(card=active_card, handler=handler)
    return mesh


class AIStackOrchestrator:
    """Sequence the eleven AI Stack layers behind a single ``run()`` entry point.

    The orchestrator is **stateless across runs** — every ``run()`` builds a
    fresh evidence chain and proof pack. State that should survive a run
    (vector store, learning store) is injected from the outside so callers
    can decide whether to share or isolate it.
    """

    __slots__ = ("_lock", "learning_store", "mesh", "rag_pipeline")

    def __init__(
        self,
        *,
        mesh: AgentMesh | None = None,
        rag_pipeline: RAGPipeline | None = None,
        learning_store: InMemoryLearningStore | None = None,
    ) -> None:
        self.mesh = mesh or _default_mesh()
        if rag_pipeline is None:
            embedder = Embedder(dimension=256)
            store = InMemoryVectorStore(dimension=256)
            rag_pipeline = RAGPipeline(embedder=embedder, store=store)
        self.rag_pipeline = rag_pipeline
        self.learning_store = learning_store
        self._lock = threading.Lock()

    def run(self, payload: AIStackInput) -> AIStackResult:
        """Execute the eleven layers in order and assemble a single result."""
        with self._lock:
            return _execute(self, payload)


def _execute(orchestrator: AIStackOrchestrator, payload: AIStackInput) -> AIStackResult:
    started = _now()
    started_perf = time.perf_counter()
    run_id = f"ais_{uuid.uuid4().hex[:16]}"
    chain = new_chain(tenant_id=payload.tenant_id, run_id=run_id)

    proof_pack = new_proof_pack(
        tenant_id=payload.tenant_id,
        customer_handle=payload.customer_handle,
        offer_tier=payload.offer_tier.value,
    )
    passports: list[DecisionPassport] = []
    layer_results: list[LayerResult] = []
    governance_blocked = False
    doctrine_clean = True

    # ── L1: Source Passport ───────────────────────────────────────────────
    l1_started = time.perf_counter()
    passport = _coerce_passport(payload.source_passport)
    ok_ai, errors = source_passport_valid_for_ai(passport)
    validation = validate_passport(passport)
    summary_ar = "تم اعتماد جواز المصدر" if ok_ai else "رفض جواز المصدر — لا يجوز استخدام الذكاء"
    summary_en = (
        "Source passport approved" if ok_ai else "Source passport rejected — AI use blocked"
    )
    l1_payload = {
        "passport_id": passport.source_id,
        "errors": list(errors),
        "missing": list(validation.missing),
    }
    chain.append(
        layer="L1_source_passport",
        artifact_type="passport_validation",
        content=l1_payload,
        summary=summary_en,
    )
    proof_pack.sections_ar["source_passports"] = (
        f"المعرف: {passport.source_id}؛ الحالة: "
        + ("معتمد" if ok_ai else "غير معتمد")
    )
    proof_pack.sections_en["source_passports"] = (
        f"id: {passport.source_id}; status: "
        + ("approved" if ok_ai else "rejected")
    )
    layer_results.append(
        LayerResult(
            layer="L1_source_passport",
            status=LayerStatus.OK if ok_ai else LayerStatus.BLOCKED,
            summary_ar=summary_ar,
            summary_en=summary_en,
            duration_ms=int((time.perf_counter() - l1_started) * 1000),
            payload=l1_payload,
            blocked_reason=None if ok_ai else "source_passport_invalid",
        )
    )
    if not ok_ai:
        governance_blocked = True
        _record_feedback(
            orchestrator,
            from_governance_block(
                tenant_id=payload.tenant_id,
                run_id=run_id,
                layer="L1_source_passport",
                reason=", ".join(errors),
            ),
        )
        return _finalize(
            payload=payload,
            run_id=run_id,
            started=started,
            started_perf=started_perf,
            proof_pack=proof_pack,
            passports=passports,
            chain=chain,
            layer_results=layer_results,
            governance_blocked=True,
            doctrine_clean=True,
        )

    # ── L2: Data Quality Score ────────────────────────────────────────────
    l2_started = time.perf_counter()
    dq_record = {
        "company_name": payload.company_name,
        "sector": payload.sector,
        "challenge_ar": payload.challenge_ar,
        "challenge_en": payload.challenge_en,
        "source": passport.source_type,
    }
    dq_score, dq_breakdown = _summarize_dq(dq_record)
    l2_payload = {"score": dq_score, **dq_breakdown}
    chain.append(
        layer="L2_data_quality",
        artifact_type="dq_score",
        content=l2_payload,
        summary=f"DQ score = {dq_score}",
    )
    proof_pack.sections_ar["quality_scores"] = f"درجة جودة البيانات: {dq_score}/100"
    proof_pack.sections_en["quality_scores"] = f"data quality score: {dq_score}/100"
    layer_results.append(
        LayerResult(
            layer="L2_data_quality",
            status=LayerStatus.OK,
            summary_ar=f"درجة جودة البيانات {dq_score}",
            summary_en=f"data quality {dq_score}",
            duration_ms=int((time.perf_counter() - l2_started) * 1000),
            payload=l2_payload,
        )
    )

    # ── L3: Intelligence / RAG ────────────────────────────────────────────
    l3_started = time.perf_counter()
    if payload.rag_documents:
        orchestrator.rag_pipeline.index_documents(
            tenant_id=payload.tenant_id,
            documents=payload.rag_documents,
            namespace=run_id,
        )
    context = orchestrator.rag_pipeline.retrieve(
        tenant_id=payload.tenant_id,
        query=payload.challenge_ar,
        namespace=run_id if payload.rag_documents else None,
        top_k=4,
        max_context_chars=2000,
    )
    l3_payload = {
        "hits": [hit.to_dict() for hit in context.hits],
        "context_chars": context.used_chars,
        "truncated": context.truncated,
    }
    chain.append(
        layer="L3_intelligence",
        artifact_type="rag_context",
        content=l3_payload,
        summary=f"{len(context.hits)} hits, {context.used_chars} chars",
    )
    proof_pack.sections_ar["inputs"] = (
        f"المدخلات: {payload.company_name} في قطاع {payload.sector}؛ التحدي: "
        f"{payload.challenge_ar}"
    )
    proof_pack.sections_en["inputs"] = (
        f"inputs: {payload.company_name} in {payload.sector}; challenge: "
        f"{payload.challenge_en or payload.challenge_ar}"
    )
    layer_results.append(
        LayerResult(
            layer="L3_intelligence",
            status=LayerStatus.OK,
            summary_ar=f"تم استرجاع {len(context.hits)} مقاطع",
            summary_en=f"retrieved {len(context.hits)} chunks",
            duration_ms=int((time.perf_counter() - l3_started) * 1000),
            payload=l3_payload,
        )
    )

    # ── L4: Model Router (advisory metadata) ──────────────────────────────
    l4_started = time.perf_counter()
    route = get_model_route(ModelTask.ARABIC_WRITING)
    l4_payload = {
        "task": route.task.value,
        "quality_tier": route.quality_tier,
        "cost_class": route.cost_class,
        "fallback": route.fallback_task.value if route.fallback_task else None,
    }
    chain.append(
        layer="L4_model_router",
        artifact_type="route_selection",
        content=l4_payload,
        summary=f"route: {route.task.value} ({route.quality_tier})",
    )
    layer_results.append(
        LayerResult(
            layer="L4_model_router",
            status=LayerStatus.OK,
            summary_ar=f"اختيار المسار: {route.task.value}",
            summary_en=f"route selected: {route.task.value}",
            duration_ms=int((time.perf_counter() - l4_started) * 1000),
            payload=l4_payload,
        )
    )

    # ── L5: Agent Mesh ────────────────────────────────────────────────────
    l5_started = time.perf_counter()
    base_payload: dict[str, Any] = {
        "tenant_id": payload.tenant_id,
        "customer_handle": payload.customer_handle,
        "company_name": payload.company_name,
        "sector": payload.sector,
        "challenge_ar": payload.challenge_ar,
        "challenge_en": payload.challenge_en or payload.challenge_ar,
        "offer_tier": payload.offer_tier.value,
        "rag_context": context.context_text,
    }
    plan = plan_for_offer(offer_tier=payload.offer_tier.value, base_payload=base_payload)
    trace: MeshTrace = orchestrator.mesh.execute(plan)
    l5_payload = trace.to_dict()
    chain.append(
        layer="L5_agent_mesh",
        artifact_type="mesh_trace",
        content=l5_payload,
        summary=(
            f"{len(trace.runs)} runs, halted={trace.halted}, all_ok={trace.all_ok}"
        ),
    )
    work_summary_ar = "؛ ".join(
        f"{r.agent_name}: {r.output_summary}" for r in trace.runs
    )
    work_summary_en = "; ".join(
        f"{r.agent_name}: {r.output_summary}" for r in trace.runs
    )
    proof_pack.sections_ar["work_completed"] = work_summary_ar or "(لم تنفذ أي مهام)"
    proof_pack.sections_en["work_completed"] = work_summary_en or "(no tasks executed)"
    proof_pack.sections_ar["outputs"] = work_summary_ar or "(لا توجد مخرجات)"
    proof_pack.sections_en["outputs"] = work_summary_en or "(no outputs)"
    layer_results.append(
        LayerResult(
            layer="L5_agent_mesh",
            status=LayerStatus.OK if trace.all_ok else LayerStatus.DEGRADED,
            summary_ar=f"المهام: {len(trace.runs)}؛ نجاح: {trace.all_ok}",
            summary_en=f"runs: {len(trace.runs)}; all_ok: {trace.all_ok}",
            duration_ms=int((time.perf_counter() - l5_started) * 1000),
            payload=l5_payload,
            blocked_reason=trace.halt_reason if trace.halted else None,
        )
    )

    # Issue a Decision Passport per successful run.
    for run in trace.runs:
        if run.status != "ok":
            continue
        passport_record = issue_passport(
            tenant_id=payload.tenant_id,
            decision_type=_decision_type_for_agent(run.agent_id),
            summary_ar=str(_extract_lang(run.output, "ar") or run.output_summary),
            summary_en=str(_extract_lang(run.output, "en") or run.output_summary),
            content=run.output if isinstance(run.output, Mapping) else {"output": run.output},
            sensitivity=Sensitivity.S1_INTERNAL,
            reversibility=Reversibility.R1_QUICK,
            confidence=Confidence.C2_MEDIUM,
            external_action=False,
            metadata={"agent_id": run.agent_id, "step": run.metadata.get("step")},
        )
        passports.append(passport_record)

    # ── L6: Governance Gate ───────────────────────────────────────────────
    l6_started = time.perf_counter()
    # Scan the union of customer input + AI outputs so guaranteed-claim
    # tokens leaking from either side are caught.
    combined_text = " ".join(
        filter(
            None,
            [
                payload.challenge_ar,
                payload.challenge_en,
                proof_pack.sections_ar.get("outputs"),
                proof_pack.sections_en.get("outputs"),
                proof_pack.sections_ar.get("work_completed"),
                proof_pack.sections_en.get("work_completed"),
            ],
        )
    )
    governance_decision = governance_decide(
        action_type="customer_facing_proposal",
        context={
            "text": combined_text,
            "external_use": False,
            "risk_score": 0.2,
        },
        actor=payload.actor,
    )
    l6_payload = {
        "decision": governance_decision.decision,
        "reason": governance_decision.reason,
        "risk_level": governance_decision.risk_level,
        "approval_required": governance_decision.approval_required,
    }
    chain.append(
        layer="L6_governance",
        artifact_type="governance_decision",
        content=l6_payload,
        summary=(
            f"governance={governance_decision.decision} risk={governance_decision.risk_level}"
        ),
    )
    proof_pack.sections_ar["governance_decisions"] = (
        f"القرار: {governance_decision.decision} — السبب: {governance_decision.reason}"
    )
    proof_pack.sections_en["governance_decisions"] = (
        f"decision: {governance_decision.decision} — reason: {governance_decision.reason}"
    )
    if governance_decision.decision == "block":
        governance_blocked = True
        layer_results.append(
            LayerResult(
                layer="L6_governance",
                status=LayerStatus.BLOCKED,
                summary_ar="حُجب من قِبَل الحوكمة",
                summary_en="blocked by governance",
                duration_ms=int((time.perf_counter() - l6_started) * 1000),
                payload=l6_payload,
                blocked_reason=governance_decision.reason,
            )
        )
        _record_feedback(
            orchestrator,
            from_governance_block(
                tenant_id=payload.tenant_id,
                run_id=run_id,
                layer="L6_governance",
                reason=governance_decision.reason,
            ),
        )
        # Fall through to finalize so the partial proof pack is still recorded.
    else:
        layer_results.append(
            LayerResult(
                layer="L6_governance",
                status=LayerStatus.OK,
                summary_ar=f"الحوكمة: {governance_decision.decision}",
                summary_en=f"governance: {governance_decision.decision}",
                duration_ms=int((time.perf_counter() - l6_started) * 1000),
                payload=l6_payload,
            )
        )

    # ── Doctrine scan (redundant safety net) ───────────────────────────────
    body_for_scan = " ".join(
        (
            payload.challenge_ar,
            payload.challenge_en,
            proof_pack.sections_ar.get("outputs", ""),
            proof_pack.sections_en.get("outputs", ""),
            proof_pack.sections_ar.get("work_completed", ""),
            proof_pack.sections_en.get("work_completed", ""),
            proof_pack.sections_ar.get("problem", ""),
            proof_pack.sections_en.get("problem", ""),
        )
    )
    doctrine_ok, violation_token = _scan_doctrine(body_for_scan)
    if not doctrine_ok:
        doctrine_clean = False
        governance_blocked = True
        _record_feedback(
            orchestrator,
            from_doctrine_violation(
                tenant_id=payload.tenant_id,
                run_id=run_id,
                layer="L6_governance",
                violation=violation_token or "unknown",
            ),
        )

    # ── L7: Proof Pack v2 assembly ────────────────────────────────────────
    l7_started = time.perf_counter()
    _fill_proof_pack_defaults(
        proof_pack,
        payload=payload,
        passports=passports,
        evidence_head=chain.head.chain_hash if chain.head else "",
        governance_decision=l6_payload,
        retainer_suggestion=_extract_retainer(trace),
    )
    proof_pack.proof_score = composite_proof_score(
        sections_ar=proof_pack.sections_ar,
        sections_en=proof_pack.sections_en,
        evidence_count=len(chain),
        governance_blocked=governance_blocked,
    )
    proof_pack.governance_decisions = (governance_decision.decision,)
    proof_pack.decision_passport_ids = tuple(p.passport_id for p in passports)
    proof_pack.evidence_head_hash = chain.head.chain_hash if chain.head else ""
    proof_pack.completed_at = _now_iso()
    l7_payload = {
        "pack_id": proof_pack.pack_id,
        "proof_score": proof_pack.proof_score,
        "section_count": len(proof_pack.sections_ar),
        "evidence_count": len(chain),
    }
    chain.append(
        layer="L7_proof_pack",
        artifact_type="proof_pack_v2",
        content=l7_payload,
        summary=f"proof_score={proof_pack.proof_score}",
    )
    layer_results.append(
        LayerResult(
            layer="L7_proof_pack",
            status=LayerStatus.OK,
            summary_ar=f"درجة الإثبات: {proof_pack.proof_score}",
            summary_en=f"proof score: {proof_pack.proof_score}",
            duration_ms=int((time.perf_counter() - l7_started) * 1000),
            payload=l7_payload,
        )
    )

    # ── L8: Value Ledger (advisory; no monetary entry created) ────────────
    l8_started = time.perf_counter()
    l8_payload = {
        "advisory_only": True,
        "reason": "no_invoice_paid_yet",
        "estimated_band": "estimated",
    }
    chain.append(
        layer="L8_value_ledger",
        artifact_type="value_ledger_advisory",
        content=l8_payload,
        summary="advisory only — awaiting invoice_paid signal",
    )
    proof_pack.sections_ar["value_metrics"] = (
        "لا يوجد قيد قيمة مالي بعد — بانتظار إشارة الدفع (invoice_paid)."
    )
    proof_pack.sections_en["value_metrics"] = (
        "no monetary value entry yet — awaiting invoice_paid signal."
    )
    layer_results.append(
        LayerResult(
            layer="L8_value_ledger",
            status=LayerStatus.SKIPPED,
            summary_ar="السجل غير مفعّل — لا فاتورة مدفوعة بعد",
            summary_en="ledger skipped — no invoice paid yet",
            duration_ms=int((time.perf_counter() - l8_started) * 1000),
            payload=l8_payload,
        )
    )

    # ── L9: Capital Ledger (proof pack itself is a capital asset draft) ──
    l9_started = time.perf_counter()
    l9_payload = {
        "asset_kind": "proof_pack_draft",
        "asset_ref": proof_pack.pack_id,
        "persisted": False,
        "reason": "persisted_on_governance_clearance_and_invoice_paid",
    }
    chain.append(
        layer="L9_capital_ledger",
        artifact_type="capital_asset_draft",
        content=l9_payload,
        summary=f"proof pack {proof_pack.pack_id} registered as capital draft",
    )
    proof_pack.sections_ar["capital_assets_created"] = (
        f"مسودة أصل رأسمالي: {proof_pack.pack_id}"
    )
    proof_pack.sections_en["capital_assets_created"] = (
        f"capital asset draft: {proof_pack.pack_id}"
    )
    layer_results.append(
        LayerResult(
            layer="L9_capital_ledger",
            status=LayerStatus.OK,
            summary_ar=f"مسودة أصل: {proof_pack.pack_id}",
            summary_en=f"asset draft: {proof_pack.pack_id}",
            duration_ms=int((time.perf_counter() - l9_started) * 1000),
            payload=l9_payload,
        )
    )

    # ── L10: Adoption / Retainer readiness (recommendation only) ─────────
    l10_started = time.perf_counter()
    recommended = _extract_retainer(trace)
    l10_payload = {
        "recommended_offer": recommended or payload.offer_tier.value,
        "proof_score": proof_pack.proof_score,
    }
    chain.append(
        layer="L10_adoption",
        artifact_type="retainer_recommendation",
        content=l10_payload,
        summary=f"recommended={recommended or payload.offer_tier.value}",
    )
    proof_pack.sections_ar["recommended_next_step"] = (
        f"الخطوة الموصى بها: تأكيد الباقة {l10_payload['recommended_offer']}"
    )
    proof_pack.sections_en["recommended_next_step"] = (
        f"recommended next step: confirm tier {l10_payload['recommended_offer']}"
    )
    proof_pack.sections_ar["retainer_expansion_path"] = (
        f"مسار التوسع: ابدأ بـ {payload.offer_tier.value} ثم ارفع إلى "
        f"{l10_payload['recommended_offer']}."
    )
    proof_pack.sections_en["retainer_expansion_path"] = (
        f"expansion path: start with {payload.offer_tier.value} → upgrade to "
        f"{l10_payload['recommended_offer']}."
    )
    layer_results.append(
        LayerResult(
            layer="L10_adoption",
            status=LayerStatus.OK,
            summary_ar=f"التوصية: {l10_payload['recommended_offer']}",
            summary_en=f"recommendation: {l10_payload['recommended_offer']}",
            duration_ms=int((time.perf_counter() - l10_started) * 1000),
            payload=l10_payload,
        )
    )

    # ── L11: Self-Evolving (shadow-mode feedback) ────────────────────────
    l11_started = time.perf_counter()
    outcome_kind = OutcomeKind.SUCCESS if not governance_blocked else OutcomeKind.FAILURE
    feedback = make_feedback_event(
        tenant_id=payload.tenant_id,
        run_id=run_id,
        layer="L11_self_evolving",
        outcome_kind=outcome_kind,
        outcome_value=float(proof_pack.proof_score),
        doctrine_clean=doctrine_clean and not governance_blocked,
        decision_id=passports[0].passport_id if passports else None,
        learnings={
            "offer_tier": payload.offer_tier.value,
            "proof_score": proof_pack.proof_score,
            "dq_score": dq_score,
        },
    )
    _record_feedback(orchestrator, feedback)
    l11_payload = {
        "event_id": feedback.event_id,
        "outcome_kind": feedback.outcome_kind,
        "doctrine_clean": feedback.doctrine_clean,
    }
    chain.append(
        layer="L11_self_evolving",
        artifact_type="feedback_event",
        content=l11_payload,
        summary=f"feedback recorded: {feedback.outcome_kind}",
    )
    layer_results.append(
        LayerResult(
            layer="L11_self_evolving",
            status=LayerStatus.OK,
            summary_ar=f"تم تسجيل تغذية راجعة: {feedback.outcome_kind}",
            summary_en=f"feedback recorded: {feedback.outcome_kind}",
            duration_ms=int((time.perf_counter() - l11_started) * 1000),
            payload=l11_payload,
        )
    )

    return _finalize(
        payload=payload,
        run_id=run_id,
        started=started,
        started_perf=started_perf,
        proof_pack=proof_pack,
        passports=passports,
        chain=chain,
        layer_results=layer_results,
        governance_blocked=governance_blocked,
        doctrine_clean=doctrine_clean,
    )


def _decision_type_for_agent(agent_id: str) -> str:
    mapping = {
        AGENT_ICP: "icp_classification",
        AGENT_PAIN: "pain_extraction",
        AGENT_QUALIFICATION: "qualification",
        AGENT_PROPOSAL: "proposal_draft",
        AGENT_RETAINER_RECOMMEND: "retainer_recommendation",
        AGENT_SECTOR_INTEL: "model_routing",
    }
    return mapping.get(agent_id, "model_routing")


def _extract_lang(output: Any, lang: str) -> str | None:
    if isinstance(output, Mapping):
        value = output.get(lang)
        if value:
            return str(value)
    return None


def _extract_retainer(trace: MeshTrace) -> str | None:
    for run in trace.runs:
        if run.agent_id == AGENT_RETAINER_RECOMMEND and isinstance(run.output, Mapping):
            tier = run.output.get("recommended_tier")
            if isinstance(tier, str) and tier.strip():
                return tier.strip()
    return None


def _fill_proof_pack_defaults(
    proof_pack: ProofPackV2,
    *,
    payload: AIStackInput,
    passports: list[DecisionPassport],
    evidence_head: str,
    governance_decision: Mapping[str, Any],
    retainer_suggestion: str | None,
) -> None:
    """Populate the canonical 14 sections with safe bilingual defaults."""
    # Executive summary
    proof_pack.sections_ar["executive_summary"] = (
        f"تشخيص قصير للعميل {payload.company_name} في قطاع {payload.sector}. "
        "النتائج مسودة وتحتاج مراجعة المؤسس قبل أي تواصل خارجي."
    )
    proof_pack.sections_en["executive_summary"] = (
        f"Short diagnostic for {payload.company_name} in {payload.sector}. "
        "Results are drafts and need founder review before any outbound action."
    )
    # Problem
    proof_pack.sections_ar["problem"] = payload.challenge_ar
    proof_pack.sections_en["problem"] = payload.challenge_en or payload.challenge_ar
    # Blocked risks
    proof_pack.sections_ar["blocked_risks"] = (
        "لا توجد ادعاءات إيراد مضمونة؛ لا توجد اتصالات خارجية بدون موافقة."
    )
    proof_pack.sections_en["blocked_risks"] = (
        "No guaranteed-revenue claims; no outbound actions without explicit approval."
    )
    # Limitations
    proof_pack.sections_ar["limitations"] = (
        "هذه نسخة تشخيصية مبدئية ضمن الباقة المجانية / السريعة. تحتاج تأكيد بيانات "
        "إضافية من العميل قبل تحويلها إلى قرار تجاري."
    )
    proof_pack.sections_en["limitations"] = (
        "This is a preliminary diagnostic snapshot within the free / sprint tier. "
        "Needs additional customer data before becoming a commercial decision."
    )
    if not proof_pack.sections_ar.get("recommended_next_step"):
        proof_pack.sections_ar["recommended_next_step"] = (
            f"الخطوة التالية: تأكيد {retainer_suggestion or payload.offer_tier.value}"
        )
    if not proof_pack.sections_en.get("recommended_next_step"):
        proof_pack.sections_en["recommended_next_step"] = (
            f"next step: confirm {retainer_suggestion or payload.offer_tier.value}"
        )


def _record_feedback(orchestrator: AIStackOrchestrator, event: Any) -> None:
    """Persist a feedback event to the orchestrator's learning store, if any."""
    if orchestrator.learning_store is not None:
        orchestrator.learning_store.append(event)
    else:
        record_feedback(event)


def _finalize(
    *,
    payload: AIStackInput,
    run_id: str,
    started: datetime,
    started_perf: float,
    proof_pack: ProofPackV2,
    passports: list[DecisionPassport],
    chain: EvidenceChain,
    layer_results: list[LayerResult],
    governance_blocked: bool,
    doctrine_clean: bool,
) -> AIStackResult:
    completed = _now()
    duration_ms = int((time.perf_counter() - started_perf) * 1000)
    return AIStackResult(
        run_id=run_id,
        tenant_id=payload.tenant_id,
        customer_handle=payload.customer_handle,
        offer_tier=payload.offer_tier,
        started_at=started,
        completed_at=completed,
        duration_ms=duration_ms,
        layers=layer_results,
        proof_pack_id=proof_pack.pack_id,
        proof_score=proof_pack.proof_score,
        decision_passport_ids=[p.passport_id for p in passports],
        evidence_head_hash=chain.head.chain_hash if chain.head else "",
        governance_blocked=governance_blocked,
        doctrine_clean=doctrine_clean,
        recommended_offer=(
            proof_pack.sections_en.get("recommended_next_step", "")
            .replace("next step: confirm ", "")
            .strip()
        ),
        proof_pack_markdown=render_markdown(proof_pack),
    )


_DEFAULT_ORCHESTRATOR_LOCK = threading.Lock()
_DEFAULT_ORCHESTRATOR: AIStackOrchestrator | None = None


def _default_orchestrator() -> AIStackOrchestrator:
    global _DEFAULT_ORCHESTRATOR
    with _DEFAULT_ORCHESTRATOR_LOCK:
        if _DEFAULT_ORCHESTRATOR is None:
            _DEFAULT_ORCHESTRATOR = AIStackOrchestrator()
        return _DEFAULT_ORCHESTRATOR


def run_ai_stack(payload: AIStackInput) -> AIStackResult:
    """Module-level convenience: run the stack with a shared default orchestrator."""
    return _default_orchestrator().run(payload)


def reset_default_orchestrator() -> None:
    """Tests call this between cases to prevent cross-test state leakage."""
    global _DEFAULT_ORCHESTRATOR
    with _DEFAULT_ORCHESTRATOR_LOCK:
        _DEFAULT_ORCHESTRATOR = None


__all__ = [
    "AIStackOrchestrator",
    "reset_default_orchestrator",
    "run_ai_stack",
]
