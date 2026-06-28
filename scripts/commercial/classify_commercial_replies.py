#!/usr/bin/env python3
"""Classify inbound replies into controlled reply types."""
from __future__ import annotations

from _common import DATA_DIR, dump, load_json

from app.commercial import reply_classifier


def main() -> int:
    records = load_json(DATA_DIR / "replies.sample.json", key="replies")
    classified = reply_classifier.classify_replies(records)
    dump({"replies": [r.to_dict() for r in classified], "count": len(classified)})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
