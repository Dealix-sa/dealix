#!/usr/bin/env python3
"""Generate the ten first Dealix sector landing pages."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.growth._common import (  # noqa: E402
    DATA_DIR,
    assert_single_cta,
    ensure_dirs,
    write_json,
)

_OUT = DATA_DIR / "sector_pages.json"

# slug, name_en, name_ar, pain_ar, single CTA, recommended OS modules.
_SECTORS: list[dict[str, Any]] = [
    {
        "slug": "consulting",
        "name_en": "Consulting",
        "name_ar": "الاستشارات",
        "pain_ar": "صعوبة إثبات قيمة كل ارتباط استشاري أمام العميل.",
        "recommended_os": ["proof_os", "value_os", "governance_os"],
        "cta": "Command Sprint",
    },
    {
        "slug": "training",
        "name_en": "Training",
        "name_ar": "التدريب",
        "pain_ar": "ضعف متابعة أثر التدريب بعد انتهاء البرنامج.",
        "recommended_os": ["adoption_os", "value_os", "proof_os"],
        "cta": "Free Diagnostic",
    },
    {
        "slug": "marketing-agencies",
        "name_en": "Marketing Agencies",
        "name_ar": "وكالات التسويق",
        "pain_ar": "تسرب العملاء بين الحملة والنتيجة دون سجل واضح.",
        "recommended_os": ["value_os", "sales_os", "proof_os"],
        "cta": "Business OS Score",
    },
    {
        "slug": "it-services",
        "name_en": "IT Services",
        "name_ar": "خدمات تقنية المعلومات",
        "pain_ar": "غياب وضوح حالة التسليم لكل عميل في الوقت الحقيقي.",
        "recommended_os": ["adoption_os", "data_os", "value_os"],
        "cta": "Free Diagnostic",
    },
    {
        "slug": "recruitment",
        "name_en": "Recruitment",
        "name_ar": "التوظيف",
        "pain_ar": "فقدان سياق المرشحين والعملاء بين التفاعلات.",
        "recommended_os": ["capital_os", "data_os", "value_os"],
        "cta": "Command Sprint",
    },
    {
        "slug": "accounting-advisory",
        "name_en": "Accounting and Advisory",
        "name_ar": "المحاسبة والاستشارات المالية",
        "pain_ar": "صعوبة ربط العمل المنجز بقيمة موثقة للعميل.",
        "recommended_os": ["proof_os", "value_os", "governance_os"],
        "cta": "Command Sprint",
    },
    {
        "slug": "facility-management",
        "name_en": "Facility Management",
        "name_ar": "إدارة المرافق",
        "pain_ar": "تشتت طلبات الخدمة وغياب سجل قابل للإثبات.",
        "recommended_os": ["adoption_os", "data_os", "proof_os"],
        "cta": "Free Diagnostic",
    },
    {
        "slug": "logistics",
        "name_en": "Logistics",
        "name_ar": "الخدمات اللوجستية",
        "pain_ar": "ضعف وضوح حالة الشحنات أمام العميل لحظة بلحظة.",
        "recommended_os": ["adoption_os", "data_os", "value_os"],
        "cta": "Business OS Score",
    },
    {
        "slug": "real-estate-services",
        "name_en": "Real Estate Services",
        "name_ar": "خدمات العقار",
        "pain_ar": "تسرب العملاء المحتملين بسبب بطء وعدم انتظام المتابعة.",
        "recommended_os": ["sales_os", "value_os", "proof_os"],
        "cta": "Free Diagnostic",
    },
    {
        "slug": "business-services",
        "name_en": "Business Services",
        "name_ar": "خدمات الأعمال",
        "pain_ar": "اعتماد كبير على الذاكرة الفردية بدل سجل تشغيلي موحد.",
        "recommended_os": ["capital_os", "data_os", "adoption_os"],
        "cta": "Command Sprint",
    },
]


def _build_page(sector: dict[str, Any]) -> dict[str, Any]:
    """Compose a single deterministic sector-page record."""
    name_ar = sector["name_ar"]
    name_en = sector["name_en"]
    return {
        "slug": f"/ar/industries/{sector['slug']}",
        "sector_id": sector["slug"],
        "name_ar": name_ar,
        "name_en": name_en,
        "pain_ar": sector["pain_ar"],
        "why_tools_fail_ar": (
            f"أدوات {name_ar} التقليدية تركز على المهام لا على إثبات القيمة، "
            "فتترك فجوة بين العمل المنجز والقيمة الموثقة للعميل."
        ),
        "how_dealix_helps": [
            "تشغيل مسار الإيراد من العميل المحتمل حتى الدفعة المؤكدة بسجل واضح.",
            "بناء سجل إثبات لكل ارتباط دون أي ادعاء مضمون.",
            "موجز قيادي تنفيذي أسبوعي بقرار واحد وإجراء تالٍ واحد.",
        ],
        "recommended_os": sector["recommended_os"],
        "sample_command_pack": {
            "revenue_map": "stage_table_with_owners",
            "proof_register": "one_evidence_per_engagement",
            "executive_command_brief": "weekly_one_decision",
            "next_action_board": "single_next_action_per_client",
        },
        "proof_trust_line_ar": (
            "نعرض أنماطاً تشغيلية مجهّلة المصدر فقط، بلا أسماء عملاء ولا شعارات "
            "ولا أرقام مضمونة."
        ),
        "sprint_offer": {
            "name": "Command Sprint",
            "duration_days": 7,
            "price_sar_range": [499, 1500],
            "deliverables": [
                "revenue_map",
                "proof_register",
                "executive_command_brief",
                "next_action_board",
            ],
        },
        "cta": sector["cta"],
    }


def build_pages() -> list[dict[str, Any]]:
    """Return validated sector pages sorted by sector id."""
    pages = [_build_page(s) for s in _SECTORS]
    for page in pages:
        assert_single_cta(page["cta"])
    return sorted(pages, key=lambda p: p["sector_id"])


def main() -> int:
    """Write the sector pages and print a summary line."""
    ensure_dirs()
    pages = build_pages()
    size = write_json(_OUT, pages)
    print(f"sector_pages: wrote {len(pages)} sectors to {_OUT} ({size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
