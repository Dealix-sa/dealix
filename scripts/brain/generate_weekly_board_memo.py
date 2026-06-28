"""Generate a Weekly Board Memo from the Company Brain Map.

The memo summarises signal movement, open decisions, detected bottlenecks, and
a non-deterministic scenario outlook. It is written to
``reports/brain/weekly_board_memo_<date>.md`` and returned as a string.

No deterministic predictions are made — the outlook section uses scenario
language with confidence levels.
"""
from __future__ import annotations

import os
from datetime import UTC, datetime
from typing import Any

from scripts.brain.build_company_brain_map import build_company_brain_map
from scripts.brain.detect_bottlenecks import detect_bottlenecks
from scripts.brain.generate_future_radar import generate_future_radar

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REPORTS_DIR = os.path.join(REPO_ROOT, "reports", "brain")


def generate_weekly_board_memo(
    brain_map: dict[str, Any] | None = None,
    reports_dir: str | None = None,
) -> str:
    """Generate and persist a weekly board memo. Returns the memo text."""
    bm = brain_map or build_company_brain_map()
    bottlenecks = detect_bottlenecks(bm)
    radar = generate_future_radar(profile=bm.get("profile", {}))

    today = datetime.now(UTC).date().isoformat()
    counts = bm.get("counts", {})

    lines: list[str] = []
    lines.append(f"# Weekly Board Memo — {today}")
    lines.append("")
    lines.append("> Scenarios, not predictions. Every outlook carries a confidence level. No guaranteed outcomes.")
    lines.append("")
    lines.append("## 1. Ledger snapshot")
    lines.append("")
    for name, count in counts.items():
        lines.append(f"- **{name}**: {count} records")
    lines.append("")
    lines.append("## 2. Open decisions")
    lines.append("")
    decisions = bm.get("ledgers", {}).get("decisions", [])
    if not decisions:
        lines.append("- No decisions recorded yet.")
    else:
        for dec in decisions[-10:]:
            lines.append(
                f"- [{dec.get('confidence', '?')}] {dec.get('decision', '')[:80]} "
                f"— owner: {dec.get('owner', '?')} — review: {dec.get('review_date', '?')}"
            )
    lines.append("")
    lines.append("## 3. Bottlenecks")
    lines.append("")
    if not bottlenecks:
        lines.append("- No bottlenecks detected.")
    else:
        for b in bottlenecks:
            lines.append(
                f"- [{b['confidence']}] {b['area']}: {b['description']} "
                f"(owner: {b.get('suggested_review_owner', '?')})"
            )
    lines.append("")
    lines.append("## 4. Scenario outlook (30-day horizon)")
    lines.append("")
    lines.append(radar.get("note", ""))
    lines.append("")
    for area, scenarios in radar.get("horizons", {}).get("30_day", {}).items():
        lines.append(f"### {area}")
        for sk in ("base", "upside", "downside"):
            sc = scenarios.get(sk, {})
            lines.append(f"- **{sk}** [{sc.get('confidence', '?')}]: {sc.get('scenario', '')}")
        lines.append("")

    memo = "\n".join(lines)

    out_dir = reports_dir or REPORTS_DIR
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"weekly_board_memo_{today}.md")
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(memo)

    return memo


if __name__ == "__main__":
    print(generate_weekly_board_memo())
