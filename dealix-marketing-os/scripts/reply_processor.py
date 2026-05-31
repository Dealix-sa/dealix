"""Reply processor: classifies incoming replies and updates opportunity status."""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import uuid
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from dotenv import load_dotenv

load_dotenv(BASE_DIR.parent / ".env")

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)

MEMORY_DIR = BASE_DIR / "memory"
REPLIES_PATH = MEMORY_DIR / "replies.jsonl"
SUPPRESSION_PATH = MEMORY_DIR / "suppression.jsonl"
OPPORTUNITIES_PATH = MEMORY_DIR / "opportunities.jsonl"

REPLY_CLASSIFICATIONS = [
    "interested",
    "details_requested",
    "not_now",
    "wrong_person",
    "not_interested",
    "pricing",
    "security_concern",
    "opt_out",
]

NEXT_ACTIONS = {
    "interested": "Schedule discovery call immediately. Respond within 2 hours.",
    "details_requested": "Send one-pager or relevant case study. Follow up in 2 days.",
    "not_now": "Move to nurture. Schedule light-touch follow-up in 90 days.",
    "wrong_person": "Ask for referral to correct contact. Update buyer mapping.",
    "not_interested": "Log and suppress for 6 months. No further outreach.",
    "pricing": "Send pricing overview or schedule a discovery call to discuss.",
    "security_concern": "Escalate to founder. Prepare security briefing.",
    "opt_out": "Immediately add to suppression list. No further contact.",
}


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    records = []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return records


def rewrite_jsonl(path: Path, records: list[dict]) -> None:
    with open(path, "w") as fh:
        for rec in records:
            fh.write(json.dumps(rec) + "\n")


def classify_reply_via_claude(reply_text: str, company_name: str) -> dict | None:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        log.error("ANTHROPIC_API_KEY not set")
        return None

    import anthropic

    client = anthropic.Anthropic(api_key=api_key)

    classifications_str = " | ".join(REPLY_CLASSIFICATIONS)

    prompt = f"""You are a B2B reply classification engine.

Company: {company_name}
Reply text:
---
{reply_text}
---

Classify this reply into exactly one of these categories:
{classifications_str}

Also extract:
- key_signal: the main signal phrase from the reply
- sentiment: positive|neutral|negative
- urgency: low|medium|high

Return a JSON object:
{{
  "classification": "one of the categories above",
  "key_signal": "extracted phrase",
  "sentiment": "positive|neutral|negative",
  "urgency": "low|medium|high",
  "reasoning": "one sentence explanation"
}}

Return only valid JSON. No explanation."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = message.content[0].text.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return json.loads(raw)
    except Exception as exc:
        log.error("Reply classification failed: %s", exc)
        return None


def add_to_suppression(company_id: str, company_name: str, reason: str) -> None:
    record = {
        "id": f"supp-{uuid.uuid4().hex[:12]}",
        "company_id": company_id,
        "company_name": company_name,
        "reason": reason,
        "suppressed_at": datetime.utcnow().isoformat() + "Z",
    }
    with open(SUPPRESSION_PATH, "a") as fh:
        fh.write(json.dumps(record) + "\n")
    log.info("Added %s to suppression list", company_name)


def process_reply_record(reply_data: dict) -> None:
    company_id = reply_data.get("company_id", "")
    company_name = reply_data.get("company_name", "")
    reply_text = reply_data.get("reply_text", "")

    if not reply_text:
        log.error("No reply_text in reply data")
        return

    classification = classify_reply_via_claude(reply_text, company_name)
    if not classification:
        return

    reply_class = classification.get("classification", "not_interested")
    next_action = NEXT_ACTIONS.get(reply_class, "Review and determine next step.")

    reply_record = {
        "id": f"reply-{uuid.uuid4().hex[:12]}",
        "company_id": company_id,
        "company_name": company_name,
        "reply_text": reply_text,
        "classification": reply_class,
        "key_signal": classification.get("key_signal", ""),
        "sentiment": classification.get("sentiment", "neutral"),
        "urgency": classification.get("urgency", "low"),
        "reasoning": classification.get("reasoning", ""),
        "next_action": next_action,
        "received_at": reply_data.get("received_at", datetime.utcnow().isoformat() + "Z"),
        "processed_at": datetime.utcnow().isoformat() + "Z",
    }

    with open(REPLIES_PATH, "a") as fh:
        fh.write(json.dumps(reply_record) + "\n")

    if reply_class == "opt_out":
        add_to_suppression(company_id, company_name, "opt_out")

    opportunities = read_jsonl(OPPORTUNITIES_PATH)
    updated = False
    for opp in opportunities:
        if opp.get("company_id") == company_id or opp.get("id") == company_id:
            opp["reply_status"] = reply_class
            opp["last_reply_at"] = reply_record["processed_at"]
            if reply_class in ("not_interested", "opt_out"):
                opp["status"] = "closed_lost"
            elif reply_class == "interested":
                opp["status"] = "discovery_scheduled"
            updated = True
            break

    if updated:
        rewrite_jsonl(OPPORTUNITIES_PATH, opportunities)

    print(f"\nReply classified: {reply_class}")
    print(f"Key signal: {classification.get('key_signal', '')}")
    print(f"Sentiment: {classification.get('sentiment', '')}")
    print(f"Next action: {next_action}")


def interactive_mode() -> None:
    print("Reply Processor — Interactive Mode")
    print("Enter reply details (Ctrl+C to exit)")
    company_name = input("Company name: ").strip()
    company_id = input("Company ID (or press Enter to skip): ").strip() or f"manual-{uuid.uuid4().hex[:8]}"
    print("Paste reply text (press Enter twice when done):")
    lines = []
    while True:
        line = input()
        if line == "" and lines and lines[-1] == "":
            break
        lines.append(line)
    reply_text = "\n".join(lines).strip()

    reply_data = {
        "company_id": company_id,
        "company_name": company_name,
        "reply_text": reply_text,
        "received_at": datetime.utcnow().isoformat() + "Z",
    }
    process_reply_record(reply_data)


def run_from_file(reply_file: str) -> None:
    path = Path(reply_file)
    if not path.exists():
        log.error("Reply file not found: %s", reply_file)
        sys.exit(1)

    with open(path) as fh:
        reply_data = json.load(fh)

    if isinstance(reply_data, list):
        for item in reply_data:
            process_reply_record(item)
    else:
        process_reply_record(reply_data)


def main() -> None:
    parser = argparse.ArgumentParser(description="Process and classify incoming replies")
    parser.add_argument("--reply-file", help="Path to JSON file with reply data")
    parser.add_argument("--interactive", action="store_true", help="Enter reply interactively")
    args = parser.parse_args()

    if args.interactive:
        interactive_mode()
    elif args.reply_file:
        run_from_file(args.reply_file)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
