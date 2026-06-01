#!/usr/bin/env python3
"""CLI: route a scored company to recommended offers from 03_OFFERS.yml.

Usage:
    python scripts/os_route_offer.py --input company.json
    python scripts/os_route_offer.py --demo
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from os_runtime.scorer import score_company
from os_runtime.offer_router import route

DEMO_COMPANY: dict = {
    "company_name": "Al-Nakheel Facilities Management",
    "operations_complexity": "high",
    "reporting_burden": "high",
    "maintenance_or_field_ops": True,
    "multi_branch_or_scale": "many",
    "operations_data_roles": "strong",
    "growth_expansion_signals": "strong",
    "reachable_decision_maker": "clear",
    "founder_background_fit": "strong",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Route a company to recommended Dealix offers")
    parser.add_argument("--input", type=str, help="Path to company JSON file")
    parser.add_argument("--demo", action="store_true", help="Use demo company data")
    args = parser.parse_args()

    if args.demo:
        data = DEMO_COMPANY
    elif args.input:
        path = Path(args.input)
        if not path.exists():
            print(f"ERROR: File not found: {path}", file=sys.stderr)
            return 1
        try:
            data = json.loads(path.read_text())
        except json.JSONDecodeError as exc:
            print(f"ERROR: Invalid JSON in {path}: {exc}", file=sys.stderr)
            return 1
    else:
        print("ERROR: Provide --input <file> or --demo", file=sys.stderr)
        return 1

    scored = score_company(data)
    scored["sector"] = data.get("sector", "")
    scored["budget_sar"] = data.get("budget_sar")
    scored["company_size"] = data.get("employee_count_estimate", "")

    offers = route(scored)
    print(json.dumps(offers, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
