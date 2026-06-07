#!/usr/bin/env python3
"""Dealix quote generator — مولّد عروض الأسعار.

Builds a DRAFT quote from the single source of truth (``os/config/pricing.yml``,
``os/config/packages.yml``) and fills the AR/EN templates in ``sales/``.
Computes VAT and runs a margin check via ``calculate_margin``.

Governance: the output is always a DRAFT. It is never sent to a client until the
founder approves it (approval gates G03/G04). This script never sends anything.

Usage:
  # list available offers
  python scripts/generate_quote.py --list

  # generate a quote for an offer
  python scripts/generate_quote.py --offer pilot_pro_api --client "Acme FM" --lang ar

  # add a monthly package and write to a file
  python scripts/generate_quote.py --offer maintenance_intelligence_os \\
      --client "Acme FM" --monthly managed_os --out reports/quote_acme.md

Terminal markers:
  QUOTE_DRAFT_OK
  QUOTE_MARGIN_BREACH
"""

from __future__ import annotations

import argparse
import datetime as _dt
import sys
from pathlib import Path

import yaml

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from scripts.calculate_margin import estimate_cost, evaluate  # noqa: E402

_PRICING = _REPO / "os" / "config" / "pricing.yml"
_PACKAGES = _REPO / "os" / "config" / "packages.yml"
_PAYMENT = _REPO / "os" / "config" / "payment_terms.yml"
_UNIT_ECON = _REPO / "finance" / "unit_economics.yml"
_TEMPLATES = {"ar": _REPO / "sales" / "QUOTE_TEMPLATE_AR.md",
              "en": _REPO / "sales" / "QUOTE_TEMPLATE_EN.md"}


def _load(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"missing config: {path}")
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _typical(block: dict, *keys: str) -> float | None:
    """Pick a representative price from an offer block."""
    if "price" in block:
        return float(block["price"])
    for lo, hi in (("price_min", "price_max"), ("setup_min", "setup_max")):
        if lo in block and hi in block:
            return (float(block[lo]) + float(block[hi])) / 2
        if lo in block:
            return float(block[lo])
    for k in keys:
        if k in block:
            return float(block[k])
    return None


def find_offer(pricing: dict, key: str) -> tuple[str, dict] | None:
    """Locate an offer across entry_offers / pilots / production.systems."""
    for group in ("entry_offers", "pilots"):
        if key in pricing.get(group, {}):
            return group, pricing[group][key]
    systems = pricing.get("production", {}).get("systems", {})
    if key in systems:
        return "production", systems[key]
    return None


def list_offers(pricing: dict) -> None:
    print("Entry offers:")
    for k in pricing.get("entry_offers", {}):
        print(f"  - {k}")
    print("Pilots:")
    for k in pricing.get("pilots", {}):
        print(f"  - {k}")
    print("Production systems:")
    for k in pricing.get("production", {}).get("systems", {}):
        print(f"  - {k}")


def _kind_for(group: str) -> str:
    return {"entry_offers": "audit", "pilots": "pilot", "production": "production"}[group]


def build_quote(offer_key: str, client: str, lang: str,
                monthly_key: str | None) -> tuple[str, dict]:
    pricing = _load(_PRICING)
    packages = _load(_PACKAGES)
    payment = _load(_PAYMENT)
    unit_econ = _load(_UNIT_ECON)
    vat_rate = float(pricing.get("vat", {}).get("rate", 0.15))

    found = find_offer(pricing, offer_key)
    if not found:
        raise SystemExit(f"unknown offer '{offer_key}'. Use --list to see options.")
    group, offer = found
    kind = _kind_for(group)

    name = offer.get("name_en") or offer.get("name_ar") or offer_key
    price = _typical(offer)
    if price is None:
        raise SystemExit(f"offer '{offer_key}' has no resolvable price")

    # line items
    rows = [(name, offer.get("name_ar", ""), price)]
    subtotal = sum(r[2] for r in rows)
    vat_amount = subtotal * vat_rate
    total = subtotal + vat_amount

    # margin check (estimate cost)
    cost = estimate_cost(subtotal, kind, unit_econ)
    margin = evaluate(subtotal, cost, kind)

    # monthly subscription
    sub = {}
    if monthly_key:
        pkg = packages.get("packages", {}).get(monthly_key)
        if not pkg:
            raise SystemExit(f"unknown package '{monthly_key}'")
        monthly_fee = _typical(pkg)
        sub = {
            "package": pkg.get("name_en", monthly_key),
            "monthly_fee": monthly_fee,
            "included": pkg.get("included_actions", "—"),
        }

    min_term = payment.get("subscriptions", {}).get("min_term_months", 6)

    # render line items table
    if lang == "ar":
        line_items = "\n".join(
            f"| {nm_ar or nm} | {nm} | {p:,.0f} |" for nm, nm_ar, p in rows
        )
    else:
        line_items = "\n".join(f"| {nm} | {nm} | {p:,.0f} |" for nm, _nm_ar, p in rows)

    today = _dt.date.today()
    valid_until = today + _dt.timedelta(days=14)
    fields = {
        "client_name": client,
        "date": today.isoformat(),
        "quote_id": f"DLX-{today:%Y%m%d}-{offer_key[:6].upper().rstrip('_')}",
        "valid_until": valid_until.isoformat(),
        "problem_statement": "(يُملأ) / (to fill)",
        "scope_summary": name,
        "line_items": line_items,
        "subtotal": f"{subtotal:,.0f}",
        "vat_amount": f"{vat_amount:,.0f}",
        "total_with_vat": f"{total:,.0f}",
        "subscription_package": sub.get("package", "—"),
        "monthly_fee": f"{sub['monthly_fee']:,.0f}" if sub else "—",
        "usage_included": str(sub.get("included", "—")),
        "usage_overage": "حسب os/config/usage_meters.yml / per usage_meters.yml",
        "min_term_months": str(min_term),
        "deliverables": "\n".join(f"- {d}" for d in offer.get("deliverables", offer.get("includes", []))) or "(يُملأ)",
        "assumptions": "(يُملأ) / (to fill)",
        "next_step": "حجز مكالمة Discovery / Book a discovery call",
        "margin_check": f"{margin['gross_margin_pct']}% "
                        f"({'OK' if margin['meets_guardrail'] else 'BREACH'})",
    }

    template = _TEMPLATES[lang].read_text(encoding="utf-8")
    for k, v in fields.items():
        template = template.replace("{{ " + k + " }}", str(v))

    return template, margin


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Dealix quote generator (drafts only)")
    p.add_argument("--list", action="store_true", help="list available offers")
    p.add_argument("--offer", help="offer key (see --list)")
    p.add_argument("--client", default="(Client)", help="client name")
    p.add_argument("--lang", choices=["ar", "en"], default="ar")
    p.add_argument("--monthly", help="monthly package key (e.g. managed_os)")
    p.add_argument("--out", help="write the draft to this path instead of stdout")
    args = p.parse_args(argv)

    if args.list:
        list_offers(_load(_PRICING))
        return 0
    if not args.offer:
        p.error("provide --offer (or --list)")

    quote, margin = build_quote(args.offer, args.client, args.lang, args.monthly)

    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(quote, encoding="utf-8")
        print(f"draft written to {out}")
    else:
        print(quote)

    if not margin["meets_guardrail"]:
        print("QUOTE_MARGIN_BREACH", file=sys.stderr)
        return 1
    print("QUOTE_DRAFT_OK", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
