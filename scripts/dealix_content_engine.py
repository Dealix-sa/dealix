#!/usr/bin/env python3
"""Dealix Content Engine — daily bilingual LinkedIn drafts to build inbound demand.

Derives educational posts from the same sector pains used in outreach, so the
content reinforces the sales narrative. Posts teach first, with a soft CTA to the
free diagnostic — no hard sell, no ROI claims, no fake proof. Writes drafts only;
nothing is published. The founder reviews and posts manually.

Usage:
    python3 scripts/dealix_content_engine.py                 # one post per sector
    python3 scripts/dealix_content_engine.py --sector clinic
    python3 scripts/dealix_content_engine.py --dry-run
"""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PITCHES = REPO_ROOT / "data" / "outreach" / "sector_pitches.json"
OUT_ROOT = REPO_ROOT / "reports" / "content"

HASHTAGS = "#الذكاء_الاصطناعي #السعودية #ريادة_الأعمال #رؤية_2030 #Dealix #AI #SaudiArabia"


def build_post(sector_key: str, sec: dict, co: dict) -> str:
    label = sec.get("label_ar", sector_key)
    hook_ar = sec["pain_ar"]
    fix_ar = sec["fix_ar"]
    hook_en = sec["pain_en"]
    fix_en = sec["fix_en"]
    return "\n".join([
        f"# مسودة منشور LinkedIn — {label}",
        f"_تاريخ: {date.today().isoformat()} · راجِع وانشُر بنفسك. لا نشر تلقائي._",
        "",
        "---",
        "",
        "## العربية",
        "",
        f"💡 {hook_ar}",
        "",
        "السبب غالبًا ليس الفريق — بل غياب نظام يلتقط ويُتابع بإيقاع ثابت.",
        "",
        f"ما نفعله في Dealix: {fix_ar}",
        "",
        "النتيجة التي نستهدفها: لا يضيع عميل محتمل بسبب رد متأخر، ووضوح كامل في غرفة قيادة واحدة.",
        "",
        "لو حاب تشوف وين تتسرّب الفرص عندك — التشخيص المجاني (30 نقطة) بدون التزام:",
        f"{co['diagnostic']}",
        "",
        HASHTAGS,
        "",
        "---",
        "",
        "## English",
        "",
        f"💡 {hook_en}",
        "",
        "It's rarely the team — it's the missing system that captures and follows up on a steady cadence.",
        "",
        f"What Dealix does: {fix_en}",
        "",
        "The target outcome: no lead lost to a slow reply, full clarity in one command room.",
        "",
        f"Want to see where opportunities leak for you? Free 30-point diagnostic, no commitment: {co['diagnostic']}",
        "",
        HASHTAGS,
        "",
    ])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sector", help="Only this sector (default: all)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    data = json.loads(PITCHES.read_text(encoding="utf-8"))
    co = data["company"]
    sectors = data["sectors"]
    keys = [args.sector] if args.sector else list(sectors)
    keys = [k for k in keys if k in sectors]
    if not keys:
        print(f"قطاع غير معروف. المتاح: {', '.join(sectors)}")
        return 1

    if args.dry_run:
        print(f"[dry-run] سيُولّد {len(keys)} منشور: {', '.join(keys)}")
        return 0

    out_dir = OUT_ROOT / date.today().isoformat()
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for k in keys:
        path = out_dir / f"linkedin-{k}.md"
        path.write_text(build_post(k, sectors[k], co), encoding="utf-8")
        written.append(path)

    print(f"تم إنشاء {len(written)} مسودة منشور في: {out_dir}")
    print("راجِع وانشُر بنفسك — لا نشر تلقائي.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
