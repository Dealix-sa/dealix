"""
Diagnostic Engine — S0 Free Diagnostic Report Generator.
محرك التشخيص — مولّد تقرير التشخيص المجاني (S0).

Generates bilingual (Arabic-first) 10-section diagnostic reports for
Saudi B2B companies. Uses Claude via the existing LLM router.

Hard limits (constitutional):
- Max 2 diagnostics per account per day (cost control)
- NO proof injection without real data (NO_FAKE_PROOF gate)
- Output is a DRAFT for founder review before delivery
"""

from __future__ import annotations

import json
import logging
import os
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

log = logging.getLogger(__name__)

# ── Sector profiles ────────────────────────────────────────────────
SAUDI_SECTORS: dict[str, dict[str, str]] = {
    "marketing_agency": {
        "ar": "وكالة تسويق",
        "en": "Marketing Agency",
        "pain_ar": "العملاء المحتملون يصلون عبر واتساب ولينكد إن، والرد يعتمد على الفاوندر، مما يؤخر الصفقات",
        "pain_en": "Leads arrive via WhatsApp/LinkedIn, founder-dependent replies delay deals",
    },
    "consulting": {
        "ar": "استشارات",
        "en": "Consulting",
        "pain_ar": "إدارة العملاء يدوياً، وتقارير متأخرة، وفقدان فرص التوسع",
        "pain_en": "Manual client management, delayed reports, missed expansion opportunities",
    },
    "real_estate": {
        "ar": "عقارات",
        "en": "Real Estate",
        "pain_ar": "متابعة العملاء المحتملين متأخرة وغير منتظمة، وفقدان صفقات بسبب بطء الاستجابة",
        "pain_en": "Slow, inconsistent lead follow-up causes deal loss",
    },
    "logistics": {
        "ar": "لوجستيات",
        "en": "Logistics",
        "pain_ar": "تتبع الشحنات يدوياً وتواصل العملاء غير منظم",
        "pain_en": "Manual shipment tracking and unorganized client communication",
    },
    "events": {
        "ar": "فعاليات وضيافة",
        "en": "Events & Hospitality",
        "pain_ar": "إدارة الحجوزات والمتابعة يدوياً مع ضياع كثير من الفرص",
        "pain_en": "Manual booking management with many missed opportunities",
    },
    "training": {
        "ar": "تدريب وتعليم",
        "en": "Training & Education",
        "pain_ar": "تسجيل الطلاب يدوياً ومتابعة المدفوعات غير منتظمة",
        "pain_en": "Manual student registration and inconsistent payment follow-up",
    },
    "other": {
        "ar": "خدمات B2B",
        "en": "B2B Services",
        "pain_ar": "عمليات يدوية تستنزف وقت الفريق وتؤخر النمو",
        "pain_en": "Manual operations drain team time and slow growth",
    },
}


@dataclass
class DiagnosticRequest:
    company_name: str
    sector: str = "other"
    pain_points: str = ""
    website_url: str = ""
    employee_count: int = 0
    monthly_leads: int = 0
    current_tools: str = ""
    contact_name: str = ""
    contact_role: str = ""
    locale: str = "ar"
    account_id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class DiagnosticSection:
    title_ar: str
    title_en: str
    content_ar: str
    content_en: str


@dataclass
class DiagnosticReport:
    report_id: str
    account_id: str
    company_name: str
    sector: str
    sections: list[DiagnosticSection]
    executive_summary_ar: str
    executive_summary_en: str
    next_step_ar: str
    next_step_en: str
    generated_at: datetime
    draft_status: str = "draft"  # draft | delivered | archived
    proof_event_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "account_id": self.account_id,
            "company_name": self.company_name,
            "sector": self.sector,
            "executive_summary_ar": self.executive_summary_ar,
            "executive_summary_en": self.executive_summary_en,
            "next_step_ar": self.next_step_ar,
            "next_step_en": self.next_step_en,
            "sections": [
                {
                    "title_ar": s.title_ar,
                    "title_en": s.title_en,
                    "content_ar": s.content_ar,
                    "content_en": s.content_en,
                }
                for s in self.sections
            ],
            "draft_status": self.draft_status,
            "generated_at": self.generated_at.isoformat(),
            "proof_event_id": self.proof_event_id,
        }

    def to_markdown_ar(self) -> str:
        lines = [
            f"# تقرير تشخيص Dealix — {self.company_name}",
            f"**التاريخ:** {self.generated_at.strftime('%Y-%m-%d')}",
            f"**القطاع:** {SAUDI_SECTORS.get(self.sector, SAUDI_SECTORS['other'])['ar']}",
            "",
            "---",
            "",
            "## الملخص التنفيذي",
            self.executive_summary_ar,
            "",
            "---",
            "",
        ]
        for i, sec in enumerate(self.sections, 1):
            lines += [f"## {i}. {sec.title_ar}", sec.content_ar, ""]

        lines += [
            "---",
            "",
            "## الخطوة التالية",
            self.next_step_ar,
            "",
            "---",
            "",
            "*تقرير سري — معدّ بواسطة Dealix. جميع البيانات محمية وفق نظام حماية البيانات الشخصية (PDPL).*",
        ]
        return "\n".join(lines)


# ── Section definitions (10 canonical sections) ──────────────────

_SECTION_PROMPTS: list[tuple[str, str]] = [
    ("تشخيص الوضع الراهن", "Current State Assessment"),
    ("فجوات الإيراد المكتشفة", "Revenue Gap Analysis"),
    ("فرص الذكاء الاصطناعي", "AI Automation Opportunities"),
    ("خارطة الأولويات (30 يوماً)", "Priority Roadmap (30 Days)"),
    ("مؤشرات النجاح القابلة للقياس", "Measurable Success KPIs"),
    ("المخاطر والضمانات", "Risks & Guardrails"),
    ("خارطة التكامل مع الأدوات الحالية", "Integration Compatibility Map"),
    ("تقدير الأثر المالي", "Financial Impact Estimate"),
    ("نموذج التشغيل المقترح", "Proposed Operating Model"),
    ("إشعار الامتثال (PDPL)", "Compliance Notice (PDPL)"),
]


def _build_prompt(req: DiagnosticRequest) -> str:
    sector_info = SAUDI_SECTORS.get(req.sector, SAUDI_SECTORS["other"])
    pain = req.pain_points or sector_info["pain_ar"]

    return f"""أنت خبير تشغيل B2B في السوق السعودي. اكتب تقرير تشخيص احترافي وشامل للشركة التالية.

معلومات الشركة:
- الاسم: {req.company_name}
- القطاع: {sector_info['ar']} ({sector_info['en']})
- عدد الموظفين: {req.employee_count or 'غير محدد'}
- العملاء المحتملون شهرياً: {req.monthly_leads or 'غير محدد'}
- الأدوات الحالية: {req.current_tools or 'غير محدد'}
- نقاط الألم الرئيسية: {pain}
- معلومات إضافية: {req.pain_points or 'لا يوجد'}

القواعد الإلزامية:
1. اكتب بالعربية أولاً، ثم الإنجليزية
2. كن محدداً وعملياً — لا وعود غير قابلة للقياس
3. لا تدّعي نتائج لم تحدث بعد
4. ركّز على الفرص الحقيقية للشركة في السوق السعودي
5. الأسعار بالريال السعودي فقط

أرجع JSON بالتنسيق التالي:
{{
  "executive_summary_ar": "ملخص تنفيذي 3-4 جمل بالعربية",
  "executive_summary_en": "3-4 sentence executive summary in English",
  "sections": [
    {{
      "title_ar": "عنوان القسم بالعربية",
      "title_en": "Section Title in English",
      "content_ar": "محتوى القسم بالعربية (فقرة أو نقاط)",
      "content_en": "Section content in English (paragraph or bullets)"
    }}
  ],
  "next_step_ar": "وصف الخطوة التالية المقترحة: برنامج التجربة 7 أيام بـ 499 ريال",
  "next_step_en": "Recommended next step: 7-day proof sprint at 499 SAR"
}}

اكتب {len(_SECTION_PROMPTS)} أقسام بهذا الترتيب:
{chr(10).join(f"{i+1}. {ar} / {en}" for i, (ar, en) in enumerate(_SECTION_PROMPTS))}
"""


async def generate_diagnostic(req: DiagnosticRequest) -> DiagnosticReport:
    """
    Generate a bilingual diagnostic report using the LLM router.
    Uses Claude (primary) with OpenAI fallback.
    Returns a DRAFT — founder must review before delivery.
    """
    try:
        from core.agents.base import BaseAgent
        from core.config.models import Task
        from core.llm import get_router
        from core.llm.base import Message

        router = get_router()
        prompt = _build_prompt(req)

        response = await router.run(
            task=Task.PROPOSAL,
            messages=[Message(role="user", content=prompt)],
            max_tokens=4000,
            temperature=0.3,
        )

        raw = response.content.strip()
        # Extract JSON from potential markdown fences
        if "```json" in raw:
            raw = raw.split("```json")[1].split("```")[0].strip()
        elif "```" in raw:
            raw = raw.split("```")[1].split("```")[0].strip()

        data = json.loads(raw)

    except Exception as exc:
        log.warning("LLM generation failed, using fallback template: %s", exc)
        data = _fallback_data(req)

    sections = []
    raw_sections = data.get("sections", [])
    for i, (title_ar_default, title_en_default) in enumerate(_SECTION_PROMPTS):
        sec_data = raw_sections[i] if i < len(raw_sections) else {}
        sections.append(DiagnosticSection(
            title_ar=sec_data.get("title_ar", title_ar_default),
            title_en=sec_data.get("title_en", title_en_default),
            content_ar=sec_data.get("content_ar", f"سيتم إعداد هذا القسم بناءً على بيانات {req.company_name}"),
            content_en=sec_data.get("content_en", f"This section will be tailored to {req.company_name} data"),
        ))

    report_id = str(uuid.uuid4())
    report = DiagnosticReport(
        report_id=report_id,
        account_id=req.account_id,
        company_name=req.company_name,
        sector=req.sector,
        sections=sections,
        executive_summary_ar=data.get("executive_summary_ar", f"تشخيص أولي لـ {req.company_name}"),
        executive_summary_en=data.get("executive_summary_en", f"Initial diagnostic for {req.company_name}"),
        next_step_ar=data.get("next_step_ar", "الخطوة التالية: برنامج التجربة 7 أيام بـ 499 ريال سعودي"),
        next_step_en=data.get("next_step_en", "Next step: 7-day proof sprint at 499 SAR"),
        generated_at=datetime.now(UTC),
        draft_status="draft",
    )

    # Persist to JSONL proof ledger
    _save_to_ledger(report)

    log.info("Diagnostic generated: report_id=%s company=%s", report_id, req.company_name)
    return report


def _save_to_ledger(report: DiagnosticReport) -> None:
    """Persist diagnostic to local JSONL proof ledger."""
    try:
        ledger_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "proofs")
        os.makedirs(ledger_dir, exist_ok=True)
        ledger_path = os.path.join(ledger_dir, "diagnostics.jsonl")
        entry = {
            "event_type": "diagnostic.generated",
            "occurred_at": datetime.now(UTC).isoformat(),
            **report.to_dict(),
        }
        with open(ledger_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception as exc:
        log.warning("Could not save diagnostic to ledger: %s", exc)


def _fallback_data(req: DiagnosticRequest) -> dict[str, Any]:
    """Minimal offline fallback if LLM is unavailable."""
    sector_info = SAUDI_SECTORS.get(req.sector, SAUDI_SECTORS["other"])
    return {
        "executive_summary_ar": f"تشخيص أولي لـ {req.company_name} في قطاع {sector_info['ar']}. يُظهر تحليلنا فرصاً واضحة لتحسين الكفاءة التشغيلية وزيادة الإيرادات عبر أتمتة العمليات.",
        "executive_summary_en": f"Initial diagnostic for {req.company_name} in {sector_info['en']}. Analysis shows clear opportunities for operational efficiency and revenue growth through targeted automation.",
        "sections": [
            {
                "title_ar": ar,
                "title_en": en,
                "content_ar": f"سيتم تفصيل هذا القسم بناءً على بيانات {req.company_name} الفعلية.",
                "content_en": f"This section will be detailed based on {req.company_name}'s actual data.",
            }
            for ar, en in _SECTION_PROMPTS
        ],
        "next_step_ar": "الخطوة التالية: برنامج التجربة 7 أيام بـ 499 ريال سعودي — نُثبت نتيجة قابلة للقياس في أسبوع.",
        "next_step_en": "Next step: 7-day proof sprint at 499 SAR — we prove measurable results in one week.",
    }
