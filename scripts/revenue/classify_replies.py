#!/usr/bin/env python3
"""
Classify replies from a simple CSV (company, email, body) into categories.
This is a deterministic rule-based classifier; no LLM required.
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.revenue._lib import REPO_ROOT, today_str, write_csv


def classify(body: str) -> dict[str, str]:
    text = body.lower()

    # Stop / opt-out detection
    if re.search(r"\b(stop|إيقاف|إلغاء|unsubscribe|لا ترغب|remove|احذف)\b", text):
        return {"category": "opt_out", "sentiment": "negative", "next_action": "remove_from_queue"}

    # Positive signals
    positive = ["مهتم", "تواصل", "موافق", "ابدأ", "كلفة", "سعر", "تفاصيل", "interested", "yes", "ok", "details", "price"]
    if any(p in text for p in positive):
        return {"category": "interest", "sentiment": "positive", "next_action": "send_proposal"}

    # Questions
    questions = ["؟", "?", "ما هو", "كيف", "لماذا", "what is", "how", "why"]
    if any(q in text for q in questions):
        return {"category": "question", "sentiment": "neutral", "next_action": "answer_question"}

    # Negative
    negative = ["لا", "غير", "ليس", "مش", "not", "no", "busy"]
    if any(n in text for n in negative):
        return {"category": "not_interested", "sentiment": "negative", "next_action": "close_lost"}

    return {"category": "unknown", "sentiment": "neutral", "next_action": "manual_review"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Classify replies")
    parser.add_argument("--input", required=True, help="CSV with columns company,email,body")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    input_path = REPO_ROOT / args.input
    if not input_path.exists():
        print(f"Missing input: {input_path}")
        return 1

    rows: list[dict[str, str]] = []
    with input_path.open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            result = classify(row.get("body", ""))
            row["category"] = result["category"]
            row["sentiment"] = result["sentiment"]
            row["next_action"] = result["next_action"]
            row["classified_at"] = today_str()
            rows.append(row)

    output_path = REPO_ROOT / args.output if args.output else REPO_ROOT / "ledgers" / "reply_log.csv"
    if rows:
        write_csv(output_path, rows, list(rows[0].keys()))
    print(f"Classified {len(rows)} replies → {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
