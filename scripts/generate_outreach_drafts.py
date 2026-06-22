"""Generate bilingual outreach drafts for the top scored leads.

Writes snake_case JSON to ``business/persuasion/exports/outreach-drafts-<date>.json``
matching the review pipeline schema (``review_status`` / ``disclaimer`` / ``generated_at``).

Usage:
    python3 scripts/generate_outreach_drafts.py --top 10 --language both --channel whatsapp --mode demo
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCORED_PATH = REPO_ROOT / "business" / "_data" / "scored_leads.json"
EXPORT_DIR = REPO_ROOT / "business" / "persuasion" / "exports"


AR_BODY = (
    "مرحباً،\n\n"
    "لاحظنا أن {company} في قطاع {segment} ينمو بشكل جيد. نرى فرصة لتحويل العمليات "
    "اليومية إلى نظام تشغيلي قابل للقياس.\n\n"
    "هل لديك ١٥ دقيقة هذا الأسبوع لمراجعة سريعة؟"
)
EN_BODY = (
    "Hi,\n\n"
    "We noticed {company} is growing well in {segment}. We see an opportunity to "
    "turn daily operations into a measurable operating system.\n\n"
    "Do you have 15 minutes this week for a quick review?"
)
DISCLAIMER = "DRAFT — Do not send without human review."

DEMO_ACCOUNTS = [
    {"id": "demo-001", "name": "Acme Saudi", "segment": "B2B Services"},
    {"id": "demo-002", "name": "Beta Clinic", "segment": "Healthcare"},
    {"id": "demo-003", "name": "Gamma Logistics", "segment": "Logistics"},
    {"id": "demo-004", "name": "Delta Marketing", "segment": "Marketing Agency"},
    {"id": "demo-005", "name": "Epsilon Real Estate", "segment": "Real Estate"},
]


def load_accounts() -> list[dict]:
    if SCORED_PATH.exists():
        data = json.loads(SCORED_PATH.read_text(encoding="utf-8"))
        return data.get("accounts", [])
    return DEMO_ACCOUNTS


def build_draft(account: dict, language: str, channel: str) -> dict:
    company = account.get("name") or account.get("id", "unknown")
    segment = account.get("segment", "")
    body = (AR_BODY if language == "ar" else EN_BODY).format(
        company=company, segment=segment
    )
    return {
        "account_id": account.get("id", ""),
        "company": company,
        "language": language,
        "channel": channel,
        "subject": None,
        "body": body,
        "review_status": "pending_review",
        "generated_at": dt.datetime.now(dt.UTC).isoformat().replace("+00:00", "Z"),
        "disclaimer": DISCLAIMER,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--top", type=int, default=10)
    parser.add_argument("--language", choices=["ar", "en", "both"], default="both")
    parser.add_argument("--channel", default="whatsapp")
    parser.add_argument("--mode", choices=["demo", "live"], default="demo")
    args = parser.parse_args()

    accounts = load_accounts()[: args.top]
    if not accounts:
        print(f"no accounts available (looked at {SCORED_PATH})")
        return 1

    languages = ["ar", "en"] if args.language == "both" else [args.language]
    drafts = [build_draft(a, lang, args.channel) for a in accounts for lang in languages]

    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    today = dt.date.today().isoformat()
    out_file = EXPORT_DIR / f"outreach-drafts-{today}.json"
    out_file.write_text(
        json.dumps(drafts, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"wrote {len(drafts)} drafts to {out_file} (mode={args.mode})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
