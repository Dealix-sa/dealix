#!/usr/bin/env python3
"""Capital OS weekly investor readiness brief script.

Generates a weekly investor brief by calling /api/v1/capital-os/* endpoints
or reading the local ledger in dry-run mode.

Usage:
  python scripts/run_capital_os_brief.py [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def run(dry_run: bool) -> None:
    today = date.today().isoformat()
    output_dir = ROOT / "data" / "founder_briefs"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"CAPITAL_OS_{today}.md"

    if dry_run:
        # Use local capital_os module directly — no HTTP
        try:
            from auto_client_acquisition.capital_os import list_assets
            from auto_client_acquisition.investment_os import (
                FUNDING_READINESS_ITEMS,
                OPERATING_COVENANTS,
            )
            assets = list_assets(limit=200)
            checklist = list(FUNDING_READINESS_ITEMS)
            covenants = list(OPERATING_COVENANTS) if OPERATING_COVENANTS else []
        except Exception as exc:
            print(f"[Capital OS] Import error: {exc}", file=sys.stderr)
            assets = []
            checklist = []
            covenants = []

        brief = f"""# Capital OS — Investor Readiness Brief
## أسبوع {today}

**Generated**: {datetime.now(timezone.utc).isoformat()}
**Mode**: dry-run (local modules)

---

## Capital Assets in Ledger
- **Total Assets**: {len(assets)}

## Funding Readiness Checklist ({len(checklist)} items)
"""
        for item in checklist:
            brief += f"- [ ] {item}\n"

        brief += f"""
## Operating Covenants ({len(covenants)} items)
"""
        for c in covenants[:5]:
            brief += f"- {c}\n"

        brief += "\n---\n_is_estimate=True. Review before external sharing._\n"
        output_path.write_text(brief, encoding="utf-8")
        print(f"[Capital OS] Brief written → {output_path}")
        return

    # Live mode
    import urllib.request
    api_base = os.environ.get("DEALIX_API_BASE", "https://api.dealix.me")
    admin_key = os.environ.get("DEALIX_ADMIN_API_KEY", "")

    def _get(path: str) -> dict:
        url = f"{api_base}{path}"
        req = urllib.request.Request(url, headers={"X-Admin-API-Key": admin_key})
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())

    try:
        checklist_data = _get("/api/v1/capital-os/funding-checklist")
        readiness_data = _get("/api/v1/capital-os/readiness-score")
    except Exception as exc:
        print(f"[Capital OS] API call failed: {exc}", file=sys.stderr)
        sys.exit(1)

    score = readiness_data.get("readiness_score", 0)
    band = readiness_data.get("band", "unknown")

    brief = f"""# Capital OS — Investor Readiness Brief
## أسبوع {today}

**Generated**: {datetime.now(timezone.utc).isoformat()}
**Mode**: live

---

## Investor Readiness Score
- **Score**: {score}/100
- **Band**: {band}

## Funding Checklist
"""
    for item in checklist_data.get("checklist", []):
        brief += f"- [ ] {item}\n"

    brief += "\n---\n_is_estimate=True. Review before external sharing._\n"
    output_path.write_text(brief, encoding="utf-8")
    print(f"[Capital OS] Brief written → {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    run(dry_run=args.dry_run)
