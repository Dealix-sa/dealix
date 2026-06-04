"""Validate a commercial seed-leads JSONL file.

Enforces schema and safety: no scraping markers, consent must be declared,
no obviously-personal email/phone fields required. Missing file is OK (the
generator falls back to research-required placeholders).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

# Run both as `python scripts/<file>.py` and `python -m scripts.<file>`.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.commercial_launch_core import SEED_LEADS

REQUIRED_KEYS = [
    "lead_id",
    "company_name",
    "country",
    "vertical_hint",
    "language_hint",
    "source",
    "consent_status",
    "research_status",
]
ALLOWED_CONSENT = {"none", "public_business_contact", "opt_in", "inbound"}
FORBIDDEN_SOURCES = {"scraped", "scraper", "purchased_list", "linkedin_scrape"}


def validate_leads(path: Path | None = None) -> dict[str, Any]:
    path = path or SEED_LEADS
    report: dict[str, Any] = {
        "path": str(path),
        "exists": path.exists(),
        "valid": True,
        "count": 0,
        "errors": [],
        "warnings": [],
    }
    if not path.exists():
        report["warnings"].append(
            "Leads file missing — generator will use research-required placeholders."
        )
        return report

    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            lead = json.loads(line)
        except json.JSONDecodeError as exc:
            report["valid"] = False
            report["errors"].append(f"line {i}: invalid JSON ({exc})")
            continue
        report["count"] += 1
        for key in REQUIRED_KEYS:
            if key not in lead:
                report["valid"] = False
                report["errors"].append(f"line {i}: missing required key '{key}'")
        if lead.get("consent_status") not in ALLOWED_CONSENT:
            report["valid"] = False
            report["errors"].append(
                f"line {i}: consent_status '{lead.get('consent_status')}' not in {sorted(ALLOWED_CONSENT)}"
            )
        if str(lead.get("source", "")).lower() in FORBIDDEN_SOURCES:
            report["valid"] = False
            report["errors"].append(
                f"line {i}: forbidden source '{lead.get('source')}' (no scraping)"
            )
        if lead.get("consent_status") == "none":
            report["warnings"].append(
                f"line {i}: consent_status=none — research/consent required before any contact"
            )
    return report


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Validate commercial seed leads.")
    ap.add_argument("--file", default=None)
    args = ap.parse_args(argv)
    report = validate_leads(Path(args.file) if args.file else None)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
