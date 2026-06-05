#!/usr/bin/env python3
"""Generate an enterprise sales room pack (drafts, for founder review).

Writes outputs/enterprise_sales_rooms/YYYY-MM-DD/<company_slug>/ with 7 draft
documents. No unverified claims, no security certifications that do not exist,
no guaranteed ROI. Never sends anything externally.

Run: python scripts/enterprise_sales_room_generate.py --company "Acme Co"
"""

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

NON_NEGOTIABLE = (
    "AI يجهّز ويحلّل ويصيغ ويُقيّم ويرتّب ويوصي. "
    "المؤسس يراجع ويعتمد ويبيع ويرسل يدويًا. النظام لا يرسل خارجيًا أبدًا."
)
DRAFT_BANNER = "DRAFT — review only. لا claims غير مثبتة. لا شهادات أمنية غير موجودة. لا ROI مضمون."


def slugify(name: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", name.strip().lower())
    return s.strip("-") or "company"


def _doc(title: str, body_sections: list[tuple[str, list[str]]]) -> str:
    lines = [f"# {title}", "", f"> {DRAFT_BANNER}", "", f"> {NON_NEGOTIABLE}", ""]
    for h, bullets in body_sections:
        lines.append(f"## {h}")
        lines.append("")
        for b in bullets:
            lines.append(f"- {b}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def build_pack(company: str) -> dict[str, str]:
    c = company
    return {
        "stakeholder_map.md": _doc(
            f"Stakeholder Map — {c}",
            [
                (
                    "الأدوار",
                    [
                        "economic buyer",
                        "champion",
                        "technical/security gatekeeper",
                        "procurement",
                        "end users",
                    ],
                ),
                ("ملاحظات", ["[يكملها المؤسس بأسماء وأدوار فعلية]"]),
            ],
        ),
        "business_case.md": _doc(
            f"Business Case — {c}",
            [
                (
                    "المشكلة وكلفتها (assumptions)",
                    ["[وصف الألم الإيرادي/التشغيلي — كل رقم assumption]"],
                ),
                ("النطاق المقترح", ["[العرض المناسب من السلم]"]),
                ("الأثر المقدّر", ["[تقدير موسوم كافتراض — لا ROI مضمون]"]),
            ],
        ),
        "executive_proposal.md": _doc(
            f"Executive Proposal — {c}",
            [
                ("الملخّص التنفيذي", ["[القيمة في 3 أسطر]"]),
                ("النطاق والمخرجات", ["[المخرجات المحددة]"]),
                ("الجدول والسعر", ["[ضمن أرضية السعر]"]),
                ("الخطوة التالية", ["[pilot أو retainer]"]),
            ],
        ),
        "security_legal_pack.md": _doc(
            f"Security & Legal Pack — {c}",
            [
                (
                    "الممارسات الأمنية",
                    [
                        "أطر مرجعية: NIST CSF / OWASP كأطر تحقق لا كشهادات.",
                        "وضع PDPL-aware دون ادعاء امتثال كامل غير مراجَع.",
                        "لا ادعاء ISO 27001 / SOC 2 ما لم يوجد فعليًا.",
                    ],
                ),
                ("القانوني", ["قوالب تعاقد تحتاج مراجعة قانونية قبل الاستخدام."]),
            ],
        ),
        "procurement_pack.md": _doc(
            f"Procurement Pack — {c}",
            [
                ("معلومات المورّد", ["[بيانات Dealix الرسمية]"]),
                ("نطاق العمل", ["[SOW مرجعي]"]),
                ("الشروط", ["مراجع شروط (قوالب) — تحتاج مراجعة قانونية."]),
            ],
        ),
        "pilot_governance.md": _doc(
            f"Pilot Governance — {c}",
            [
                (
                    "العناصر",
                    ["نطاق محدود", "معايير نجاح مقاسة", "بوابة قبول", "مسار التحول إلى retainer"],
                )
            ],
        ),
        "close_plan.md": _doc(
            f"Close Plan — {c}",
            [
                ("الخطوات المتبادلة", ["[خطوات + تواريخ + مالكون]"]),
                ("المخاطر", ["[مخاطر الإغلاق]"]),
                ("المتابعة", ["تُعتمد وتُرسل يدويًا من المؤسس."]),
            ],
        ),
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--company", required=True)
    p.add_argument("--date", default=date.today().isoformat())
    p.add_argument("--out-root", type=Path, default=REPO / "outputs" / "enterprise_sales_rooms")
    args = p.parse_args(argv)

    out_dir = args.out_root / args.date / slugify(args.company)
    out_dir.mkdir(parents=True, exist_ok=True)
    pack = build_pack(args.company)
    for fname, content in pack.items():
        (out_dir / fname).write_text(content, encoding="utf-8")
    print(f"enterprise_sales_room_generate: wrote {len(pack)} drafts to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
