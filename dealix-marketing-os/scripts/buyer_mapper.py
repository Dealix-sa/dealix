"""Buyer mapper: maps companies to specific buyer contacts via persona matching."""

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
OPPORTUNITIES_PATH = MEMORY_DIR / "opportunities.jsonl"
CONTACTS_PATH = MEMORY_DIR / "contacts.jsonl"


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


def load_personas_config() -> dict:
    with open(CONFIG_DIR / "buyer-personas.yml") as fh:
        return yaml.safe_load(fh)


def map_buyer_via_claude(opportunity: dict, personas_config: dict) -> dict | None:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        log.error("ANTHROPIC_API_KEY not set")
        return None

    import anthropic

    client = anthropic.Anthropic(api_key=api_key)

    personas_text = json.dumps(personas_config["personas"], indent=2)

    prompt = f"""You are a B2B buyer mapping engine. Map a realistic buyer contact for this company.

Company: {opportunity['company_name']}
Sector: {opportunity['sector']}
Country: {opportunity['country']}
Target buyer title: {opportunity.get('buyer_title', 'Operations Director')}
Primary offer: {opportunity.get('primary_offer', '')}
Pain angle: {opportunity.get('pain_angle', '')}

Available personas:
{personas_text}

Generate a realistic (fictitious) buyer contact. Return a JSON object with:
{{
  "first_name": "realistic first name for {opportunity['country']}",
  "last_name": "realistic last name for {opportunity['country']}",
  "title": "exact job title",
  "persona_id": "matching persona id from the list",
  "language_register": "formal|semi-formal|direct",
  "preferred_cta": "best CTA for this persona",
  "outreach_notes": "any special considerations for outreach to this person"
}}

Return only valid JSON. No explanation."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = message.content[0].text.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return json.loads(raw)
    except Exception as exc:
        log.error("Buyer mapping failed for %s: %s", opportunity.get("company_name"), exc)
        return None


def run(limit: int) -> None:
    personas_config = load_personas_config()
    opportunities = read_jsonl(OPPORTUNITIES_PATH)
    eligible = [o for o in opportunities if o.get("status") == "offer_routed"][:limit]

    existing_contacts = read_jsonl(CONTACTS_PATH)
    existing_company_ids = {c["company_id"] for c in existing_contacts}

    if not eligible:
        log.info("No eligible opportunities to map buyers for")
        return

    processed = 0
    for opp in eligible:
        if opp["company_id"] in existing_company_ids:
            log.info("Contact already exists for %s", opp["company_name"])
            continue

        log.info("Mapping buyer for %s", opp["company_name"])
        buyer = map_buyer_via_claude(opp, personas_config)
        if not buyer:
            continue

        contact = {
            "id": f"contact-{uuid.uuid4().hex[:12]}",
            "company_id": opp["company_id"],
            "opportunity_id": opp["id"],
            "company_name": opp["company_name"],
            "first_name": buyer.get("first_name", ""),
            "last_name": buyer.get("last_name", ""),
            "title": buyer.get("title", ""),
            "persona_id": buyer.get("persona_id", ""),
            "language_register": buyer.get("language_register", "formal"),
            "preferred_cta": buyer.get("preferred_cta", ""),
            "outreach_notes": buyer.get("outreach_notes", ""),
            "status": "mapped",
            "created_at": datetime.utcnow().isoformat() + "Z",
        }

        with open(CONTACTS_PATH, "a") as fh:
            fh.write(json.dumps(contact) + "\n")

        processed += 1
        log.info("Mapped buyer %s %s for %s", buyer.get("first_name"), buyer.get("last_name"), opp["company_name"])

    print(f"Mapped {processed} buyers")


def main() -> None:
    parser = argparse.ArgumentParser(description="Map buyer contacts to opportunities")
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()
    run(args.limit)


if __name__ == "__main__":
    main()
