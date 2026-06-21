"""Shared utilities for the Dealix revenue machine scripts."""
from __future__ import annotations

import csv
import json
import os
import re
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]


def today_str() -> str:
    return os.environ.get("DEALIX_DATE", date.today().isoformat())


def load_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def load_segments() -> dict[str, Any]:
    path = REPO_ROOT / "data" / "outreach" / "saudi_icp_segments.json"
    if not path.exists():
        return {"segments": []}
    return json.loads(path.read_text(encoding="utf-8"))


def segment_by_id(segments: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {s["id"]: s for s in segments}


def normalize_email(email: str) -> str:
    return email.lower().strip()


def has_public_contact(row: dict[str, str]) -> bool:
    return bool(row.get("public_contact") or row.get("email") or row.get("linkedin"))


def website_quality(website: str) -> int:
    if not website:
        return 0
    if re.match(r"https?://", website):
        return 2
    return 1


def parse_date(value: str) -> date | None:
    if not value:
        return None
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%d/%m/%Y"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    return None


def days_since(value: str) -> int | None:
    d = parse_date(value)
    if d is None:
        return None
    return (date.today() - d).days


def score_target(row: dict[str, str]) -> dict[str, Any]:
    """Deterministic scoring of a target row."""
    score = 0.0
    reasons: list[str] = []

    # Sector match (1 = known, 0.5 = unknown)
    segments = segment_by_id(load_segments()["segments"])
    sector = row.get("sector", "").strip().lower()
    if sector in segments:
        score += 1.0
        reasons.append("known_sector")
    else:
        score += 0.2
        reasons.append("unknown_sector")

    # City tier
    city = row.get("city", "").strip().lower()
    if city in {"riyadh", "jeddah", "dammam"}:
        score += 0.8
        reasons.append("tier1_city")
    elif city:
        score += 0.4
        reasons.append("other_city")

    # Public contact
    if has_public_contact(row):
        score += 0.7
        reasons.append("public_contact")

    # Website quality
    wq = website_quality(row.get("website", ""))
    if wq == 2:
        score += 0.6
        reasons.append("https_website")
    elif wq == 1:
        score += 0.3
        reasons.append("website_no_https")

    # Confidence
    try:
        confidence = float(row.get("confidence", "0"))
    except ValueError:
        confidence = 0.0
    score += confidence
    reasons.append(f"confidence_{confidence}")

    # Verification status
    vstatus = row.get("verification_status", "").strip().lower()
    if vstatus == "verified_public":
        score += 0.5
        reasons.append("verified_public")
    elif vstatus == "placeholder":
        score += 0.0
        reasons.append("placeholder")
    elif vstatus:
        score += 0.2
        reasons.append("partial_verification")

    # Source URL
    if row.get("source_url") and row.get("source_url").strip().startswith("http"):
        score += 0.4
        reasons.append("has_source_url")

    # Pain hypothesis quality
    pain = row.get("pain_hypothesis", "").strip()
    if len(pain) > 30:
        score += 0.3
        reasons.append("clear_pain")

    final = round(min(score, 5.0), 2)
    return {
        "score": final,
        "reasons": reasons,
        "tier": "hot" if final >= 3.5 else "warm" if final >= 2.5 else "cold",
    }


def ensure_dirs() -> None:
    (REPO_ROOT / "outbox").mkdir(exist_ok=True)
    (REPO_ROOT / "reports" / "revenue").mkdir(parents=True, exist_ok=True)
    (REPO_ROOT / "ledgers").mkdir(exist_ok=True)


def opt_out_line(language: str = "ar") -> str:
    if language == "ar":
        return '\nإذا لم ترغب في تلقي رسائلنا، أرسل "إيقاف" وسنزيل تواصلك فورًا.'
    return '\nIf you do not wish to receive these messages, reply STOP and we will remove you immediately.'
