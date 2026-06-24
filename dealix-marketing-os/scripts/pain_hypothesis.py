"""Pain hypothesis: generates structured pain hypotheses from company briefs."""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from dotenv import load_dotenv

load_dotenv(BASE_DIR.parent / ".env")

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)

MEMORY_DIR = BASE_DIR / "memory"
BRIEFS_PATH = MEMORY_DIR / "company_briefs.jsonl"


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


def generate_pain_hypothesis(brief: dict) -> dict | None:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        log.error("ANTHROPIC_API_KEY not set")
        return None

    import anthropic

    client = anthropic.Anthropic(api_key=api_key)

    prompt = f"""Given this company brief, generate a structured pain hypothesis for B2B outreach.

Company: {brief['company_name']}
Sector: {brief['sector']}
Country: {brief['country']}
What they do: {brief.get('what_they_do', '')}
Likely pain points: {brief.get('likely_pain_points', [])}
Operations complexity: {brief.get('operations_complexity', 'medium')}
Best buyer: {brief.get('best_buyer_title', '')}

Return a JSON object with:
{{
  "primary_pain": "the single most likely operational pain",
  "pain_evidence": "what signals suggest this pain exists",
  "cost_of_inaction": "what it costs them to not solve this",
  "trigger_questions": ["question to ask to confirm pain", "another question"],
  "pain_intensity": "low|medium|high",
  "urgency": "low|medium|high",
  "hypothesis_confidence": 70
}}

Return only valid JSON. No explanation."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = message.content[0].text.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return json.loads(raw)
    except Exception as exc:
        log.error("Pain hypothesis failed for %s: %s", brief.get("company_name"), exc)
        return None


def run(limit: int) -> None:
    briefs = read_jsonl(BRIEFS_PATH)
    eligible = [b for b in briefs if b.get("status") == "researched" and not b.get("pain_hypothesis")][:limit]

    if not eligible:
        log.info("No eligible briefs for pain hypothesis")
        return

    processed = 0
    brief_map = {b["id"]: b for b in briefs}

    for brief in eligible:
        log.info("Generating pain hypothesis for %s", brief["company_name"])
        hypothesis = generate_pain_hypothesis(brief)
        if hypothesis:
            brief_map[brief["id"]]["pain_hypothesis"] = hypothesis
            processed += 1

    with open(BRIEFS_PATH, "w") as fh:
        for rec in brief_map.values():
            fh.write(json.dumps(rec) + "\n")

    print(f"Generated pain hypotheses for {processed} companies")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate pain hypotheses from company briefs")
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()
    run(args.limit)


if __name__ == "__main__":
    main()
