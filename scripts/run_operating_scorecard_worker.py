#!/usr/bin/env python3
"""Operating Scorecard — composite signal across the four pillars.

Wraps run_ceo_summary_worker but also probes evals/eval_status.csv and
security/security_status.csv so /control-plane has a richer signal.
"""
from __future__ import annotations

import csv
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


def _runtime_dir() -> Path:
    return Path(os.getenv("PRIVATE_OPS") or os.getenv("DEALIX_PRIVATE_OPS_DIR") or "/opt/dealix-ops-private").expanduser()


def _last_row(path: Path) -> dict[str, str] | None:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8", newline="") as fh:
        last = None
        for r in csv.DictReader(fh):
            last = r
        return last


def main() -> int:
    base = _runtime_dir()
    if not base.exists():
        print(f"SKIP: private ops not bootstrapped at {base}")
        return 0
    eval_last = _last_row(base / "evals" / "eval_status.csv")
    sec_last = _last_row(base / "security" / "security_status.csv")
    out = base / "founder" / "operating_scorecard.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        f"""# Dealix Operating Scorecard

_Last composite refresh: {datetime.now(timezone.utc).isoformat()}_

| Signal          | Value                                |
|-----------------|--------------------------------------|
| Eval gate       | {eval_last.get('suite') if eval_last else 'unknown'} |
| Eval failures   | {eval_last.get('fail') if eval_last else 'unknown'}  |
| Secrets scan    | {sec_last.get('secrets_scan') if sec_last else 'unknown'} |
| PDPL review     | {sec_last.get('pdpl_review') if sec_last else 'unknown'} |

Source: scripts/run_operating_scorecard_worker.py (CEO Copilot).
""",
        encoding="utf-8",
    )
    print(f"[ok] composite scorecard refreshed -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
