"""Re-score an existing draft_queue.jsonl with the quality/compliance/fit/priority model."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

# Run both as `python scripts/<file>.py` and `python -m scripts.<file>`.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.commercial_launch_core import (
    compliance_gate,
    fit_score,
    load_all_configs,
    priority_score,
    quality_gate,
)


def score_drafts(path: Path) -> dict[str, Any]:
    cfg = load_all_configs()
    weights = cfg["founder_rules"]["priority_score"]["weights"]
    rows = [json.loads(ln) for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    scored = []
    for d in rows:
        # restore minimal internal hints for scoring
        d.setdefault("_sector_en", d.get("buyer_persona", ""))
        d.setdefault("_sector_ar", "")
        d.setdefault("_sensitive", False)
        d.setdefault("_all_offer_names", [])
        q, _ = quality_gate(d, cfg)
        c, risk, _ = compliance_gate(d, cfg)
        f = fit_score(d)
        p = priority_score(q, c, f, weights)
        scored.append(
            {
                "draft_id": d.get("draft_id"),
                "quality_score": q,
                "compliance_score": c,
                "fit_score": f,
                "priority_score": p,
                "risk_level": risk,
            }
        )
    scored.sort(key=lambda r: r["priority_score"], reverse=True)
    return {
        "total": len(scored),
        "top": scored[:10],
        "avg_priority": round(sum(s["priority_score"] for s in scored) / max(1, len(scored)), 1),
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Score commercial drafts.")
    ap.add_argument("--file", required=True)
    args = ap.parse_args(argv)
    print(json.dumps(score_drafts(Path(args.file)), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
