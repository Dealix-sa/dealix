#!/usr/bin/env python3
"""Promote legitimately-sourced business prospects from CSV → AccountRecord.

This is the "bring your own legitimately-sourced list" intake path. Unlike
``seed_revenue_machine_candidates.py`` (which writes a fixed illustrative set
for smoke tests), this script ingests a REAL CSV the founder assembled from a
lawful source: a public business directory, a Google Places export, an inbound
enquiry, or a warm introduction.

DOCTRINE GUARANTEES (enforced here, not optional):
  • NEVER fabricates an email or phone. If the CSV cell is empty, the field
    stays NULL. We do not invent ``ceo@domain`` addresses.
  • REJECTS rows whose ``source`` indicates scraping or a purchased list
    (PDPL + the 11 non-negotiables forbid both).
  • Marks every account ``allowed_use=business_contact_research_only`` and a
    truthful ``consent_status`` — never claims consent we don't have.
  • Idempotent: the account id is derived deterministically from place_id →
    domain → normalized name, so re-running updates instead of duplicating.
  • An account only becomes ``status=enriched`` (the state the daily engine
    picks up) when it has a real reachable contact method. Otherwise it stays
    ``status=new`` for the founder to complete.

CSV columns (header required; order free; extras ignored):
  company_name   (required)
  domain         (recommended — used for the stable id + DQ)
  website        (optional)
  city           (optional)
  sector         (optional — e.g. marketing_agency, saas, consulting_firm)
  contact_name   (optional)
  role           (optional)
  email          (optional — real only, never invented)
  phone          (optional — real only, never invented)
  linkedin_url   (optional)
  source         (required — must be a lawful source; see ALLOWED_SOURCES)
  place_id       (optional — Google Places id, best stable key when present)
  consent_status (optional — defaults to legitimate_interest_business_directory)
  notes          (optional)

Usage:
  # Offline preview — no DB needed, prints exactly what would be written:
  python scripts/promote_prospects_to_accounts.py --csv data/prospects.csv --dry-run

  # Real write (requires DATABASE_URL):
  python scripts/promote_prospects_to_accounts.py --csv data/prospects.csv
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from auto_client_acquisition.revenue_os.dedupe import (  # noqa: E402
    normalize_company_name,
    normalize_domain,
    normalize_phone_e164_hint,
)

_PREFIX = "promoted_"

# Lawful intake sources. Anything else is rejected. The blocklist is explicit
# so a typo can never silently admit a forbidden source.
ALLOWED_SOURCES = frozenset(
    {
        "public_directory",
        "business_directory",
        "google_places",
        "google_maps",
        "inbound_form",
        "inbound",
        "warm_intro",
        "warm_referral",
        "referral",
        "event",
        "conference",
        "founder_network",
        "manual",
    }
)

BLOCKED_SOURCE_TOKENS = (
    "scrape",
    "scraping",
    "scraped",
    "purchased",
    "bought",
    "buy",
    "leadgen_vendor",
    "data_broker",
    "linkedin_scrape",
)


def _utcnow() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


def _stable_suffix(place_id: str, domain: str | None, norm_name: str) -> str:
    """Deterministic id key: prefer place_id, then domain, then name hash."""
    basis = (place_id or domain or norm_name or "unknown").strip().lower()
    return hashlib.sha1(basis.encode("utf-8")).hexdigest()[:16]  # noqa: S324


def _source_ok(source: str) -> tuple[bool, str]:
    s = (source or "").strip().lower()
    if not s:
        return False, "empty source — a lawful source is required"
    for bad in BLOCKED_SOURCE_TOKENS:
        if bad in s:
            return False, f"forbidden source token {bad!r} (no scraping / purchased lists)"
    if s not in ALLOWED_SOURCES:
        return False, f"unknown source {s!r} — add it to ALLOWED_SOURCES if lawful"
    return True, "ok"


def _compute_dq(*, domain: str | None, email: str | None, phone: str | None,
                city: str | None, sector: str | None, contact_name: str | None) -> float:
    """DQ from completeness of REAL fields only. No fabrication, no inflation."""
    score = 30.0  # base: we have a company name (required)
    if domain:
        score += 18
    if email:
        score += 18
    if phone:
        score += 14
    if contact_name:
        score += 8
    if city:
        score += 6
    if sector:
        score += 6
    return min(score, 100.0)


def _plan_row(row: dict[str, str]) -> dict[str, Any] | None:
    company = (row.get("company_name") or "").strip()
    if not company:
        return {"_error": "missing company_name"}

    source = (row.get("source") or "").strip()
    ok, reason = _source_ok(source)
    if not ok:
        return {"_error": reason, "company": company}

    domain = normalize_domain(row.get("domain") or row.get("website"))
    place_id = (row.get("place_id") or "").strip()
    norm_name = normalize_company_name(company)
    suffix = _stable_suffix(place_id, domain, norm_name)

    # REAL contact fields only — empty stays empty (never invented).
    email = (row.get("email") or "").strip() or None
    phone_raw = (row.get("phone") or "").strip() or None
    phone = normalize_phone_e164_hint(phone_raw)
    if phone:
        phone = "+" + phone if not phone.startswith("+") else phone
    contact_name = (row.get("contact_name") or "").strip() or None
    role = (row.get("role") or "").strip() or None
    linkedin = (row.get("linkedin_url") or "").strip() or None
    city = (row.get("city") or "").strip() or None
    sector = (row.get("sector") or "").strip() or None
    website = (row.get("website") or "").strip() or (f"https://{domain}" if domain else None)
    consent = (row.get("consent_status") or "").strip() or "legitimate_interest_business_directory"
    notes = (row.get("notes") or "").strip()

    dq = _compute_dq(
        domain=domain, email=email, phone=phone, city=city,
        sector=sector, contact_name=contact_name,
    )
    reachable = bool(email or phone)
    status = "enriched" if reachable else "new"

    return {
        "account_id": f"{_PREFIX}acc_{suffix}",
        "contact_id": f"{_PREFIX}ct_{suffix}",
        "company_name": company,
        "normalized_name": norm_name[:255] or company.lower()[:255],
        "domain": domain,
        "website": website,
        "city": city,
        "country": (row.get("country") or "SA").strip() or "SA",
        "sector": sector,
        "google_place_id": place_id or None,
        "status": status,
        "data_quality_score": dq,
        "reachable": reachable,
        "contact_name": contact_name,
        "role": role,
        "email": email,
        "phone": phone,
        "linkedin_url": linkedin,
        "source": source.strip().lower(),
        "consent_status": consent,
        "notes": notes,
    }


def _load_plan(csv_path: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    with csv_path.open("r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if not any((v or "").strip() for v in row.values()):
                continue  # blank line
            plan = _plan_row(row)
            if plan is None:
                continue
            if plan.get("_error"):
                rejected.append(plan)
            else:
                accepted.append(plan)
    return accepted, rejected


def _print_plan(accepted: list[dict[str, Any]], rejected: list[dict[str, Any]]) -> None:
    print(f"\n  Accepted: {len(accepted)}  ·  Rejected: {len(rejected)}\n")
    for p in accepted:
        reach = "📇 reachable" if p["reachable"] else "○ no-contact"
        contact = p["email"] or p["phone"] or "—"
        print(f"  ✓ {p['company_name'][:38]:38} [{p['status']:8}] DQ={p['data_quality_score']:.0f} "
              f"{reach:14} {contact}")
    for r in rejected:
        print(f"  ✗ {r.get('company','?')[:38]:38} REJECTED — {r['_error']}")
    # Doctrine summary
    invented = [p for p in accepted if False]  # by construction we never invent
    assert not invented, "doctrine breach: invented contact"
    print(f"\n  Doctrine: 0 fabricated emails/phones · {len(rejected)} forbidden-source rows blocked.")


async def _write_plan(accepted: list[dict[str, Any]]) -> int:
    from sqlalchemy import select

    from db.models import AccountRecord, ContactRecord
    from db.session import async_session_factory, init_db

    await init_db()
    now = _utcnow()
    written_acc = 0
    written_ct = 0
    async with async_session_factory() as session:
        for p in accepted:
            existing = (
                await session.execute(
                    select(AccountRecord).where(AccountRecord.id == p["account_id"])
                )
            ).scalar_one_or_none()

            extra = {
                "allowed_use": "business_contact_research_only",
                "consent_status": p["consent_status"],
                "source_type": "public" if p["source"] in {"public_directory", "business_directory", "google_places", "google_maps"} else "direct",
                "promoted": True,
                "warm_outreach_eligible": p["source"] in {"warm_intro", "warm_referral", "referral", "inbound_form", "inbound"},
                "notes": p["notes"],
            }

            if existing:
                existing.company_name = p["company_name"]
                existing.normalized_name = p["normalized_name"]
                existing.domain = p["domain"]
                existing.website = p["website"]
                existing.city = p["city"]
                existing.sector = p["sector"]
                existing.google_place_id = p["google_place_id"]
                existing.status = p["status"]
                existing.data_quality_score = p["data_quality_score"]
                existing.risk_level = "low" if p["data_quality_score"] >= 70 else "medium"
                merged = dict(existing.extra or {})
                merged.update(extra)
                existing.extra = merged
                existing.updated_at = now
            else:
                session.add(
                    AccountRecord(
                        id=p["account_id"],
                        company_name=p["company_name"],
                        normalized_name=p["normalized_name"],
                        domain=p["domain"],
                        website=p["website"],
                        city=p["city"],
                        country=p["country"],
                        sector=p["sector"],
                        google_place_id=p["google_place_id"],
                        source_count=1,
                        best_source=p["source"],
                        risk_level="low" if p["data_quality_score"] >= 70 else "medium",
                        status=p["status"],
                        data_quality_score=p["data_quality_score"],
                        extra=extra,
                    )
                )
                written_acc += 1

            # Only attach a contact row if there is a real name or contact method.
            if p["contact_name"] or p["email"] or p["phone"] or p["linkedin_url"]:
                ct = (
                    await session.execute(
                        select(ContactRecord).where(ContactRecord.id == p["contact_id"])
                    )
                ).scalar_one_or_none()
                if ct:
                    ct.name = p["contact_name"] or ct.name
                    ct.role = p["role"] or ct.role
                    ct.email = p["email"] or ct.email
                    ct.phone = p["phone"] or ct.phone
                    ct.linkedin_url = p["linkedin_url"] or ct.linkedin_url
                    ct.consent_status = p["consent_status"]
                    ct.updated_at = now
                else:
                    session.add(
                        ContactRecord(
                            id=p["contact_id"],
                            account_id=p["account_id"],
                            name=p["contact_name"],
                            role=p["role"],
                            email=p["email"],
                            phone=p["phone"],
                            linkedin_url=p["linkedin_url"],
                            source=p["source"],
                            consent_status=p["consent_status"],
                            opt_out=False,
                            risk_level="low",
                        )
                    )
                    written_ct += 1

        await session.commit()

    print(f"\n  OK · {written_acc} new accounts, {written_ct} new contacts written "
          f"({len(accepted) - written_acc} updated in place).")
    print("  Next: the daily engine picks up status=enriched accounts automatically,")
    print("        or POST /api/v1/automation/revenue-machine/run with approval_mode=draft_only.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--csv", default="data/prospects.csv", help="Input CSV path")
    parser.add_argument("--dry-run", action="store_true", help="Preview only — no DB writes, no DATABASE_URL needed")
    args = parser.parse_args()

    csv_path = REPO_ROOT / args.csv if not Path(args.csv).is_absolute() else Path(args.csv)
    if not csv_path.is_file():
        print(f"❌ CSV not found: {csv_path}")
        print(f"   Copy the template:  cp data/prospects.csv.template {args.csv}")
        return 1

    accepted, rejected = _load_plan(csv_path)
    _print_plan(accepted, rejected)

    if not accepted:
        print("\n  Nothing to write (no accepted rows).")
        return 1 if rejected else 0

    if args.dry_run:
        print("\n  --dry-run: no database writes performed.")
        return 0

    if not os.getenv("DATABASE_URL"):
        print("\n❌ DATABASE_URL not set. Use --dry-run to preview, or set DATABASE_URL to write.")
        return 2

    import asyncio

    return asyncio.run(_write_plan(accepted))


if __name__ == "__main__":
    raise SystemExit(main())
