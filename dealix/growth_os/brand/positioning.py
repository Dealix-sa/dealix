"""Brand positioning — hero line + four audience messages (section 48)."""

from __future__ import annotations

from typing import Final

from pydantic import BaseModel, ConfigDict, Field

from dealix.growth_os.schemas import BilingualLabel


class AudienceMessage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    audience_key: str = Field(..., min_length=1)
    headline: BilingualLabel
    subhead: BilingualLabel
    proof_anchor: BilingualLabel


class BrandPositioning(BaseModel):
    model_config = ConfigDict(extra="forbid")

    hero_line: BilingualLabel
    audiences: list[AudienceMessage] = Field(min_length=4, max_length=4)


BRAND_POSITIONING: Final[BrandPositioning] = BrandPositioning(
    hero_line=BilingualLabel(
        ar="منصة الذكاء الاصطناعي التشغيلية التي تتحول إلى إيراد موثّق",
        en="The operational AI platform that turns into verified revenue",
    ),
    audiences=[
        AudienceMessage(
            audience_key="founders",
            headline=BilingualLabel(
                ar="قرارات أوضح بإيراد موثّق",
                en="Clearer decisions backed by verified revenue",
            ),
            subhead=BilingualLabel(
                ar="لوحة المؤسس + Revenue Hunter",
                en="Founder dashboard plus Revenue Hunter",
            ),
            proof_anchor=BilingualLabel(
                ar="نتائج موثّقة بفواتير وعقود",
                en="Outcomes backed by invoices and agreements",
            ),
        ),
        AudienceMessage(
            audience_key="enterprise",
            headline=BilingualLabel(
                ar="حوكمة AI متوافقة مع PDPL",
                en="AI governance aligned with PDPL",
            ),
            subhead=BilingualLabel(
                ar="منصة تحكم بصلاحيات وموافقات",
                en="Control plane with permissions and approvals",
            ),
            proof_anchor=BilingualLabel(
                ar="جلسات تنفيذية + Policy Map",
                en="Executive briefings plus a policy map",
            ),
        ),
        AudienceMessage(
            audience_key="agencies",
            headline=BilingualLabel(
                ar="AI تحت علامة وكالتك",
                en="AI under your agency brand",
            ),
            subhead=BilingualLabel(
                ar="برنامج White-label + Revshare",
                en="White-label program with revenue share",
            ),
            proof_anchor=BilingualLabel(
                ar="قوالب تسليم + ProofPack",
                en="Delivery templates and ProofPack",
            ),
        ),
        AudienceMessage(
            audience_key="ai_users_governance",
            headline=BilingualLabel(
                ar="استخدم AI مع موافقات وسجلات",
                en="Use AI with approvals and audit logs",
            ),
            subhead=BilingualLabel(
                ar="حوكمة، Approvals، تدقيق",
                en="Governance, approvals, audit",
            ),
            proof_anchor=BilingualLabel(
                ar="مصفوفة سياسات قابلة للتدقيق",
                en="Auditable policy matrix",
            ),
        ),
    ],
)


__all__ = ["BRAND_POSITIONING", "AudienceMessage", "BrandPositioning"]
