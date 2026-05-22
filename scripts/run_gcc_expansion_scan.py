#!/usr/bin/env python3
"""GCC Expansion Intelligence — weekly market scan script.

Runs market intelligence scan across all 6 GCC countries.
Supports --dry-run (local modules) and live mode (API call).

Usage:
  python scripts/run_gcc_expansion_scan.py [--dry-run]
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

COUNTRIES = ["SA", "AE", "KW", "BH", "QA", "OM"]
COUNTRY_NAMES_AR = {
    "SA": "المملكة العربية السعودية",
    "AE": "الإمارات العربية المتحدة",
    "KW": "الكويت",
    "BH": "البحرين",
    "QA": "قطر",
    "OM": "عُمان",
}
COUNTRY_NAMES_EN = {
    "SA": "Saudi Arabia",
    "AE": "UAE",
    "KW": "Kuwait",
    "BH": "Bahrain",
    "QA": "Qatar",
    "OM": "Oman",
}


def run(dry_run: bool) -> None:
    today = date.today().isoformat()
    output_dir = ROOT / "data" / "founder_briefs"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"GCC_EXPANSION_{today}.md"

    if dry_run:
        signal_types = []
        try:
            from auto_client_acquisition.market_intelligence import SIGNAL_TYPES
            signal_types = list(SIGNAL_TYPES) if SIGNAL_TYPES else []
        except Exception as exc:
            print(f"[GCC Scan] Import warning (non-fatal): {exc}", file=sys.stderr)

        brief = f"""# رادار التوسع الخليجي — GCC Expansion Scan
## {today}

**Generated**: {datetime.now(timezone.utc).isoformat()}
**Mode**: dry-run (local modules)
**Signal Types Available**: {len(signal_types)}

---

## GCC Markets Coverage

| Code | Country (AR) | Country (EN) | Status |
|------|-------------|--------------|--------|
"""
        for code in COUNTRIES:
            brief += f"| **{code}** | {COUNTRY_NAMES_AR[code]} | {COUNTRY_NAMES_EN[code]} | scanning |\n"

        brief += f"""
---

## API Endpoints Available
- `GET /api/v1/gcc-expansion/gcc-overview` — All 6 markets summary
- `GET /api/v1/gcc-expansion/market-scan?country=SA` — Sector pulse per country
- `GET /api/v1/gcc-expansion/hot-cities?country=SA` — City heat ranking
- `GET /api/v1/gcc-expansion/opportunity-feed?country=SA` — Ranked opportunities
- `POST /api/v1/gcc-expansion/signal-detect` — Detect hiring/funding/ads/tender signals

---
_is_estimate=True. All market intelligence requires founder validation before action._
"""
        output_path.write_text(brief, encoding="utf-8")
        print(f"[GCC Scan] Brief written → {output_path}")
        return

    # Live mode
    import urllib.request
    api_base = os.environ.get("DEALIX_API_BASE", "https://api.dealix.me")
    admin_key = os.environ.get("DEALIX_ADMIN_API_KEY", "")
    url = f"{api_base}/api/v1/gcc-expansion/gcc-overview"

    req = urllib.request.Request(url, headers={"X-Admin-API-Key": admin_key})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
    except Exception as exc:
        print(f"[GCC Scan] API call failed: {exc}", file=sys.stderr)
        sys.exit(1)

    countries = data.get("countries", [])
    brief = f"""# رادار التوسع الخليجي — GCC Expansion Scan
## {today}

**Generated**: {datetime.now(timezone.utc).isoformat()}
**Mode**: live

---

## GCC Overview
"""
    for c in countries:
        code = c.get("country_code", "")
        name_ar = c.get("country_name_ar", "")
        top_sector = c.get("top_sector", "N/A")
        heat = c.get("heat_score", 0)
        brief += f"- **{code}** {name_ar}: Top sector = {top_sector}, Heat = {heat:.1f}/100\n"

    if not countries:
        brief += "_No country data returned from API._\n"

    brief += "\n---\n_is_estimate=True. All figures require founder validation._\n"
    output_path.write_text(brief, encoding="utf-8")
    print(f"[GCC Scan] Brief written → {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    run(dry_run=args.dry_run)
