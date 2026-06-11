#!/usr/bin/env python3
"""
Dealix Outreach Draft Generator
Generates draft messages for WhatsApp/email in Arabic and English.
Never sends. All drafts have review_status = pending_review.
"""

import argparse
import json
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

def load_json(path: Path):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}

def generate_draft(account: dict, language: str, channel: str) -> dict:
    name = account.get("name", "there")
    company = account.get("company", "your company")
    sector = account.get("sector", "your industry")
    if language == "ar":
        body = (
            f"مرحباً {name}،\n\n"
            f"لاحظنا أن {company} في قطاع {sector} ينمو بشكل جيد. "
            f"نرى فرصة لتحويل العمليات اليومية إلى نظام تشغيلي قابل للقياس.\n\n"
            f"هل لديك ١٥ دقيقة هذا الأسبوع لمراجعة سريعة؟"
        )
    else:
        body = (
            f"Hi {name},\n\n"
            f"We noticed {company} is growing well in {sector}. "
            f"We see an opportunity to turn daily operations into a measurable operating system.\n\n"
            f"Do you have 15 minutes this week for a quick review?"
        )
    return {
        "account_id": account.get("id"),
        "company": company,
        "language": language,
        "channel": channel,
        "subject": f"Dealix — {sector} operating system" if channel == "email" else None,
        "body": body,
        "review_status": "pending_review",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "disclaimer": "DRAFT — Do not send without human review.",
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--top", type=int, default=10)
    parser.add_argument("--language", choices=["ar", "en", "both"], default="both")
    parser.add_argument("--channel", choices=["whatsapp", "email", "both"], default="whatsapp")
    parser.add_argument("--mode", choices=["demo", "production"], default="demo")
    parser.add_argument("--input", default=None)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    if args.mode == "demo":
        accounts = [
            {"id": "demo-001", "name": "Ahmed", "company": "Acme Saudi", "sector": "B2B Services"},
            {"id": "demo-002", "name": "Sara", "company": "Beta Clinic", "sector": "Healthcare"},
            {"id": "demo-003", "name": "Khalid", "company": "Gamma Logistics", "sector": "Logistics"},
        ]
    else:
        inp = Path(args.input) if args.input else REPO / "business" / "crm" / "exports" / "leads-scored.json"
        if not inp.exists():
            print("[FAIL] No input leads for production mode.")
            return
        data = json.loads(inp.read_text(encoding="utf-8"))
        accounts = data if isinstance(data, list) else data.get("leads", [])

    accounts = accounts[:args.top]
    languages = ["ar", "en"] if args.language == "both" else [args.language]
    channels = ["whatsapp", "email"] if args.channel == "both" else [args.channel]

    drafts = []
    for acc in accounts:
        for lang in languages:
            for ch in channels:
                drafts.append(generate_draft(acc, lang, ch))

    out_path = Path(args.output) if args.output else REPO / "business" / "persuasion" / "exports" / f"outreach-drafts-{datetime.utcnow().strftime('%Y-%m-%d')}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(drafts, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[PASS] Generated {len(drafts)} drafts. Output: {out_path}")
    for d in drafts:
        print(f"  {d['account_id']} {d['language']} {d['channel']} -> {d['review_status']}")

if __name__ == "__main__":
    main()
