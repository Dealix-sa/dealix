#!/usr/bin/env python3
"""M&A Radar daily scan script.

Calls /api/v1/m-and-a/radar and writes a founder brief markdown file.
Supports --dry-run (no external writes to the API; reads ledger locally).

Usage:
  python scripts/run_m_and_a_radar_scan.py [--dry-run]
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
    output_path = output_dir / f"MA_RADAR_{today}.md"

    if dry_run:
        # Read ledger locally (no HTTP)
        ledger_path = ROOT / "var" / "m_and_a_proposals.jsonl"
        rows: list[dict] = []
        if ledger_path.exists():
            for line in ledger_path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line:
                    try:
                        rows.append(json.loads(line))
                    except Exception:
                        pass

        total_pipeline = sum(r.get("proposed_offer_sar", 0) for r in rows)
        avg_multiple = (
            sum(r.get("multiplier", 0) for r in rows) / len(rows) if rows else 0.0
        )

        brief = f"""# رادار الاستحواذ والاندماج — {today}
## M&A Radar Daily Brief

**Generated**: {datetime.now(timezone.utc).isoformat()}
**Mode**: dry-run (local ledger read)

---

## KPIs
- **Targets Evaluated**: {len(rows)}
- **Total Pipeline**: SAR {total_pipeline:,.0f}
- **Avg EBITDA Multiple**: {avg_multiple:.1f}x

## Recent Proposals
"""
        for r in rows[-5:]:
            brief += (
                f"- **{r.get('company_name', 'Unknown')}** | "
                f"SAR {r.get('proposed_offer_sar', 0):,.0f} | "
                f"{r.get('multiplier', 0)}x | "
                f"Sector: {r.get('sector', 'general')}\n"
            )

        if not rows:
            brief += "_No proposals in ledger yet._\n"

        brief += "\n---\n_is_estimate=True. All figures require founder review._\n"
        output_path.write_text(brief, encoding="utf-8")
        print(f"[M&A Radar] Brief written → {output_path}")
        return

    # Live mode: call the API
    import urllib.request
    api_base = os.environ.get("DEALIX_API_BASE", "https://api.dealix.me")
    admin_key = os.environ.get("DEALIX_ADMIN_API_KEY", "")
    url = f"{api_base}/api/v1/m-and-a/radar"

    req = urllib.request.Request(url, headers={"X-Admin-API-Key": admin_key})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
    except Exception as exc:
        print(f"[M&A Radar] API call failed: {exc}", file=sys.stderr)
        sys.exit(1)

    brief = f"""# رادار الاستحواذ والاندماج — {today}
## M&A Radar Daily Brief

**Generated**: {datetime.now(timezone.utc).isoformat()}
**Mode**: live

---

## KPIs
- **Targets Evaluated**: {data.get('targets_evaluated', 0)}
- **Total Pipeline**: SAR {data.get('total_pipeline_sar', 0):,.0f}
- **Avg EBITDA Multiple**: {data.get('avg_ebitda_multiple', 0):.1f}x

---
_is_estimate=True. All figures require founder review._
"""
    output_path.write_text(brief, encoding="utf-8")
    print(f"[M&A Radar] Brief written → {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    run(dry_run=args.dry_run)
