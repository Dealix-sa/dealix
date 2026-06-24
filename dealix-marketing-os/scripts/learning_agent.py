"""Learning agent: analyzes reply patterns to improve outreach playbook."""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import uuid
from datetime import date, datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from dotenv import load_dotenv

load_dotenv(BASE_DIR.parent / ".env")

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)

MEMORY_DIR = BASE_DIR / "memory"
OUTPUTS_DIR = BASE_DIR / "outputs"
REPORTS_DIR = OUTPUTS_DIR / "reports"
LEARNING_LOG_PATH = MEMORY_DIR / "learning_log.jsonl"
REPLIES_PATH = MEMORY_DIR / "replies.jsonl"
DRAFT_QUEUE_PATH = MEMORY_DIR / "draft_queue.jsonl"
OPPORTUNITIES_PATH = MEMORY_DIR / "opportunities.jsonl"


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


def analyze_patterns_via_claude(replies: list[dict], drafts: list[dict], opportunities: list[dict]) -> dict | None:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        log.error("ANTHROPIC_API_KEY not set")
        return None

    import anthropic

    client = anthropic.Anthropic(api_key=api_key)

    reply_summary = [
        {
            "company": r.get("company_name", ""),
            "classification": r.get("classification", ""),
            "sentiment": r.get("sentiment", ""),
            "key_signal": r.get("key_signal", ""),
        }
        for r in replies[:50]
    ]

    draft_performance = []
    for d in drafts:
        if d.get("quality_score") is not None:
            draft_performance.append({
                "draft_type": d.get("draft_type", ""),
                "quality_score": d.get("quality_score"),
                "approved": d.get("approved_for_review", False),
                "sector": d.get("sector", ""),
            })

    sector_reply_rates: dict[str, dict[str, int]] = {}
    for opp in opportunities:
        sector = opp.get("sector", "unknown")
        if sector not in sector_reply_rates:
            sector_reply_rates[sector] = {"total": 0, "replied": 0}
        sector_reply_rates[sector]["total"] += 1
        if opp.get("reply_status"):
            sector_reply_rates[sector]["replied"] += 1

    data = {
        "total_replies": len(replies),
        "reply_classifications": {},
        "reply_sample": reply_summary[:20],
        "draft_performance_sample": draft_performance[:20],
        "sector_reply_rates": sector_reply_rates,
    }
    for r in replies:
        cls = r.get("classification", "unknown")
        data["reply_classifications"][cls] = data["reply_classifications"].get(cls, 0) + 1

    prompt = f"""You are a B2B outreach learning analyst. Analyze this outreach performance data and extract actionable insights.

Data:
{json.dumps(data, indent=2)}

Analyze and return a JSON object with:
{{
  "top_performing_angles": ["angle 1", "angle 2", "angle 3"],
  "high_response_sectors": ["sector 1", "sector 2"],
  "best_performing_subjects": ["subject pattern 1", "subject pattern 2"],
  "ctas_that_generate_meetings": ["cta 1", "cta 2"],
  "offers_opening_conversation": ["offer 1", "offer 2"],
  "phrases_to_avoid": ["phrase 1", "phrase 2"],
  "followup_timing_insight": "specific insight about follow-up timing",
  "overall_response_rate_estimate": "X%",
  "key_insights": ["insight 1", "insight 2", "insight 3"],
  "persuasion_yml_suggestions": [
    "Specific suggestion to improve the persuasion.yml formula",
    "Another specific suggestion"
  ]
}}

If there is insufficient data, still provide the structure with reasonable defaults and note "insufficient_data" where applicable.
Return only valid JSON. No explanation."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = message.content[0].text.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return json.loads(raw)
    except Exception as exc:
        log.error("Learning analysis failed: %s", exc)
        return None


def render_learning_report(analysis: dict, data_summary: dict) -> str:
    today = date.today().isoformat()
    top_angles = "\n".join(f"{i+1}. {a}" for i, a in enumerate(analysis.get("top_performing_angles", []))) or "Insufficient data"
    avoid = "\n".join(f"- {p}" for p in analysis.get("phrases_to_avoid", [])) or "- Insufficient data"
    insights = "\n".join(f"- {i}" for i in analysis.get("key_insights", [])) or "- Insufficient data"
    suggestions = "\n".join(f"{i+1}. {s}" for i, s in enumerate(analysis.get("persuasion_yml_suggestions", []))) or "No suggestions yet"
    high_sectors = ", ".join(analysis.get("high_response_sectors", [])) or "Insufficient data"
    best_ctas = "\n".join(f"- {c}" for c in analysis.get("ctas_that_generate_meetings", [])) or "- Insufficient data"

    return f"""# Dealix Learning Agent Report
**Date:** {today}

## Data Coverage
- Total replies analyzed: {data_summary.get('total_replies', 0)}
- Total drafts in pipeline: {data_summary.get('total_drafts', 0)}
- Total opportunities: {data_summary.get('total_opportunities', 0)}

## Reply Classification Breakdown
{chr(10).join(f"- {k}: {v}" for k, v in data_summary.get('reply_classifications', {}).items()) or "- No reply data yet"}

## Top Performing Angles
{top_angles}

## High-Response Sectors
{high_sectors}

## CTAs That Generate Meetings
{best_ctas}

## Phrases to Avoid
{avoid}

## Follow-Up Timing Insight
{analysis.get('followup_timing_insight', 'Insufficient data')}

## Estimated Response Rate
{analysis.get('overall_response_rate_estimate', 'Insufficient data')}

## Key Insights
{insights}

## Suggested Updates to persuasion.yml
(These are suggestions only — do not auto-apply. Review before updating config.)
{suggestions}
"""


def run() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    replies = read_jsonl(REPLIES_PATH)
    drafts = read_jsonl(DRAFT_QUEUE_PATH)
    opportunities = read_jsonl(OPPORTUNITIES_PATH)

    reply_classifications: dict[str, int] = {}
    for r in replies:
        cls = r.get("classification", "unknown")
        reply_classifications[cls] = reply_classifications.get(cls, 0) + 1

    data_summary = {
        "total_replies": len(replies),
        "total_drafts": len(drafts),
        "total_opportunities": len(opportunities),
        "reply_classifications": reply_classifications,
    }

    if len(replies) == 0:
        log.info("No reply data available for learning analysis — generating baseline report")

    analysis = analyze_patterns_via_claude(replies, drafts, opportunities)
    if not analysis:
        log.error("Failed to generate learning analysis")
        return

    report_md = render_learning_report(analysis, data_summary)
    today = date.today().isoformat()
    md_path = REPORTS_DIR / f"{today}_learning.md"
    with open(md_path, "w") as fh:
        fh.write(report_md)
    log.info("Wrote learning report: %s", md_path)

    learning_record = {
        "id": f"learn-{uuid.uuid4().hex[:12]}",
        "date": today,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "top_angle": analysis.get("top_performing_angles", [""])[0],
        "high_response_sectors": analysis.get("high_response_sectors", []),
        "key_insights": analysis.get("key_insights", []),
        "reply_count_analyzed": len(replies),
        "suggestions": analysis.get("persuasion_yml_suggestions", []),
    }

    with open(LEARNING_LOG_PATH, "a") as fh:
        fh.write(json.dumps(learning_record) + "\n")

    print(f"Learning report: {md_path}")
    print("\nSuggested persuasion.yml updates (review before applying):")
    for s in analysis.get("persuasion_yml_suggestions", []):
        print(f"  - {s}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze reply patterns and generate learning insights")
    parser.parse_args()
    run()


if __name__ == "__main__":
    main()
