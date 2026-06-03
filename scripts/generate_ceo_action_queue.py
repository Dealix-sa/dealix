#!/usr/bin/env python3
"""Generate the ordered CEO action queue using the priority router."""
from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from control_plane.priority_router import candidates_from_pipeline, rank  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="../dealix-ops-private")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if not root.exists():
        print(f"ERROR: private root missing: {root}")
        return 1

    candidates = candidates_from_pipeline(root / "pipeline" / "pipeline_tracker.csv")
    ordered = rank(candidates)

    lines = [f"# CEO Action Queue\nGenerated on: {dt.date.today().isoformat()}\n"]
    if not ordered:
        lines.append("- (pipeline is empty — add 25 leads to begin)")
    for i, c in enumerate(ordered[:10], start=1):
        lines.append(f"{i}. [{c.raw_score:.2f}] {c.description}")
    out_path = root / "founder" / "ceo_action_queue.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
