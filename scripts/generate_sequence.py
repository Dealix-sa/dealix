#!/usr/bin/env python3
"""Generate a 3-touch outreach sequence for a prospect brief.

Reads brief from data/prospect_briefs/{brief_id}.json, calls
personalized_outreach.generate_sequence(), writes drafts to
data/prospect_briefs/{brief_id}_sequence.json.

Doctrine:
  - Each touch is a DRAFT — queued in approval_center separately
  - Founder approves per-touch (no bulk-approve allowed)
  - Doctrine #2: cold WhatsApp blocked at agent level

Usage:
    python scripts/generate_sequence.py --brief-id prospect_abc123 --channel linkedin_dm
    python scripts/generate_sequence.py --brief-id prospect_abc123 --channel whatsapp_warm --warm-consent
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

BRIEF_DIR = REPO / "data" / "prospect_briefs"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--brief-id", required=True)
    ap.add_argument(
        "--channel",
        required=True,
        choices=["linkedin_dm", "email", "whatsapp_warm"],
    )
    ap.add_argument("--warm-consent", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    brief_path = BRIEF_DIR / f"{args.brief_id}.json"
    if not brief_path.is_file():
        sys.stderr.write(f"FATAL: brief not found at {brief_path}\n")
        return 2

    try:
        brief = json.loads(brief_path.read_text(encoding="utf-8"))
    except Exception as exc:
        sys.stderr.write(f"FATAL: cannot parse brief: {exc}\n")
        return 2

    try:
        from auto_client_acquisition.agents.personalized_outreach import (
            generate_sequence,
        )
    except Exception as exc:
        sys.stderr.write(
            f"FATAL: cannot import personalized_outreach: {exc}\n"
            "Try `pip install -e .[dev]` first.\n"
        )
        return 2

    drafts = generate_sequence(
        prospect_brief=brief,
        channel=args.channel,
        warm_consent=args.warm_consent,
    )

    if not drafts:
        sys.stderr.write(
            "WARN: no drafts generated. Possible reasons:\n"
            "  - Cold WhatsApp blocked (Doctrine #2 — pass --warm-consent if applicable)\n"
            "  - Voice anti-pattern matched (Doctrine #4)\n"
        )
        return 1

    out = {
        "brief_id": args.brief_id,
        "channel": args.channel,
        "touches": [d.to_dict() for d in drafts],
        "next_step": (
            "Founder reviews each touch in approval_center "
            "(/ar/ops/approvals?brief_id=" + args.brief_id + "). "
            "Approve / edit / reject per touch. NO bulk-approve."
        ),
    }

    if args.dry_run:
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return 0

    out_path = BRIEF_DIR / f"{args.brief_id}_sequence.json"
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"OK: wrote {out_path.relative_to(REPO)}")
    print(f"Generated {len(drafts)} drafts for {args.channel}.")
    for d in drafts:
        print(f"  - Touch {d.touch_n}: {d.draft_id}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
