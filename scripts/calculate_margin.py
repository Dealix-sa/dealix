#!/usr/bin/env python3
"""Dealix margin calculator — حاسبة الهامش.

Computes gross/net margin for an offer and checks it against the guardrails in
``os/config/margin_guardrails.yml``. Direct cost can be supplied explicitly or
estimated from ``finance/unit_economics.yml`` ratios by offer type.

Usage:
  # explicit cost
  python scripts/calculate_margin.py --revenue 60000 --cost 21000 --kind pilot

  # estimate cost from unit_economics ratios
  python scripts/calculate_margin.py --revenue 150000 --kind production --estimate

  # JSON output (for other scripts / CI)
  python scripts/calculate_margin.py --revenue 15000 --kind subscription --estimate --json

Terminal markers (grep-friendly):
  MARGIN_OK            -> margin meets guardrail
  MARGIN_BREACH        -> margin below guardrail (needs documented exception)

Exit code 0 if margin meets the guardrail (or no guardrail applies), 1 on breach.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

_REPO = Path(__file__).resolve().parents[1]
_GUARDRAILS = _REPO / "os" / "config" / "margin_guardrails.yml"
_UNIT_ECON = _REPO / "finance" / "unit_economics.yml"

# map offer "kind" -> guardrail key in margin_guardrails.yml::margins
_GUARDRAIL_KEY = {
    "project": "project_gross_margin_min",
    "production": "project_gross_margin_min",
    "audit": "project_gross_margin_min",
    "pilot": "project_gross_margin_min",
    "subscription": "subscription_gross_margin_min",
    "retainer": "retainer_gross_margin_min",
    "usage_overage": "subscription_gross_margin_min",
}


def _load(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"missing config: {path}")
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def estimate_cost(revenue: float, kind: str, unit_econ: dict) -> float:
    """Estimate direct cost from unit_economics ratios."""
    ratios = unit_econ.get("assumed_direct_cost_ratio", {})
    # production maps to "production", everything else by its own name
    ratio = ratios.get(kind)
    if ratio is None:
        raise ValueError(
            f"no assumed_direct_cost_ratio for kind '{kind}'. "
            f"known: {sorted(ratios)}"
        )
    return revenue * float(ratio)


def gross_margin(revenue: float, cost: float) -> float:
    if revenue <= 0:
        raise ValueError("revenue must be > 0")
    return (revenue - cost) / revenue


def guardrail_for(kind: str, guardrails: dict) -> float | None:
    key = _GUARDRAIL_KEY.get(kind)
    if key is None:
        return None
    return guardrails.get("margins", {}).get(key)


def evaluate(revenue: float, cost: float, kind: str) -> dict:
    guardrails = _load(_GUARDRAILS)
    margin = gross_margin(revenue, cost)
    floor = guardrail_for(kind, guardrails)
    net_target = guardrails.get("margins", {}).get("net_margin_target")
    meets = True if floor is None else margin >= floor
    return {
        "kind": kind,
        "revenue": round(revenue, 2),
        "direct_cost": round(cost, 2),
        "gross_profit": round(revenue - cost, 2),
        "gross_margin": round(margin, 4),
        "gross_margin_pct": round(margin * 100, 1),
        "guardrail_min": floor,
        "guardrail_min_pct": None if floor is None else round(floor * 100, 1),
        "net_margin_target_pct": None if net_target is None else round(net_target * 100, 1),
        "meets_guardrail": meets,
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Dealix margin calculator")
    p.add_argument("--revenue", type=float, required=True, help="revenue (SAR, ex-VAT)")
    p.add_argument("--cost", type=float, help="direct cost (SAR). Omit with --estimate.")
    p.add_argument(
        "--kind",
        required=True,
        choices=sorted(set(list(_GUARDRAIL_KEY) + ["project"])),
        help="offer kind for guardrail selection",
    )
    p.add_argument("--estimate", action="store_true", help="estimate cost from unit_economics")
    p.add_argument("--json", action="store_true", help="emit JSON")
    args = p.parse_args(argv)

    if args.cost is None and not args.estimate:
        p.error("provide --cost or --estimate")

    cost = args.cost
    if cost is None:
        cost = estimate_cost(args.revenue, args.kind, _load(_UNIT_ECON))

    result = evaluate(args.revenue, cost, args.kind)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Offer kind     : {result['kind']}")
        print(f"Revenue (ex-VAT): {result['revenue']:,.0f} SAR")
        print(f"Direct cost    : {result['direct_cost']:,.0f} SAR"
              + ("  (estimated)" if args.cost is None else ""))
        print(f"Gross profit   : {result['gross_profit']:,.0f} SAR")
        print(f"Gross margin   : {result['gross_margin_pct']}%")
        if result["guardrail_min_pct"] is not None:
            print(f"Guardrail min  : {result['guardrail_min_pct']}%")

    if result["meets_guardrail"]:
        print("MARGIN_OK")
        return 0
    print(
        "MARGIN_BREACH — below guardrail. Do not sign without a documented exception "
        "(see os/config/discount_policy.yml#low_margin_exceptions)."
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
