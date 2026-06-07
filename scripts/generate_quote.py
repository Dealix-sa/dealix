#!/usr/bin/env python3
"""Dealix quote generator — يولّد عرض سعر من العرض/الباقة/القطاع.

Reads the canonical configs:
  - os/config/pricing.yml        (entry/pilot/production offers, terms, VAT)
  - os/config/packages.yml       (monthly packages + included usage allowance)
  - os/config/usage_meters.yml   (overage pricing)

and renders a bilingual (AR/EN) quote in Markdown with:
  - One-off (setup/offer) amount + 15% VAT
  - Monthly subscription + 15% VAT (optional 10% annual-prepay discount)
  - Included usage allowance + overage note
  - 50/30/20 project payment schedule
  - DRAFT + founder-approval banner (this tool NEVER sends a quote)

Doctrine: prices are estimates (ex-VAT). Sharing a price with a customer
requires founder approval (os/01_CLAUDE.md). This script only drafts.

Usage:
  python scripts/generate_quote.py --client "Acme FM" \\
      --offer maintenance_intelligence_os --package managed_os
  python scripts/generate_quote.py --client "X" --offer pilot_pro_with_api
  python scripts/generate_quote.py --client "Y" --package managed_os --annual --out quote.md
"""

from __future__ import annotations

import argparse
import datetime as _dt
import sys
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = REPO_ROOT / "os" / "config"


def _load(name: str) -> dict[str, Any]:
    with (CONFIG_DIR / name).open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def load_configs() -> dict[str, dict[str, Any]]:
    return {
        "pricing": _load("pricing.yml"),
        "packages": _load("packages.yml"),
        "meters": _load("usage_meters.yml"),
    }


def find_offer(pricing: dict[str, Any], key: str) -> tuple[str, dict[str, Any]] | None:
    """Locate an offer by key across entry/pilot/production. Returns (category, offer)."""
    for category in ("entry_offers", "pilot_offers", "production_offers"):
        section = pricing.get(category, {})
        if key in section and isinstance(section[key], dict):
            return category, section[key]
    return None


def _offer_setup_sar(offer: dict[str, Any]) -> int:
    """Best single quoted figure for the one-off part of an offer (min of range)."""
    for field in ("price_sar", "setup_sar_min", "price_sar_min"):
        if field in offer:
            return int(offer[field])
    return 0


def _offer_monthly_sar(offer: dict[str, Any]) -> int:
    for field in ("monthly_sar_min",):
        if field in offer:
            return int(offer[field])
    return 0


def _ar_months(n: int) -> str:
    """Arabic month phrasing for small counts (2 -> شهرين)."""
    return {1: "شهر", 2: "شهرين"}.get(int(n), f"{int(n)} أشهر")


def _vat_lines(amount: float, vat_rate: float) -> dict[str, float]:
    vat = round(amount * vat_rate)
    return {"ex_vat": round(amount), "vat": vat, "incl_vat": round(amount) + vat}


def build_quote(
    *,
    client: str,
    offer_key: str | None = None,
    package_key: str | None = None,
    setup_override: float | None = None,
    monthly_override: float | None = None,
    annual_prepay: bool = False,
    case_study: bool = False,
    configs: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Compute a structured quote. Pure function — no I/O side effects."""
    configs = configs or load_configs()
    pricing = configs["pricing"]
    packages = configs["packages"]
    meters = configs["meters"]

    gov = pricing.get("governance", {})
    vat_rate = float(gov.get("vat_rate", 0.15))
    discounts = pricing.get("discounts", {})
    terms = pricing.get("payment_terms", {})

    offer_name_ar = offer_name_en = None
    offer_category = None
    setup_sar = 0.0
    monthly_sar = 0.0
    allowance_note: str | None = None

    if offer_key:
        found = find_offer(pricing, offer_key)
        if not found:
            raise KeyError(f"unknown offer: {offer_key}")
        offer_category, offer = found
        offer_name_ar = offer.get("name_ar")
        offer_name_en = offer.get("name_en")
        setup_sar = float(_offer_setup_sar(offer))
        if offer_category == "production_offers":
            monthly_sar = float(_offer_monthly_sar(offer))

    if package_key:
        pkg = packages.get("packages", {}).get(package_key)
        if not pkg:
            raise KeyError(f"unknown package: {package_key}")
        monthly_sar = float(pkg["price_monthly_sar"])
        used = pkg.get("included_usage") or {}
        if used:
            meter = meters.get("meters", {}).get(used.get("meter", ""), {})
            block = meter.get("block_size", 1000)
            over = meter.get("overage_per_block_sar_typical") or meter.get(
                "overage_per_block_sar_min", 0
            )
            allowance_note = (
                f"يشمل {used.get('quota_per_month', 0):,} عملية شهريًا. "
                f"كل {block:,} عملية إضافية = {over:,} ر.س (ex-VAT) — لا خصم على التجاوز."
            )

    if setup_override is not None:
        setup_sar = float(setup_override)
    if monthly_override is not None:
        monthly_sar = float(monthly_override)

    # Discounts
    applied: list[str] = []
    if case_study and setup_sar > 0:
        rate = float(discounts.get("first_3_case_study", 0.15))
        setup_sar = round(setup_sar * (1 - rate))
        applied.append(f"Case-study −{rate * 100:.0f}% (أول 3 عملاء)")

    monthly_effective = monthly_sar
    annual_total_ex_vat = None
    if annual_prepay and monthly_sar > 0:
        rate = float(terms.get("subscription", {}).get("annual_prepay_discount", 0.10))
        monthly_effective = round(monthly_sar * (1 - rate))
        annual_total_ex_vat = monthly_effective * 12
        applied.append(f"Annual prepay −{rate * 100:.0f}%")

    setup = _vat_lines(setup_sar, vat_rate) if setup_sar else None
    monthly = _vat_lines(monthly_effective, vat_rate) if monthly_effective else None

    # 50/30/20 schedule on the one-off setup
    schedule = []
    if setup:
        for ms in terms.get("project_milestones", []):
            amt = round(setup["ex_vat"] * float(ms["pct"]))
            schedule.append(
                {
                    "name_ar": ms["name_ar"],
                    "name_en": ms["name_en"],
                    "pct": float(ms["pct"]),
                    "amount_ex_vat": amt,
                    "amount_incl_vat": amt + round(amt * vat_rate),
                }
            )

    return {
        "client": client,
        "currency": pricing.get("meta", {}).get("currency", "SAR"),
        "vat_rate": vat_rate,
        "offer_key": offer_key,
        "offer_category": offer_category,
        "offer_name_ar": offer_name_ar,
        "offer_name_en": offer_name_en,
        "package_key": package_key,
        "setup": setup,
        "monthly": monthly,
        "monthly_list_sar": round(monthly_sar) if monthly_sar else None,
        "annual_total_ex_vat": annual_total_ex_vat,
        "allowance_note": allowance_note,
        "discounts_applied": applied,
        "schedule": schedule,
        "subscription_terms": terms.get("subscription", {}),
        "is_estimate": bool(gov.get("is_estimate", True)),
    }


def render_quote_md(q: dict[str, Any]) -> str:
    cur = q["currency"]
    today = _dt.date.today()
    valid_until = today + _dt.timedelta(days=30)
    lines: list[str] = []
    lines.append("> **DRAFT — مسودة داخلية.** مشاركة أي سعر مع العميل تتطلب موافقة المؤسس")
    lines.append("> (Gate — `os/01_CLAUDE.md`). هذه الأداة لا تُرسل العروض.")
    lines.append("")
    lines.append(f"# عرض سعر — Dealix | Quote — {q['client']}")
    lines.append("")
    lines.append(f"**التاريخ / Date:** {today.isoformat()}  ")
    lines.append(f"**صالح حتى / Valid until:** {valid_until.isoformat()} (30 يوم)  ")
    lines.append("**العملة / Currency:** SAR — كل الأسعار قبل الضريبة (ex-VAT, +15% VAT)")
    lines.append("")
    if q["offer_name_ar"] or q["offer_name_en"]:
        lines.append(f"**العرض / Offer:** {q['offer_name_ar'] or ''} — {q['offer_name_en'] or ''}")
        lines.append("")

    if q["setup"]:
        s = q["setup"]
        lines.append("## 1. رسوم التأسيس / Setup (one-off)")
        lines.append("")
        lines.append("| البند / Item | المبلغ (ex-VAT) | VAT 15% | الإجمالي / Total |")
        lines.append("|---|--:|--:|--:|")
        lines.append(f"| Setup | {s['ex_vat']:,} {cur} | {s['vat']:,} | {s['incl_vat']:,} {cur} |")
        lines.append("")

    if q["monthly"]:
        m = q["monthly"]
        lines.append("## 2. الاشتراك الشهري / Monthly subscription")
        lines.append("")
        lines.append("| البند / Item | المبلغ (ex-VAT) | VAT 15% | الإجمالي / Total |")
        lines.append("|---|--:|--:|--:|")
        label = "Monthly"
        if q["monthly_list_sar"] and q["monthly_list_sar"] != m["ex_vat"]:
            label = f"Monthly (list {q['monthly_list_sar']:,})"
        lines.append(
            f"| {label} | {m['ex_vat']:,} {cur} | {m['vat']:,} | {m['incl_vat']:,} {cur} |"
        )
        if q["annual_total_ex_vat"]:
            lines.append(
                f"| Annual prepay (12×) | {q['annual_total_ex_vat']:,} {cur} (ex-VAT) | | |"
            )
        lines.append("")
        if q["allowance_note"]:
            lines.append(f"> **الاستخدام / Usage:** {q['allowance_note']}")
            lines.append("")
        st = q["subscription_terms"]
        if st:
            lines.append(
                f"> الحد الأدنى للعقد: {_ar_months(st.get('min_term_months', 6))} "
                f"(الأفضل {_ar_months(st.get('preferred_term_months', 12))}). "
                f"الدفع شهري مقدم. إلغاء مبكر = "
                f"{_ar_months(st.get('early_cancel_penalty_months', 2))} كتعويض."
            )
            lines.append("")

    if q["schedule"]:
        lines.append("## 3. جدول الدفع / Payment schedule (50/30/20)")
        lines.append("")
        lines.append("| المرحلة / Milestone | % | المبلغ (ex-VAT) | الإجمالي / Total |")
        lines.append("|---|--:|--:|--:|")
        for ms in q["schedule"]:
            lines.append(
                f"| {ms['name_ar']} / {ms['name_en']} | {ms['pct'] * 100:.0f}% | "
                f"{ms['amount_ex_vat']:,} {cur} | {ms['amount_incl_vat']:,} {cur} |"
            )
        lines.append("")

    if q["discounts_applied"]:
        lines.append("## الخصومات المطبّقة / Discounts applied")
        for d in q["discounts_applied"]:
            lines.append(f"- {d}")
        lines.append("")

    lines.append("---")
    lines.append(
        "*أسعار تقديرية (ex-VAT) صالحة 30 يوم. تُضاف ضريبة القيمة المضافة 15% حسب "
        "أنظمة ZATCA. فاتورة رسمية ZATCA تُصدر بعد توقيع العقد.*"
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Dealix bilingual quote generator (draft only)")
    p.add_argument("--client", required=True, help="Client name")
    p.add_argument("--offer", dest="offer_key", help="Offer key (entry/pilot/production)")
    p.add_argument("--package", dest="package_key", help="Monthly package key")
    p.add_argument("--setup", type=float, default=None, help="Override one-off setup (SAR)")
    p.add_argument("--monthly", type=float, default=None, help="Override monthly (SAR)")
    p.add_argument("--annual", action="store_true", help="Apply 10% annual-prepay discount")
    p.add_argument("--case-study", action="store_true", help="Apply 15% case-study discount")
    p.add_argument("--out", default=None, help="Write quote to this path (else stdout)")
    args = p.parse_args(argv)

    if not args.offer_key and not args.package_key:
        p.error("provide at least one of --offer or --package")

    quote = build_quote(
        client=args.client,
        offer_key=args.offer_key,
        package_key=args.package_key,
        setup_override=args.setup,
        monthly_override=args.monthly,
        annual_prepay=args.annual,
        case_study=args.case_study,
    )
    md = render_quote_md(quote)
    if args.out:
        Path(args.out).write_text(md + "\n", encoding="utf-8")
        print(f"Quote draft written to {args.out} (DRAFT — needs founder approval before sending)")
    else:
        print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
