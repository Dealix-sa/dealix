#!/usr/bin/env python3
"""Generate Dealix founder market-entry decision and operating boards."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.market_entry_readiness import (
    build_market_entry_snapshot,
    load_market_entry_signals,
    write_market_entry_artifacts,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--signals",
        default="data/examples/dealix_market_entry_signals.demo.yaml",
    )
    parser.add_argument(
        "--output-dir",
        default="reports/commercial/market_entry",
    )
    args = parser.parse_args()

    payload = load_market_entry_signals(ROOT / args.signals)
    snapshot = build_market_entry_snapshot(payload, repo_root=ROOT)
    written = write_market_entry_artifacts(snapshot, ROOT / args.output_dir)
    print(f"DEALIX_MARKET_ENTRY_STAGE={snapshot['stage']}")
    print(f"EXTERNAL_ACTIONS_EXECUTED={snapshot['external_actions_executed']}")
    print(f"OPEN_GATES={len(snapshot['blockers'])}")
    print(f"ARTIFACTS_WRITTEN={len(written)}")
    return 0 if snapshot["stage"] != "blocked" else 2


if __name__ == "__main__":
    raise SystemExit(main())
