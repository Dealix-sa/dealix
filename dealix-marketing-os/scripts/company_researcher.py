"""Company researcher: enriches raw leads into full company briefs via Claude."""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import uuid
from datetime import date
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
RAW_LEADS_PATH = MEMORY_DIR / "raw_leads.jsonl"
BRIEFS_PATH = MEMORY_DIR / "company_briefs.jsonl"


def load_scoring_config() -> dict:
    with open(CONFIG_DIR / "scoring.yml") as fh:
        return yaml.safe_load(fh)


def load_offers_config() -> dict:
    with open(CONFIG_DIR / "offers.yml") as fh:
        return yaml.safe_load(fh)


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


def compute_fit_score(brief: dict, scoring: dict) -> int:
    score = 0
    dims = {d["id"]: d for d in scoring["dimensions"]}

    ops_complexity = brief.get("operations_complexity", "low")
    d = dims.get("operational_complexity", {})
    score += d.get("levels", {}).get(ops_complexity, 5)

    data_intensity = brief.get("data_intensity", "low")
    d = dims.get("data_intensity", {})
    score += d.get("levels", {}).get(data_intensity, 4)

    sector_priority = brief.get("_sector_priority", 3)
    d = dims.get("sector_priority", {})
    if sector_priority == 1:
        score += d.get("levels", {}).get("priority_1", 8)
    elif sector_priority == 2:
        score += d.get("levels", {}).get("priority_2", 14)
    else:
        score += d.get("levels", {}).get("priority_3", 8)

    buyer_access = brief.get("_buyer_accessibility", "medium")
    d = dims.get("buyer_accessibility", {})
    score += d.get("levels", {}).get(buyer_access, 9)

    pain_signal = brief.get("_pain_signal_strength", "weak")
    d = dims.get("pain_signal_strength", {})
    score += d.get("levels", {}).get(pain_signal, 2)

    deal_size = brief.get("_deal_size_potential", "medium")
    d = dims.get("deal_size_potential", {})
    score += d.get("levels", {}).get(deal_size, 6)

    return min(score, 100)


def best_offer_for_sector(sector: str, offers_config: dict) -> str:
    for offer in offers_config["offers"]:
        if sector in offer.get("target_sectors", []):
            return offer["id"]
    return offers_config.get("default_offer", "field_ops_intelligence")


def research_company_via_claude(lead: dict, offers_config: dict) -> dict | None:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        log.error("ANTHROPIC_API_KEY not set")
        return None

    import anthropic

    client = anthropic.Anthropic(api_key=api_key)

    offers_text = "\n".join(
        f"- {o['id']}: {o['label']} ({o['tagline']}) — sectors: {o['target_sectors']}"
        for o in offers_config["offers"]
    )

    prompt = f"""You are a B2B operations intelligence analyst. Research this GCC company and return a structured JSON object.

Company: {lead['company_name']}
Website hint: {lead.get('website_hint', 'unknown')}
Sector: {lead['sector']}
Country: {lead['country']}

Available Dealix offers:
{offers_text}

Return a JSON object with exactly these fields (no extra fields, no markdown):
{{
  "what_they_do": "one sentence description",
  "business_model": "B2B services / B2C / mixed",
  "likely_departments": ["list", "of", "departments"],
  "likely_workflows": ["list", "of", "key", "workflows"],
  "likely_pain_points": ["list", "of", "operational", "pains"],
  "public_signals": ["any", "signals", "about", "their", "operations"],
  "operations_complexity": "low|medium|high",
  "data_intensity": "low|medium|high",
  "best_buyer_title": "most likely decision maker title",
  "best_offer": "one of the offer IDs above",
  "why_this_offer_fits": "one sentence explanation",
  "draft_angle": "opening angle for cold outreach",
  "confidence": 60,
  "status": "researched",
  "_buyer_accessibility": "low|medium|high",
  "_pain_signal_strength": "weak|moderate|strong",
  "_deal_size_potential": "low|medium|high"
}}

Base your response on what is plausible for a {lead['sector']} company in {lead['country']}.
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
        log.error("Claude research failed for %s: %s", lead["company_name"], exc)
        return None


def run(limit: int) -> None:
    scoring = load_scoring_config()
    offers = load_offers_config()
    sectors_config: dict[str, int] = {}
    try:
        import yaml as _yaml
        with open(CONFIG_DIR / "markets.yml") as fh:
            markets = _yaml.safe_load(fh)
        for s in markets.get("sectors", []):
            sectors_config[s["id"]] = s.get("priority", 3)
    except Exception:
        pass

    leads = read_jsonl(RAW_LEADS_PATH)
    raw_leads = [l for l in leads if l.get("status") == "raw"][:limit]

    if not raw_leads:
        log.info("No raw leads to research")
        return

    existing_briefs = read_jsonl(BRIEFS_PATH)
    existing_ids = {b["id"] for b in existing_briefs}

    processed = 0
    for lead in raw_leads:
        if lead["id"] in existing_ids:
            log.info("Brief already exists for %s, skipping", lead["company_name"])
            continue

        log.info("Researching %s", lead["company_name"])
        enrichment = research_company_via_claude(lead, offers)
        if not enrichment:
            continue

        sector_priority = sectors_config.get(lead.get("sector", ""), 3)
        enrichment["_sector_priority"] = sector_priority

        brief = {
            "id": lead["id"],
            "company_name": lead["company_name"],
            "website": lead.get("website_hint", ""),
            "country": lead.get("country", ""),
            "sector": lead.get("sector", ""),
            "what_they_do": enrichment.get("what_they_do", ""),
            "business_model": enrichment.get("business_model", ""),
            "likely_departments": enrichment.get("likely_departments", []),
            "likely_workflows": enrichment.get("likely_workflows", []),
            "likely_pain_points": enrichment.get("likely_pain_points", []),
            "public_signals": enrichment.get("public_signals", []),
            "operations_complexity": enrichment.get("operations_complexity", "medium"),
            "data_intensity": enrichment.get("data_intensity", "medium"),
            "best_buyer_title": enrichment.get("best_buyer_title", ""),
            "best_offer": enrichment.get("best_offer", best_offer_for_sector(lead.get("sector", ""), offers)),
            "why_this_offer_fits": enrichment.get("why_this_offer_fits", ""),
            "draft_angle": enrichment.get("draft_angle", ""),
            "confidence": enrichment.get("confidence", 50),
            "fit_score": 0,
            "research_date": date.today().isoformat(),
            "status": enrichment.get("status", "researched"),
            "_buyer_accessibility": enrichment.get("_buyer_accessibility", "medium"),
            "_pain_signal_strength": enrichment.get("_pain_signal_strength", "weak"),
            "_deal_size_potential": enrichment.get("_deal_size_potential", "medium"),
            "_sector_priority": sector_priority,
        }
        brief["fit_score"] = compute_fit_score(brief, scoring)

        with open(BRIEFS_PATH, "a") as fh:
            fh.write(json.dumps(brief) + "\n")

        for lead_rec in leads:
            if lead_rec["id"] == lead["id"]:
                lead_rec["status"] = "researched"
                break

        rewrite_jsonl(RAW_LEADS_PATH, leads)
        processed += 1
        log.info("Completed brief for %s (fit_score=%d)", lead["company_name"], brief["fit_score"])

    print(f"Researched {processed} companies")


def main() -> None:
    parser = argparse.ArgumentParser(description="Enrich raw leads into company briefs")
    parser.add_argument("--limit", type=int, default=20, help="Max leads to research")
    args = parser.parse_args()
    run(args.limit)


if __name__ == "__main__":
    main()
