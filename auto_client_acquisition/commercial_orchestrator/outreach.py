"""Outreach draft renderer — builds a COMPANY-LEVEL, bilingual (AR + EN),
doctrine-safe first-touch draft inviting a prospect to the free diagnostic.

Doctrine properties (enforced by tests/test_no_*):
- Company-level only. No personal names, emails, or phone numbers.
- A sector observation is framed as a HYPOTHESIS, never a claim about the
  specific company's internals.
- No guaranteed outcomes. Carries the same "estimated ≠ guaranteed" disclaimer
  as the proposal renderer.
- This is a DRAFT. It is never sent by this module — it is queued for founder
  approval. The closing line states that explicitly.

Pure function, no I/O, no LLM call — deterministic and auditable.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

# Bilingual, neutral sector labels for the greeting line.
_SECTOR_AR: dict[str, str] = {
    "real_estate": "العقار",
    "logistics": "اللوجستيات",
    "healthcare": "الرعاية الصحية",
    "training": "التدريب",
    "engineering": "الهندسة",
    "construction": "المقاولات",
    "facilities_management": "إدارة المرافق",
    "marketing_agency": "التسويق",
    "ecommerce": "التجارة الإلكترونية",
    "food_and_beverage": "المطاعم والضيافة الغذائية",
    "wholesale_distribution": "التوزيع والجملة",
    "manufacturing": "التصنيع",
    "professional_services": "الخدمات المهنية",
    "insurance": "التأمين",
    "automotive": "السيارات",
    "hospitality": "الضيافة",
    "oil_gas_services": "خدمات النفط والغاز",
    "technology": "التقنية",
    "project_management": "إدارة المشاريع",
    "education": "التعليم",
    "fintech": "التقنية المالية",
    "agritech": "التقنية الزراعية",
    "b2b_services": "خدمات الأعمال",
}

_DISCLAIMER = "_Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة._"
_DRAFT_FOOTER = (
    "_This is a draft prepared for founder review. Nothing is sent until a human "
    "approves it and confirms the recipient. / هذه مسوّدة للمراجعة. لا يُرسل شيء قبل "
    "موافقة بشرية وتأكيد جهة التواصل._"
)


@dataclass
class OutreachContext:
    company_name: str
    sector: str
    city: str = ""
    name_ar: str = ""
    pain_hypothesis_en: str = ""
    pain_hypothesis_ar: str = ""
    icp_band: str = "warm"
    diagnostic_offer: str = "free_ai_ops_diagnostic"
    extra: dict[str, Any] = field(default_factory=dict)

    def sector_ar(self) -> str:
        return _SECTOR_AR.get(self.sector, "الأعمال")

    def display_ar(self) -> str:
        return self.name_ar or self.company_name


def render_outreach_draft(ctx: OutreachContext) -> dict[str, str]:
    """Return {subject_en, subject_ar, body_md} for a first-touch draft."""
    sector_en = ctx.sector.replace("_", " ")
    pain_en = ctx.pain_hypothesis_en or (
        f"many {sector_en} companies lose revenue in scattered follow-up"
    )
    pain_ar = ctx.pain_hypothesis_ar or (
        f"كثير من شركات {ctx.sector_ar()} تفقد إيراداً في تشتّت المتابعة"
    )

    subject_en = f"A quick revenue-intelligence read for {ctx.company_name}"
    subject_ar = f"قراءة سريعة لذكاء الإيراد لـ {ctx.display_ar()}"

    body_md = f"""# Outreach Draft — {ctx.company_name}

**To the team at {ctx.company_name}** ({sector_en}{', ' + ctx.city if ctx.city else ''})

Hello — I'm reaching out from **Dealix**, a Saudi-first revenue-intelligence
company. We help B2B teams find where revenue quietly leaks and turn scattered
follow-up into a ranked, governed plan — in Arabic and English, PDPL-aware, and
approval-first (we never send anything on your behalf without your sign-off).

A common pattern we see in **{sector_en}**: {pain_en}. We don't assume this is
true for you — that's exactly what our **free AI Ops Diagnostic** checks: a
one-page read of where the biggest revenue opportunities likely are, with three
concrete next steps, at no cost and no commitment.

If useful, reply and we'll share the one-pager — or book the free diagnostic.

{_DISCLAIMER}

---

# مسوّدة تواصل — {ctx.display_ar()}

**إلى فريق {ctx.display_ar()}** ({ctx.sector_ar()}{'، ' + ctx.city if ctx.city else ''})

السلام عليكم — أتواصل معكم من **Dealix**، شركة سعودية لذكاء الإيراد. نساعد فرق
B2B على اكتشاف أين يتسرّب الإيراد بهدوء، وتحويل المتابعة المبعثرة إلى خطة مرتّبة
ومحوكمة — بالعربية والإنجليزية، متوافقة مع PDPL، وبمبدأ الموافقة أولاً (لا نرسل
أي شيء نيابةً عنكم دون اعتمادكم).

نمط شائع في **{ctx.sector_ar()}**: {pain_ar}. لا نفترض أن هذا ينطبق عليكم — وهذا
بالضبط ما يفحصه **التشخيص المجاني للعمليات بالذكاء الاصطناعي**: صفحة واحدة تبيّن
أين تُرجَّح أكبر فرص الإيراد، مع ثلاث خطوات تالية واضحة، بلا تكلفة وبلا التزام.

إن كان مفيداً، ردّوا ونشارككم الصفحة — أو احجزوا التشخيص المجاني.

{_DISCLAIMER}

---

{_DRAFT_FOOTER}
"""
    return {
        "subject_en": subject_en,
        "subject_ar": subject_ar,
        "body_md": body_md,
    }


__all__ = ["OutreachContext", "render_outreach_draft"]
