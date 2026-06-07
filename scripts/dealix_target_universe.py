#!/usr/bin/env python3
"""Dealix Saudi B2B Target Universe — load, govern, score, and daily-select accounts.

Doctrine (enforced here, not optional):
  - Every account MUST carry a public ``source_url`` (non-negotiable #4/#7: no
    un-sourced claims / source-less knowledge).
  - ``contact`` MUST be empty — the universe stores **company-level public
    business info only**, never personal PII (non-negotiable #6). Personal
    contacts are added by the founder via warm intro at use time.
  - ``channel`` MUST be an approval-first channel (warm_intro / referral /
    inbound). No cold / scraping / automation channels (non-negotiables #1-3, #8).
  - ``source_type`` MUST be a storable Tier-1 source (public_business_info,
    warm_intro, referral, inbound). Scraping / purchased lists are rejected.

This module ONLY reads, scores, and ranks. It never contacts anyone. The daily
draft pack (``scripts/dealix_daily_draft_pack.py``) consumes ``daily_selection``
to produce approval-gated drafts.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
UNIVERSE_CSV = (
    REPO_ROOT / "docs/commercial/operations/targeting/saudi_b2b_target_universe.csv"
)

# Approval-first channels only (non-negotiables #1, #2, #3, #8).
ALLOWED_CHANNELS = {"warm_intro", "referral", "inbound", "partner_referral", "manual"}
# Storable Tier-1 sources only (mirrors source_registry allow-list).
ALLOWED_SOURCE_TYPES = {
    "public_business_info",
    "warm_intro",
    "partner_referral",
    "referral",
    "inbound_form",
    "inbound",
    "crm_import",
    "founder_observation",
}
BLOCKED_SOURCE_TYPES = {"scraping", "purchased_list", "cold_whatsapp", "linkedin_automation"}

# Segment fit with the Governed Revenue/AI Ops ICP (0-1).
SEGMENT_FIT = {
    "agency_wedge": 1.0,
    "crm_revops_gap": 0.95,
    "saas": 0.9,
    "ai_without_governance": 0.85,
    "clinic_lead_followup": 0.7,
    "agency_followup": 0.9,
    "b2b_services_founder_led": 1.0,
    "real_estate": 0.6,
    "crm_implementer_partner": 0.8,
}
# Tier fit — SMB/midmarket close faster than enterprise (slow track).
TIER_FIT = {"smb": 1.0, "midmarket": 0.85, "enterprise": 0.55}
# Motion weight — A (warm wedge) is the fast path; D (executive) is slower.
MOTION_FIT = {"A": 1.0, "B": 0.85, "C": 0.8, "D": 0.7, "": 0.75}
PRIORITY_FIT = {"high": 1.0, "medium": 0.75, "low": 0.5, "": 0.6}


class UniverseError(ValueError):
    """Raised when a row violates the doctrine (un-sourced, PII, cold channel)."""


@dataclass
class Account:
    company: str
    segment: str
    city: str
    sector: str
    tier: str
    motion: str
    priority: str
    offer_id: str
    pain_hypothesis: str
    why_now: str
    channel: str
    source_type: str
    source_url: str
    contact_status: str
    status: str
    notes: str
    raw: dict[str, str] = field(default_factory=dict)

    # ---- scoring ---------------------------------------------------------
    def icp_score(self) -> int:
        """Transparent, deterministic 0-100 ICP score."""
        seg = SEGMENT_FIT.get(self.segment, 0.6)
        tier = TIER_FIT.get(self.tier, 0.7)
        motion = MOTION_FIT.get(self.motion, 0.75)
        pr = PRIORITY_FIT.get((self.priority or "").lower(), 0.6)
        why_now = 1.0 if self.why_now.strip() else 0.6
        # Weighted blend → 0..1, then scaled to 0..100.
        blend = (
            0.34 * seg
            + 0.20 * tier
            + 0.16 * motion
            + 0.16 * pr
            + 0.14 * why_now
        )
        return round(blend * 100)

    def score_breakdown(self) -> dict[str, float]:
        return {
            "segment_fit": SEGMENT_FIT.get(self.segment, 0.6),
            "tier_fit": TIER_FIT.get(self.tier, 0.7),
            "motion_fit": MOTION_FIT.get(self.motion, 0.75),
            "priority_fit": PRIORITY_FIT.get((self.priority or "").lower(), 0.6),
            "why_now": 1.0 if self.why_now.strip() else 0.6,
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "company": self.company,
            "segment": self.segment,
            "city": self.city,
            "sector": self.sector,
            "tier": self.tier,
            "motion": self.motion,
            "priority": self.priority,
            "offer_id": self.offer_id,
            "pain_hypothesis": self.pain_hypothesis,
            "why_now": self.why_now,
            "channel": self.channel,
            "source_type": self.source_type,
            "source_url": self.source_url,
            "contact_status": self.contact_status,
            "icp_score": self.icp_score(),
            "score_breakdown": self.score_breakdown(),
            "governance_decision": "research_only",  # not approved for outreach
        }


# Common PII signatures we must never store in a target universe row.
def _looks_like_pii(value: str) -> bool:
    v = (value or "").strip()
    if not v:
        return False
    if "@" in v:  # email
        return True
    digits = sum(c.isdigit() for c in v)
    if digits >= 7:  # phone-like
        return True
    return False


def load_accounts(path: Path | None = None) -> list[Account]:
    p = path or UNIVERSE_CSV
    if not p.is_file():
        raise UniverseError(f"universe_csv_not_found:{p}")
    accounts: list[Account] = []
    with p.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=2):  # row 1 = header
            company = (row.get("company") or "").strip()
            if not company:
                continue
            source_url = (row.get("source_url") or "").strip()
            source_type = (row.get("source_type") or "").strip().lower()
            channel = (row.get("channel") or "").strip().lower()
            contact = (row.get("contact") or "").strip()

            # --- doctrine gates ---
            if not source_url:
                raise UniverseError(f"row {i} ({company}): missing source_url (#4/#7)")
            if source_type in BLOCKED_SOURCE_TYPES:
                raise UniverseError(f"row {i} ({company}): blocked source_type={source_type} (#1)")
            if source_type and source_type not in ALLOWED_SOURCE_TYPES:
                raise UniverseError(
                    f"row {i} ({company}): source_type={source_type!r} not in allow-list"
                )
            if channel and channel not in ALLOWED_CHANNELS:
                raise UniverseError(
                    f"row {i} ({company}): channel={channel!r} is not approval-first (#1-3,#8)"
                )
            if contact and _looks_like_pii(contact):
                raise UniverseError(
                    f"row {i} ({company}): contact column contains PII — keep it empty (#6)"
                )

            accounts.append(
                Account(
                    company=company,
                    segment=(row.get("segment") or "").strip(),
                    city=(row.get("city") or "").strip(),
                    sector=(row.get("sector") or "").strip(),
                    tier=(row.get("tier") or "").strip().lower(),
                    motion=(row.get("motion") or "").strip().upper(),
                    priority=(row.get("priority") or "").strip().lower(),
                    offer_id=(row.get("offer_id") or "").strip(),
                    pain_hypothesis=(row.get("pain_hypothesis") or "").strip(),
                    why_now=(row.get("why_now") or "").strip(),
                    channel=channel or "warm_intro",
                    source_type=source_type or "public_business_info",
                    source_url=source_url,
                    contact_status=(row.get("contact_status") or "needs_warm_intro").strip(),
                    status=(row.get("status") or "not_contacted").strip(),
                    notes=(row.get("notes") or "").strip(),
                    raw=dict(row),
                )
            )
    return accounts


def ranked(accounts: list[Account] | None = None) -> list[Account]:
    rows = accounts if accounts is not None else load_accounts()
    return sorted(rows, key=lambda a: (a.icp_score(), a.company), reverse=True)


def daily_selection(
    accounts: list[Account] | None = None,
    *,
    top_n: int = 10,
    on_date: date | None = None,
    rotate: bool = False,
) -> list[Account]:
    """Select today's batch from the ranked universe.

    Default (``rotate=False``): the highest-value accounts first — work the top
    of the funnel consistently (standard ABM). With ``rotate=True`` the batch
    cycles through the whole universe by date so every account is touched over a
    full rotation (day 0 → ranks [0:n], day 1 → [n:2n], …).
    """
    rows = ranked(accounts)
    if not rows:
        return []
    n = max(1, min(top_n, len(rows)))
    if not rotate:
        return rows[:n]
    d = on_date or datetime.now(UTC).date()
    windows = (len(rows) + n - 1) // n
    start = (d.toordinal() % windows) * n
    selection = rows[start : start + n]
    if len(selection) < n:  # wrap to the front to always return a full batch
        selection += rows[: n - len(selection)]
    return selection


def build_today_plan(
    *, top_n: int = 10, on_date: date | None = None, rotate: bool = False
) -> dict[str, Any]:
    accounts = load_accounts()
    sel = daily_selection(accounts, top_n=top_n, on_date=on_date, rotate=rotate)
    d = on_date or datetime.now(UTC).date()
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "date": d.isoformat(),
        "universe_size": len(accounts),
        "top_n": top_n,
        "selection": [a.to_dict() for a in sel],
        "policy": {
            "external_send_requires_approval": True,
            "no_cold_outreach": True,
            "no_scraping": True,
            "contact_pii_stored": False,
            "every_account_sourced": True,
        },
        "founder_note_ar": (
            "هذه حسابات بحث عامة (معلومات شركات منشورة) — تتطلب مقدمة دافئة قبل أي "
            "تواصل. أضِف صفوف شبكتك الدافئة في أعلى الأولوية. لا إرسال بارد."
        ),
        "founder_note_en": (
            "Public-research accounts (published company info) — require a warm "
            "intro before any contact. Add your own warm-network rows at top "
            "priority. No cold outreach."
        ),
    }


def _print_human(plan: dict[str, Any]) -> None:
    print(f"Dealix Target Universe — {plan['date']}")
    print(f"  universe: {plan['universe_size']} accounts | today's batch: {plan['top_n']}")
    print("  policy: warm-intro-first · sourced · no PII · no cold/scraping")
    print("")
    for i, a in enumerate(plan["selection"], start=1):
        print(
            f"  {i:>2}. [{a['icp_score']:>3}] {a['company']}  "
            f"({a['segment']}/{a['tier']}/{a['city']}) → {a['offer_id']}"
        )
        print(f"      why-now: {a['why_now']}")
        print(f"      source : {a['source_url']}")
    print("")
    print(f"  ⚠ {plan['founder_note_en']}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Dealix Saudi B2B Target Universe")
    ap.add_argument("--top", type=int, default=10, help="accounts in today's batch")
    ap.add_argument("--date", type=str, default="", help="ISO date (default: today UTC)")
    ap.add_argument("--json", action="store_true", help="emit JSON")
    ap.add_argument("--all", action="store_true", help="rank the whole universe")
    ap.add_argument(
        "--rotate",
        action="store_true",
        help="cycle the batch through the whole universe by date (default: top-N)",
    )
    args = ap.parse_args(argv)

    on_date = date.fromisoformat(args.date) if args.date else None
    try:
        if args.all:
            rows = ranked()
            plan = {
                "generated_at": datetime.now(UTC).isoformat(),
                "universe_size": len(rows),
                "selection": [a.to_dict() for a in rows],
            }
        else:
            plan = build_today_plan(top_n=args.top, on_date=on_date, rotate=args.rotate)
    except UniverseError as exc:
        print(f"DOCTRINE_VIOLATION: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
    else:
        if args.all:
            for i, a in enumerate(plan["selection"], start=1):
                print(f"{i:>2}. [{a['icp_score']:>3}] {a['company']} ({a['segment']}/{a['tier']})")
        else:
            _print_human(plan)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
