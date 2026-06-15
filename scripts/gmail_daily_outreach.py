"""Daily Gmail outreach generator for Saudi B2B ICP targets.

Standalone script — reads/writes JSON only, no FastAPI, no database.

Usage:
    python scripts/gmail_daily_outreach.py                      # generate today's emails + print
    python scripts/gmail_daily_outreach.py --mode drafts        # also create Gmail drafts
    python scripts/gmail_daily_outreach.py --sector real_estate_developer
    python scripts/gmail_daily_outreach.py --count 5

Output:
    data/daily_outreach_{date}.json   — digest of all generated emails
    stdout                            — formatted summary
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

# ── Try to import from canonical email module; fall back to inline ──────────
try:
    from auto_client_acquisition.email.daily_targeting import (
        angle_for,
        render_outreach_email,
        _subject_hook_for,
    )
    _IMPORT_OK = True
except Exception:  # pragma: no cover
    _IMPORT_OK = False

    def angle_for(sector: str | None) -> str:  # type: ignore[misc]
        _ANGLE_MAP: dict[str, str] = {
            "real_estate_developer": (
                "كل lead عقاري متأخر دقيقة = احتمال خسارة العميل لمنافس. Dealix يرد خلال 45 ثانية بالعربي الخليجي، "
                "يأخذ الميزانية + الموقع + الموعد، ويسلم العميل المؤهل لمندوبكم."
            ),
            "construction": (
                "بدل ما تضيع طلبات تسعير المشاريع بين واتساب + اتصالات + إيميلات، Dealix يجمع المواصفات + الميزانية + "
                "المهلة الزمنية لكل طلب، ويفرز الجاهز للتسعير عن الباقي."
            ),
            "hospitality": (
                "حجوزات MICE + إفطار/سحور + قاعات = leads عربية تحتاج رد فوري. Dealix يخدم العميل بالعربي ويحجز موعد معاينة."
            ),
            "events": (
                "كل lead لقاعة حفل = موسم. Dealix يرد فوراً، يأخذ التاريخ + العدد + الباقة، ويحجز معاينة في تقويم فريقكم."
            ),
            "logistics": (
                "RFQ شحن: العميل يطلب عرض، إذا تأخرتم 10 دقائق رحل لمنافس. Dealix يرد بالعربي خلال دقيقة، "
                "يجمع الوزن + الوجهة + التاريخ، ويفتح ticket في نظامكم."
            ),
            "restaurant_chain": (
                "Dealix يرد على استفسارات التموين + الحجوزات + الفرنشايز بالعربي خلال 45 ثانية، ويفرز الجاد منها للإدارة."
            ),
            "healthcare_clinic": (
                "Dealix يرد على استفسارات المرضى بالعربي خلال 45 ثانية، يحجز المواعيد، ويرسل التذكيرات"
                " — بدون ما تضيع appointment واحدة."
            ),
            "car_dealership": (
                "كل استفسار تشتري سيارة متأخر = عميل راح لمعرض ثاني. Dealix يرد خلال 45 ثانية بالعربي،"
                " يأخذ الميزانية + الموديل + موعد التجربة."
            ),
        }
        if not sector:
            return "Dealix يرد على inbound leads بالعربي الخليجي خلال 45 ثانية."
        return _ANGLE_MAP.get(sector.lower(), "Dealix يرد على inbound leads بالعربي الخليجي خلال 45 ثانية.")

    def _subject_hook_for(sector: str | None) -> str:  # type: ignore[misc]
        _HOOKS: dict[str, str] = {
            "real_estate_developer": "رد فوري على leads العقار",
            "construction": "تنظيم RFQ المشاريع",
            "hospitality": "حجوزات MICE بالعربي",
            "events": "leads قاعات الأفراح",
            "logistics": "RFQ الشحن في دقيقة",
            "restaurant_chain": "تموين وحجوزات فورية",
            "healthcare_clinic": "حجز مواعيد لا تضيع",
            "car_dealership": "leads السيارات — رد فوري",
        }
        if not sector:
            return "رد فوري على inbound leads"
        return _HOOKS.get(sector.lower(), "رد فوري على inbound leads")

    def render_outreach_email(target: dict[str, Any]) -> dict[str, str]:  # type: ignore[misc]
        company = (target.get("company_ar") or target.get("company_name") or "فريقكم").strip()
        sector = target.get("sector") or ""
        angle = angle_for(sector)
        hook = _subject_hook_for(sector)
        body = (
            f"السلام عليكم {company}،\n\n"
            f"{angle}\n\n"
            "وبجانب الرد الفوري، Dealix يبني لكم:\n"
            "- غرفة قيادة: شاشة واحدة تشوفون فيها كل lead، كل إيراد، كل مؤشر — لحظة بلحظة\n"
            "- نظام متابعة: follow-up تلقائي على كل استفسار مفتوح (اليوم 2، اليوم 5، اليوم 10)\n"
            "- تقرير أسبوعي: \"الإيرادات المفقودة هذا الأسبوع\" — وكيف نستردها\n\n"
            "Pilot 7 أيام بـ 499 ريال — نشتغل على leadsكم نحن، تشوفون النتيجة، ثم تقرّرون.\n"
            "تناسبكم 20 دقيقة هذا الأسبوع؟\n\n"
            "سامي\n"
            "Dealix — https://dealix.me\n"
            "احجز هنا: https://calendly.com/sami-assiri11/dealix-demo"
        )
        subject = f"Dealix — {hook} | {company}"
        return {"subject_ar": subject, "body_ar": body}


# ── Paths ────────────────────────────────────────────────────────────────────
_REPO_ROOT = Path(__file__).resolve().parent.parent
_TARGETS_PATH = _REPO_ROOT / "data" / "saudi_icp_targets.json"
_DATA_DIR = _REPO_ROOT / "data"

_COOLDOWN_DAYS = 30  # do not re-contact within this window


# ── Core functions ────────────────────────────────────────────────────────────

def load_targets(path: Path = _TARGETS_PATH) -> list[dict[str, Any]]:
    """Load the ICP target list from JSON file."""
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def save_targets(targets: list[dict[str, Any]], path: Path = _TARGETS_PATH) -> None:
    """Persist the updated ICP target list back to JSON."""
    with path.open("w", encoding="utf-8") as fh:
        json.dump(targets, fh, ensure_ascii=False, indent=2)


def is_contactable(target: dict[str, Any], today: date) -> bool:
    """Return True if the target is eligible for outreach today.

    Eligibility rules:
    - status must be "pending"
    - last_contacted must be null OR older than _COOLDOWN_DAYS
    """
    if target.get("status") != "pending":
        return False
    last_str = target.get("last_contacted")
    if last_str is None:
        return True
    try:
        last_date = date.fromisoformat(str(last_str)[:10])
        return (today - last_date).days > _COOLDOWN_DAYS
    except ValueError:
        return True


def filter_and_rank(
    targets: list[dict[str, Any]],
    today: date,
    sector_filter: str | None = None,
) -> list[dict[str, Any]]:
    """Filter contactable targets and sort by priority (P0 first), then id."""
    eligible = [t for t in targets if is_contactable(t, today)]
    if sector_filter:
        eligible = [t for t in eligible if t.get("sector") == sector_filter]
    # P0 before P1 before the rest; stable secondary sort by id
    priority_order = {"P0": 0, "P1": 1}
    eligible.sort(key=lambda t: (priority_order.get(t.get("priority", "P1"), 99), t.get("id", "")))
    return eligible


def pick_diversified(
    ranked: list[dict[str, Any]],
    count: int,
    max_per_sector: int = 3,
) -> list[dict[str, Any]]:
    """Pick up to `count` targets while capping each sector at `max_per_sector`.

    Iterates the already-priority-sorted list; first pass fills sector quotas,
    then a second pass tops up if we still need more entries.
    """
    sector_seen: dict[str, int] = {}
    chosen: list[dict[str, Any]] = []
    remainder: list[dict[str, Any]] = []

    for t in ranked:
        sec = t.get("sector", "other")
        if sector_seen.get(sec, 0) < max_per_sector and len(chosen) < count:
            chosen.append(t)
            sector_seen[sec] = sector_seen.get(sec, 0) + 1
        else:
            remainder.append(t)

    # Top-up without sector constraint if we still need more
    for t in remainder:
        if len(chosen) >= count:
            break
        chosen.append(t)

    return chosen


def build_draft(target: dict[str, Any]) -> dict[str, Any]:
    """Build the full email draft dict for a single target."""
    email = render_outreach_email(target)
    return {
        "id": target.get("id"),
        "company_ar": target.get("company_ar"),
        "company_en": target.get("company_en"),
        "sector": target.get("sector"),
        "city": target.get("city"),
        "priority": target.get("priority"),
        "contact_email": target.get("contact_email"),
        "subject_ar": email["subject_ar"],
        "body_ar": email["body_ar"],
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


def write_digest(drafts: list[dict[str, Any]], today: date) -> Path:
    """Write the daily digest JSON to data/daily_outreach_{date}.json."""
    out_path = _DATA_DIR / f"daily_outreach_{today.isoformat()}.json"
    payload = {
        "date": today.isoformat(),
        "count": len(drafts),
        "drafts": drafts,
    }
    with out_path.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
    return out_path


def mark_drafted(
    targets: list[dict[str, Any]],
    drafted_ids: set[str],
    today: date,
    path: Path = _TARGETS_PATH,
) -> None:
    """Update last_contacted = today for all drafted targets and persist."""
    today_str = today.isoformat()
    for t in targets:
        if t.get("id") in drafted_ids:
            t["last_contacted"] = today_str
    save_targets(targets, path)


def print_summary(drafts: list[dict[str, Any]]) -> None:
    """Print a formatted human-readable summary to stdout."""
    separator = "-" * 60
    print(separator)
    print(f"  Daily Outreach Digest — {len(drafts)} targets")
    print(separator)
    for i, d in enumerate(drafts, 1):
        company = d.get("company_ar", "")
        sector = d.get("sector", "")
        city = d.get("city", "")
        priority = d.get("priority", "")
        email_addr = d.get("contact_email") or "(no email yet)"
        subject = d.get("subject_ar", "")
        body = d.get("body_ar", "")
        print(f"\n[{i}] {company}")
        print(f"    Sector: {sector}  |  City: {city}  |  Priority: {priority}")
        print(f"    To: {email_addr}")
        print(f"    Subject: {subject}")
        print()
        for line in body.splitlines():
            print(f"    {line}")
        print()
        print(separator)


def create_gmail_draft_placeholder(draft: dict[str, Any]) -> None:
    """Placeholder for Gmail API draft creation.

    In production, replace this function body with a call to the Gmail API
    using credentials stored in GMAIL_* env vars. The function signature must
    not change — the script router calls it.
    """
    company = draft.get("company_ar", "")
    email_addr = draft.get("contact_email")
    if email_addr:
        print(f"DRAFT READY: {company} -> {email_addr}")
    else:
        print(f"DRAFT SKIPPED (no email): {company}")


# ── CLI entry point ────────────────────────────────────────────────────────────

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate daily Arabic outreach emails for Saudi B2B ICP targets."
    )
    parser.add_argument(
        "--mode",
        choices=["generate", "drafts"],
        default="generate",
        help="generate = print only; drafts = also call Gmail API (placeholder).",
    )
    parser.add_argument(
        "--sector",
        default=None,
        help="Filter targets to a specific sector (e.g. real_estate_developer).",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=10,
        help="Number of targets to pick (default 10).",
    )
    parser.add_argument(
        "--targets-path",
        default=str(_TARGETS_PATH),
        help="Override path to saudi_icp_targets.json.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not write any files or update last_contacted.",
    )
    return parser.parse_args(argv)


def run(argv: list[str] | None = None) -> int:
    """Main entry point — returns exit code (0 = success)."""
    args = parse_args(argv)
    targets_path = Path(args.targets_path)
    today = date.today()

    try:
        targets = load_targets(targets_path)
    except FileNotFoundError:
        print(f"ERROR: targets file not found: {targets_path}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid JSON in {targets_path}: {exc}", file=sys.stderr)
        return 1

    ranked = filter_and_rank(targets, today, sector_filter=args.sector)
    if not ranked:
        print("No contactable targets found for today.", file=sys.stderr)
        return 0

    selected = pick_diversified(ranked, count=args.count)
    drafts = [build_draft(t) for t in selected]

    # Print formatted summary
    print_summary(drafts)

    if not args.dry_run:
        # Write digest JSON
        digest_path = write_digest(drafts, today)
        print(f"\nDigest written: {digest_path}")

        # Update last_contacted
        drafted_ids = {d["id"] for d in drafts if d.get("id")}
        mark_drafted(targets, drafted_ids, today, path=targets_path)
        print(f"Updated last_contacted for {len(drafted_ids)} targets in {targets_path.name}")

    # Gmail draft mode
    if args.mode == "drafts":
        print("\n--- Gmail Drafts ---")
        for d in drafts:
            create_gmail_draft_placeholder(d)

    return 0


if __name__ == "__main__":
    sys.exit(run())
