#!/usr/bin/env python3
"""Generate guardrailed negotiation drafts from classified replies."""
from __future__ import annotations

from _common import DATA_DIR, dump, load_json

from app.commercial import negotiation_desk, reply_classifier


def main() -> int:
    records = load_json(DATA_DIR / "replies.sample.json", key="replies")
    replies = reply_classifier.classify_replies(records)
    drafts = negotiation_desk.build_negotiation_drafts(replies)
    dump({"negotiation_drafts": [d.to_dict() for d in drafts], "count": len(drafts)})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
