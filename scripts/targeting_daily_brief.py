#!/usr/bin/env python3
"""Daily Founder Brief — the 09:00 output of the company machine.

Runs the pipeline end-to-end (compliance → score → weakness → offer → drafts) and
produces the founder's morning artifacts:

    out/ranked_targets.csv          all scored companies, high→low
    out/founder_shortlist.md        top ~20 (grade A and up) to review today
    out/drafts_for_review.md        ~10 tailored drafts (approval required)
    out/daily_targeting_brief.md    one-page: best sector, best angle, top risk
    out/tomorrow_targeting_plan.md  what to research next

This script only reads the master + config and writes to out/. It never sends.

Usage:
    python scripts/targeting_daily_brief.py \\
        --in data/targeting/company_master.jsonl --out data/targeting/out
"""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

from scripts.targeting_common import COMPANY_MASTER, OUT_DIR, load_companies, load_weights
from scripts.targeting_compliance_gate import REJECTED
from scripts.targeting_compliance_gate import run as run_compliance
from scripts.targeting_draft_lab import build_draft
from scripts.targeting_offer_router import route_offer
from scripts.targeting_scorecard import rank


def _shortlist(scored: list[dict[str, Any]], weights: dict[str, Any]) -> list[dict[str, Any]]:
    min_grade = weights.get("founder_shortlist_min_grade", "A")
    size = int(weights.get("founder_shortlist_size", 20))
    grade_order = ["A+", "A", "B", "C", "D"]
    cutoff = grade_order.index(min_grade) if min_grade in grade_order else 1
    keep = [
        s
        for s in scored
        if not s["reject"] and s["grade"] in grade_order and grade_order.index(s["grade"]) <= cutoff
    ]
    return keep[:size]


def build_brief(companies: list[dict[str, Any]]) -> dict[str, Any]:
    """Run the full daily pipeline in memory and return all artifacts as text."""
    weights = load_weights()

    # 1) Compliance gate — only approved/review flow onward.
    buckets = run_compliance(companies)
    rejected = buckets[REJECTED]
    eligible = [v["company"] for k, v_list in buckets.items() if k != REJECTED for v in v_list]

    # 2) Score + rank.
    scored = rank(eligible)

    # 3) Shortlist + drafts.
    shortlist = _shortlist(scored, weights)
    by_name = {c.get("company_name"): c for c in eligible}
    drafts = []
    for s in shortlist[:10]:
        company = by_name.get(s["company_name"], {})
        drafts.append(build_draft(company, route_offer(company)))

    # 4) Aggregates for the brief.
    sectors = Counter(s["sector"] for s in scored if not s["reject"])
    best_sector = sectors.most_common(1)[0][0] if sectors else "—"
    angles = Counter(
        route_offer(by_name[s["company_name"]])["primary_os_angle"]
        for s in shortlist
        if s["company_name"] in by_name
    )
    best_angle = angles.most_common(1)[0][0] if angles else "—"
    top_risk = rejected[0]["reasons"][0] if rejected else "no compliance rejects today"

    today = date.today().isoformat()

    shortlist_md = f"# Founder Shortlist — {today}\n\n"
    shortlist_md += "| # | Company | Sector | Score | Grade | Decision |\n"
    shortlist_md += "|---|---------|--------|-------|-------|----------|\n"
    for i, s in enumerate(shortlist, 1):
        shortlist_md += (
            f"| {i} | {s['company_name']} | {s['sector']} | "
            f"{s['score']} | {s['grade']} | {s['decision']} |\n"
        )

    brief_md = f"""# Daily Targeting Brief — {today}

## التركيز اليومي / Daily focus
- **Eligible companies scored:** {len(scored)}
- **Founder shortlist (review today):** {len(shortlist)}
- **Drafts queued for approval:** {len(drafts)}
- **Compliance rejects:** {len(rejected)}

## الإشارات / Signals
- **أفضل قطاع / best sector:** `{best_sector}`
- **أفضل زاوية / best OS angle:** `{best_angle}`
- **أكبر مخاطرة / top risk:** {top_risk}

## أعلى 5 أهداف / Top 5 targets
"""
    for i, s in enumerate(scored[:5], 1):
        brief_md += (
            f"{i}. **{s['company_name']}** — {s['score']} ({s['grade']}) · {s['decision']}\n"
        )
    brief_md += (
        "\n> القاعدة: 400 بحث وليس 400 إرسال. كل رسالة يدوية، بموافقة المؤسس.\n"
        "> Rule: 400 researched, not 400 sent. Every message manual, founder-approved.\n"
    )

    tomorrow_md = f"""# Tomorrow Targeting Plan — {today}

Based on today's scores:

- **Double down on:** `{best_sector}` (highest eligible volume) via `{best_angle}` angle.
- **Add evidence for:** B-grade companies that missed the shortlist on thin evidence.
- **Hold for governance review:** {len(buckets.get('review_required', []))} sensitive-sector companies.
- **Stop ingesting from:** any source that produced a compliance reject today.

## Research targets for tomorrow
- 400 raw candidates from allowed sources (official sites, services/clients pages,
  jobs pages, news, public directories, manual LinkedIn visits — no automation).
- Normalize + dedupe → ~250-350 clean.
- Re-run this brief at 09:00.
"""

    return {
        "scored": scored,
        "shortlist": shortlist,
        "drafts": drafts,
        "rejected": rejected,
        "shortlist_md": shortlist_md,
        "brief_md": brief_md,
        "tomorrow_md": tomorrow_md,
        "best_sector": best_sector,
        "best_angle": best_angle,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Dealix daily founder targeting brief")
    ap.add_argument("--in", dest="infile", default=str(COMPANY_MASTER))
    ap.add_argument("--out", dest="outdir", default=str(OUT_DIR))
    args = ap.parse_args(argv)

    companies = load_companies(Path(args.infile))
    result = build_brief(companies)
    out_dir = Path(args.outdir)
    out_dir.mkdir(parents=True, exist_ok=True)

    (out_dir / "founder_shortlist.md").write_text(result["shortlist_md"], encoding="utf-8")
    (out_dir / "daily_targeting_brief.md").write_text(result["brief_md"], encoding="utf-8")
    (out_dir / "tomorrow_targeting_plan.md").write_text(result["tomorrow_md"], encoding="utf-8")

    # drafts_for_review.md (reuse Draft Lab formatting).
    header = (
        "# Drafts for Review — APPROVAL REQUIRED (founder)\n\n"
        "> Dealix never auto-sends. Manual review, manual send.\n\n"
    )
    blocks = [d["markdown"] for d in result["drafts"]]
    (out_dir / "drafts_for_review.md").write_text(header + "\n---\n".join(blocks), encoding="utf-8")

    print(
        f"brief written → {out_dir}  "
        f"(shortlist={len(result['shortlist'])}, drafts={len(result['drafts'])}, "
        f"best_sector={result['best_sector']}, best_angle={result['best_angle']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
