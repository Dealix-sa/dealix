#!/usr/bin/env python3
"""Generate the finance command report."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ops_runtime.finance_v2 import render_finance_command_report  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="../dealix-ops-private")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if not root.exists():
        print(f"ERROR: private root missing: {root}")
        return 1
    out_path = root / "finance" / "finance_command_report.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render_finance_command_report(root), encoding="utf-8")
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
