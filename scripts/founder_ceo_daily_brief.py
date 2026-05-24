#!/usr/bin/env python3
"""Compose the CEO daily brief.

Answers the seven questions in docs/founder/CEO_DAILY_BRIEF_SYSTEM.md from a
mix of repo-resident evidence CSVs and PRIVATE_OPS sensitive files. When
PRIVATE_OPS is not configured the brief still generates, with the sensitive
sections clearly labeled as skipped.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.private_ops import (  # noqa: E402
    is_enabled,
    missing_private_ops_note,
    resolve_csv,
    resolve_jsonl,
)

try:
    from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402
except Exception:  # noqa: BLE001
    def ensure_stdout_utf8() -> None:  # type: ignore[no-redef]
        return

BRIEFS = ROOT / "data/founder_briefs"
PIPELINE_CSV = ROOT / "docs/ops/pipeline_tracker.csv"
EVIDENCE_CSV = ROOT / "docs/commercial/operations/evidence_events_tracker.csv"


def _safe_read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8", newline="") as fh:
            return list(csv.DictReader(fh))
    except OSError:
        return []


def _read_jsonl(path: Path | None) -> list[dict[str, Any]]:
    if path is None or not path.exists():
        return []
    out: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def _decision_of_the_day(decisions: list[dict[str, Any]]) -> str:
    pending = [d for d in decisions if d.get("status") == "pending"]
    if not pending:
        return "_No pending decision._"
    pending.sort(key=lambda d: d.get("recorded_at", ""), reverse=True)
    d = pending[0]
    return f"- **{d.get('decision', '(unspecified)')}** · owner: {d.get('owner', '?')}"


def _ceo_open_items(decisions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        d for d in decisions
        if d.get("owner") == "ceo" and d.get("status") in ("pending", "executing")
    ]


def _delegatable(items: list[dict[str, Any]], min_age_days: int = 3) -> list[dict[str, Any]]:
    cutoff = datetime.now(UTC).timestamp() - (min_age_days * 86400)
    out: list[dict[str, Any]] = []
    for d in items:
        try:
            t = datetime.fromisoformat(d.get("recorded_at", "")).timestamp()
        except Exception:  # noqa: BLE001
            continue
        if t < cutoff:
            out.append(d)
    return out


def _build_brief() -> dict[str, Any]:
    today = datetime.now(UTC).strftime("%Y-%m-%d")
    enabled = is_enabled()

    decisions = _read_jsonl(resolve_jsonl("ceo/decisions.jsonl")) if enabled else []

    pipeline_rows = _safe_read_csv(PIPELINE_CSV)
    evidence_rows = _safe_read_csv(EVIDENCE_CSV)

    open_items = _ceo_open_items(decisions)
    delegatable = _delegatable(open_items)

    sources = {
        "pipeline_tracker.csv": {"path": str(PIPELINE_CSV.relative_to(ROOT)), "rows": len(pipeline_rows)},
        "evidence_events_tracker.csv": {"path": str(EVIDENCE_CSV.relative_to(ROOT)), "rows": len(evidence_rows)},
        "ceo/decisions.jsonl": {"private_ops_enabled": enabled, "rows": len(decisions)},
    }

    return {
        "date": today,
        "private_ops_enabled": enabled,
        "decision_of_the_day": _decision_of_the_day(decisions),
        "ceo_open_items_count": len(open_items),
        "delegatable_count": len(delegatable),
        "pipeline_rows": len(pipeline_rows),
        "evidence_rows": len(evidence_rows),
        "sources": sources,
    }


def _render_markdown(blob: dict[str, Any]) -> str:
    sections: list[str] = [
        f"# CEO Daily Brief — {blob['date']}",
        "",
    ]
    if not blob["private_ops_enabled"]:
        sections.append(f"> ⚠ {missing_private_ops_note('en')}")
        sections.append("")
    sections += [
        "## 1. Decision of the day",
        blob["decision_of_the_day"],
        "",
        "## 2. Cash position (last 7 days)",
        f"- Pipeline rows tracked: {blob['pipeline_rows']}",
        f"- Evidence rows last loaded: {blob['evidence_rows']}",
        "- (Source-of-truth: existing `auto_client_acquisition.proof_ledger` — see `docs/revenue/PAYMENT_CAPTURE_OS.md`)",
        "",
        "## 3. Bottlenecks (top 3)",
        "- See `scripts/dealix_bottleneck_radar.py` output (`docs/metrics/bottlenecks_recent.csv` if generated today)",
        "",
        "## 4. On the hook for me",
        f"- Open CEO-owned decisions: {blob['ceo_open_items_count']}",
        "",
        "## 5. Delegatable today",
        f"- Items aged > 3 days: {blob['delegatable_count']}",
        "- Walk: `docs/founder/DELEGATION_DECISION_TREE.md`",
        "",
        "## 6. Doubling down",
        "- See `docs/strategy/BEACHHEAD_SECTOR_SCORECARD.md` weekly output",
        "",
        "## 7. Stopping",
        "- Pipeline rows aged > 14 days without a next step",
        "",
        "## Sources",
    ]
    for name, info in blob["sources"].items():
        sections.append(f"- `{name}` — {info}")
    sections += ["", "DAILY_BRIEF_VERDICT=OK"]
    return "\n".join(sections)


def main() -> int:
    ensure_stdout_utf8()
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--json", action="store_true")
    p.add_argument("--stdout-only", action="store_true")
    args = p.parse_args()

    blob = _build_brief()
    md = _render_markdown(blob)

    if not args.stdout_only:
        BRIEFS.mkdir(parents=True, exist_ok=True)
        out = BRIEFS / f"ceo_daily_brief_{blob['date']}.md"
        out.write_text(md, encoding="utf-8")
        blob["written_path"] = str(out.relative_to(ROOT)).replace("\\", "/")

    if args.json:
        print(json.dumps(blob, ensure_ascii=False, indent=2))
    else:
        print(md)
        if blob.get("written_path"):
            print(f"\nDAILY_BRIEF: OK → {blob['written_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
