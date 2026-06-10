#!/usr/bin/env python3
"""Dealix margin calculator — حساب الهامش قبل إرسال العرض.

Reads margin floors from ``os/config/pricing.yml`` (single source of truth) and
checks a quoted price against the doctrine floors:

  - Gross margin (project):      >= 55%
  - Gross margin (subscription): >= 65%
  - Net margin target:           >= 25%

This is an internal, founder-facing guardrail. It never charges, sends, or
touches a customer — it only answers "is this quote safe to send?".

Usage:
  python scripts/calculate_margin.py --price 150000 --cost 60000 --type project
  python scripts/calculate_margin.py --price 15000 --cost 4000 --opex 2000 --type subscription
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
PRICING_PATH = REPO_ROOT / "os" / "config" / "pricing.yml"


def load_pricing(path: Path = PRICING_PATH) -> dict[str, Any]:
    """Load the canonical pricing config."""
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def gross_margin(price: float, cost: float) -> float:
    """Gross margin fraction = (price - cost) / price. 0.0 when price <= 0."""
    if price <= 0:
        return 0.0
    return (price - cost) / price


def net_margin(price: float, cost: float, opex: float) -> float:
    """Net margin fraction = (price - cost - opex) / price."""
    if price <= 0:
        return 0.0
    return (price - cost - opex) / price


def check_margin(
    price: float,
    cost: float,
    kind: str = "project",
    opex: float = 0.0,
    pricing: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return a structured pass/fail report against the doctrine floors.

    ``kind`` is "project" (one-off: audit/pilot/production setup) or
    "subscription" (monthly retainer/package).
    """
    pricing = pricing or load_pricing()
    margins = pricing.get("margins", {})
    if kind == "subscription":
        gross_floor = float(margins.get("gross_margin_subscription_min", 0.65))
    else:
        gross_floor = float(margins.get("gross_margin_project_min", 0.55))
    net_floor = float(margins.get("net_margin_target_min", 0.25))

    gm = gross_margin(price, cost)
    nm = net_margin(price, cost, opex)
    gross_ok = gm >= gross_floor
    net_ok = nm >= net_floor

    return {
        "kind": kind,
        "price_sar": price,
        "cost_sar": cost,
        "opex_sar": opex,
        "gross_margin": round(gm, 4),
        "gross_floor": gross_floor,
        "gross_ok": gross_ok,
        "net_margin": round(nm, 4),
        "net_floor": net_floor,
        "net_ok": net_ok,
        "passed": gross_ok and net_ok,
    }


def _format_report(r: dict[str, Any]) -> str:
    mark = lambda ok: "✅" if ok else "❌"  # noqa: E731
    lines = [
        "Dealix — Margin Check (ex-VAT) / فحص الهامش قبل الإرسال",
        "-" * 56,
        f"Type / النوع           : {r['kind']}",
        f"Price / السعر          : {r['price_sar']:,.0f} SAR",
        f"Cost / التكلفة         : {r['cost_sar']:,.0f} SAR",
        f"Opex / تشغيلية         : {r['opex_sar']:,.0f} SAR",
        "-" * 56,
        f"{mark(r['gross_ok'])} Gross margin / الهامش الإجمالي : "
        f"{r['gross_margin'] * 100:.1f}%  (floor {r['gross_floor'] * 100:.0f}%)",
        f"{mark(r['net_ok'])} Net margin / الهامش الصافي    : "
        f"{r['net_margin'] * 100:.1f}%  (target {r['net_floor'] * 100:.0f}%)",
        "-" * 56,
        f"VERDICT / القرار        : {'PASS — آمن للإرسال' if r['passed'] else 'FAIL — راجع السعر/التكلفة'}",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Dealix margin guardrail calculator")
    parser.add_argument("--price", type=float, required=True, help="Quoted price (ex-VAT, SAR)")
    parser.add_argument("--cost", type=float, required=True, help="Direct delivery cost (SAR)")
    parser.add_argument("--opex", type=float, default=0.0, help="Allocated operating cost (SAR)")
    parser.add_argument(
        "--type",
        dest="kind",
        choices=["project", "subscription"],
        default="project",
        help="project = one-off (audit/pilot/setup); subscription = monthly",
    )
    args = parser.parse_args(argv)

    report = check_margin(args.price, args.cost, kind=args.kind, opex=args.opex)
    print(_format_report(report))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
