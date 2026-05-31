"""Draft writer: generates all outreach content pieces per company."""

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
BRIEFS_PATH = MEMORY_DIR / "company_briefs.jsonl"
DRAFT_QUEUE_PATH = MEMORY_DIR / "draft_queue.jsonl"

TIER_A_DRAFTS = [
    "cold_email",
    "followup_1",
    "followup_2",
    "referral_request",
    "one_pager_outline",
    "linkedin_message",
    "discovery_call_agenda",
    "proposal_seed",
]
TIER_B_DRAFTS = ["cold_email", "followup_1", "followup_2", "linkedin_message"]
NURTURE_DRAFTS = ["cold_email", "linkedin_message"]


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
    with open(CONFIG_DIR / "persuasion.yml") as fh:
        return yaml.safe_load(fh)


def load_offers_config() -> dict:
    with open(CONFIG_DIR / "offers.yml") as fh:
        return yaml.safe_load(fh)


def draft_types_for_tier(tier: str) -> list[str]:
    if tier == "A":
        return TIER_A_DRAFTS
    if tier == "B":
        return TIER_B_DRAFTS
    return NURTURE_DRAFTS


def offer_label_for_id(offer_id: str, offers_config: dict) -> str:
    for o in offers_config["offers"]:
        if o["id"] == offer_id:
            return o["label"]
    return offer_id


def generate_draft_via_claude(
    draft_type: str,
    opportunity: dict,
    brief: dict,
    persuasion_config: dict,
    offers_config: dict,
) -> dict | None:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        log.error("ANTHROPIC_API_KEY not set")
        return None

    import anthropic

    client = anthropic.Anthropic(api_key=api_key)

    formula = persuasion_config.get("formula", {})
    formula_steps = "\n".join(
        f"{i+1}. {step['id']}: {step['instruction']}"
        for i, step in enumerate(formula.get("steps", []))
    )

    offer_label = offer_label_for_id(opportunity.get("primary_offer", ""), offers_config)

    type_instructions = {
        "cold_email": "Write a cold outreach email. Include subject line and body. Apply the SPECIFIC-PAIN-PROOF-ASK formula strictly. Max 200 words in body.",
        "followup_1": "Write a short follow-up email (day 5). Reference the original email briefly. One new value point. Max 100 words.",
        "followup_2": "Write a value follow-up email (day 12). Share one relevant insight or observation about their sector. Max 150 words.",
        "referral_request": "Write a referral request email. Politely ask if they can point to the right person. Max 80 words.",
        "one_pager_outline": "Write a one-page offer outline in structured sections: Problem / Solution / How It Works / Proof / Investment Range / Next Step. Use bullet points.",
        "linkedin_message": "Write a LinkedIn connection request message. Max 300 characters. Specific observation, no pitch.",
        "discovery_call_agenda": "Write a 30-minute discovery call agenda. 5-6 agenda items with time allocations. Professional, peer-level tone.",
        "proposal_seed": "Write the opening framing paragraph for a proposal (2-3 sentences). Sets context, references their pain, positions Dealix as the solution mechanism. No pricing.",
    }

    instruction = type_instructions.get(draft_type, f"Write a {draft_type} piece.")

    prompt = f"""You are a B2B outreach specialist for Dealix, an operational intelligence platform for GCC businesses.

Company: {opportunity['company_name']}
Sector: {opportunity['sector']}
Country: {opportunity['country']}
Buyer title: {opportunity.get('buyer_title', 'Operations Director')}
Primary offer: {offer_label}
Pain angle: {opportunity.get('pain_angle', '')}
Why this offer: {opportunity.get('why_this_offer', '')}
Draft angle: {brief.get('draft_angle', '')}
CTA: {opportunity.get('cta', '30-minute diagnostic call')}

Persuasion formula (SPECIFIC-PAIN-PROOF-ASK):
{formula_steps}

Task: {instruction}

IMPORTANT RULES:
- Never use guaranteed outcome language (no "guarantee", "100%", "assured results")
- Never reference cold WhatsApp, LinkedIn automation, or scraping
- Never make up specific verified percentages — use directional language only
- Be specific to this company's sector and operational context
- Tone: professional peer, GCC-appropriate formality

Return a JSON object with:
{{
  "subject": "email subject line (empty string for non-email types)",
  "body": "the full draft content"
}}

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
        log.error("Draft generation failed for %s/%s: %s", opportunity.get("company_name"), draft_type, exc)
        return None


def run() -> None:
    persuasion_config = load_persuasion_config()
    offers_config = load_offers_config()

    opportunities = read_jsonl(OPPORTUNITIES_PATH)
    eligible = [o for o in opportunities if o.get("status") == "offer_routed"]

    briefs = read_jsonl(BRIEFS_PATH)
    brief_map = {b["id"]: b for b in briefs}

    existing_drafts = read_jsonl(DRAFT_QUEUE_PATH)
    existing_keys = {(d["company_id"], d["draft_type"]) for d in existing_drafts}

    if not eligible:
        log.info("No routed opportunities to generate drafts for")
        return

    total_generated = 0

    for opp in eligible:
        tier = opp.get("tier", "nurture")
        draft_types = draft_types_for_tier(tier)
        brief = brief_map.get(opp["company_id"], {})

        for draft_type in draft_types:
            key = (opp["company_id"], draft_type)
            if key in existing_keys:
                log.debug("Draft already exists: %s/%s", opp["company_name"], draft_type)
                continue

            log.info("Generating %s for %s (tier %s)", draft_type, opp["company_name"], tier)
            content = generate_draft_via_claude(draft_type, opp, brief, persuasion_config, offers_config)
            if not content:
                continue

            draft = {
                "id": f"draft-{uuid.uuid4().hex[:12]}",
                "company_id": opp["company_id"],
                "company_name": opp["company_name"],
                "opportunity_id": opp["id"],
                "tier": tier,
                "draft_type": draft_type,
                "subject": content.get("subject", ""),
                "body": content.get("body", ""),
                "quality_score": None,
                "approved_for_review": None,
                "issues": [],
                "created_at": datetime.utcnow().isoformat() + "Z",
                "status": "draft_generated",
            }

            with open(DRAFT_QUEUE_PATH, "a") as fh:
                fh.write(json.dumps(draft) + "\n")

            existing_keys.add(key)
            total_generated += 1

    print(f"Generated {total_generated} drafts")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate outreach drafts for routed opportunities")
    parser.parse_args()
    run()


if __name__ == "__main__":
    main()
