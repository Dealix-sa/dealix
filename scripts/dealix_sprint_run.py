#!/usr/bin/env python3
"""Dealix Sprint Runner — deliver the 499 SAR 7-Day Revenue Intelligence
Sprint from the command line, no server required.

Wraps the existing, already-tested orchestrator
(``auto_client_acquisition.delivery_factory.delivery_sprint.run_sprint``)
and the Proof Pack renderers so the founder can run rung 1 of the
commercial ladder end to end from a local CSV/JSON file. Pure local
generation — NO LLM call, NO live send, NO scraping, NO network calls.
This script only ever reads founder-supplied local files and writes
local output files / prints to stdout.

Usage:
    python scripts/dealix_sprint_run.py \\
        --engagement-id <engagement_id> \\
        --customer-id <customer_id> \\
        --csv path/to/customer_accounts.csv \\
        --source-passport-json path/to/passport.json \\
        --problem-summary "Which dormant accounts are worth reviving first?"

    # Inspect the full run record as JSON (no files written):
    python scripts/dealix_sprint_run.py \\
        --engagement-id <engagement_id> --customer-id <customer_id> --json

Every output is a local file under --out-dir (default out/sprints/<id>/)
plus a stdout summary. Founder review is required before any
customer-facing send — this script never emails, WhatsApps, or POSTs
anything anywhere.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from auto_client_acquisition.delivery_factory.delivery_sprint import run_sprint
from auto_client_acquisition.proof_architecture_os.proof_pack_render import (
    proof_pack_email_body,
    proof_pack_to_markdown,
    proof_pack_to_pdf,
)

_DELIVERY_THRESHOLD = 70  # docs/03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md exit criteria


def _load_json_file(path: str | None) -> Any:
    if not path:
        return None
    text = Path(path).read_text(encoding="utf-8")
    return json.loads(text)


def _accounts_from_csv_text(raw: str) -> list[dict[str, Any]]:
    if not raw:
        return []
    reader = csv.DictReader(raw.splitlines())
    return list(reader)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description=(
            "Run the 7-Day Revenue Intelligence Sprint orchestrator locally "
            "and write the Proof Pack + run record to disk. No external "
            "send of any kind."
        ),
    )
    p.add_argument("--engagement-id", required=True, help="engagement identifier, e.g. <engagement_id>")
    p.add_argument("--customer-id", required=True, help="internal customer/account identifier")
    p.add_argument("--csv", help="path to a local customer relationship CSV file")
    p.add_argument(
        "--accounts-json",
        help="path to a JSON file with a list of account dicts (takes precedence over --csv for scoring)",
    )
    p.add_argument(
        "--source-passport-json",
        help="path to a JSON file with the SourcePassport dict (owner, source_type, allowed_use, ...)",
    )
    p.add_argument("--problem-summary", default="", help="one-line business question for this sprint")
    p.add_argument(
        "--workflow-owner-present",
        dest="workflow_owner_present",
        action="store_true",
        default=True,
        help="a named client-side workflow owner is confirmed (default: true)",
    )
    p.add_argument(
        "--no-workflow-owner-present",
        dest="workflow_owner_present",
        action="store_false",
        help="no named client-side workflow owner has been confirmed",
    )
    p.add_argument(
        "--out-dir",
        default=None,
        help="directory to write outputs into (default: out/sprints/<engagement-id>/)",
    )
    p.add_argument(
        "--json",
        action="store_true",
        help="print the full run record as JSON to stdout instead of writing files",
    )
    args = p.parse_args(argv)

    raw_csv = ""
    if args.csv:
        raw_csv = Path(args.csv).read_text(encoding="utf-8")

    accounts: list[dict[str, Any]] | None = None
    if args.accounts_json:
        accounts = _load_json_file(args.accounts_json)
    elif args.csv:
        accounts = _accounts_from_csv_text(raw_csv)

    source_passport = _load_json_file(args.source_passport_json)
    if source_passport is None:
        print(
            "WARNING: no --source-passport-json supplied. The SOP requires a "
            "signed Source Passport before Day 1 truly starts with a client. "
            "Proceeding with a dry run only — this is not a substitute for a "
            "real, founder-approved Source Passport.",
            file=sys.stderr,
        )

    run = run_sprint(
        engagement_id=args.engagement_id,
        customer_id=args.customer_id,
        source_passport=source_passport,
        raw_csv=raw_csv,
        accounts=accounts,
        problem_summary=args.problem_summary,
        workflow_owner_present=args.workflow_owner_present,
    )

    if args.json:
        print(json.dumps(run.to_dict(), indent=2, ensure_ascii=False, default=str))
        return 0

    out_dir = Path(args.out_dir) if args.out_dir else REPO_ROOT / "out" / "sprints" / args.engagement_id
    out_dir.mkdir(parents=True, exist_ok=True)

    pack = run.proof_pack or {}
    md = proof_pack_to_markdown(pack, customer_handle=args.customer_id)
    email_body = proof_pack_email_body(pack, customer_handle=args.customer_id)
    pdf_bytes = proof_pack_to_pdf(pack, customer_handle=args.customer_id)

    md_path = out_dir / "proof_pack.md"
    email_path = out_dir / "email_cover_note.txt"
    record_path = out_dir / "run_record.json"

    md_path.write_text(md, encoding="utf-8")
    email_path.write_text(email_body, encoding="utf-8")
    record_path.write_text(
        json.dumps(run.to_dict(), indent=2, ensure_ascii=False, default=str),
        encoding="utf-8",
    )

    written_paths = [md_path, email_path, record_path]
    pdf_path = out_dir / "proof_pack.pdf"
    if pdf_bytes is not None:
        pdf_path.write_bytes(pdf_bytes)
        written_paths.append(pdf_path)

    lines: list[str] = []
    lines.append(f"Dealix Sprint run — engagement: {args.engagement_id}")
    lines.append("")

    if run.governance_decision != "allow_with_review":
        lines.append(f"NEEDS REVIEW: governance_decision = {run.governance_decision!r}")
    if run.proof_score < _DELIVERY_THRESHOLD:
        lines.append(
            "BELOW DELIVERY THRESHOLD (proof_score < 70) — do not hand this "
            "off to the client yet."
        )
    if run.governance_decision != "allow_with_review" or run.proof_score < _DELIVERY_THRESHOLD:
        lines.append("")

    lines.append(f"customer_id: {args.customer_id}")
    lines.append(f"proof_score: {run.proof_score}")
    lines.append(f"proof_tier: {run.proof_tier}")
    lines.append(f"governance_decision: {run.governance_decision}")
    lines.append(f"retainer_eligible: {run.retainer_eligible}")
    lines.append(f"capital_assets_registered: {len(run.capital_assets_registered)}")
    lines.append("")

    if pdf_bytes is None:
        lines.append("(no PDF renderer available in this environment — proof_pack.pdf was not written)")

    lines.append("Files written:")
    for path in written_paths:
        lines.append(f"  - {path}")
    lines.append("")
    lines.append(
        "Founder review required before any customer-facing send — no "
        "external message has been sent by this script."
    )

    print("\n".join(lines))
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
