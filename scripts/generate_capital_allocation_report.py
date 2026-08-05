#!/usr/bin/env python3
"""generate_capital_allocation_report.py.

Print a capital-allocation snapshot in the founder's three-bucket frame:
Double Down / Cut / Invest.

Tries to use canonical modules if importable; otherwise falls back to a
local YAML template. If even the template is missing, seeds it and exits.

Read-only by default. Never sends to any external system.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = REPO_ROOT / "data" / "capital_allocation.yaml"

TEMPLATE_YAML = """# Capital allocation snapshot (template)
# Buckets: double_down / cut / invest
# Edit the rows below and re-run the report.

double_down:
  - name: example_initiative_a
    rationale: strong adoption signal
    current_spend_pct: 0
    proposed_spend_pct: 0
cut:
  - name: example_initiative_b
    rationale: low adoption, high cost
    current_spend_pct: 0
    proposed_spend_pct: 0
invest:
  - name: example_initiative_c
    rationale: high-option-value bet
    current_spend_pct: 0
    proposed_spend_pct: 0
"""

BUCKETS = ("double_down", "cut", "invest")
BUCKET_TITLES = {
    "double_down": "Double Down",
    "cut": "Cut",
    "invest": "Invest",
}


def _try_canonical_snapshot() -> dict[str, list[dict[str, Any]]] | None:
    try:
        from dealix.operating_finance_os import (  # type: ignore[import-not-found]
            capital_review,
            investment_backlog,
        )
    except Exception:
        return None
    snapshot: dict[str, list[dict[str, Any]]] = {b: [] for b in BUCKETS}
    try:
        review_fn = getattr(capital_review, "snapshot", None)
        backlog_fn = getattr(investment_backlog, "snapshot", None)
        if callable(review_fn):
            data = review_fn()
            if isinstance(data, dict):
                for b in ("double_down", "cut"):
                    rows = data.get(b)
                    if isinstance(rows, list):
                        snapshot[b].extend(rows)
        if callable(backlog_fn):
            data = backlog_fn()
            if isinstance(data, list):
                snapshot["invest"].extend(data)
    except Exception:
        return None
    return snapshot


def _parse_minimal_yaml(text: str) -> dict[str, list[dict[str, Any]]]:
    """Very small YAML subset parser: top-level keys -> lists of dict items.

    Only supports the shape produced by TEMPLATE_YAML so we avoid a PyYAML
    dependency.
    """
    result: dict[str, list[dict[str, Any]]] = {b: [] for b in BUCKETS}
    current_bucket: str | None = None
    current_item: dict[str, Any] | None = None

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if not line.startswith(" ") and line.endswith(":"):
            key = line[:-1].strip()
            current_bucket = key if key in BUCKETS else None
            current_item = None
            continue
        if current_bucket is None:
            continue
        stripped = line.strip()
        if stripped.startswith("- "):
            current_item = {}
            result[current_bucket].append(current_item)
            stripped = stripped[2:].strip()
            if ":" in stripped:
                k, _, v = stripped.partition(":")
                current_item[k.strip()] = v.strip()
            continue
        if current_item is not None and ":" in stripped:
            k, _, v = stripped.partition(":")
            current_item[k.strip()] = v.strip()
    return result


def load_yaml_input(path: Path) -> dict[str, list[dict[str, Any]]]:
    text = path.read_text()
    return _parse_minimal_yaml(text)


def render_report(snapshot: dict[str, list[dict[str, Any]]]) -> str:
    lines: list[str] = []
    lines.append("# Capital allocation snapshot")
    lines.append("")
    lines.append("Buckets: Double Down / Cut / Invest")
    lines.append("")
    for bucket in BUCKETS:
        lines.append(f"## {BUCKET_TITLES[bucket]}")
        lines.append("")
        rows = snapshot.get(bucket) or []
        if not rows:
            lines.append("- (no rows)")
            lines.append("")
            continue
        lines.append("| Name | Rationale | Current % | Proposed % |")
        lines.append("|---|---|---:|---:|")
        for row in rows:
            name = str(row.get("name", "")).strip()
            rationale = str(row.get("rationale", "")).strip()
            cur = str(row.get("current_spend_pct", "")).strip()
            prop = str(row.get("proposed_spend_pct", "")).strip()
            lines.append(f"| {name} | {rationale} | {cur} | {prop} |")
        lines.append("")
    return "\n".join(lines)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a capital-allocation snapshot report.",
    )
    parser.add_argument("--out", type=Path, default=None, help="Output file path.")
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help="YAML input path (fallback when canonical modules are unavailable).",
    )
    parser.add_argument(
        "--dry-run",
        dest="dry_run",
        action="store_true",
        default=True,
        help="Print to stdout (default).",
    )
    parser.add_argument(
        "--no-dry-run",
        dest="dry_run",
        action="store_false",
        help="Allow writing to --out.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    snapshot = _try_canonical_snapshot()
    if snapshot is None:
        input_path: Path = args.input
        if not input_path.exists():
            input_path.parent.mkdir(parents=True, exist_ok=True)
            input_path.write_text(TEMPLATE_YAML)
            print(
                f"Canonical modules unavailable. Template seeded at {input_path}. "
                "Populate it and re-run.",
            )
            return 0
        snapshot = load_yaml_input(input_path)

    report = render_report(snapshot)

    if args.dry_run or args.out is None:
        sys.stdout.write(report)
        if not report.endswith("\n"):
            sys.stdout.write("\n")
        return 0

    out_path: Path = args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report)
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
