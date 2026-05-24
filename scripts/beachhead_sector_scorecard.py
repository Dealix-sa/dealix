#!/usr/bin/env python3
"""Beachhead Sector Scorecard.

Reads docs/ops/pipeline_tracker.csv and docs/commercial/operations/evidence_events_tracker.csv,
emits per-sector weighted scores. Repo-resident sources; no PRIVATE_OPS needed.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from datetime import UTC, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

BRIEFS = ROOT / "data/founder_briefs"
PIPELINE_CSV = ROOT / "docs/ops/pipeline_tracker.csv"
EVIDENCE_CSV = ROOT / "docs/commercial/operations/evidence_events_tracker.csv"

WEIGHTS = {
    "lead_added": 1,
    "positive_reply": 2,
    "sample_or_proposal": 3,
    "paid": 5,
    "proof_event": 2,
    "friction": -1,
}


def _safe_read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def _within_window(iso_str: str, window_days: int) -> bool:
    try:
        d = datetime.fromisoformat(iso_str)
        if d.tzinfo is None:
            d = d.replace(tzinfo=UTC)
    except (ValueError, TypeError):
        return False
    return d >= datetime.now(UTC) - timedelta(days=window_days)


def _classify(event_type: str) -> str | None:
    et = (event_type or "").lower()
    if "lead" in et:
        return "lead_added"
    if "reply" in et and "positive" in et:
        return "positive_reply"
    if "sample" in et or "proposal" in et:
        return "sample_or_proposal"
    if "payment" in et or "paid" in et:
        return "paid"
    if "proof" in et:
        return "proof_event"
    if "friction" in et:
        return "friction"
    return None


def _score(window_days: int) -> dict[str, dict[str, int]]:
    pipeline = _safe_read_csv(PIPELINE_CSV)
    evidence = _safe_read_csv(EVIDENCE_CSV)
    sector_scores: dict[str, dict[str, int]] = defaultdict(lambda: {k: 0 for k in WEIGHTS})

    for row in pipeline:
        if not _within_window(row.get("created_at") or row.get("date") or "", window_days):
            continue
        sector = row.get("sector") or "unknown"
        sector_scores[sector]["lead_added"] += 1

    for row in evidence:
        if not _within_window(row.get("created_at") or row.get("date") or "", window_days):
            continue
        sector = row.get("sector") or "unknown"
        bucket = _classify(row.get("event_type", ""))
        if bucket:
            sector_scores[sector][bucket] += 1

    totals: dict[str, dict[str, int]] = {}
    for sector, counts in sector_scores.items():
        weighted = sum(counts[k] * WEIGHTS[k] for k in WEIGHTS)
        totals[sector] = {**counts, "weighted_score": weighted}
    return totals


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--json", action="store_true")
    p.add_argument("--window-days", type=int, default=28)
    args = p.parse_args()

    totals = _score(args.window_days)
    ranked = sorted(totals.items(), key=lambda kv: kv[1]["weighted_score"], reverse=True)
    blob = {
        "generated_at": datetime.now(UTC).isoformat(),
        "window_days": args.window_days,
        "sector_count": len(totals),
        "ranked": [{"sector": s, **scores} for s, scores in ranked],
    }

    BRIEFS.mkdir(parents=True, exist_ok=True)
    week_end = datetime.now(UTC).strftime("%Y-%m-%d")
    out = BRIEFS / f"sector_scorecard_{week_end}.md"

    lines = [
        f"# Beachhead Sector Scorecard — {week_end}",
        "",
        f"Window: trailing {args.window_days} days",
        f"Sectors scored: {blob['sector_count']}",
        "",
        "## Ranked",
    ]
    if not ranked:
        lines.append("- (no sector signal in window; check source CSVs)")
    for s, scores in ranked:
        lines.append(
            f"- **{s}** — weighted: {scores['weighted_score']} · "
            f"leads: {scores['lead_added']} · positive: {scores['positive_reply']} · "
            f"samples/proposals: {scores['sample_or_proposal']} · paid: {scores['paid']}"
        )
    lines += [
        "",
        "Walk: `docs/strategy/BEACHHEAD_SECTOR_SCORECARD.md`",
        "",
        "SECTORS_VERDICT=OK",
    ]
    out.write_text("\n".join(lines), encoding="utf-8")
    blob["written_path"] = str(out.relative_to(ROOT)).replace("\\", "/")

    if args.json:
        print(json.dumps(blob, ensure_ascii=False, indent=2))
    else:
        print("\n".join(lines))
        print(f"\nSECTORS: OK → {blob['written_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
