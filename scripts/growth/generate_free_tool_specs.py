#!/usr/bin/env python3
"""Render free-tool (lead magnet) specs from data/growth/free_tools.json.

Offline, deterministic. Each tool is a self-diagnostic with ONE CTA and a
claims guard (no fabricated benchmarks, no guaranteed revenue).
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "growth" / "free_tools.json"
OUT = ROOT / "reports" / "growth"


def main() -> int:
    if not DATA.exists():
        print("DEALIX_GROWTH_FREE_TOOLS=SKIP (no data file)")
        return 0
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    tools = payload.get("tools", [])
    OUT.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Free Tool Specs — Dealix Self-Growth OS",
        "",
        f"Generated: {datetime.now(UTC).isoformat()}",
        f"Source: `data/growth/free_tools.json` ({len(tools)} tools)",
        "",
        "> Each tool: self-scoring diagnostic → result → ONE recommended next step.",
        "> No fabricated benchmarks. Results are estimates, not Verified value.",
        "",
        "| Tool | Route | Goal | CTA | Recommended offer |",
        "|---|---|---|---|---|",
    ]
    for t in tools:
        lines.append(
            "| {name} | `{route}` | {goal} | {cta} | {offer} |".format(
                name=t.get("name_ar", t.get("name_en", "")),
                route=t.get("route", ""),
                goal=t.get("goal", ""),
                cta=t.get("primary_cta", ""),
                offer=t.get("recommended_offer", ""),
            )
        )
    lines.append("")
    for t in tools:
        lines += [
            f"## {t.get('name_ar', '')} — {t.get('name_en', '')} (`{t.get('slug', '')}`)",
            "",
            f"- Route: `{t.get('route', '')}`",
            f"- Inputs: {', '.join(t.get('inputs', []))}",
            f"- Output: {t.get('output', {}).get('type', '')} — shows {', '.join(t.get('output', {}).get('shows', []))}",
            f"- CTA (single): **{t.get('primary_cta', '')}**",
            f"- Claims guard: {t.get('claims_guard', '')}",
            "",
        ]
    (OUT / "FREE_TOOL_SPECS.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"DEALIX_GROWTH_FREE_TOOLS=PASS ({len(tools)} tools)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
