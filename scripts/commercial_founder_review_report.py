"""Founder review report — summarize a draft_queue.jsonl into a review digest.

Reuses the canonical report builder from the generator when regenerating from
config, or summarizes an existing draft_queue.jsonl in place.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

# Run both as `python scripts/<file>.py` and `python -m scripts.<file>`.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.commercial_launch_core import OUTPUT_ROOT


def summarize(drafts: list[dict[str, Any]]) -> dict[str, Any]:
    by_status = Counter(d.get("status") for d in drafts)
    by_channel = Counter(d.get("channel") for d in drafts)
    by_vertical = Counter(d.get("vertical") for d in drafts)
    reviewable = [
        d
        for d in drafts
        if d.get("status") in ("founder_review", "needs_research", "ready_for_manual_copy")
    ]
    top = sorted(reviewable, key=lambda d: d.get("priority_score", 0), reverse=True)[:50]
    return {
        "total": len(drafts),
        "by_status": dict(by_status),
        "by_channel": dict(by_channel),
        "by_vertical": dict(by_vertical),
        "top_50_ids": [d.get("draft_id") for d in top],
    }


def write_report(drafts: list[dict[str, Any]], out_dir: Path) -> Path:
    summary = summarize(drafts)
    out = out_dir / "founder_review_report.md"
    lines = ["# Founder Review Report (regenerated)", ""]
    lines.append(f"- Total drafts: {summary['total']}")
    for status, n in summary["by_status"].items():
        lines.append(f"- {status}: {n}")
    lines.append("\n## Channel distribution")
    for k, v in summary["by_channel"].items():
        lines.append(f"- {k}: {v}")
    lines.append("\n## Vertical distribution")
    for k, v in summary["by_vertical"].items():
        lines.append(f"- {k}: {v}")
    lines.append("\n## Top 50 draft IDs (by priority)")
    for i, did in enumerate(summary["top_50_ids"], 1):
        lines.append(f"{i}. {did}")
    lines.append("\n> Doctrine: AI drafts only. Founder approves. No external sending.")
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Build a founder review report.")
    ap.add_argument("--file", default=None, help="draft_queue.jsonl path")
    ap.add_argument("--date", default=None, help="output date dir under outputs/commercial_launch")
    args = ap.parse_args(argv)

    if args.file:
        path = Path(args.file)
        out_dir = path.parent
    else:
        # latest date dir
        dirs = sorted([p for p in OUTPUT_ROOT.glob("*") if p.is_dir()])
        if not dirs:
            print("No outputs found. Run commercial_generate_400_drafts.py first.")
            return 1
        out_dir = OUTPUT_ROOT / args.date if args.date else dirs[-1]
        path = out_dir / "draft_queue.jsonl"

    drafts = [json.loads(ln) for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    report_path = write_report(drafts, out_dir)
    print(
        json.dumps({"report": str(report_path), **summarize(drafts)}, ensure_ascii=False, indent=2)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
