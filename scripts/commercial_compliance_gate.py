"""Compliance gate CLI — block unsafe / non-compliant drafts.

Importable: compliance_check(draft) -> (score, risk_level, reasons).
A draft is compliant only when score >= threshold AND there are no block reasons.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

# Run both as `python scripts/<file>.py` and `python -m scripts.<file>`.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.commercial_launch_core import compliance_gate, load_all_configs


def compliance_check(
    draft: dict[str, Any], cfg: dict[str, Any] | None = None
) -> tuple[int, str, list[str]]:
    cfg = cfg or load_all_configs()
    return compliance_gate(draft, cfg)


def gate_file(path: Path) -> dict[str, Any]:
    cfg = load_all_configs()
    threshold = cfg["compliance"]["pass_threshold"]
    rows = [json.loads(ln) for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    blocked = []
    for d in rows:
        score, risk, reasons = compliance_gate(d, cfg)
        if reasons or score < threshold:
            blocked.append(
                {
                    "draft_id": d.get("draft_id"),
                    "score": score,
                    "risk_level": risk,
                    "reasons": reasons,
                }
            )
    return {
        "total": len(rows),
        "blocked": len(blocked),
        "pass_threshold": threshold,
        "blocked_drafts": blocked[:50],
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Compliance gate for commercial drafts.")
    ap.add_argument("--file", required=True, help="draft_queue.jsonl path")
    args = ap.parse_args(argv)
    report = gate_file(Path(args.file))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
