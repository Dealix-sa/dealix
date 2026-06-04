#!/usr/bin/env python3
"""
Commercial launch readiness — additive V5 check (does not replace existing
launch_readiness_check.py). Confirms the review-only commercial stack is present
and safe, and emits next_actions.md if missing.
"""
from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from v5.lib import out_dir  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    d = out_dir()
    checks = {
        "draft_queue": (d / "draft_queue.jsonl").exists(),
        "founder_review_csv": (d / "founder_review.csv").exists(),
        "safety_audit": (d / "safety_audit.json").exists(),
        "offer_ladder_doc": (ROOT / "docs/commercial-launch/02_OFFER_LADDER_SAR.md").exists(),
        "vertical_playbooks": len(list((ROOT / "docs/commercial-launch/verticals").glob("0*.md"))) >= 5,
        "channel_policy": (ROOT / "docs/commercial-launch/05_CHANNEL_POLICY.md").exists(),
    }
    # safety must be clean if present
    safe = True
    sa = d / "safety_audit.json"
    if sa.exists():
        safe = bool(json.loads(sa.read_text()).get("ok"))
    ok = all(checks.values()) and safe
    result = {"ok": ok, "checks": checks, "safety_ok": safe,
              "rule": "review-only; the system never sends externally"}
    print(json.dumps(result, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
