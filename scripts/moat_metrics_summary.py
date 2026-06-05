#!/usr/bin/env python3
"""Summarize Dealix moat metrics from EXAMPLE / MANUAL inputs only.

Reads data/moat_metrics_inputs.example.jsonl and writes a markdown moat report.
All values are explicit assumptions. Never sends anything externally.

Run: python scripts/moat_metrics_summary.py
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = REPO / "data" / "moat_metrics_inputs.example.jsonl"
DEFAULT_OUT = REPO / "outputs" / "moat_metrics" / "MOAT_METRICS_SUMMARY.md"

METRIC_LABELS = {
    "learning_asset_count": "Learning Asset Count — أصول التعلّم",
    "reusable_template_count": "Reusable Template Count — القوالب القابلة لإعادة الاستخدام",
    "sector_depth_score": "Sector Depth Score — عمق القطاع",
    "delivery_reuse_rate": "Delivery Reuse Rate — معدّل إعادة استخدام التسليم",
    "trust_asset_score": "Trust Asset Score — أصول الثقة",
    "category_authority_score": "Category Authority Score — سلطة الفئة",
}


def load_inputs(path: Path) -> list[dict]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def summarize(rows: list[dict]) -> dict:
    metrics = []
    for r in rows:
        metrics.append(
            {
                "metric": r["metric"],
                "label": METRIC_LABELS.get(r["metric"], r["metric"]),
                "value": r["value"],
                "max": r.get("max"),
                "is_assumption": bool(r.get("is_assumption", True)),
            }
        )
    return {
        "disclaimer": "EXAMPLE / MANUAL ASSUMPTIONS ONLY — not verified facts. No unverified claims.",
        "metric_count": len(metrics),
        "metrics": metrics,
    }


def render_md(summary: dict) -> str:
    lines = ["# Moat Metrics Summary (Assumptions Only)", "", f"> {summary['disclaimer']}", ""]
    lines += ["| Metric | Value | Max |", "|---|---|---|"]
    for m in summary["metrics"]:
        mx = "—" if m["max"] is None else str(m["max"])
        lines.append(f"| {m['label']} | {m['value']} | {mx} |")
    lines += [
        "",
        "## ملاحظات",
        "",
        "- كل القيم افتراضات (assumptions) من ملف example.",
        "- تُستخدم لقياس اتجاه عمق الموات عبر الزمن لا كحقائق نهائية.",
        "",
    ]
    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    p.add_argument("--out", type=Path, default=DEFAULT_OUT)
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)

    rows = load_inputs(args.input)
    summary = summarize(rows)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(render_md(summary), encoding="utf-8")

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(f"moat_metrics_summary: wrote {args.out} ({summary['metric_count']} metrics)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
