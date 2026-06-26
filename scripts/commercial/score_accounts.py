#!/usr/bin/env python3
"""Score accounts against Dealix ICP for Saudi B2B AI transformation."""

from __future__ import annotations

import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

# ICP scoring rubric — all weights documented here for auditability.
# Total possible: 100 points
# sector_fit:       0-30  (B2B sector alignment with WhatsApp/ops-heavy sectors)
# size_fit:         0-20  (employee count in target range 5-200)
# pain_signal:      0-30  (visible operational leakage or known pain)
# engagement_signal:0-20  (WhatsApp/email presence, prior engagement)

TIER_THRESHOLDS = {
    "HOT": 80,
    "WARM": 60,
    "COOL": 40,
}

HIGH_FIT_SECTORS = frozenset(
    {
        "real_estate",
        "automotive",
        "hospitality",
        "retail",
        "logistics",
        "healthcare_clinics",
        "education",
        "construction",
    }
)

MEDIUM_FIT_SECTORS = frozenset(
    {
        "professional_services",
        "food_beverage",
        "technology",
        "finance",
        "insurance",
    }
)


def score_sector_fit(sector: str) -> int:
    """Return 0-30 based on sector alignment with Dealix ICP."""
    s = (sector or "").lower().replace(" ", "_").replace("-", "_")
    if s in HIGH_FIT_SECTORS:
        return 30
    if s in MEDIUM_FIT_SECTORS:
        return 18
    return 6


def score_size_fit(employee_count: int | None) -> int:
    """Return 0-20 based on company size. Target: 5-200 employees."""
    if employee_count is None:
        return 8  # unknown: give partial credit
    if 10 <= employee_count <= 100:
        return 20
    if 5 <= employee_count < 10 or 100 < employee_count <= 200:
        return 12
    if 200 < employee_count <= 500:
        return 6
    return 0


def score_pain_signal(pain_signals: list[str]) -> int:
    """Return 0-30 based on number and quality of operational pain signals."""
    if not pain_signals:
        return 0
    count = len([p for p in pain_signals if p and p.strip()])
    if count >= 3:
        return 30
    if count == 2:
        return 20
    if count == 1:
        return 12
    return 0


def score_engagement_signal(has_whatsapp: bool, has_email: bool, prior_contact: bool) -> int:
    """Return 0-20 based on channel presence and engagement history."""
    score = 0
    if has_whatsapp:
        score += 10
    if has_email:
        score += 5
    if prior_contact:
        score += 5
    return min(score, 20)


def score_account(account: dict[str, Any]) -> dict[str, Any]:
    """
    Score a single account dict and return enriched dict with score, tier,
    and scoring breakdown.

    Expected keys (all optional): sector, employee_count, pain_signals (list),
    has_whatsapp (bool), has_email (bool), prior_contact (bool).
    """
    sector_fit = score_sector_fit(account.get("sector", ""))
    size_fit = score_size_fit(account.get("employee_count"))
    pain_signal = score_pain_signal(account.get("pain_signals") or [])
    engagement_signal = score_engagement_signal(
        has_whatsapp=bool(account.get("has_whatsapp", False)),
        has_email=bool(account.get("has_email", False)),
        prior_contact=bool(account.get("prior_contact", False)),
    )

    total = sector_fit + size_fit + pain_signal + engagement_signal

    if total >= TIER_THRESHOLDS["HOT"]:
        tier = "HOT"
    elif total >= TIER_THRESHOLDS["WARM"]:
        tier = "WARM"
    elif total >= TIER_THRESHOLDS["COOL"]:
        tier = "COOL"
    else:
        tier = "COLD"

    return {
        **account,
        "score": total,
        "tier": tier,
        "score_breakdown": {
            "sector_fit": sector_fit,
            "size_fit": size_fit,
            "pain_signal": pain_signal,
            "engagement_signal": engagement_signal,
        },
        "scored_at": datetime.now(UTC).isoformat(),
    }


def load_accounts(search_dirs: list[Path] | None = None) -> list[dict[str, Any]]:
    """Load raw account dicts from JSON files in data/targets/ or company/runtime/leads/."""
    dirs = search_dirs or [
        Path("data/targets"),
        Path("company/runtime/leads"),
    ]
    accounts: list[dict[str, Any]] = []
    for d in dirs:
        if not d.exists():
            continue
        for p in d.glob("*.json"):
            try:
                raw = json.loads(p.read_text(encoding="utf-8"))
                if isinstance(raw, list):
                    accounts.extend(raw)
                elif isinstance(raw, dict):
                    accounts.append(raw)
            except (json.JSONDecodeError, OSError):
                continue
    return accounts


def write_scored_accounts(scored: list[dict[str, Any]], date_str: str | None = None) -> Path:
    """Write scored accounts to company/runtime/scored_accounts_{date}.json."""
    date_str = date_str or datetime.now(UTC).strftime("%Y-%m-%d")
    out_dir = Path("company/runtime")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"scored_accounts_{date_str}.json"
    out_path.write_text(json.dumps(scored, ensure_ascii=False, indent=2), encoding="utf-8")
    return out_path


def run(dry_run: bool = True) -> dict[str, Any]:
    """Main entry point. dry_run=True means no external calls, no sending."""
    accounts = load_accounts()

    if not accounts:
        # Provide a minimal placeholder so the runner can still produce output.
        accounts = [
            {
                "company_name": "placeholder_target",
                "sector": "unknown",
                "employee_count": None,
                "pain_signals": [],
                "has_whatsapp": False,
                "has_email": False,
                "prior_contact": False,
            }
        ]

    scored = [score_account(a) for a in accounts]
    out_path = write_scored_accounts(scored)

    summary = {
        "total": len(scored),
        "hot": sum(1 for a in scored if a["tier"] == "HOT"),
        "warm": sum(1 for a in scored if a["tier"] == "WARM"),
        "cool": sum(1 for a in scored if a["tier"] == "COOL"),
        "cold": sum(1 for a in scored if a["tier"] == "COLD"),
        "output_path": str(out_path),
        "dry_run": dry_run,
    }
    return summary


if __name__ == "__main__":
    result = run(dry_run=True)
    print(json.dumps(result, ensure_ascii=False, indent=2))
