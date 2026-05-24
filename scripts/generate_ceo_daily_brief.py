#!/usr/bin/env python3
"""Generate today's CEO Daily Brief markdown.

Writes data/ceo_briefs/<YYYY-MM-DD>.md. Read-only: pulls no live customer
data and never sends. Use `--check` for verifier mode (exit 0/1 only)."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = REPO_ROOT / "data" / "ceo_briefs"


TEMPLATE = """# Dealix CEO Daily Brief — {date}

**Generated:** {now} UTC
**Source:** governance-aware aggregator (read-only)

## 1. Pipeline delta (last 24h)
- Leads in: pending live wiring
- Qualified: pending live wiring
- Stalled: pending live wiring

## 2. Approvals queue
- Open count: pending live wiring
- Top 3 high-risk: pending live wiring

## 3. Revenue checkpoint
- Day target: pending live wiring
- MTD cumulative: pending live wiring

## 4. Friction events (top 3 by severity, last 24h)
- pending live wiring

## 5. Forced decision today
- pending live wiring

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة*
"""


def write_brief() -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    out = OUT_DIR / f"{today}.md"
    out.write_text(TEMPLATE.format(date=today, now=now), encoding="utf-8")
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true",
                        help="Verifier mode: just confirm script importable.")
    args = parser.parse_args()
    if args.check:
        print("ceo_daily_brief: OK")
        return 0
    out = write_brief()
    print(f"Wrote: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
