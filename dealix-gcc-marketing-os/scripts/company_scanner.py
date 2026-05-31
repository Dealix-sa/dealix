"""
GCC Company Scanner — finds and classifies companies from configured sources.
Outputs to memory/raw_leads.jsonl and memory/companies.jsonl
"""

from __future__ import annotations
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

BASE_DIR = Path(__file__).parent.parent
MEMORY_DIR = BASE_DIR / "memory"
CONFIG_DIR = BASE_DIR / "config"


def load_config(filename: str) -> dict:
    """Load a YAML config file from the config directory."""
    path = CONFIG_DIR / filename
    if not path.exists():
        return {}
    with open(path) as f:
        return yaml.safe_load(f) or {}


def classify_company(company: dict, countries_cfg: dict, sectors_cfg: dict) -> dict:
    """Classify a raw lead into a structured company record with language, offer, and tone routing."""
    country = company.get("country", "").lower().replace(" ", "_")
    sector = company.get("sector_hint", "").lower().replace(" ", "_")
    website_lang = company.get("website_language", "")

    country_cfg = countries_cfg.get("countries", {}).get(country, {})
    sector_cfg = sectors_cfg.get("sectors", {}).get(sector, {})

    language = "en"
    if website_lang == "ar":
        language = "ar"
    elif sector_cfg.get("language_preference", "").startswith("formal_arabic"):
        language = "ar"
    elif sector_cfg.get("language_preference", "").startswith("english"):
        language = "en"
    elif "ar" in country_cfg.get("languages", ["en"]):
        language = "ar"

    priority_sectors = country_cfg.get("priority_sectors", [])
    sector_is_priority = sector in priority_sectors

    return {
        "id": str(uuid.uuid4()),
        "company": company.get("name", ""),
        "country": country,
        "sector": sector,
        "language": language,
        "website": company.get("website", ""),
        "contact_email": company.get("contact_email", ""),
        "buyer_title": sector_cfg.get("buyer_titles", ["CEO"])[0] if sector_cfg else "CEO",
        "primary_offer": sector_cfg.get("primary_offer", "ai_workflow_audit"),
        "entry_offer": sector_cfg.get("entry_offer", "ai_workflow_audit"),
        "preferred_tone": sector_cfg.get("preferred_tone", "practical"),
        "sector_is_priority": sector_is_priority,
        "classified_at": datetime.now(timezone.utc).isoformat(),
        "source": company.get("source", "manual"),
    }


def scan_and_classify(raw_leads: list[dict]) -> list[dict]:
    """Classify a list of raw lead dicts and append results to memory/companies.jsonl."""
    countries_cfg = load_config("countries.yml")
    sectors_cfg = load_config("sectors.yml")
    classified = [classify_company(lead, countries_cfg, sectors_cfg) for lead in raw_leads]

    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    out_path = MEMORY_DIR / "companies.jsonl"
    with open(out_path, "a") as f:
        for company in classified:
            f.write(json.dumps(company, ensure_ascii=False) + "\n")

    return classified


if __name__ == "__main__":
    sample_leads: list[dict[str, Any]] = [
        {
            "name": "Example Law Firm",
            "country": "saudi_arabia",
            "sector_hint": "legal",
            "website_language": "ar",
            "contact_email": "info@examplelawfirm.com.sa",
            "source": "manual_sample",
        },
    ]
    results = scan_and_classify(sample_leads)
    print(f"Classified {len(results)} companies")
