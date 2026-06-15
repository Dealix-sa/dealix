#!/usr/bin/env python3
"""
Dealix Renewal Tracker
======================
CLI to track when customer contracts are due for renewal and print bilingual
AR+EN alerts.  The founder runs this each morning to spot upcoming renewals.

Usage:
  # Add a new contract:
  python3 scripts/dealix_renewal_tracker.py add \
    --company "شركة نجم اللوجستية" \
    --sector logistics \
    --tier command_center \
    --start-date 2026-01-01 \
    --months 6 \
    --monthly-sar 9000

  # Check for upcoming renewals (30-day urgent / 60-day warning):
  python3 scripts/dealix_renewal_tracker.py check

  # Mark a contract renewed:
  python3 scripts/dealix_renewal_tracker.py update \
    --company "شركة نجم اللوجستية" \
    --status renewed

  # Print MRR + at-risk count:
  python3 scripts/dealix_renewal_tracker.py summary

Doctrine: never auto-sends.  Founder reviews all alerts before acting.
"""

from __future__ import annotations

import argparse
import csv
import uuid
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
CONTRACT_LOG = REPO_ROOT / "data/contracts/contract_log.csv"

FIELDNAMES = [
    "contract_id",
    "company",
    "sector",
    "tier",
    "start_date",
    "end_date",
    "monthly_sar",
    "status",
]

VALID_STATUSES = ["active", "renewed", "churned", "paused"]
VALID_TIERS = [
    "sprint",
    "revenue_os",
    "command_center",
    "delivery_os",
    "review_os",
]

STATUS_AR: dict[str, str] = {
    "active": "نشط",
    "renewed": "مُجدَّد",
    "churned": "خسارة",
    "paused": "موقوف",
}

TIER_AR: dict[str, str] = {
    "sprint": "التشخيص السريع",
    "revenue_os": "نظام تشغيل الإيرادات",
    "command_center": "مركز القيادة",
    "delivery_os": "نظام التسليم",
    "review_os": "نظام المراجعة والسمعة",
}

URGENT_DAYS = 30
WARNING_DAYS = 60


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _log_path() -> Path:
    """Return the path to the contract log (respects DEALIX_CONTRACTS_PATH env)."""
    env_path = _read_env_var("DEALIX_CONTRACTS_PATH")
    if env_path:
        return Path(env_path)
    return CONTRACT_LOG


def _read_env_var(name: str) -> str:
    """Read a single environment variable without importing os."""
    try:
        environ_text = Path("/proc/self/environ").read_bytes()
        for entry in environ_text.split(b"\x00"):
            if entry.startswith(name.encode() + b"="):
                return entry[len(name) + 1:].decode(errors="replace")
    except Exception:  # /proc/self/environ may not exist on non-Linux systems
        pass
    return ""


def _load_contracts() -> list[dict]:
    path = _log_path()
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return [dict(r) for r in reader]


def _save_contracts(rows: list[dict]) -> None:
    path = _log_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def _normalize(name: str) -> str:
    return name.strip().lower().replace(" ", "")


def _days_until(end_date_str: str) -> int:
    """Return calendar days from today until end_date_str (YYYY-MM-DD)."""
    try:
        end = date.fromisoformat(end_date_str)
    except ValueError:
        return 9999
    return (end - date.today()).days


# ---------------------------------------------------------------------------
# Public command functions
# ---------------------------------------------------------------------------

def cmd_add(args: argparse.Namespace) -> None:
    """Add a new contract record to the log."""
    if args.tier not in VALID_TIERS:
        print(f"[ERROR] Invalid tier '{args.tier}'. Valid: {', '.join(VALID_TIERS)}")
        return

    try:
        start = date.fromisoformat(args.start_date)
    except ValueError:
        print(f"[ERROR] Invalid start-date format '{args.start_date}'. Use YYYY-MM-DD.")
        return

    if args.months <= 0:
        print("[ERROR] --months must be a positive integer.")
        return

    end = date(
        start.year + (start.month + args.months - 1) // 12,
        (start.month + args.months - 1) % 12 + 1,
        start.day,
    )

    rows = _load_contracts()
    existing = [
        r for r in rows
        if _normalize(r.get("company", "")) == _normalize(args.company)
        and r.get("status") == "active"
    ]
    if existing:
        print(
            f"[WARN] An active contract for '{args.company}' already exists "
            f"(ends {existing[-1].get('end_date')}). "
            "Use 'update' to change status first."
        )
        return

    contract_id = f"DLX-CNT-{date.today().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
    row = {
        "contract_id": contract_id,
        "company": args.company,
        "sector": args.sector or "",
        "tier": args.tier,
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "monthly_sar": str(args.monthly_sar),
        "status": "active",
    }
    rows.append(row)
    _save_contracts(rows)

    tier_label = TIER_AR.get(args.tier, args.tier)
    print()
    print(f"  تمت الإضافة / Contract added: {args.company}")
    print(f"  الباقة / Tier : {args.tier} — {tier_label}")
    print(f"  البداية / Start: {start.isoformat()}")
    print(f"  النهاية / End  : {end.isoformat()}")
    print(f"  SAR/month     : {args.monthly_sar:,}")
    print(f"  ID            : {contract_id}")
    print()


def cmd_check(_args: argparse.Namespace) -> None:
    """Print companies whose contracts expire within 30 or 60 days."""
    rows = _load_contracts()
    active = [r for r in rows if r.get("status") == "active"]

    urgent: list[dict] = []
    warning: list[dict] = []

    for r in active:
        days = _days_until(r.get("end_date", ""))
        if days < 0:
            continue  # already expired; not shown here
        if days <= URGENT_DAYS:
            urgent.append((days, r))
        elif days <= WARNING_DAYS:
            warning.append((days, r))

    urgent.sort(key=lambda x: x[0])
    warning.sort(key=lambda x: x[0])

    print()
    print("=" * 60)
    print("  تنبيه تجديد العقود / Contract Renewal Alerts")
    print("=" * 60)

    if not urgent and not warning:
        print("  لا توجد عقود مستحقة خلال 60 يوم.")
        print("  No contracts due for renewal within 60 days.")
        print()
        return

    if urgent:
        print()
        print(f"  [عاجل / URGENT] انتهاء خلال {URGENT_DAYS} يوم / Expiring within {URGENT_DAYS} days:")
        for days, r in urgent:
            monthly = int(r.get("monthly_sar") or 0)
            print(
                f"    - {r['company']} | {r.get('tier','')} | "
                f"ينتهي / ends: {r['end_date']} ({days} يوم/days) | "
                f"{monthly:,} SAR/mo"
            )

    if warning:
        print()
        print(f"  [تحذير / WARNING] انتهاء خلال {WARNING_DAYS} يوم / Expiring within {WARNING_DAYS} days:")
        for days, r in warning:
            monthly = int(r.get("monthly_sar") or 0)
            print(
                f"    - {r['company']} | {r.get('tier','')} | "
                f"ينتهي / ends: {r['end_date']} ({days} يوم/days) | "
                f"{monthly:,} SAR/mo"
            )

    print()
    print("  الإجراء: راجع العقود أعلاه وتواصل مع العميل قبل انتهاء المدة.")
    print("  Action : Review the contracts above and contact clients before expiry.")
    print()


def cmd_update(args: argparse.Namespace) -> None:
    """Update the status of an existing contract by company name."""
    if args.status not in VALID_STATUSES:
        print(f"[ERROR] Invalid status '{args.status}'. Valid: {', '.join(VALID_STATUSES)}")
        return

    rows = _load_contracts()
    updated = False
    for row in rows:
        if _normalize(row.get("company", "")) == _normalize(args.company):
            old = row.get("status")
            row["status"] = args.status
            print(
                f"  تم التحديث / Updated: {args.company} — "
                f"{old} -> {args.status} ({STATUS_AR.get(args.status, '')})"
            )
            updated = True
            break

    if not updated:
        print(f"[NOT FOUND] '{args.company}' not found in contract_log.csv.")
        return

    _save_contracts(rows)


def cmd_summary(_args: argparse.Namespace) -> None:
    """Print MRR, active customer count, and at-risk count."""
    rows = _load_contracts()

    active = [r for r in rows if r.get("status") == "active"]
    at_risk = [
        r for r in active
        if _days_until(r.get("end_date", "")) <= WARNING_DAYS
    ]
    mrr = sum(int(r.get("monthly_sar") or 0) for r in active)

    print()
    print("=" * 55)
    print("  ملخص العقود / Contract Summary")
    print("=" * 55)
    print(f"  إجمالي العقود / Total contracts  : {len(rows)}")
    print(f"  عقود نشطة / Active contracts     : {len(active)}")
    print(f"  MRR (SAR)                        : {mrr:,}")
    print(f"  في خطر (60 يوم) / At-risk (60d)  : {len(at_risk)}")
    print()

    if at_risk:
        print("  العقود في خطر / At-risk contracts:")
        for r in at_risk:
            days = _days_until(r.get("end_date", ""))
            print(f"    - {r['company']} ({days} يوم/days remaining)")
        print()

    tier_counts: dict[str, int] = {}
    for r in active:
        t = r.get("tier", "unknown")
        tier_counts[t] = tier_counts.get(t, 0) + 1

    if tier_counts:
        print("  توزيع الباقات / Tier breakdown (active):")
        for tier, count in sorted(tier_counts.items()):
            label = TIER_AR.get(tier, tier)
            print(f"    {tier:<20} {label:<25} : {count}")
        print()

    print("=" * 55)
    print()


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Dealix Renewal Tracker — track contract renewal dates and print "
            "bilingual AR+EN alerts. Doctrine: founder reviews before acting."
        )
    )
    sub = parser.add_subparsers(dest="command")

    # add
    p_add = sub.add_parser("add", help="Add a new contract")
    p_add.add_argument("--company", required=True, help="Company name (AR or EN)")
    p_add.add_argument("--sector", default="", help="Sector key")
    p_add.add_argument(
        "--tier",
        required=True,
        choices=VALID_TIERS,
        help="Service tier",
    )
    p_add.add_argument(
        "--start-date",
        required=True,
        help="Contract start date (YYYY-MM-DD)",
    )
    p_add.add_argument(
        "--months",
        required=True,
        type=int,
        help="Contract duration in months",
    )
    p_add.add_argument(
        "--monthly-sar",
        required=True,
        type=int,
        help="Monthly retainer in SAR",
    )

    # check
    sub.add_parser("check", help="Check for upcoming renewals (30 / 60 day alerts)")

    # update
    p_upd = sub.add_parser("update", help="Update a contract status")
    p_upd.add_argument("--company", required=True, help="Company name to update")
    p_upd.add_argument(
        "--status",
        required=True,
        choices=VALID_STATUSES,
        help="New status",
    )

    # summary
    sub.add_parser("summary", help="Print MRR, active count, at-risk count")

    args = parser.parse_args()

    if args.command == "add":
        cmd_add(args)
    elif args.command == "check":
        cmd_check(args)
    elif args.command == "update":
        cmd_update(args)
    elif args.command == "summary":
        cmd_summary(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
