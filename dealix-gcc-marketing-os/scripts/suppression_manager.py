"""
Suppression list manager — prevents re-contacting opted-out or bounced contacts.
"""

from __future__ import annotations
import json
from pathlib import Path

MEMORY_DIR = Path(__file__).parent.parent / "memory"
SUPPRESSION_FILE = MEMORY_DIR / "suppression.jsonl"


def load_suppression_set() -> set[str]:
    """Load all suppressed email addresses from the JSONL store."""
    if not SUPPRESSION_FILE.exists():
        return set()
    emails: set[str] = set()
    with open(SUPPRESSION_FILE) as f:
        for line in f:
            if line.strip():
                record = json.loads(line)
                email = record.get("email", "").lower().strip()
                if email:
                    emails.add(email)
    return emails


def add_to_suppression(email: str, reason: str, source: str = "manual") -> None:
    """Append an email address to the suppression list with reason and source."""
    SUPPRESSION_FILE.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "email": email.lower().strip(),
        "reason": reason,
        "source": source,
        "added_at": __import__("datetime").datetime.utcnow().isoformat(),
    }
    with open(SUPPRESSION_FILE, "a") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def is_suppressed(email: str) -> bool:
    """Return True if the given email is in the suppression list."""
    return email.lower().strip() in load_suppression_set()


def filter_drafts(drafts: list[dict]) -> tuple[list[dict], list[dict]]:
    """Split drafts into (clean, blocked) based on suppression list."""
    suppressed = load_suppression_set()
    clean, blocked = [], []
    for draft in drafts:
        email = draft.get("contact_email", "").lower().strip()
        if email and email in suppressed:
            draft["suppression_blocked"] = True
            blocked.append(draft)
        else:
            clean.append(draft)
    return clean, blocked
