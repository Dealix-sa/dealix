"""
Reply processor — classifies inbound replies and updates learning log.
"""

from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path

MEMORY_DIR = Path(__file__).parent.parent / "memory"


REPLY_CATEGORIES = {
    "positive_interested": [
        "نعم", "يناسبنا", "نحن مهتمون", "أرسل", "تفضل",
        "yes", "interested", "send", "please share", "sounds good", "tell me more",
    ],
    "soft_no_timing": [
        "مشغولين", "مو وقت", "لاحقًا", "بعدين",
        "not now", "busy", "later", "next quarter", "maybe later",
    ],
    "hard_no": [
        "لا نحتاج", "غير مناسب", "مو مهتمين",
        "not interested", "please remove", "unsubscribe", "stop",
    ],
    "referral": [
        "تواصل مع", "كلم",
        "speak to", "contact", "you should talk to",
    ],
    "bounce_permanent": [],
    "bounce_temporary": [],
    "auto_reply": ["out of office", "on leave", "vacation", "auto-reply"],
    "question": ["?", "ما هو", "كيف", "what is", "how does", "can you"],
}


def classify_reply(reply_text: str) -> str:
    """Classify an inbound reply body into one of the known reply categories."""
    text = reply_text.lower()
    for category, signals in REPLY_CATEGORIES.items():
        if any(signal in text for signal in signals):
            return category
    return "unclassified"


def process_reply(reply: dict) -> dict:
    """Process an inbound reply dict: classify, suppress opt-outs, and write to logs."""
    body = reply.get("body", "")
    category = classify_reply(body)
    reply["category"] = category
    reply["processed_at"] = datetime.now(timezone.utc).isoformat()

    if category == "hard_no":
        from suppression_manager import add_to_suppression
        email = reply.get("from_email", "")
        if email:
            add_to_suppression(email, reason="opt_out_reply", source="reply_processor")

    log_path = MEMORY_DIR / "learning_log.jsonl"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a") as f:
        f.write(json.dumps({
            "type": "reply",
            "company": reply.get("company"),
            "sector": reply.get("sector"),
            "angle": reply.get("angle"),
            "language": reply.get("language"),
            "category": category,
            "draft_id": reply.get("draft_id"),
        }, ensure_ascii=False) + "\n")

    replies_path = MEMORY_DIR / "replies.jsonl"
    with open(replies_path, "a") as f:
        f.write(json.dumps(reply, ensure_ascii=False) + "\n")

    return reply
