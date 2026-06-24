"""Founder marketing report: daily report of pipeline state, top companies, actions needed."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from datetime import date, datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from dotenv import load_dotenv

load_dotenv(BASE_DIR.parent / ".env")

import yaml

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)

MEMORY_DIR = BASE_DIR / "memory"
CONFIG_DIR = BASE_DIR / "config"
OUTPUTS_DIR = BASE_DIR / "outputs"
REPORTS_DIR = OUTPUTS_DIR / "reports"
REVIEW_QUEUE_DIR = OUTPUTS_DIR / "review_queue"


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    records = []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return records


def load_persuasion_config() -> dict:
    try:
        with open(CONFIG_DIR / "persuasion.yml") as fh:
            return yaml.safe_load(fh)
    except Exception:
        return {}


def build_stats() -> dict:
    raw_leads = read_jsonl(MEMORY_DIR / "raw_leads.jsonl")
    briefs = read_jsonl(MEMORY_DIR / "company_briefs.jsonl")
    opportunities = read_jsonl(MEMORY_DIR / "opportunities.jsonl")
    drafts = read_jsonl(MEMORY_DIR / "draft_queue.jsonl")
    approved_sends = read_jsonl(MEMORY_DIR / "approved_sends.jsonl")
    replies = read_jsonl(MEMORY_DIR / "replies.jsonl")
    learning_log = read_jsonl(MEMORY_DIR / "learning_log.jsonl")

    today = date.today().isoformat()
    today_raw = [l for l in raw_leads if l.get("scan_date", "") == today]
    today_briefs = [b for b in briefs if b.get("research_date", "") == today]
    today_drafts = [d for d in drafts if (d.get("created_at", "") or "")[:10] == today]

    tier_a = [o for o in opportunities if o.get("tier") == "A"]
    qualified = [b for b in briefs if b.get("fit_score", 0) >= 60]
    approved_for_review = [d for d in drafts if d.get("approved_for_review")]
    interested = [r for r in replies if r.get("classification") == "interested"]

    top_companies = sorted(
        [
            {
                "company_name": o["company_name"],
                "sector": o.get("sector", ""),
                "fit_score": o.get("fit_score", 0),
                "tier": o.get("tier", ""),
                "offer": o.get("primary_offer", ""),
                "company_id": o.get("company_id", ""),
            }
            for o in opportunities
        ],
        key=lambda x: x["fit_score"],
        reverse=True,
    )[:10]

    for company in top_companies:
        company_drafts = [d for d in drafts if d.get("company_id") == company["company_id"]]
        approved_d = [d for d in company_drafts if d.get("approved_for_review")]
        company["draft_count"] = len(company_drafts)
        company["approved_drafts"] = len(approved_d)
        company["best_score"] = max((d.get("quality_score") or 0 for d in company_drafts), default=0)

    latest_learning = sorted(learning_log, key=lambda x: x.get("date", ""), reverse=True)[:5]
    top_angles = [l.get("top_angle", "") for l in latest_learning if l.get("top_angle")]

    return {
        "date": today,
        "raw_scanned": len(today_raw),
        "qualified_companies": len(qualified),
        "tier_a_companies": len(tier_a),
        "briefs_completed": len(today_briefs),
        "drafts_generated": len(today_drafts),
        "drafts_passed_gate": len([d for d in today_drafts if d.get("approved_for_review")]),
        "ready_for_review": len(approved_for_review),
        "interested_count": len(interested),
        "top_companies": top_companies,
        "top_angles": top_angles,
        "total_opportunities": len(opportunities),
        "total_replies": len(replies),
        "total_approved_sends": len(approved_sends),
    }


def write_review_queue(stats: dict, drafts: list[dict]) -> None:
    REVIEW_QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    top_ids = {c["company_id"] for c in stats["top_companies"]}
    top_drafts = sorted(
        [d for d in drafts if d.get("approved_for_review") and d.get("company_id") in top_ids],
        key=lambda x: x.get("quality_score") or 0,
        reverse=True,
    )[:20]

    path = REVIEW_QUEUE_DIR / f"{stats['date']}_review_queue.jsonl"
    with open(path, "w") as fh:
        for d in top_drafts:
            fh.write(json.dumps(d) + "\n")
    log.info("Wrote %d drafts to review queue: %s", len(top_drafts), path)


def render_markdown(stats: dict, persuasion_config: dict) -> str:
    daily_limit = persuasion_config.get("daily_limits", {}).get("sends_per_day", 20)
    today = stats["date"]

    top_companies_rows = "\n".join(
        f"| {i+1} | {c['company_name']} | {c['sector']} | {c['fit_score']} | {c['tier']} | {c['offer']} | {c['best_score']} |"
        for i, c in enumerate(stats["top_companies"])
    )
    if not top_companies_rows:
        top_companies_rows = "| — | No companies yet | — | — | — | — | — |"

    angles_text = "\n".join(f"{i+1}. {a}" for i, a in enumerate(stats["top_angles"])) or "1. No learning data yet"

    return f"""# Dealix Daily Marketing Report
**Date:** {today}

## Today's Pipeline
| Metric | Count |
|--------|-------|
| Raw companies scanned | {stats['raw_scanned']} |
| Qualified companies | {stats['qualified_companies']} |
| Tier A companies | {stats['tier_a_companies']} |
| Company briefs completed | {stats['briefs_completed']} |
| Drafts generated | {stats['drafts_generated']} |
| Drafts passed quality gate | {stats['drafts_passed_gate']} |
| Ready for founder review | {stats['ready_for_review']} |
| Recommended sends today | {min(daily_limit, stats['ready_for_review'])} |

## Top 10 Companies Today
| # | Company | Sector | Fit | Tier | Offer | Draft Score |
|---|---------|--------|-----|------|-------|-------------|
{top_companies_rows}

## Best Performing Angles (from Learning Agent)
{angles_text}

## Risks & Attention Needed
- Ensure all approved drafts are reviewed before sending
- Check suppression list before any outreach
- Verify buyer titles are accurate for each company
- Confirm offer routing matches sector pain profile

## Founder Actions Today
1. Review top 20 drafts in: outputs/review_queue/{today}_review_queue.jsonl
2. Approve sends (target: {daily_limit} today)
3. Reply to {stats['interested_count']} interested leads
4. Log any replies received into memory/replies.jsonl
5. Review rejected drafts in outputs/rejected/{today}_rejected.jsonl

## Pipeline Totals
| Metric | Total |
|--------|-------|
| All opportunities | {stats['total_opportunities']} |
| All replies | {stats['total_replies']} |
| Total approved sends | {stats['total_approved_sends']} |

## Review Queue Summary
Top drafts ready for founder review are in:
`outputs/review_queue/{today}_review_queue.jsonl`

Top 10 companies by fit score and recommended action:
{chr(10).join(f"{i+1}. {c['company_name']} (Tier {c['tier']}, fit {c['fit_score']}, {c['approved_drafts']} drafts approved) — recommended: {'immediate outreach' if c['tier'] == 'A' else 'standard sequence'}" for i, c in enumerate(stats['top_companies'][:10])) or "No companies in pipeline yet."}
"""


def run() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    persuasion_config = load_persuasion_config()
    stats = build_stats()
    drafts = read_jsonl(MEMORY_DIR / "draft_queue.jsonl")

    write_review_queue(stats, drafts)

    md = render_markdown(stats, persuasion_config)
    md_path = REPORTS_DIR / f"{stats['date']}_founder_report.md"
    with open(md_path, "w") as fh:
        fh.write(md)
    log.info("Wrote founder report: %s", md_path)

    summary = {
        "date": stats["date"],
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "pipeline": {
            "raw_scanned": stats["raw_scanned"],
            "qualified": stats["qualified_companies"],
            "tier_a": stats["tier_a_companies"],
            "briefs_completed": stats["briefs_completed"],
            "drafts_generated": stats["drafts_generated"],
            "drafts_approved": stats["drafts_passed_gate"],
            "ready_for_review": stats["ready_for_review"],
        },
        "top_companies": [
            {"company_name": c["company_name"], "tier": c["tier"], "fit_score": c["fit_score"]}
            for c in stats["top_companies"]
        ],
        "report_path": str(md_path),
    }

    json_path = REPORTS_DIR / f"{stats['date']}_summary.json"
    with open(json_path, "w") as fh:
        json.dump(summary, fh, indent=2)
    log.info("Wrote summary JSON: %s", json_path)

    print(f"Report generated: {md_path}")
    print(f"Summary JSON: {json_path}")
    print(f"Pipeline: {stats['qualified_companies']} qualified, {stats['tier_a_companies']} Tier A, {stats['ready_for_review']} ready for review")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate daily founder marketing report")
    parser.parse_args()
    run()


if __name__ == "__main__":
    main()
