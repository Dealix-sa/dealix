"""Generate the capital allocation report from private_ops state.

Reads finance/capital_allocation.csv + finance/roi_priority_matrix.csv,
emits a markdown digest ranked by ROI:cost ratio. Pure read-only.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _private_ops_runtime import (  # noqa: E402
    ledger_path,
    parse_args,
    read_csv,
    today_iso,
    write_or_print,
)


def _to_float(s: str | None, default: float = 0.0) -> float:
    try:
        return float((s or "0").replace(",", "").replace("SAR", "").strip())
    except (TypeError, ValueError):
        return default


def main() -> int:
    args = parse_args("generate_capital_allocation_report")
    po = args.private_ops

    cap = ledger_path(po, "finance", "capital_allocation.csv")
    roi = ledger_path(po, "finance", "roi_priority_matrix.csv")

    _, cap_rows = read_csv(cap)
    _, roi_rows = read_csv(roi)

    if args.strict and not cap_rows:
        print(f"[strict] no rows in {cap}", file=sys.stderr)
        return 1

    def _key(r: dict[str, str]) -> float:
        expected = _to_float(r.get("expected_return_sar"))
        cost = max(_to_float(r.get("cost_sar")), 1.0)
        return expected / cost

    ranked = sorted(roi_rows, key=_key, reverse=True)

    lines = [f"# Capital Allocation Report — {today_iso()}\n"]
    lines.append("Source: private_ops/finance (read-only). Recommendations only — founder approves.\n")
    lines.append("## ROI-ranked priorities\n")
    if not ranked:
        lines.append("- (no entries yet — populate finance/roi_priority_matrix.csv)\n")
    else:
        lines.append("| Rank | Initiative | Cost (SAR) | Expected return (SAR) | ROI:cost | Owner |")
        lines.append("|---|---|---:|---:|---:|---|")
        for i, r in enumerate(ranked[:20], start=1):
            cost = _to_float(r.get("cost_sar"))
            ret = _to_float(r.get("expected_return_sar"))
            ratio = (ret / cost) if cost else 0.0
            lines.append(
                f"| {i} | {r.get('initiative', '?')} | {cost:,.0f} | {ret:,.0f} | "
                f"{ratio:,.2f} | {r.get('owner', '?')} |"
            )

    lines.append("\n## Current allocation (snapshot)\n")
    if not cap_rows:
        lines.append("- (no entries)\n")
    else:
        lines.append("| Bucket | Allocated (SAR) | Spent (SAR) | Remaining (SAR) |")
        lines.append("|---|---:|---:|---:|")
        for r in cap_rows:
            allocated = _to_float(r.get("allocated_sar"))
            spent = _to_float(r.get("spent_sar"))
            remaining = allocated - spent
            lines.append(
                f"| {r.get('bucket', '?')} | {allocated:,.0f} | {spent:,.0f} | {remaining:,.0f} |"
            )

    write_or_print("\n".join(lines), args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
