#!/usr/bin/env python3
"""Generate outreach email drafts for today. Never sends externally.

This script writes draft email files to ``outbox/<date>/`` for human review.
It never sends anything — drafts only. A ``source_url`` is required for every
prospect (no source, no entry).

Usage:
    python scripts/revenue/generate_outreach_drafts.py [--input ledgers/prospects.csv]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.revenue._lib import REPO_ROOT, load_csv, opt_out_line, score_target, today_str
from scripts.revenue.validate_targets import validate_rows


def slugify(name: str) -> str:
    return re.sub(r"[^\w\-]+", "-", name).strip("-").lower()[:50]


def build_email(row: dict[str, str]) -> str:
    company = row.get("company_name") or row.get("company") or "شركتكم"
    company = company.strip()
    sector = row.get("sector", "sector").strip()
    city = row.get("city", "").strip()
    source = (row.get("source_url") or "").strip()

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
        f"Subject: {company} — فكرة عملية لتحسين التشغيل",
        "",
        "السلام عليكم،",
        "",
        f"أنا من Dealix. نعمل مع شركات {sector_ar} في {city or 'السعودية'} على بناء أنظمة تشغيل مدعومة بالذكاء الاصطناعي.",
        "",
        "اقتراحنا ليس أداة إضافية. نبني نظام تشغيل بسيط يشمل:",
        "- غرفة قيادة مركزية (Command Center)",
        "- متابعة تلقائية عبر WhatsApp/Email",
        "- SLA Dashboard واضح",
        "- تقرير يومي للإدارة",
        "",
        "نبدأ بـ Pilot صغير 7-14 يوم على ألم واحد فقط.",
        "",
        f"إذا مناسب، أرسل لكم تصور صفحة واحدة مخصص لـ {company}.",
        "",
        "تحياتي،",
        "فريق Dealix",
        opt_out_line("ar"),
        "",
        f"[Source: {source}]",  # traceability — no source, no entry
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate outreach email drafts — never sends")
    parser.add_argument("--input", default="ledgers/prospects.csv")
    parser.add_argument("--min-score", type=float, default=2.0)
    parser.add_argument("--limit", type=int, default=100)
    args = parser.parse_args()

    rows = load_csv(REPO_ROOT / args.input)
    if not rows:
        print(f"No rows in {args.input}")
        return 1

    # Validate — no source, no entry
    issues, valid = validate_rows(rows)
    if issues:
        print(f"Validation issues ({len(issues)}):")
        for issue in issues:
            print(f"  {issue}")

    out_dir = REPO_ROOT / "outbox" / today_str()
    out_dir.mkdir(parents=True, exist_ok=True)

    generated = 0
    for row in valid[: args.limit]:
        result = score_target(row)
        if result["score"] < args.min_score:
            continue
        path = out_dir / f"{slugify(row.get('company_name', 'unknown'))}_step1.md"
        path.write_text(build_email(row), encoding="utf-8")
        generated += 1

    print(f"Generated {generated} outreach drafts in {out_dir}")
    print("No external send. Drafts only. Review before any manual send.")
    return 0


if __name__ == "__main__":
    sys.exit(main())