#!/usr/bin/env python3
"""
Generate Arabic outreach drafts for ready_for_review / approved_to_send prospects.

Rules enforced:
  - Never auto-sends
  - Polite Arabic by default
  - No fake metrics or prior-relationship claims
  - Includes low-pressure CTA
  - Includes opt-out language
  - Customized by sector and pain_hypothesis
  - Saved to outbox/YYYY-MM-DD/ only

Usage:
    python scripts/founder/generate_outreach_drafts.py
    python scripts/founder/generate_outreach_drafts.py --limit 10
    python scripts/founder/generate_outreach_drafts.py --dry-run
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROSPECTS = ROOT / "ledgers" / "prospects.csv"
TODAY = date.today().isoformat()
OUTBOX = ROOT / "outbox" / TODAY

SECTOR_OPENERS: dict[str, str] = {
    "healthcare": "في قطاع الرعاية الصحية والعيادات، كثير من الفرص تضيع بين واتساب وجداول الحجوزات.",
    "عيادات": "في قطاع العيادات والمراكز الطبية، متابعة الحجوزات والاستفسارات تحتاج نظام واضح.",
    "training": "في قطاع التدريب، التسجيلات والاستفسارات تحتاج متابعة سريعة قبل أن يذهب العميل للمنافس.",
    "تدريب": "في قطاع التدريب والتعليم، سرعة الاستجابة للمهتمين تؤثر مباشرة على الإيراد.",
    "restaurant": "في قطاع المطاعم، إدارة التقييمات والمتابعة مع العملاء تؤثر على السمعة والعودة.",
    "مطعم": "في قطاع المطاعم والكافيهات، التقييمات والشكاوى تحتاج ردود منظمة وسريعة.",
    "real_estate": "في قطاع العقار، متابعة العروض والعملاء المهتمين يحتاج نظام تتبع يومي.",
    "عقار": "في قطاع العقار، كثير من العملاء المهتمين يضيعون بدون متابعة منظمة.",
    "logistics": "في قطاع اللوجستيات، تنسيق العمليات والتواصل مع العملاء يستفيد من الأتمتة الذكية.",
}

DEFAULT_OPENER = "في كثير من الشركات، الفرص تضيع بين واتساب، الإيميل، والمتابعة اليدوية."


def build_draft(row: dict[str, str]) -> str:
    company = (row.get("company_name") or "فريقكم").strip()
    sector = (row.get("sector") or "").strip().lower()
    pain = (row.get("pain_hypothesis") or "").strip()
    product = (row.get("recommended_product") or "Diagnostic Sprint / Revenue Command Room OS").strip()
    angle = (row.get("dealix_angle") or "ترتيب المتابعة وتحويل الفرص إلى إيراد").strip()

    opener = SECTOR_OPENERS.get(sector, DEFAULT_OPENER)

    pain_line = f"\nالتحدي الذي نرى شركات مثلكم تواجهه: **{pain}**\n" if pain else ""

    return f"""السلام عليكم فريق {company}،

أنا سامي من Dealix.

{opener}
{pain_line}
نساعد الشركات على بناء نظام تشغيل يومي يجيب على:
- من يحتاج متابعة اليوم؟
- ماذا نرسل؟
- أين الفرص العالقة؟
- وما القرار التالي؟

التوصية المبدئية لكم: {product}
زاوية البداية: {angle}

البداية عندنا تكون بتشخيص مختصر من صفحة واحدة، بدون تغيير أنظمتكم الحالية، يوضح أين تضيع الفرص وكيف ممكن نبني Pilot خلال 7 أيام.

إذا مناسب، أرسل لكم نموذج مختصر.
وإذا غير مناسب، أوقف التواصل فورًا.

---
⚠️ مسودة — يحتاج مراجعة المؤسس قبل الإرسال
لا إرسال تلقائي — يمكن إيقاف التواصل فورًا
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate outreach drafts")
    parser.add_argument("--limit", type=int, default=25, help="Max drafts to generate")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not PROSPECTS.exists():
        print("WARN: ledgers/prospects.csv not found.")
        return 0

    with PROSPECTS.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    eligible = [
        r for r in rows
        if (r.get("verification_status") or "").strip() in {"ready_for_review", "approved_to_send"}
        and (r.get("owner_decision") or "").strip() not in {"reject", "do_not_contact"}
    ]

    if not eligible:
        print("No eligible prospects (need verification_status=ready_for_review or approved_to_send).")
        return 0

    batch = eligible[:args.limit]

    if args.dry_run:
        print(f"DRY RUN — would generate {len(batch)} drafts.")
        for r in batch[:3]:
            print(f"  {r['company_name']} ({r.get('sector','')}) → {r.get('recommended_product','')}")
        return 0

    OUTBOX.mkdir(parents=True, exist_ok=True)
    manifest: list[dict] = []

    for idx, row in enumerate(batch, 1):
        company = row.get("company_name") or f"company_{idx}"
        safe = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in company)[:60]
        draft_text = build_draft(row)
        path = OUTBOX / f"{idx:02d}_{safe}_draft.txt"
        path.write_text(draft_text, encoding="utf-8")
        manifest.append({
            "company": company,
            "sector": row.get("sector", ""),
            "product": row.get("recommended_product", ""),
            "status": row.get("verification_status", ""),
            "file": str(path.relative_to(ROOT)),
        })

    manifest_path = OUTBOX / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"DRAFTS_OK: {len(manifest)} drafts written to {OUTBOX}")
    print(f"Manifest:  {manifest_path}")
    print("ACTION: Review each draft before sending. No auto-send.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
