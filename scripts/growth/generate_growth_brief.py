#!/usr/bin/env python3
"""Generate the founder-facing weekly growth brief and a metrics snapshot line."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.growth._common import (  # noqa: E402
    DATA_DIR,
    REPORTS_DIR,
    append_jsonl,
    ensure_dirs,
    now_iso,
    read_json,
)

_OUT = REPORTS_DIR / "growth_brief.md"
_METRICS = DATA_DIR / "growth_metrics.jsonl"

_FREE_TOOLS = DATA_DIR / "free_tools.json"
_CALENDAR = DATA_DIR / "content_calendar.json"
_EXPERIMENTS = DATA_DIR / "experiments.jsonl"
_PARTNERS = DATA_DIR / "partner_targets.csv"

# Funnel target ratios for the self-selling distribution engine.
_FUNNEL_TARGETS: dict[str, float] = {
    "visitor_to_tool_start": 0.25,
    "tool_start_to_complete": 0.60,
    "complete_to_diagnostic": 0.20,
    "diagnostic_to_sprint": 0.30,
    "sprint_to_managed": 0.25,
}


def _load_experiments() -> list[dict[str, Any]]:
    """Read experiment records from JSONL, tolerating an absent file."""
    if not _EXPERIMENTS.exists():
        return []
    records: list[dict[str, Any]] = []
    for line in _EXPERIMENTS.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        records.append(json.loads(line))
    return sorted(records, key=lambda r: r.get("id", ""))


def _count_partners() -> int:
    """Count partner-target rows, tolerating an absent file."""
    if not _PARTNERS.exists():
        return 0
    with _PARTNERS.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        rows = list(reader)
    return max(0, len(rows) - 1)


def _this_week_entries(calendar: Any) -> list[dict[str, Any]]:
    """Return up to the first seven calendar entries as this week's plan."""
    if not isinstance(calendar, dict):
        return []
    entries = calendar.get("entries", [])
    if not isinstance(entries, list):
        return []
    return entries[:7]


def build_markdown() -> str:
    """Compose the founder weekly brief from the generated data files."""
    tools = read_json(_FREE_TOOLS) or []
    calendar = read_json(_CALENDAR) or {}
    experiments = _load_experiments()
    partner_count = _count_partners()
    week_entries = _this_week_entries(calendar)

    lines: list[str] = []
    lines.append("# Dealix Growth Brief")
    lines.append("")
    lines.append(f"Generated: {now_iso()}")
    lines.append("")

    lines.append("## Free Tools")
    lines.append("")
    lines.append(f"Total free tools: {len(tools)}")
    for tool in sorted(tools, key=lambda t: t.get("id", "")):
        lines.append(f"- {tool.get('name_en')} -> CTA: {tool.get('cta')}")
    lines.append("")

    lines.append("## This Week's Content")
    lines.append("")
    if week_entries:
        for entry in week_entries:
            lines.append(
                f"- {entry.get('date')} ({entry.get('day_type')}): "
                f"{entry.get('content_type')} -> CTA: {entry.get('single_cta')}",
            )
    else:
        lines.append("- No calendar entries available.")
    lines.append("")

    lines.append("## Top Experiments")
    lines.append("")
    if experiments:
        for exp in experiments[:5]:
            lines.append(
                f"- {exp.get('id')}: {exp.get('hypothesis')} "
                f"[metric: {exp.get('metric')}]",
            )
    else:
        lines.append("- No experiments in backlog.")
    lines.append("")

    lines.append("## Partner Targets")
    lines.append("")
    lines.append(f"Partner target categories: {partner_count}")
    lines.append("")

    lines.append("## Funnel Metric Targets")
    lines.append("")
    for stage, ratio in sorted(_FUNNEL_TARGETS.items()):
        lines.append(f"- {stage}: {ratio:.0%}")
    lines.append("")

    lines.append("## Guardrails")
    lines.append("")
    lines.append(
        "- One CTA per asset (Business OS Score / Free Diagnostic / Command Sprint).",
    )
    lines.append("- Approval-first: no external publish without founder approval.")
    lines.append("- No fake proof, no fake scarcity, no guaranteed-revenue claims.")
    lines.append("- PDPL-aware. No cold WhatsApp automation, no scraping.")
    lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def _snapshot_record(tools: int, partners: int, experiments: int) -> dict[str, Any]:
    """Build the machine-readable metrics snapshot record."""
    return {
        "generated_at": now_iso(),
        "free_tools": tools,
        "partner_targets": partners,
        "experiments_backlog": experiments,
        "funnel_targets": dict(sorted(_FUNNEL_TARGETS.items())),
    }


def main() -> int:
    """Write the growth brief and append a metrics snapshot line."""
    ensure_dirs()
    markdown = build_markdown()
    _OUT.write_text(markdown, encoding="utf-8")
    size = len(markdown.encode("utf-8"))

    tools = read_json(_FREE_TOOLS) or []
    record = _snapshot_record(
        tools=len(tools),
        partners=_count_partners(),
        experiments=len(_load_experiments()),
    )
    append_jsonl(_METRICS, record)

    print(
        f"growth_brief: wrote brief to {_OUT} ({size} bytes); "
        f"appended metrics snapshot to {_METRICS}",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
