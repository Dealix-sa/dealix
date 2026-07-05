#!/usr/bin/env python3
"""Dealix daily commercial draft pack.

Creates a multi-channel review pack for the founder. It prepares draft assets
only and writes JSON plus Markdown reports.
"""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "business" / "commercial" / "daily_channels"
REPORT_DIR = ROOT / "reports" / "commercial"
ACCOUNT_FILES = [
    ROOT / "business" / "_data" / "scored_leads.json",
    ROOT / "business" / "_data" / "leads.json",
    ROOT / "business" / "crm" / "prospects.seed.json",
]
CHANNELS = ["email", "whatsapp", "linkedin", "phone", "proposal_followup", "founder_content"]


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def load_accounts() -> list[dict[str, Any]]:
    for path in ACCOUNT_FILES:
        payload = read_json(path)
        accounts = payload.get("accounts") or payload.get("leads") or []
        if isinstance(accounts, list) and accounts:
            return [item for item in accounts if isinstance(item, dict)]
    return [
        {"id": "demo-001", "name": "Demo Clinic", "segment": "Healthcare"},
        {"id": "demo-002", "name": "Demo Logistics", "segment": "Logistics"},
        {"id": "demo-003", "name": "Demo Services", "segment": "B2B Services"},
    ]


def account_name(account: dict[str, Any]) -> str:
    return str(account.get("company") or account.get("name") or account.get("id") or "Unknown account")


def account_segment(account: dict[str, Any]) -> str:
    return str(account.get("segment") or account.get("industry") or account.get("vertical") or "Saudi B2B")


def score(account: dict[str, Any]) -> float:
    for key in ("score", "fit_score", "dealix_score", "priority_score"):
        value = account.get(key)
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            try:
                return float(value)
            except ValueError:
                continue
    return 50.0


def draft_body(company: str, segment: str, channel: str, language: str) -> str:
    if language == "ar":
        base = f"مسودة {channel} لـ {company}: نقدر نجهز مراجعة قصيرة لفرص المتابعة والمبيعات في قطاع {segment} ونطلع لك أولويات تنفيذ واضحة."
        return base + " هل يناسبكم ملخص صفحة واحدة أو موعد قصير هذا الأسبوع؟"
    base = f"{channel} draft for {company}: Dealix can prepare a short review of follow-up and revenue execution opportunities in {segment}."
    return base + " Would a one-page snapshot or a short slot this week work?"


def build_draft(account: dict[str, Any], channel: str, language: str) -> dict[str, Any]:
    company = account_name(account)
    segment = account_segment(account)
    return {
        "date": dt.date.today().isoformat(),
        "account_id": account.get("id", company),
        "company": company,
        "segment": segment,
        "score": score(account),
        "channel": channel,
        "language": language,
        "subject": None if channel in {"whatsapp", "phone", "linkedin"} else f"Dealix review for {company}",
        "body": draft_body(company, segment, channel, language),
        "cta": "one-page snapshot or 15-minute diagnostic",
        "review_status": "draft_pending_human_review",
        "action_status": "review_required",
    }


def write_markdown(drafts: list[dict[str, Any]], path: Path) -> None:
    lines = [
        f"# Dealix Daily Commercial Draft Pack - {dt.date.today().isoformat()}",
        "",
        "Review pack across commercial channels.",
        "",
        f"Total drafts: {len(drafts)}",
        "",
    ]
    for draft in drafts[:30]:
        lines.extend([
            f"## {draft['company']} - {draft['channel']} - {draft['language']}",
            f"Score: {draft['score']}",
            f"Status: {draft['action_status']}",
            "",
            draft["body"],
            "",
        ])
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    today = dt.date.today().isoformat()
    accounts = sorted(load_accounts(), key=score, reverse=True)[:10]
    drafts = [
        build_draft(account, channel, language)
        for account in accounts
        for channel in CHANNELS
        for language in ("ar", "en")
    ]
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    json_path = OUT_DIR / f"commercial-draft-pack-{today}.json"
    md_path = REPORT_DIR / f"commercial-draft-pack-{today}.md"
    json_path.write_text(json.dumps(drafts, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(drafts, md_path)
    print(f"wrote {len(drafts)} drafts to {json_path}")
    print(f"wrote report to {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
