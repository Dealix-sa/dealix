#!/usr/bin/env python3
"""Generate the Objection Intelligence report."""

from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from market_attack_common import (  # type: ignore[import-not-found]
    BOOTSTRAP_ROOT,
    ReportContext,
    load_with_fallback,
    now_iso,
    private_ops_root,
    safe_int,
    write_markdown,
)


def main() -> int:
    priv = private_ops_root()
    primary = priv / "market_attack" / "objection_library.csv"
    bootstrap = BOOTSTRAP_ROOT / "market_attack" / "objection_library.csv"

    _, rows, source = load_with_fallback(primary, bootstrap)
    ctx = ReportContext(
        name="Objection Intelligence Report",
        runtime_paths_checked=[primary],
        fallback_paths_used=[] if source == "runtime" else [bootstrap],
        started_at=now_iso(),
    )

    by_sector_stage: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    recurring: list[dict[str, str]] = []
    needs_asset: list[dict[str, str]] = []
    for r in rows:
        sector = r.get("sector", "unknown")
        stage = r.get("stage", "unknown")
        by_sector_stage[(sector, stage)].append(r)
        freq = safe_int(r.get("frequency"))
        if freq >= 3 and r.get("asset_needed", "none") not in ("", "none"):
            needs_asset.append(r)
        if (r.get("status") or "").strip() == "recurring":
            recurring.append(r)

    lines = ctx.header()
    lines += [
        "## Objections by sector x stage",
        "",
    ]
    for (sector, stage), items in sorted(by_sector_stage.items()):
        lines.append(f"### {sector} — {stage}")
        lines.append("")
        lines.append("| Objection | Freq | Response Angle | Asset Needed | Status | Next |")
        lines.append("| --------- | ---- | -------------- | ------------ | ------ | ---- |")
        for it in items:
            lines.append(
                f"| {it.get('objection','')} | {it.get('frequency','0')} "
                f"| {it.get('response_angle','')} | {it.get('asset_needed','')} "
                f"| {it.get('status','')} | {it.get('next_action','')} |"
            )
        lines.append("")

    lines += [
        "## High-frequency objections that need an asset",
        "",
    ]
    if not needs_asset:
        lines.append("_None._")
    else:
        for r in needs_asset:
            lines.append(
                f"- {r.get('objection','')} (sector: {r.get('sector','')}, "
                f"freq {r.get('frequency','0')}) — asset: {r.get('asset_needed','')}"
            )

    lines += [
        "",
        "## Recurring (open > 30 days, needs founder attention)",
        "",
    ]
    if not recurring:
        lines.append("_None._")
    else:
        for r in recurring:
            lines.append(
                f"- {r.get('objection','')} (sector: {r.get('sector','')}, "
                f"owner: {r.get('owner','')})"
            )

    lines += [
        "",
        "## Doctrine",
        "",
        "- The customer's wording is preserved verbatim.",
        "- A high-frequency objection without a linked asset is flagged.",
        "- We do not promise outcomes to defuse an objection.",
    ]

    out = priv / "market_attack" / "objection_intelligence_report.md"
    write_markdown(out, lines)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
