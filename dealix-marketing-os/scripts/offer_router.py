"""Offer router: routes each researched company to the best offer."""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import uuid
from datetime import datetime
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
BRIEFS_PATH = MEMORY_DIR / "company_briefs.jsonl"
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


def rewrite_jsonl(path: Path, records: list[dict]) -> None:
    with open(path, "w") as fh:
        for rec in records:
            fh.write(json.dumps(rec) + "\n")


def load_offers_config() -> dict:
    with open(CONFIG_DIR / "offers.yml") as fh:
        return yaml.safe_load(fh)


def load_personas_config() -> dict:
    with open(CONFIG_DIR / "buyer-personas.yml") as fh:
        return yaml.safe_load(fh)


def load_scoring_config() -> dict:
    with open(CONFIG_DIR / "scoring.yml") as fh:
        return yaml.safe_load(fh)


def tier_for_score(score: int, scoring: dict) -> str:
    tiers = scoring.get("tiers", {})
    if score >= tiers.get("A", {}).get("min_score", 80):
        return "A"
    if score >= tiers.get("B", {}).get("min_score", 60):
        return "B"
    return "nurture"


def route_via_claude(brief: dict, offers_config: dict, personas_config: dict) -> dict | None:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        log.error("ANTHROPIC_API_KEY not set")
        return None

    import anthropic

    client = anthropic.Anthropic(api_key=api_key)

    offers_text = "\n".join(
        f"- id: {o['id']}\n  label: {o['label']}\n  sectors: {o['target_sectors']}\n  pains: {o['pain_cluster']}\n  cta: {o['cta']}"
        for o in offers_config["offers"]
    )

    personas_text = "\n".join(
        f"- id: {p['id']}\n  titles: {p['titles']}\n  cta: {p['preferred_cta']}"
        for p in personas_config["personas"]
    )

    prompt = f"""You are a B2B offer routing engine. Given this company brief, determine the best offer and buyer routing.

Company: {brief['company_name']}
Sector: {brief['sector']}
Country: {brief['country']}
What they do: {brief.get('what_they_do', '')}
Pain points: {brief.get('likely_pain_points', [])}
Operations complexity: {brief.get('operations_complexity', 'medium')}
Data intensity: {brief.get('data_intensity', 'medium')}
Current best offer: {brief.get('best_offer', '')}
Fit score: {brief.get('fit_score', 0)}

Available offers:
{offers_text}

Available buyer personas:
{personas_text}

Return a JSON object with exactly these fields:
{{
  "primary_offer": "offer id from the list",
  "backup_offer": "second best offer id",
  "buyer_title": "exact job title to target",
  "pain_angle": "the specific pain to lead with",
  "why_this_offer": "one sentence explanation of fit",
  "cta": "specific call to action",
  "risk_notes": "any risks or caveats for this routing"
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
        log.error("Offer routing failed for %s: %s", brief.get("company_name"), exc)
        return None


def run() -> None:
    offers_config = load_offers_config()
    personas_config = load_personas_config()
    scoring_config = load_scoring_config()

    briefs = read_jsonl(BRIEFS_PATH)
    eligible = [b for b in briefs if b.get("status") == "researched"]

    existing_opps = read_jsonl(OPPORTUNITIES_PATH)
    existing_opp_ids = {o["company_id"] for o in existing_opps}

    if not eligible:
        log.info("No researched briefs to route")
        return

    processed = 0
    brief_map = {b["id"]: b for b in briefs}

    for brief in eligible:
        if brief["id"] in existing_opp_ids:
            log.info("Opportunity already exists for %s, skipping", brief["company_name"])
            brief_map[brief["id"]]["status"] = "offer_routed"
            continue

        log.info("Routing offer for %s", brief["company_name"])
        routing = route_via_claude(brief, offers_config, personas_config)
        if not routing:
            continue

        tier = tier_for_score(brief.get("fit_score", 0), scoring_config)

        opportunity = {
            "id": f"opp-{uuid.uuid4().hex[:12]}",
            "company_id": brief["id"],
            "company_name": brief["company_name"],
            "sector": brief.get("sector", ""),
            "country": brief.get("country", ""),
            "fit_score": brief.get("fit_score", 0),
            "tier": tier,
            "primary_offer": routing.get("primary_offer", ""),
            "backup_offer": routing.get("backup_offer", ""),
            "buyer_title": routing.get("buyer_title", ""),
            "pain_angle": routing.get("pain_angle", ""),
            "why_this_offer": routing.get("why_this_offer", ""),
            "cta": routing.get("cta", ""),
            "risk_notes": routing.get("risk_notes", ""),
            "status": "offer_routed",
            "created_at": datetime.utcnow().isoformat() + "Z",
        }

        with open(OPPORTUNITIES_PATH, "a") as fh:
            fh.write(json.dumps(opportunity) + "\n")

        brief_map[brief["id"]]["status"] = "offer_routed"
        brief_map[brief["id"]].update({
            "primary_offer": routing.get("primary_offer", ""),
            "buyer_title": routing.get("buyer_title", ""),
            "tier": tier,
        })

        processed += 1
        log.info("Routed %s -> tier=%s offer=%s", brief["company_name"], tier, routing.get("primary_offer"))

    rewrite_jsonl(BRIEFS_PATH, list(brief_map.values()))
    print(f"Routed {processed} companies to offers")


def main() -> None:
    parser = argparse.ArgumentParser(description="Route companies to best offers")
    parser.parse_args()
    run()


if __name__ == "__main__":
    main()
