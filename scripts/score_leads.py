"""Deterministic lead scoring.

Usage:
    python3 scripts/score_leads.py
    python3 scripts/score_leads.py --mode demo
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
LEADS_PATH = REPO_ROOT / "business" / "_data" / "leads.json"
OUT_PATH = REPO_ROOT / "business" / "_data" / "scored_leads.json"


# Segment weights: how likely each segment is to close at our price points
SEGMENT_WEIGHT = {
    "marketing_agency": 25,
    "training": 20,
    "consulting": 18,
    "b2b_services": 18,
    "logistics": 15,
    "real_estate": 12,
    "clinic": 10,
    "retail": 8,
}


def score(account: dict) -> int:
    base = 30
    base += SEGMENT_WEIGHT.get(account.get("segment", ""), 5)
    if account.get("sourceNote"):
        base += 10
    if account.get("visibleSignal"):
        base += 10
    if account.get("weaknessHypothesis"):
        base += 10
    if account.get("demo"):
        base -= 5  # demo is not traction
    return min(100, max(0, base))


def _tier(score: int) -> str:
    if score >= 80:
        return "A"
    if score >= 60:
        return "B"
    if score >= 40:
        return "C"
    return "D"


def score_lead(lead: dict) -> dict:
    """Compatibility wrapper: accepts a lead dict with scoring dimensions
    (fit, pain_clarity, budget_signal, urgency) or legacy account fields.
    Returns ``{"score": int, "tier": str}``.
    """
    # New-style dimension-based scoring (tests/v3/test_scoring.py shape)
    if any(k in lead for k in ("fit", "pain_clarity", "budget_signal", "urgency")):
        total = (
            int(lead.get("fit", 0))
            + int(lead.get("pain_clarity", 0))
            + int(lead.get("budget_signal", 0))
            + int(lead.get("urgency", 0))
        )
        total = min(100, max(0, total))
        return {"score": total, "tier": _tier(total)}
    # Legacy account-based scoring
    s = score(lead)
    return {"score": s, "tier": _tier(s)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=["demo", "live"],
        default="demo",
        help="demo (default) scores locally; live is a no-op placeholder for future pipeline",
    )
    args = parser.parse_args()

    if args.mode == "live":
        import os as _os

        if _os.environ.get("EXTERNAL_SEND_ENABLED", "").lower() not in ("true", "1"):
            print("live mode requires EXTERNAL_SEND_ENABLED=true")
            return 2

    if not LEADS_PATH.exists():
        print(f"missing: {LEADS_PATH}")
        return 1
    data = json.loads(LEADS_PATH.read_text(encoding="utf-8"))
    accounts = data.get("accounts", [])
    scored = []
    for a in accounts:
        a["score"] = score(a)
        scored.append(a)
    scored.sort(key=lambda a: a["score"], reverse=True)
    OUT_PATH.write_text(
        json.dumps({"accounts": scored, "version": "1.0"}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"scored {len(scored)} -> {OUT_PATH}")
    for a in scored[:5]:
        print(f"  {a['score']:3d}  {a['id']}  {a['name']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
