"""Autonomous Distribution Engine — the unified pipeline.

This module is the *single contract* between the 9 canonical OS layers.
It performs no external I/O. It does not call HTTP, email, payment, or
WhatsApp APIs directly — every external action is queued as a DRAFT that
must pass `approval_center` before sending.

Doctrine guarantees (enforced in code, tested in tests/test_no_*):
    - Every public function returns a dataclass with `governance_decision`.
    - Every external-facing draft passes the governance gate first.
    - PII never escapes (relies on data_os.pii_classifier).
    - Source Passport is required for any AI-assisted processing.
    - Capital asset registration is gated on a real payment ref.
    - Retainer offer is gated on adoption_band >= "B".

Bilingual labels are kept for founder digests and tenant-facing text.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Literal

from auto_client_acquisition.adoption_os import (
    AdoptionDimensions,
    adoption_band,
    adoption_score,
    wave2_retainer_eligibility,
)
from auto_client_acquisition.capital_os import CapitalAssetType
from auto_client_acquisition.client_os import client_expansion_recommendation
from auto_client_acquisition.compliance_trust_os.approval_engine import (
    GovernanceDecision,
)
from auto_client_acquisition.data_os import (
    SourcePassport,
    compute_dq,
    source_passport_valid_for_ai,
    validate_account_row,
)
from auto_client_acquisition.governance_os import (
    audit_draft_text,
    governance_decision_from_passport_ai_gate,
    governance_decision_from_policy_check,
    intake_violations_for_source,
    policy_check_draft,
)
from auto_client_acquisition.proof_os import (
    build_empty_proof_pack_v2,
    proof_pack_completeness_score,
    proof_pack_score_with_governance_penalty,
    proof_pack_v2_sections_complete,
)
from auto_client_acquisition.sales_os import (
    ICPDimensions,
    QualificationResult,
    icp_score,
    qualify,
)

# Bilingual disclaimer required on every customer-facing markdown.
DISCLAIMER_AR_EN = (
    "Estimated value is not Verified value / "
    "القيمة التقديرية ليست قيمة مُتحقَّقة"
)


def _utc_now_iso() -> str:
    return datetime.now(tz=timezone.utc).isoformat(timespec="seconds")


# ---------------------------------------------------------------------------
# Lead processing
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class LeadDecision:
    """Outcome of the lead intake pipeline."""

    governance_decision: GovernanceDecision
    qualification: QualificationResult | None
    dq_score: int
    icp: int
    recommended_offer: str
    rung: int  # 0..4 in the 5-rung ladder
    reasons: tuple[str, ...]
    doctrine_violations: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    rationale_ar: str
    rationale_en: str
    timestamp: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "governance_decision": self.governance_decision.value,
            "qualification": (
                self.qualification.to_dict() if self.qualification else None
            ),
            "dq_score": self.dq_score,
            "icp": self.icp,
            "recommended_offer": self.recommended_offer,
            "rung": self.rung,
            "reasons": list(self.reasons),
            "doctrine_violations": list(self.doctrine_violations),
            "evidence_refs": list(self.evidence_refs),
            "rationale_ar": self.rationale_ar,
            "rationale_en": self.rationale_en,
            "timestamp": self.timestamp,
        }


_OFFER_TO_RUNG = {
    "revenue_intelligence_sprint": 1,
    "data_to_revenue_diagnostic": 2,
    "data_to_revenue_pack": 2,
    "managed_revenue_ops": 3,
    "custom_ai_setup": 4,
    "capability_diagnostic": 0,
    "free_diagnostic": 0,
    "refer_out_governance_not_accepted": -1,
    "refer_out_not_enough_fit": -1,
    "not_a_fit_decline_politely": -1,
}


def _offer_to_rung(offer: str) -> int:
    return _OFFER_TO_RUNG.get(offer, 0)


def process_lead(
    *,
    lead_row: dict[str, Any],
    source_passport: SourcePassport,
    icp_dims: ICPDimensions,
    discovery_answers: dict[str, Any] | None = None,
    raw_request_text: str = "",
) -> LeadDecision:
    """Unified lead processing across DATA → GOVERNANCE → SALES.

    Steps:
        1. Validate source under PDPL (`governance_os.intake_violations_for_source`).
        2. Validate account row + compute DQ score (`data_os`).
        3. Gate AI use on Source Passport (`data_os.source_passport_valid_for_ai`).
        4. Score ICP and run qualification (`sales_os`).
        5. Map to 5-rung ladder + emit governance decision.

    Returns:
        LeadDecision — carries a governance_decision that downstream callers
        MUST honor before any external action.
    """
    answers = discovery_answers or {}
    evidence: list[str] = []
    reasons: list[str] = []
    doctrine_violations: list[str] = []

    # 1. PDPL intake gate.
    intake_issues = intake_violations_for_source(source_passport.source_type)
    if intake_issues:
        doctrine_violations.extend(intake_issues)
        return LeadDecision(
            governance_decision=GovernanceDecision.BLOCK,
            qualification=None,
            dq_score=0,
            icp=0,
            recommended_offer="not_a_fit_decline_politely",
            rung=-1,
            reasons=("intake_violation",),
            doctrine_violations=tuple(doctrine_violations),
            evidence_refs=("intake_gate",),
            rationale_ar="مصدر غير مسموح بموجب PDPL — تم الرفض.",
            rationale_en="Source disallowed under PDPL — declined.",
            timestamp=_utc_now_iso(),
        )
    evidence.append(f"source_passport:{source_passport.source_type}")

    # 2. Row validation + DQ score.
    validation = validate_account_row(lead_row, 0)
    if not getattr(validation, "ok", True):
        reasons.append("row_validation_failed")

    cols = list(lead_row.keys()) or ["company_name", "sector", "city"]
    dq_obj = compute_dq(
        [lead_row],
        columns=cols,
        has_valid_passport=True,
    )
    dq = int(getattr(dq_obj, "overall", 0))
    evidence.append(f"dq_score:{dq}")

    # 3. AI use gate — relies on Source Passport.
    ai_ok, ai_errs = source_passport_valid_for_ai(source_passport)
    ai_gate = governance_decision_from_passport_ai_gate(ai_ok, ai_errs)
    if ai_gate is GovernanceDecision.BLOCK:
        return LeadDecision(
            governance_decision=GovernanceDecision.BLOCK,
            qualification=None,
            dq_score=dq,
            icp=0,
            recommended_offer="not_a_fit_decline_politely",
            rung=-1,
            reasons=("ai_gate_blocked",) + tuple(reasons),
            doctrine_violations=tuple(doctrine_violations) + tuple(ai_errs),
            evidence_refs=tuple(evidence),
            rationale_ar="جواز المصدر لا يسمح بمعالجة AI — تم الإيقاف.",
            rationale_en="Source passport does not permit AI use — blocked.",
            timestamp=_utc_now_iso(),
        )
    evidence.append(f"ai_gate:{ai_gate.value}")

    # 4. ICP + qualification.
    icp = icp_score(icp_dims)
    evidence.append(f"icp:{icp}")
    q = qualify(
        pain_clear=bool(answers.get("pain_clear")),
        owner_present=bool(answers.get("owner_present")),
        data_available=bool(answers.get("data_available")),
        accepts_governance=bool(answers.get("accepts_governance")),
        has_budget=bool(answers.get("has_budget")),
        wants_safe_methods=bool(answers.get("wants_safe_methods", True)),
        proof_path_visible=bool(answers.get("proof_path_visible")),
        retainer_path_visible=bool(answers.get("retainer_path_visible")),
        raw_request_text=raw_request_text,
        sector=str(answers.get("sector") or ""),
        city=str(answers.get("city") or ""),
    )
    evidence.append(f"qualification:{q.decision}")
    doctrine_violations.extend(q.doctrine_violations)

    rung = _offer_to_rung(q.recommended_offer)

    # 5. Final governance decision — REQUIRE_APPROVAL for any external send.
    if q.doctrine_violations:
        gov = GovernanceDecision.BLOCK
    elif q.decision in ("reject", "refer_out"):
        gov = GovernanceDecision.BLOCK
    elif ai_gate is GovernanceDecision.REQUIRE_APPROVAL:
        gov = GovernanceDecision.REQUIRE_APPROVAL
    else:
        # Outreach is *always* draft-only; require approval to send.
        gov = GovernanceDecision.REQUIRE_APPROVAL

    rationale_ar = (
        f"تقييم: ICP={icp} | DQ={dq} | qualification={q.decision} | "
        f"رتبة={rung}. القرار: {gov.value}."
    )
    rationale_en = (
        f"Score: ICP={icp} | DQ={dq} | qualification={q.decision} | "
        f"rung={rung}. Decision: {gov.value}."
    )

    return LeadDecision(
        governance_decision=gov,
        qualification=q,
        dq_score=dq,
        icp=icp,
        recommended_offer=q.recommended_offer,
        rung=rung,
        reasons=tuple(reasons) + tuple(q.reasons),
        doctrine_violations=tuple(doctrine_violations),
        evidence_refs=tuple(evidence),
        rationale_ar=rationale_ar,
        rationale_en=rationale_en,
        timestamp=_utc_now_iso(),
    )


# ---------------------------------------------------------------------------
# Outreach draft governance
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class OutreachDraftDecision:
    governance_decision: GovernanceDecision
    safe_to_queue: bool
    reasons: tuple[str, ...]
    rationale_ar: str
    rationale_en: str
    timestamp: str


def audit_outreach_draft(text: str, channel: str = "email") -> OutreachDraftDecision:
    """Run the governance gate on an outreach draft.

    Channels: email, whatsapp, linkedin. WhatsApp/LinkedIn cold sends are
    permanently BLOCKED by doctrine (no automation). Email is draft-only
    awaiting founder approval.
    """
    check = policy_check_draft(text)
    text_violations = audit_draft_text(text)
    gov = governance_decision_from_policy_check(check)

    reasons: list[str] = []
    if not check.allowed:
        reasons.extend(check.issues)
    if text_violations:
        reasons.extend(text_violations)

    if channel in ("whatsapp", "linkedin"):
        gov = GovernanceDecision.BLOCK
        reasons.append(f"{channel}_automation_forbidden_by_doctrine")

    safe = gov in (
        GovernanceDecision.ALLOW,
        GovernanceDecision.ALLOW_WITH_REVIEW,
        GovernanceDecision.REQUIRE_APPROVAL,
        GovernanceDecision.DRAFT_ONLY,
    )

    return OutreachDraftDecision(
        governance_decision=gov,
        safe_to_queue=safe,
        reasons=tuple(reasons),
        rationale_ar="تم فحص المسودة عبر بوابة الحوكمة. لن تُرسل دون موافقة المؤسس.",
        rationale_en="Draft passed through the governance gate. Will NOT send without founder approval.",
        timestamp=_utc_now_iso(),
    )


# ---------------------------------------------------------------------------
# Payment / Capital
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class PaymentDecision:
    governance_decision: GovernanceDecision
    capital_asset_eligible: bool
    asset_type: str | None
    invoice_ref: str
    amount_sar: float
    rung: int
    rationale_ar: str
    rationale_en: str
    timestamp: str


def process_payment(
    *,
    invoice_ref: str,
    amount_sar: float,
    moyasar_status: Literal["pending", "paid", "failed", "refunded"],
    moyasar_mode: Literal["test", "live"],
    customer_id: str,
    rung: int,
    proof_pack_score: int,
) -> PaymentDecision:
    """Process a confirmed payment and decide whether a capital asset registers.

    Capital asset is registered ONLY when:
        - moyasar_status == 'paid'
        - proof_pack_score >= 70 (so we don't capitalize unverified value)

    The mode is recorded for audit; live-mode payment is the only one that
    counts toward revenue KPIs but a test payment can still register an asset
    for engineering verification (founder must explicitly approve via the
    approval_center). To keep the engine deterministic, both test and live
    paid statuses are eligible — downstream approval_center decides publish.
    """
    if moyasar_status != "paid":
        return PaymentDecision(
            governance_decision=GovernanceDecision.BLOCK,
            capital_asset_eligible=False,
            asset_type=None,
            invoice_ref=invoice_ref,
            amount_sar=amount_sar,
            rung=rung,
            rationale_ar="الدفعة غير مكتملة — لا تسجيل أصل رأسمالي.",
            rationale_en="Payment not paid — no capital asset registered.",
            timestamp=_utc_now_iso(),
        )

    if proof_pack_score < 70:
        return PaymentDecision(
            governance_decision=GovernanceDecision.ALLOW_WITH_REVIEW,
            capital_asset_eligible=False,
            asset_type=None,
            invoice_ref=invoice_ref,
            amount_sar=amount_sar,
            rung=rung,
            rationale_ar="درجة Proof Pack دون 70 — يلزم تحسين الأثر قبل التسجيل.",
            rationale_en="Proof Pack score below 70 — improve evidence before capitalizing.",
            timestamp=_utc_now_iso(),
        )

    # Map rung -> CapitalAssetType (best-fit using existing enum values).
    rung_to_asset = {
        1: CapitalAssetType.DRAFT_TEMPLATE.value,
        2: CapitalAssetType.PROOF_EXAMPLE.value,
        3: CapitalAssetType.SCORING_RULE.value,
        4: CapitalAssetType.PRODUCTIZATION_SIGNAL.value,
    }
    asset_type = rung_to_asset.get(rung, CapitalAssetType.PROOF_EXAMPLE.value)

    gov = GovernanceDecision.ALLOW if moyasar_mode == "live" else GovernanceDecision.ALLOW_WITH_REVIEW

    return PaymentDecision(
        governance_decision=gov,
        capital_asset_eligible=True,
        asset_type=asset_type,
        invoice_ref=invoice_ref,
        amount_sar=amount_sar,
        rung=rung,
        rationale_ar=(
            f"دفعة مؤكدة عبر Moyasar ({moyasar_mode}). أصل رأسمالي مرشّح: {asset_type}."
        ),
        rationale_en=(
            f"Payment confirmed via Moyasar ({moyasar_mode}). Eligible capital asset: {asset_type}."
        ),
        timestamp=_utc_now_iso(),
    )


# ---------------------------------------------------------------------------
# Proof Pack assembly
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class ProofPackDecision:
    governance_decision: GovernanceDecision
    score: int
    score_with_penalty: int
    sections_complete: bool
    missing_sections: tuple[str, ...]
    publish_eligible: bool
    rationale_ar: str
    rationale_en: str
    timestamp: str


def assemble_proof_pack(
    *,
    sections: dict[str, str] | None = None,
    governance_blocked: bool = False,
) -> ProofPackDecision:
    """Assemble a Proof Pack v2 and decide publish-eligibility.

    Args:
        sections: partial PP_v2 sections (section_name -> markdown content).
        governance_blocked: whether any governance gate fired during sprint.
    """
    pack = build_empty_proof_pack_v2()
    if sections:
        for k, v in sections.items():
            if k in pack:
                pack[k] = v

    complete, missing = proof_pack_v2_sections_complete(pack)
    score = proof_pack_completeness_score(pack)
    score_with_penalty = proof_pack_score_with_governance_penalty(
        pack, governance_blocked=governance_blocked
    )

    publish_eligible = complete and score_with_penalty >= 70

    if publish_eligible:
        gov = GovernanceDecision.REQUIRE_APPROVAL  # founder always approves publish
    elif score_with_penalty >= 50:
        gov = GovernanceDecision.ALLOW_WITH_REVIEW
    else:
        gov = GovernanceDecision.BLOCK

    return ProofPackDecision(
        governance_decision=gov,
        score=score,
        score_with_penalty=score_with_penalty,
        sections_complete=complete,
        missing_sections=tuple(missing),
        publish_eligible=publish_eligible,
        rationale_ar=(
            f"Proof Pack: درجة={score}، بعد الجزاء={score_with_penalty}. "
            f"النشر {'ممكن بانتظار موافقة المؤسس' if publish_eligible else 'غير مسموح بعد'}."
        ),
        rationale_en=(
            f"Proof Pack: score={score}, after penalty={score_with_penalty}. "
            f"Publish {'allowed pending founder approval' if publish_eligible else 'not yet permitted'}."
        ),
        timestamp=_utc_now_iso(),
    )


# ---------------------------------------------------------------------------
# Retainer assessment
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class RetainerDecision:
    governance_decision: GovernanceDecision
    eligible: bool
    adoption_band: str
    adoption_score_value: int
    next_offer: str | None
    blockers: tuple[str, ...]
    rationale_ar: str
    rationale_en: str
    timestamp: str


def assess_retainer(
    *,
    adoption_dims: AdoptionDimensions,
    customer_id: str,
    proof_score: int,
    workflow_owner_exists: bool,
    monthly_workflow_exists: bool,
    governance_risk_controlled: bool,
) -> RetainerDecision:
    """Decide if a customer is retainer-ready (Wave 2 eligibility).

    Uses adoption_os.wave2_retainer_eligibility for the canonical check.
    """
    score = adoption_score(adoption_dims)
    band = adoption_band(score)

    eligible, blockers = wave2_retainer_eligibility(
        proof_score=proof_score,
        adoption_score=score,
        workflow_owner_exists=workflow_owner_exists,
        monthly_workflow_exists=monthly_workflow_exists,
        governance_risk_controlled=governance_risk_controlled,
    )

    if eligible:
        gov = GovernanceDecision.REQUIRE_APPROVAL
        next_offer = client_expansion_recommendation("expansion_pull_strong")
    else:
        gov = GovernanceDecision.BLOCK
        next_offer = None

    return RetainerDecision(
        governance_decision=gov,
        eligible=eligible,
        adoption_band=band,
        adoption_score_value=score,
        next_offer=next_offer,
        blockers=tuple(blockers),
        rationale_ar=(
            f"تبني العميل={band} (درجة={score}). الأهلية للاحتفاظ: "
            f"{'نعم' if eligible else 'لا — استكمل المتطلبات أولاً'}."
        ),
        rationale_en=(
            f"Adoption band={band} (score={score}). Retainer eligibility: "
            f"{'yes' if eligible else 'no — finish the gates first'}."
        ),
        timestamp=_utc_now_iso(),
    )


__all__ = [
    "DISCLAIMER_AR_EN",
    "LeadDecision",
    "OutreachDraftDecision",
    "PaymentDecision",
    "ProofPackDecision",
    "RetainerDecision",
    "assemble_proof_pack",
    "assess_retainer",
    "audit_outreach_draft",
    "process_lead",
    "process_payment",
]
