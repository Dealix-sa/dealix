"""Market scanner: generates company stubs via Claude for GCC B2B sectors."""

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


def load_config() -> dict:
    with open(CONFIG_DIR / "markets.yml") as fh:
        return yaml.safe_load(fh)


def load_existing_names() -> set[str]:
    if not RAW_LEADS_PATH.exists():
        return set()
    names: set[str] = set()
    with open(RAW_LEADS_PATH) as fh:
        for line in fh:
            line = line.strip()
            if line:
                try:
                    names.add(json.loads(line)["company_name"].lower())
                except (json.JSONDecodeError, KeyError):
                    pass
    return names


def scan_via_claude(sector: dict, region: dict, count: int) -> list[dict]:
    """Call Claude to generate realistic GCC B2B company candidates
    based on sector and region config and return a structured JSON list."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        log.error("ANTHROPIC_API_KEY not set — cannot call Claude")
        return []

    import anthropic

    client = anthropic.Anthropic(api_key=api_key)

    prompt = f"""You are a GCC market research tool. Generate {count} realistic B2B company stubs for the following criteria.

Sector: {sector['label']}
Keywords: {', '.join(sector['keywords'])}
Region: {region['name']}
Min employees: {sector.get('min_employees', 20)}

Return a JSON array of objects, each with exactly these fields:
- company_name (string, realistic Arabic or English company name operating in {region['name']})
- website_hint (string, plausible domain like companyname.com or companyname.com.sa)
- sector (string, use: {sector['id']})
- country (string, use: {region['name']})
- source (string, always "market_scanner_ai")

Return only valid JSON. No explanation. No markdown fences."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = message.content[0].text.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return json.loads(raw)
    except Exception as exc:
        log.error("Claude call failed: %s", exc)
        return []


def run(sector_id: str | None, count: int) -> None:
    config = load_config()
    existing_names = load_existing_names()

    sectors = config["sectors"]
    regions = config["regions"]

    if sector_id:
        sectors = [s for s in sectors if s["id"] == sector_id]
        if not sectors:
            log.error("Sector %r not found in config", sector_id)
            sys.exit(1)

    total_new = 0
    total_dup = 0

    MEMORY_DIR.mkdir(parents=True, exist_ok=True)

    for sector in sectors:
        for region in sorted(regions, key=lambda r: r["priority"]):
            per_region = max(1, count // (len(regions) * len(sectors)))
            stubs = scan_via_claude(sector, region, per_region)
            new_records = []
            for stub in stubs:
                name = stub.get("company_name", "").strip()
                if not name:
                    continue
                if name.lower() in existing_names:
                    total_dup += 1
                    continue
                record = {
                    "id": f"lead-{uuid.uuid4().hex[:12]}",
                    "company_name": name,
                    "website_hint": stub.get("website_hint", ""),
                    "sector": stub.get("sector", sector["id"]),
                    "country": stub.get("country", region["name"]),
                    "source": stub.get("source", "market_scanner_ai"),
                    "scan_date": date.today().isoformat(),
                    "status": "raw",
                }
                new_records.append(record)
                existing_names.add(name.lower())
                total_new += 1

            with open(RAW_LEADS_PATH, "a") as fh:
                for rec in new_records:
                    fh.write(json.dumps(rec) + "\n")

    scanned = total_new + total_dup
    print(f"Scanned {scanned} leads, {total_new} new, {total_dup} duplicates")


def main() -> None:
    parser = argparse.ArgumentParser(description="Market scanner for GCC B2B leads")
    parser.add_argument("--sector", help="Sector ID to scan")
    parser.add_argument("--count", type=int, default=50, help="Number of leads to generate")
    args = parser.parse_args()
    run(args.sector, args.count)


if __name__ == "__main__":
    main()
