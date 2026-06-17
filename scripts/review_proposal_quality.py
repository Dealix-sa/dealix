#!/usr/bin/env python3
"""
Dealix Proposal Quality Reviewer
Checks latest generated proposal for required sections.
"""

import argparse
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--latest", action="store_true")
    parser.add_argument("--path", default=None)
    args = parser.parse_args()

    if args.path:
        prop_path = Path(args.path)
    else:
        gen_dir = REPO / "business" / "proposals" / "generated"
        if not gen_dir.exists():
            print("[FAIL] No generated proposals found.")
            return
        files = sorted(gen_dir.glob("proposal-*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
        if not files:
            print("[FAIL] No proposal files.")
            return
        prop_path = files[0]

    prop = json.loads(prop_path.read_text(encoding="utf-8"))
    required = [
        "executive_summary",
        "client_situation_hypothesis",
        "scope",
        "deliverables",
        "implementation_timeline",
        "governance",
        "proof_plan",
        "client_responsibilities",
        "exclusions",
        "pricing",
        "next_step",
        "signature_placeholder",
    ]
    missing = [k for k in required if k not in prop]
    if missing:
        print(f"[FAIL] Missing sections in {prop_path}: {missing}")
    else:
        print(f"[PASS] Proposal quality check passed for {prop_path}")
        print(f"  Account: {prop['meta']['account_id']}")
        print(f"  Offer: {prop['meta']['offer']}")
        print(f"  Review status: {prop['meta']['review_status']}")

if __name__ == "__main__":
    main()
