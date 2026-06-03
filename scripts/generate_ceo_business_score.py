#!/usr/bin/env python3
"""Generate the CEO business score and append to history."""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ops_runtime.business_audit import compute_score, render  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="../dealix-ops-private")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if not root.exists():
        print(f"ERROR: private root missing: {root}")
        return 1
    score, top_action = compute_score(root)
    out_path = root / "business_audit" / "ceo_business_score.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render(root), encoding="utf-8")

    history = root / "business_audit" / "score_history.csv"
    new_file = not history.exists()
    with history.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new_file:
            w.writerow(["date", "score", "top_action", "notes"])
        w.writerow([dt.date.today().isoformat(), score, top_action, ""])
    print(f"Wrote {out_path} (score={score})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
