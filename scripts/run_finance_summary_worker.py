#!/usr/bin/env python3
"""Snapshot finance summary into a markdown report and refresh worker state."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from api.internal import runtime_reader  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--private-ops",
        default=os.environ.get("DEALIX_PRIVATE_OPS", "/opt/dealix-ops-private"),
    )
    args = parser.parse_args(argv)
    root = Path(args.private_ops).expanduser().resolve()
    os.environ["DEALIX_PRIVATE_OPS"] = str(root)

    finance = runtime_reader.finance_summary()
    out = root / "founder" / "finance_summary.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        f"""# Finance Summary

Generated: {datetime.now(timezone.utc).isoformat()}
Source: {finance['source']}

- Cash collected (SAR): {finance['cash_collected_sar']}
- Pipeline (SAR): {finance['pipeline_sar']}
- Weighted pipeline (SAR): {finance['weighted_pipeline_sar']}
- Payment follow-ups: {finance['payment_follow_ups']}
- MRR (SAR): {finance['mrr_sar']}
""",
        encoding="utf-8",
    )

    subprocess.run(
        [
            sys.executable,
            str(REPO / "scripts" / "update_worker_state.py"),
            "--worker", "finance_summary",
            "--status", "ok",
            "--private-ops", str(root),
        ],
        check=False,
    )
    print(f"finance summary written: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
