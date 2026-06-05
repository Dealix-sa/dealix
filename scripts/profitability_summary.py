#!/usr/bin/env python3
"""Summarize Dealix offer profitability from EXAMPLE / MANUAL inputs only.

Reads data/profitability_inputs.example.jsonl (or --input), computes per-offer
gross margin, and writes a markdown summary. Every figure is an explicit
assumption — this script never reads or writes real revenue figures and never
sends anything externally.

Run: python scripts/profitability_summary.py
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = REPO / "data" / "profitability_inputs.example.jsonl"
DEFAULT_OUT = REPO / "outputs" / "profitability" / "PROFITABILITY_SUMMARY.md"

# Pricing floors (SAR) — assumptions, mirror docs/profitability-os/04_PRICING_FLOOR_POLICY.md
PRICING_FLOOR = {
    "free_diagnostic": 0,
    "sprint_499": 499,
    "data_pack_1500": 1500,
    "managed_ops": 2999,
    "custom_ai": 5000,
}
# Minimum acceptable gross margin ratio (assumption / guardrail).
MIN_GROSS_MARGIN = 0.40


def load_inputs(path: Path) -> list[dict]:
    rows: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows


def summarize(rows: list[dict]) -> dict:
    items = []
    for r in rows:
        price = float(r.get("price", 0))
        cost = float(r.get("delivery_cost", 0))
        units = int(r.get("units", 1))
        margin = price - cost
        ratio = (margin / price) if price > 0 else None
        floor = PRICING_FLOOR.get(r.get("offer", ""), 0)
        flags = []
        if price > 0 and price < floor:
            flags.append("below_pricing_floor")
        if ratio is not None and ratio < MIN_GROSS_MARGIN:
            flags.append("below_margin_guardrail")
        items.append(
            {
                "offer": r.get("offer"),
                "price": price,
                "delivery_cost": cost,
                "units": units,
                "gross_margin": margin,
                "gross_margin_ratio": ratio,
                "flags": flags,
                "is_assumption": bool(r.get("is_assumption", True)),
            }
        )
    return {
        "disclaimer": "EXAMPLE / MANUAL ASSUMPTIONS ONLY — not real revenue. No guaranteed ROI.",
        "min_gross_margin_guardrail": MIN_GROSS_MARGIN,
        "items": items,
    }


def render_md(summary: dict) -> str:
    lines = ["# Profitability Summary (Assumptions Only)", ""]
    lines += [f"> {summary['disclaimer']}", ""]
    lines += [
        f"Gross-margin guardrail (assumption): **{summary['min_gross_margin_guardrail']:.0%}**",
        "",
    ]
    lines += [
        "| Offer | Price (SAR) | Delivery Cost (SAR) | Gross Margin (SAR) | Margin % | Flags |",
        "|---|---|---|---|---|---|",
    ]
    for it in summary["items"]:
        ratio = "n/a" if it["gross_margin_ratio"] is None else f"{it['gross_margin_ratio']:.0%}"
        flags = ", ".join(it["flags"]) or "—"
        lines.append(
            f"| {it['offer']} | {it['price']:.0f} | {it['delivery_cost']:.0f} | "
            f"{it['gross_margin']:.0f} | {ratio} | {flags} |"
        )
    lines += [
        "",
        "## ملاحظات",
        "",
        "- كل الأرقام افتراضات (assumptions) من ملف example فقط.",
        "- أي علم `below_pricing_floor` أو `below_margin_guardrail` يتطلب مراجعة المؤسس قبل القبول.",
        "- لا ROI مضمون ولا أرقام إيراد حقيقية في المستودع.",
        "",
    ]
    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    p.add_argument("--out", type=Path, default=DEFAULT_OUT)
    p.add_argument("--json", action="store_true", help="Print JSON summary to stdout")
    args = p.parse_args(argv)

    rows = load_inputs(args.input)
    summary = summarize(rows)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(render_md(summary), encoding="utf-8")

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(f"profitability_summary: wrote {args.out} ({len(summary['items'])} offers)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
