#!/usr/bin/env python3
"""
Generate one-page proposal briefs for hot leads.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.revenue._lib import REPO_ROOT, load_csv, score_target, today_str


def slugify(name: str) -> str:
    return re.sub(r"[^\w\-]+", "-", name).strip("-").lower()[:50]


def build_brief(row: dict[str, str], score: str) -> str:
    company = row.get("company", "العميل").strip()
    sector = row.get("sector", "").strip()
    pain = row.get("pain", row.get("pain_hypothesis", "تحديات تشغيلية")).strip()
    city = row.get("city", "").strip()

    sector_offers = {
        "logistics": "Command Center OS + WhatsApp Follow-up + SLA Dashboard",
        "real_estate": "Lead Intelligence OS + WhatsApp Follow-up + Pipeline Dashboard",
        "clinics": "Patient Operations OS + Booking + Reviews + Recall workflows",
        "restaurants": "Operations OS + Unified Inbox + Reservation + Delivery SLA",
        "training": "Enrollment OS + Lead Nurture + Attendance Dashboard",
        "agency": "Agency Delivery OS + Client Workspaces + Approval Workflow",
        "ecommerce": "Revenue Operations OS + Cart Recovery + Support SLA",
        "b2b_services": "Proposal & Renewal OS + Pipeline + Renewal Alerts",
    }
    offer = sector_offers.get(sector, "AI Business Operating System مخصص")

    lines = [
        f"# عرض تجربي — {company}",
        "",
        f"**تاريخ:** {today_str()}  ",
        f"**القطاع:** {sector}  ",
        f"**المدينة:** {city}  ",
        f"**درجة التأهيل:** {score}",
        "",
        "## الفرضية",
        f"{company} تواجه ألم: {pain}.",
        "",
        "## العرض",
        f"{offer}.",
        "",
        "## نطاق الـ Pilot",
        "- مدة: 7-14 يوم",
        "- ألم واحد محدد",
        "- ناتج قابل للقياس (baseline + after)",
        "",
        "## الاستثمار",
        "- رسوم تشخيص: 4,999 ريال",
        "- Pilot شهر واحد: 14,999 ريال",
        "- اشتراك شهري بعد نجاح الـ Pilot: يحدد حسب النطاق",
        "",
        "## مناطق القياس المتوقعة",
        "- وقت الاستجابة للعميل",
        "- معدل تحويل الفرص",
        "- عدد الساعات اليدوية المستعادة",
        "- SLA compliance",
        "",
        "## الخطوة التالية",
        "اجتماع Discovery 30 دقيقة لتأكيد الألم والبيانات المتاحة.",
        "",
        "---",
        "*Dealix — AI Business Operating Systems للشركات السعودية*",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate proposal briefs for hot leads")
    parser.add_argument("--input", default="ledgers/prospects.csv")
    parser.add_argument("--min-score", type=float, default=3.5)
    args = parser.parse_args()

    rows = load_csv(REPO_ROOT / args.input)
    out_dir = REPO_ROOT / "reports" / "revenue" / today_str() / "proposals"
    out_dir.mkdir(parents=True, exist_ok=True)

    generated = 0
    for row in rows:
        result = score_target(row)
        if result["score"] < args.min_score:
            continue
        path = out_dir / f"{slugify(row.get('company', 'unknown'))}_proposal.md"
        path.write_text(build_brief(row, str(result["score"])), encoding="utf-8")
        generated += 1

    print(f"Generated {generated} proposal briefs in {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
