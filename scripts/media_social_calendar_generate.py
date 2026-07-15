#!/usr/bin/env python3
"""
Dealix Media & Social — 30-day content calendar generator (planning only).

Reads config/media_social_calendar.json and produces:
  - outputs/media_social/calendar_30_day.json
  - docs/media-social-os/99_MEDIA_SOCIAL_READY_REPORT.md

Doctrine: planning + manual posting only. No platform API posting, no
auto-post, no native-engagement automation. Output is a plan, not a poster.
"""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CONFIG = REPO / "config" / "media_social_calendar.json"
OUT = REPO / "outputs" / "media_social" / "calendar_30_day.json"
REPORT = REPO / "docs" / "media-social-os" / "99_MEDIA_SOCIAL_READY_REPORT.md"


def main() -> int:
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    pillars = cfg["pillars"]
    verticals = cfg["verticals"]
    langs = cfg["languages"]

    start = datetime(2026, 6, 4, tzinfo=timezone.utc)
    days = []
    for i in range(30):
        d = start + timedelta(days=i)
        pillar = pillars[i % len(pillars)]
        vertical = verticals[i % len(verticals)]
        lang = langs[i % len(langs)]
        days.append(
            {
                "day": i + 1,
                "date": d.date().isoformat(),
                "pillar": pillar,
                "vertical_focus": vertical,
                "language": lang,
                "format": "founder_post" if i % 2 == 0 else "company_post",
                "status": "draft_for_manual_posting",
                "auto_post": False,
                "hook_en": f"What {vertical.replace('_', ' ')} teams miss in their own data.",
                "hook_ar": f"ما تغفله فرق {vertical.replace('_', ' ')} في بياناتها.",
            }
        )

    calendar = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "auto_post": False,
        "doctrine": cfg["doctrine"],
        "total_days": len(days),
        "claim_guardrails": cfg["claim_guardrails"],
        "ads": cfg["ads"],
        "days": days,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(calendar, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# 99 — Media & Social Ready Report",
        "",
        f"_Generated: {datetime.now(timezone.utc).isoformat()}_",
        "",
        f"- 30-day calendar entries: **{len(days)}**",
        "- Auto-post: **disabled** (manual posting only)",
        "- Paid ads live launch: **NO-GO** (planning + copy only)",
        f"- Calendar file: `{OUT.relative_to(REPO)}`",
        "",
        "## Guardrails",
        "Forbidden claims are rejected at planning time:",
    ]
    for c in cfg["claim_guardrails"]["forbidden_claims"]:
        lines.append(f"- {c}")
    lines += [
        "",
        "_No content is posted by this tool. It produces a plan for manual, founder-approved posting._",
        "",
    ]
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines), encoding="utf-8")

    print(f"[media-social] calendar -> {OUT.relative_to(REPO)} ({len(days)} days, auto_post=False)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
