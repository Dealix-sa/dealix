"""Static ICP matrix — the 7 Ideal Customer Profiles Dealix sells into.

Each ICP is metadata only. No PII, no real customer names.
"""

from __future__ import annotations

from typing import Final

from pydantic import BaseModel, ConfigDict, Field


class ICPDefinition(BaseModel):
    model_config = ConfigDict(extra="forbid")

    key: str = Field(..., min_length=1)
    name_ar: str
    name_en: str
    primary_pain_ar: str
    primary_pain_en: str
    primary_offer: str
    decision_makers: list[str]
    typical_arr_band_usd: tuple[int, int]
    proof_assets: list[str]
    disqualifiers: list[str]


ICP_MATRIX: Final[dict[str, ICPDefinition]] = {
    "agencies": ICPDefinition(
        key="agencies",
        name_ar="وكالات التسويق والإعلام",
        name_en="Marketing and Media Agencies",
        primary_pain_ar="حاجة لتقديم AI موثق للعميل دون مخاطر",
        primary_pain_en="Need to deliver governed AI to clients without risk",
        primary_offer="agency_white_label",
        decision_makers=["founder", "head_of_strategy", "head_of_delivery"],
        typical_arr_band_usd=(12_000, 120_000),
        proof_assets=["white_label_brief", "case_template", "governance_one_pager"],
        disqualifiers=["pure_creative_no_ops", "no_recurring_clients"],
    ),
    "b2b_smb": ICPDefinition(
        key="b2b_smb",
        name_ar="شركات B2B متوسطة وصغيرة",
        name_en="B2B SMB (10-200 employees)",
        primary_pain_ar="قنوات بيع بطيئة وغير موثقة",
        primary_pain_en="Slow, unverified sales channels",
        primary_offer="revenue_hunter",
        decision_makers=["ceo", "cco", "head_of_sales"],
        typical_arr_band_usd=(6_000, 60_000),
        proof_assets=["revenue_diagnostic", "proof_pack", "roi_sheet"],
        disqualifiers=["pre_revenue", "no_sales_function"],
    ),
    "founders": ICPDefinition(
        key="founders",
        name_ar="مؤسسون ومالكون",
        name_en="Founders and Owners",
        primary_pain_ar="القرارات تعتمد على الحدس بدون لوحة موثوقة",
        primary_pain_en="Decisions driven by intuition with no trusted dashboard",
        primary_offer="founder_dashboard",
        decision_makers=["founder"],
        typical_arr_band_usd=(3_000, 24_000),
        proof_assets=["founder_dashboard_sample", "decision_log_template"],
        disqualifiers=["no_revenue_data", "refuses_metrics"],
    ),
    "ai_users_governance": ICPDefinition(
        key="ai_users_governance",
        name_ar="مستخدمو AI يحتاجون حوكمة",
        name_en="AI Users Needing Governance",
        primary_pain_ar="استخدام مفتوح بدون موافقات أو سجلات",
        primary_pain_en="Open AI usage without approvals or audit trails",
        primary_offer="ai_governance_kit",
        decision_makers=["cto", "head_of_data", "head_of_compliance"],
        typical_arr_band_usd=(8_000, 80_000),
        proof_assets=["governance_kit", "approval_log_template", "policy_matrix"],
        disqualifiers=["no_ai_usage", "no_policy_owner"],
    ),
    "enterprise": ICPDefinition(
        key="enterprise",
        name_ar="مؤسسات كبيرة",
        name_en="Enterprise (200+ employees)",
        primary_pain_ar="تحتاج خطة AI موثقة مع PDPL",
        primary_pain_en="Need governed AI plan aligned with PDPL",
        primary_offer="enterprise_program",
        decision_makers=["cio", "cdo", "head_of_risk"],
        typical_arr_band_usd=(60_000, 600_000),
        proof_assets=["enterprise_program_brief", "pdpl_alignment_map", "rfp_response_kit"],
        disqualifiers=["no_executive_sponsor", "no_budget_cycle"],
    ),
    "consultants": ICPDefinition(
        key="consultants",
        name_ar="مستشارون مستقلون",
        name_en="Independent Consultants",
        primary_pain_ar="حاجة لأدوات احترافية لتسليم نتائج",
        primary_pain_en="Need professional toolkit to deliver outcomes",
        primary_offer="consultant_toolkit",
        decision_makers=["consultant_owner"],
        typical_arr_band_usd=(2_400, 18_000),
        proof_assets=["consultant_toolkit", "engagement_template"],
        disqualifiers=["non_recurring_only"],
    ),
    "training_providers": ICPDefinition(
        key="training_providers",
        name_ar="مزودو التدريب",
        name_en="Training Providers",
        primary_pain_ar="حاجة لمحتوى وإثبات نتائج للمتدربين",
        primary_pain_en="Need curriculum and outcome evidence for trainees",
        primary_offer="training_curriculum_kit",
        decision_makers=["academic_director", "head_of_curriculum"],
        typical_arr_band_usd=(5_000, 40_000),
        proof_assets=["curriculum_kit", "trainee_outcome_template"],
        disqualifiers=["no_certification_path"],
    ),
}


def list_icps() -> list[ICPDefinition]:
    """Return all ICPs in stable insertion order."""
    return list(ICP_MATRIX.values())


def get_icp(key: str) -> ICPDefinition:
    """Return a single ICP by key. Raises KeyError if not found."""
    if key not in ICP_MATRIX:
        raise KeyError(f"unknown ICP key: {key!r}")
    return ICP_MATRIX[key]


__all__ = ["ICP_MATRIX", "ICPDefinition", "get_icp", "list_icps"]
