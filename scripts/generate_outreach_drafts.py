"""Generate bilingual outreach drafts for the top scored leads.

Writes the canonical review queue to ``business/_data/outreach_review_queue.json``
and a compatibility export to ``business/persuasion/exports``.

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
CANONICAL_QUEUE_PATH = REPO_ROOT / "business" / "_data" / "outreach_review_queue.json"
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
REVIEW_STATUS = "draft_pending_human_review"
LEGACY_REVIEW_STATUS = "pending_review"
PENDING_REVIEW_STATUSES = {None, REVIEW_STATUS, LEGACY_REVIEW_STATUS}

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


def build_draft(
    account: dict,
    language: str,
    channel: str,
    generated_at: str | None = None,
) -> dict:
    company = account.get("name") or account.get("id", "unknown")
    segment = account.get("segment", "")
    body = (AR_BODY if language == "ar" else EN_BODY).format(
        company=company,
        segment=segment,
    )
    account_id = str(account.get("id", ""))
    timestamp = generated_at or dt.datetime.now(dt.UTC).isoformat().replace("+00:00", "Z")
    draft_id = f"draft-{account_id}-{language}"
    return {
        "id": draft_id,
        "draftId": draft_id,
        "accountId": account_id,
        "company": company,
        "language": language,
        "channel": channel,
        "subject": None,
        "body": body,
        "createdAt": timestamp,
        "reviewStatus": REVIEW_STATUS,
        "reviewer": None,
        "reviewedAt": None,
        "decidedAt": None,
        "rejectionReason": None,
        "demo": bool(account.get("demo", True)),
        "disclaimer": DISCLAIMER,
        "safetyFlags": [
            "no_roi_claim",
            "no_fake_testimonial",
            "no_pressure",
            "human_review_required",
        ],
    }


def _draft_identifier(draft: dict) -> str:
    return str(draft.get("draftId") or draft.get("id") or "")


def _preserved_decision(record: dict, identifier: str) -> dict:
    preserved = dict(record)
    preserved.setdefault("id", identifier)
    preserved.setdefault("draftId", identifier)
    return preserved


def _merge_existing_decisions(drafts: list[dict]) -> list[dict]:
    """Preserve decided records instead of resetting human review on refresh.

    Pending records may be regenerated from current source data. A decided record is
    retained in full so changed copy cannot inherit an earlier approval implicitly.
    Decided records that fall outside the refreshed top-N input remain in the queue as
    immutable review evidence.
    """
    if not CANONICAL_QUEUE_PATH.exists():
        return drafts

    try:
        existing_payload = json.loads(CANONICAL_QUEUE_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return drafts

    existing_by_id = {
        identifier: record
        for record in existing_payload.get("drafts", [])
        if isinstance(record, dict) and (identifier := _draft_identifier(record))
    }

    merged: list[dict] = []
    generated_ids: set[str] = set()
    for draft in drafts:
        identifier = _draft_identifier(draft)
        generated_ids.add(identifier)
        existing = existing_by_id.get(identifier)
        if existing and existing.get("reviewStatus") not in PENDING_REVIEW_STATUSES:
            merged.append(_preserved_decision(existing, identifier))
        else:
            merged.append(draft)

    for identifier, existing in existing_by_id.items():
        if identifier in generated_ids:
            continue
        if existing.get("reviewStatus") in PENDING_REVIEW_STATUSES:
            continue
        merged.append(_preserved_decision(existing, identifier))

    return merged


def _compatibility_draft(draft: dict) -> dict:
    """Preserve the previous snake_case contract without making it canonical."""
    return {
        "account_id": draft["accountId"],
        "company": draft["company"],
        "language": draft["language"],
        "channel": draft["channel"],
        "subject": draft["subject"],
        "body": draft["body"],
        "review_status": LEGACY_REVIEW_STATUS,
        "generated_at": draft["createdAt"],
        "disclaimer": draft["disclaimer"],
    }


def write_outputs(
    drafts: list[dict],
    mode: str,
    date: dt.date | None = None,
) -> tuple[Path, Path]:
    today = (date or dt.date.today()).isoformat()
    CANONICAL_QUEUE_PATH.parent.mkdir(parents=True, exist_ok=True)
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    governed_drafts = _merge_existing_decisions(drafts)
    canonical_payload = {
        "version": "1.2",
        "mode": mode,
        "notice": "Draft only. Human approval is required before any external send.",
        "drafts": governed_drafts,
    }
    CANONICAL_QUEUE_PATH.write_text(
        json.dumps(canonical_payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    compatibility_path = EXPORT_DIR / f"outreach-drafts-{today}.json"
    compatibility_path.write_text(
        json.dumps(
            [_compatibility_draft(draft) for draft in governed_drafts],
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return CANONICAL_QUEUE_PATH, compatibility_path


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
    drafts = [
        build_draft(account, language, args.channel)
        for account in accounts
        for language in languages
    ]
    canonical_path, compatibility_path = write_outputs(drafts, args.mode)
    print(f"wrote {len(drafts)} governed drafts to {canonical_path} (mode={args.mode})")
    print(f"wrote compatibility export to {compatibility_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
