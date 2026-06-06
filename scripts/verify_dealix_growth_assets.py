#!/usr/bin/env python3
"""Verify Dealix growth assets exist and are well-formed.

Primary check: ``data/growth/first_30_targets.csv`` exists, has a header row
and at least one data row. Secondary check: optional growth documentation under
``docs/06_growth`` is reported when present. The CSV may be created by a
parallel content process; if it is missing at runtime the verifier reports it
as missing rather than crashing.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

TARGETS_CSV = ROOT / "data" / "growth" / "first_30_targets.csv"
GROWTH_DOCS_DIR = ROOT / "docs" / "06_growth"


def _check_targets_csv(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {
            "label": "first_30_targets_csv",
            "status": "FAIL",
            "detail": f"missing: {path.relative_to(ROOT)}",
            "rows": 0,
        }
    try:
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.reader(handle)
            rows = [r for r in reader if any(cell.strip() for cell in r)]
    except Exception as exc:  # pragma: no cover - defensive
        return {
            "label": "first_30_targets_csv",
            "status": "FAIL",
            "detail": f"unreadable: {exc}",
            "rows": 0,
        }
    if not rows:
        return {
            "label": "first_30_targets_csv",
            "status": "FAIL",
            "detail": "empty file (no header)",
            "rows": 0,
        }
    data_rows = len(rows) - 1
    if data_rows < 1:
        return {
            "label": "first_30_targets_csv",
            "status": "FAIL",
            "detail": "header present but no data rows",
            "rows": data_rows,
        }
    return {
        "label": "first_30_targets_csv",
        "status": "PASS",
        "detail": f"header + {data_rows} data row(s)",
        "rows": data_rows,
    }


def _check_growth_docs(directory: Path) -> dict[str, Any]:
    if not directory.is_dir():
        return {
            "label": "growth_docs",
            "status": "INFO",
            "detail": "optional growth docs directory not present",
            "count": 0,
        }
    files = [p for p in directory.rglob("*.md") if p.is_file()]
    return {
        "label": "growth_docs",
        "status": "PASS" if files else "INFO",
        "detail": f"{len(files)} markdown doc(s)",
        "count": len(files),
    }


def check_growth_assets() -> dict[str, Any]:
    """Check growth assets. Verdict driven by the required CSV only."""
    csv_result = _check_targets_csv(TARGETS_CSV)
    docs_result = _check_growth_docs(GROWTH_DOCS_DIR)
    items = [csv_result, docs_result]
    verdict = "PASS" if csv_result["status"] == "PASS" else "FAIL"
    missing = [i["label"] for i in items if i["status"] == "FAIL"]
    return {"items": items, "missing": missing, "verdict": verdict}


def _print_table(result: dict[str, Any]) -> None:
    print("== Dealix Growth Assets ==")
    for item in result["items"]:
        print(f"  [{item['status']}] {item['label']}: {item['detail']}")
    print(f"Verdict: {result['verdict']}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args(argv)

    result = check_growth_assets()
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        _print_table(result)
    return 0 if result["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
