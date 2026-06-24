"""
Draft generator — builds draft packages from classified company briefs.
Uses config for language, sector, persuasion angle, and offer routing.
"""

from __future__ import annotations
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

import yaml

BASE_DIR = Path(__file__).parent.parent
MEMORY_DIR = BASE_DIR / "memory"
CONFIG_DIR = BASE_DIR / "config"
PROMPTS_DIR = BASE_DIR / "prompts"


def load_config(filename: str) -> dict:
    """Load a YAML config file from the config directory."""
    path = CONFIG_DIR / filename
    return yaml.safe_load(path.read_text()) if path.exists() else {}


def load_prompt(filename: str) -> str:
    """Load a prompt file from the prompts directory."""
    path = PROMPTS_DIR / filename
    return path.read_text(encoding="utf-8") if path.exists() else ""


def build_draft_metadata(company: dict, channel: str, draft_type: str, angle: str) -> dict:
    """Build a draft metadata record for a given company, channel, type, and angle."""
    date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
    short_id = str(uuid.uuid4())[:8]
    company_slug = company.get("company", "unknown").lower().replace(" ", "_")[:30]

    return {
        "id": f"dq_{date_str}_{short_id}",
        "company": company.get("company", ""),
        "country": company.get("country", ""),
        "sector": company.get("sector", ""),
        "language": company.get("language", "en"),
        "buyer_title": company.get("buyer_title", ""),
        "offer": company.get("primary_offer", "ai_workflow_audit"),
        "entry_offer": company.get("entry_offer", "ai_workflow_audit"),
        "angle": angle,
        "channel": channel,
        "draft_type": draft_type,
        "draft_path": f"outputs/review_queue/{company_slug}_{channel}_{draft_type}.md",
        "quality_score": 0,
        "compliance_score": 0,
        "priority": "B",
        "status": "pending_quality_gate",
        "send_allowed": False,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def select_angle(sector: str, draft_type: str, persuasion_cfg: dict) -> str:
    """Select the A/B testing angle for a given sector and draft type."""
    angles = persuasion_cfg.get("ab_testing_angles", {}).get(sector, {})
    if draft_type == "cold_email":
        return angles.get("angle_a", "workflow_efficiency")
    elif draft_type == "followup_1":
        return angles.get("angle_b", "time_savings")
    return angles.get("angle_c", "knowledge_reuse")


def generate_draft_package(company: dict) -> list[dict]:
    """Generate the full draft package for a single classified company."""
    persuasion_cfg = load_config("persuasion.yml")
    scoring_cfg = load_config("scoring.yml")
    channel_cfg = load_config("channel-strategy.yml")

    sector = company.get("sector", "b2b_services")
    score = company.get("fit_score", 70)

    tier_a_threshold = scoring_cfg.get("scoring", {}).get("thresholds", {}).get("tier_a_priority", 85)
    tier_b_threshold = scoring_cfg.get("scoring", {}).get("thresholds", {}).get("tier_b_qualified", 70)

    if score >= tier_a_threshold:
        draft_types = channel_cfg.get("channel_strategy", {}).get("draft_package_per_company", {}).get("full", [
            "cold_email", "followup_1", "followup_2", "linkedin_short", "website_form_version",
        ])
    elif score >= tier_b_threshold:
        draft_types = channel_cfg.get("channel_strategy", {}).get("draft_package_per_company", {}).get("standard", [
            "cold_email", "followup_1", "linkedin_short", "website_form_version",
        ])
    else:
        draft_types = ["cold_email", "website_form_version"]

    channel_map = {
        "cold_email": "email",
        "followup_1": "email",
        "followup_2": "email",
        "linkedin_short": "linkedin",
        "website_form_version": "website_form",
        "whatsapp_business_short": "whatsapp_business",
        "referral_ask": "referral",
        "one_pager_recommendation": "email",
        "discovery_call_agenda": "email",
        "proposal_seed": "email",
    }

    drafts = []
    for draft_type in draft_types:
        channel = channel_map.get(draft_type, "email")
        angle = select_angle(sector, draft_type, persuasion_cfg)
        draft = build_draft_metadata(company, channel, draft_type, angle)
        drafts.append(draft)

    return drafts


def generate_all_drafts(companies: list[dict]) -> list[dict]:
    """Generate draft packages for all companies and append to memory/draft_queue.jsonl."""
    all_drafts: list[dict] = []
    for company in companies:
        drafts = generate_draft_package(company)
        all_drafts.extend(drafts)

    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    queue_path = MEMORY_DIR / "draft_queue.jsonl"
    with open(queue_path, "a") as f:
        for draft in all_drafts:
            f.write(json.dumps(draft, ensure_ascii=False) + "\n")

    return all_drafts
