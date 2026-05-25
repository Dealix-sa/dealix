"""Revenue portfolio — five buckets, twenty-five plus streams (section 44)."""

from __future__ import annotations

from typing import Final

from pydantic import BaseModel, ConfigDict, Field

from dealix.growth_os.streams.stream_card import RevenueStreamCard

STREAM_BUCKETS: Final[tuple[str, ...]] = (
    "fast",
    "monthly",
    "partner",
    "enterprise",
    "platform",
)


def _card(
    bucket: str,
    key: str,
    ar: str,
    en: str,
    *,
    repeatability: str = "occasional",
    risk: str = "medium",
    margin_pct: float = 0.4,
    retainer_potential: float = 0.4,
) -> RevenueStreamCard:
    return RevenueStreamCard(
        stream_key=key,
        bucket=bucket,
        label_ar=ar,
        label_en=en,
        repeatability=repeatability,  # type: ignore[arg-type]
        risk=risk,  # type: ignore[arg-type]
        margin_pct=margin_pct,
        retainer_potential=retainer_potential,
    )


# 25+ streams across the 5 buckets. Numbers are defaults; actuals come at runtime.
_STREAMS: Final[tuple[RevenueStreamCard, ...]] = (
    # ── Fast (one-off, quick close) ─────────────────────────────────
    _card("fast", "revenue_diagnostic", "تشخيص الإيراد", "Revenue Diagnostic", repeatability="one_off", risk="low", margin_pct=0.65, retainer_potential=0.5),
    _card("fast", "ai_trust_kit", "حزمة الثقة في AI", "AI Trust Kit", repeatability="one_off", risk="low", margin_pct=0.60, retainer_potential=0.4),
    _card("fast", "mcp_risk_review", "مراجعة مخاطر MCP", "MCP Risk Review", repeatability="one_off", risk="low", margin_pct=0.55, retainer_potential=0.3),
    _card("fast", "governance_one_pager", "صفحة حوكمة واحدة", "Governance One-Pager", repeatability="one_off", risk="low", margin_pct=0.7, retainer_potential=0.2),
    _card("fast", "executive_briefing", "إحاطة تنفيذية", "Executive Briefing", repeatability="occasional", risk="low", margin_pct=0.6, retainer_potential=0.4),
    # ── Monthly (recurring services) ────────────────────────────────
    _card("monthly", "revenue_hunter_retainer", "صياد الإيراد بالشهر", "Revenue Hunter Retainer", repeatability="retainer_native", risk="low", margin_pct=0.55, retainer_potential=0.95),
    _card("monthly", "ai_governance_retainer", "حوكمة AI بالشهر", "AI Governance Retainer", repeatability="retainer_native", risk="low", margin_pct=0.5, retainer_potential=0.9),
    _card("monthly", "founder_dashboard_subscription", "اشتراك لوحة المؤسس", "Founder Dashboard Subscription", repeatability="recurring", risk="low", margin_pct=0.7, retainer_potential=0.85),
    _card("monthly", "market_radar_subscription", "اشتراك رادار السوق", "Market Radar Subscription", repeatability="recurring", risk="low", margin_pct=0.75, retainer_potential=0.8),
    _card("monthly", "consultant_toolkit", "حزمة المستشار", "Consultant Toolkit", repeatability="recurring", risk="low", margin_pct=0.65, retainer_potential=0.7),
    # ── Partner-led ─────────────────────────────────────────────────
    _card("partner", "agency_white_label", "منصة بعلامة الوكالة", "Agency White-label", repeatability="retainer_native", risk="medium", margin_pct=0.45, retainer_potential=0.9),
    _card("partner", "agency_program_membership", "عضوية برنامج الوكالات", "Agency Program Membership", repeatability="recurring", risk="low", margin_pct=0.7, retainer_potential=0.8),
    _card("partner", "training_provider_kit", "حزمة مزود التدريب", "Training Provider Kit", repeatability="recurring", risk="low", margin_pct=0.65, retainer_potential=0.7),
    _card("partner", "referral_revshare", "حصة الإحالة", "Referral Revshare", repeatability="occasional", risk="low", margin_pct=0.9, retainer_potential=0.4),
    _card("partner", "channel_enablement_workshop", "ورشة تمكين القنوات", "Channel Enablement Workshop", repeatability="occasional", risk="medium", margin_pct=0.55, retainer_potential=0.5),
    # ── Enterprise ──────────────────────────────────────────────────
    _card("enterprise", "enterprise_program", "برنامج المؤسسات", "Enterprise Program", repeatability="retainer_native", risk="medium", margin_pct=0.4, retainer_potential=0.95),
    _card("enterprise", "pdpl_alignment_engagement", "التوافق مع PDPL", "PDPL Alignment Engagement", repeatability="occasional", risk="medium", margin_pct=0.5, retainer_potential=0.6),
    _card("enterprise", "ai_governance_kit_enterprise", "حزمة حوكمة AI للمؤسسات", "AI Governance Kit (Enterprise)", repeatability="recurring", risk="medium", margin_pct=0.5, retainer_potential=0.8),
    _card("enterprise", "rfp_response_kit", "حزمة الرد على RFP", "RFP Response Kit", repeatability="occasional", risk="medium", margin_pct=0.45, retainer_potential=0.5),
    _card("enterprise", "executive_quarterly_review", "مراجعة تنفيذية فصلية", "Executive Quarterly Review", repeatability="recurring", risk="low", margin_pct=0.6, retainer_potential=0.7),
    # ── Platform ────────────────────────────────────────────────────
    _card("platform", "agentic_control_plane_seats", "مقاعد منصة التحكم", "Agentic Control Plane Seats", repeatability="recurring", risk="low", margin_pct=0.8, retainer_potential=0.9),
    _card("platform", "proof_pack_credits", "أرصدة ProofPack", "ProofPack Credits", repeatability="occasional", risk="low", margin_pct=0.8, retainer_potential=0.5),
    _card("platform", "policy_matrix_api", "API مصفوفة السياسات", "Policy Matrix API", repeatability="recurring", risk="low", margin_pct=0.85, retainer_potential=0.8),
    _card("platform", "approvals_workflow_addon", "إضافة سير الموافقات", "Approvals Workflow Add-on", repeatability="recurring", risk="low", margin_pct=0.8, retainer_potential=0.8),
    _card("platform", "audit_export_addon", "إضافة تصدير التدقيق", "Audit Export Add-on", repeatability="recurring", risk="low", margin_pct=0.85, retainer_potential=0.7),
    _card("platform", "marketplace_partner_revshare", "حصة شركاء السوق", "Marketplace Partner Revshare", repeatability="recurring", risk="medium", margin_pct=0.6, retainer_potential=0.7),
)


class RevenuePortfolio(BaseModel):
    model_config = ConfigDict(extra="forbid")

    buckets: tuple[str, ...] = STREAM_BUCKETS
    streams: list[RevenueStreamCard] = Field(default_factory=list)

    def by_bucket(self) -> dict[str, list[RevenueStreamCard]]:
        out: dict[str, list[RevenueStreamCard]] = {b: [] for b in self.buckets}
        for s in self.streams:
            out.setdefault(s.bucket, []).append(s)
        return out


REVENUE_PORTFOLIO: Final[RevenuePortfolio] = RevenuePortfolio(streams=list(_STREAMS))


def list_streams() -> list[RevenueStreamCard]:
    return list(REVENUE_PORTFOLIO.streams)


__all__ = [
    "REVENUE_PORTFOLIO",
    "STREAM_BUCKETS",
    "RevenuePortfolio",
    "list_streams",
]
