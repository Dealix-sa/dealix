#!/usr/bin/env python3
"""
Commercial Safety Audit — verifies every draft is review-only and compliant.

Fails (exit 1) if ANY draft:
  - is missing/false the forced safety flags (send must be blocked), or
  - contains a banned phrase (guaranteed ROI, scraping, auto-send, etc.).
Writes safety_audit.json to today's output dir.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from v5.lib import BANNED_PHRASES, out_dir  # noqa: E402

REQUIRED_FLAGS = {
    "send_allowed": False,
    "external_send_blocked": True,
    "requires_founder_approval": True,
    "no_auto_send": True,
}


def audit(date: str | None = None) -> dict:
    d = out_dir(date)
    queue = d / "draft_queue.jsonl"
    if not queue.exists():
        return {"ok": False, "error": "draft_queue.jsonl not found — run the draft factory first"}

    total = 0
    flag_violations: list[str] = []
    phrase_violations: list[str] = []
    for line in queue.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        dr = json.loads(line)
        total += 1
        for k, expected in REQUIRED_FLAGS.items():
            if dr.get(k) != expected:
                flag_violations.append(f"{dr.get('draft_id')}: {k}={dr.get(k)} (expected {expected})")
        text = f"{dr.get('subject','')} {dr.get('body','')} {dr.get('cta','')}".lower()
        if dr.get("opt_out", "") == "":
            phrase_violations.append(f"{dr.get('draft_id')}: missing opt_out")
        for banned in BANNED_PHRASES:
            if banned in text:
                phrase_violations.append(f"{dr.get('draft_id')}: banned phrase '{banned}'")

    ok = not flag_violations and not phrase_violations
    result = {
        "ok": ok,
        "date": date or d.name,
        "total_drafts": total,
        "flag_violations": flag_violations[:50],
        "phrase_violations": phrase_violations[:50],
        "flag_violation_count": len(flag_violations),
        "phrase_violation_count": len(phrase_violations),
        "invariant": "the system never sends externally",
    }
    (d / "safety_audit.json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    return result


def main() -> int:
    r = audit()
    print(json.dumps({k: r[k] for k in ("ok", "total_drafts", "flag_violation_count", "phrase_violation_count") if k in r}, indent=2))
    return 0 if r.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
