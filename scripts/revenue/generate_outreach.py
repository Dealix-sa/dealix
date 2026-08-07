#!/usr/bin/env python3
"""
Generate outreach email drafts for today.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.revenue._lib import REPO_ROOT, load_csv, opt_out_line, score_target, today_str


def slugify(name: str) -> str:
    return re.sub(r"[^\w\-]+", "-", name).strip("-").lower()[:50]


def build_email(row: dict[str, str]) -> str:
    company = row.get("company", "شركتكم").strip()
    sector = row.get("sector", "sector").strip()
    pain = row.get("pain", row.get("pain_hypothesis", "تحديات التشغيل اليومية")).strip()
    city = row.get("city", "").strip()
    email = row.get("email", "").strip()

    sector_names = {
        "logistics": "الخدمات اللوجستية",
        "real_estate": "العقارات",
        "clinics": "الرعاية الصحية",
        "restaurants": "المطاعم والمقاهي",
        "training": "التدريب والتعليم",
        "agency": "التسويق",
        "ecommerce": "التجارة الإلكترونية",
        "b2b_services": "خدمات B2B",
    }
    sector_ar = sector_names.get(sector, sector)

    lines = [
        f"To: {email}",
        f"Subject: {company} — فكرة عملية لتحويل {pain[:40]} إلى نظام تشغيلي",
        "",
        "السلام عليكم،",
        "",
        f"أنا من Dealix. نعمل مع شركات {sector_ar} في {city or 'السعودية'} على بناء أنظمة تشغيل مدعومة بالذكاء الاصطناعي.",
        "",
        f"لاحظنا أن كثير من الشركات في قطاع {sector_ar} تواجه ألم: {pain}.",
        "",
        "اقتراحنا ليس أداة إضافية. نبني نظام تشغيل بسيط يشمل:",
        "- غرفة قيادة مركزية (Command Center)",
        "- متابعة تلقائية عبر WhatsApp/Email",
        "- SLA Dashboard واضح",
        "- تقرير يومي للإدارة",
        "- دليل قياسي قبل/بعد",
        "",
        "نبدأ بـ Pilot صغير 7-14 يوم على ألم واحد فقط.",
        "",
        f"إذا مناسب، أرسل لكم تصور صفحة واحدة مخصص لـ {company}.",
        "",
        "تحياتي،",
        "فريق Dealix",
        opt_out_line("ar"),
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate outreach drafts")
    parser.add_argument("--input", default="ledgers/prospects.csv")
    parser.add_argument("--min-score", type=float, default=2.0)
    parser.add_argument("--limit", type=int, default=100)
    args = parser.parse_args()

    rows = load_csv(REPO_ROOT / args.input)
    if not rows:
        print(f"No rows in {args.input}")
        return 1

    out_dir = REPO_ROOT / "outbox" / today_str()
    out_dir.mkdir(parents=True, exist_ok=True)

    generated = 0
    for row in rows[: args.limit]:
        result = score_target(row)
        if result["score"] < args.min_score:
            continue
        path = out_dir / f"{slugify(row.get('company', 'unknown'))}_step1.md"
        path.write_text(build_email(row), encoding="utf-8")
        generated += 1

    print(f"Generated {generated} outreach drafts in {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
