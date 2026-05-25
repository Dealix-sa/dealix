"""Three core revenue funnels with their staged steps."""

from __future__ import annotations

from typing import Final

from pydantic import BaseModel, ConfigDict, Field


class FunnelStage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    key: str
    label_ar: str
    label_en: str
    success_signal: str


class Funnel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    key: str
    label_ar: str
    label_en: str
    target_icp_keys: list[str]
    primary_offer_key: str
    stages: list[FunnelStage] = Field(default_factory=list)


FUNNELS: Final[dict[str, Funnel]] = {
    "revenue_hunter": Funnel(
        key="revenue_hunter",
        label_ar="مسار صياد الإيراد",
        label_en="Revenue Hunter Funnel",
        target_icp_keys=["b2b_smb", "founders"],
        primary_offer_key="revenue_hunter",
        stages=[
            FunnelStage(key="awareness", label_ar="الوعي", label_en="Awareness", success_signal="page_view_or_inbound"),
            FunnelStage(key="diagnostic_request", label_ar="طلب تشخيص", label_en="Diagnostic Request", success_signal="diagnostic_form_submitted"),
            FunnelStage(key="diagnostic_delivered", label_ar="تسليم التشخيص", label_en="Diagnostic Delivered", success_signal="report_acknowledged"),
            FunnelStage(key="offer", label_ar="العرض", label_en="Offer", success_signal="offer_sent"),
            FunnelStage(key="commit", label_ar="الالتزام", label_en="Commit", success_signal="signed_agreement"),
            FunnelStage(key="retainer", label_ar="الـ retainer", label_en="Retainer", success_signal="retainer_active"),
        ],
    ),
    "ai_trust_kit": Funnel(
        key="ai_trust_kit",
        label_ar="مسار حزمة الثقة في AI",
        label_en="AI Trust Kit Funnel",
        target_icp_keys=["enterprise", "ai_users_governance"],
        primary_offer_key="ai_trust_kit",
        stages=[
            FunnelStage(key="risk_inquiry", label_ar="استفسار مخاطر", label_en="Risk Inquiry", success_signal="risk_question_logged"),
            FunnelStage(key="kit_request", label_ar="طلب الحزمة", label_en="Kit Request", success_signal="kit_form_submitted"),
            FunnelStage(key="walkthrough", label_ar="جلسة استعراض", label_en="Walkthrough", success_signal="walkthrough_held"),
            FunnelStage(key="policy_map", label_ar="خريطة السياسة", label_en="Policy Map", success_signal="policy_map_accepted"),
            FunnelStage(key="purchase", label_ar="الشراء", label_en="Purchase", success_signal="payment_received"),
            FunnelStage(key="governance_retainer", label_ar="حوكمة بالشهر", label_en="Governance Retainer", success_signal="retainer_active"),
        ],
    ),
    "agency_white_label": Funnel(
        key="agency_white_label",
        label_ar="مسار وكالة بعلامة بيضاء",
        label_en="Agency White-label Funnel",
        target_icp_keys=["agencies"],
        primary_offer_key="agency_white_label",
        stages=[
            FunnelStage(key="agency_inquiry", label_ar="استفسار وكالة", label_en="Agency Inquiry", success_signal="inquiry_received"),
            FunnelStage(key="discovery", label_ar="جلسة اكتشاف", label_en="Discovery", success_signal="discovery_held"),
            FunnelStage(key="white_label_brief", label_ar="ملف التسليم", label_en="White-label Brief", success_signal="brief_accepted"),
            FunnelStage(key="pilot_client", label_ar="عميل تجريبي", label_en="Pilot Client", success_signal="pilot_signed"),
            FunnelStage(key="expansion", label_ar="التوسّع", label_en="Expansion", success_signal="additional_clients_signed"),
            FunnelStage(key="program_membership", label_ar="عضوية البرنامج", label_en="Program Membership", success_signal="membership_active"),
        ],
    ),
}


def list_funnels() -> list[Funnel]:
    return list(FUNNELS.values())


def get_funnel(key: str) -> Funnel:
    if key not in FUNNELS:
        raise KeyError(f"unknown funnel key: {key!r}")
    return FUNNELS[key]


__all__ = ["FUNNELS", "Funnel", "FunnelStage", "get_funnel", "list_funnels"]
