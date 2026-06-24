"""Suppression manager: manages the suppression list to prevent re-contacting opted-out leads."""

from __future__ import annotations

import argparse
import json
import logging
import sys
import uuid
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from dotenv import load_dotenv

load_dotenv(BASE_DIR.parent / ".env")

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)

MEMORY_DIR = BASE_DIR / "memory"
SUPPRESSION_PATH = MEMORY_DIR / "suppression.jsonl"
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


def is_suppressed(company_id: str) -> bool:
    suppressed = read_jsonl(SUPPRESSION_PATH)
    return any(s.get("company_id") == company_id for s in suppressed)


def add_suppression(company_id: str, company_name: str, reason: str) -> None:
    if is_suppressed(company_id):
        log.info("%s is already suppressed", company_name)
        return
    record = {
        "id": f"supp-{uuid.uuid4().hex[:12]}",
        "company_id": company_id,
        "company_name": company_name,
        "reason": reason,
        "suppressed_at": datetime.utcnow().isoformat() + "Z",
    }
    with open(SUPPRESSION_PATH, "a") as fh:
        fh.write(json.dumps(record) + "\n")
    log.info("Suppressed: %s (reason: %s)", company_name, reason)


def list_suppressed() -> list[dict]:
    return read_jsonl(SUPPRESSION_PATH)


def check_batch(company_ids: list[str]) -> dict[str, bool]:
    suppressed = read_jsonl(SUPPRESSION_PATH)
    suppressed_ids = {s["company_id"] for s in suppressed}
    return {cid: cid in suppressed_ids for cid in company_ids}


def run(action: str, company_id: str, company_name: str, reason: str) -> None:
    if action == "add":
        if not company_id or not company_name:
            log.error("--company-id and --company-name required for add action")
            sys.exit(1)
        add_suppression(company_id, company_name, reason or "manual")
        print(f"Suppressed: {company_name}")

    elif action == "check":
        if not company_id:
            log.error("--company-id required for check action")
            sys.exit(1)
        result = is_suppressed(company_id)
        print(f"{company_id}: {'SUPPRESSED' if result else 'not suppressed'}")

    elif action == "list":
        records = list_suppressed()
        if not records:
            print("No suppressed companies")
            return
        print(f"Suppressed companies ({len(records)}):")
        for rec in records:
            print(f"  {rec.get('company_name', rec.get('company_id', ''))} — {rec.get('reason', '')} — {rec.get('suppressed_at', '')[:10]}")

    elif action == "sync-opportunities":
        suppressed = read_jsonl(SUPPRESSION_PATH)
        suppressed_ids = {s["company_id"] for s in suppressed}
        opportunities = read_jsonl(OPPORTUNITIES_PATH)
        updated = 0
        for opp in opportunities:
            if opp.get("company_id") in suppressed_ids and not opp.get("suppressed"):
                opp["suppressed"] = True
                opp["status"] = "suppressed"
                updated += 1
        with open(OPPORTUNITIES_PATH, "w") as fh:
            for opp in opportunities:
                fh.write(json.dumps(opp) + "\n")
        print(f"Synced suppression status for {updated} opportunities")

    else:
        log.error("Unknown action: %s", action)
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Manage suppression list")
    parser.add_argument("--action", choices=["add", "check", "list", "sync-opportunities"], required=True)
    parser.add_argument("--company-id", default="", help="Company ID")
    parser.add_argument("--company-name", default="", help="Company name")
    parser.add_argument("--reason", default="manual", help="Suppression reason")
    args = parser.parse_args()
    run(args.action, args.company_id, args.company_name, args.reason)


if __name__ == "__main__":
    main()
