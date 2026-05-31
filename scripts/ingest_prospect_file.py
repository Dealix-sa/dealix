#!/usr/bin/env python3
"""Ingest a prospect CSV/XLSX file → research briefs + 3-touch sequences.

For each row in the file:
  1. Validate required columns (name_ar, name_en, company, sector_hint)
  2. Normalize sector via sector_registry.normalize_hint()
  3. Generate Source Passport (Doctrine #5)
  4. Generate research brief via research_prospect.build_brief()
  5. Generate 3-touch sequence via personalized_outreach.generate_sequence()
  6. Stage everything in data/prospect_briefs/ with batch_id

All output is DRAFT only. Founder approves via approval_center.
No autonomous send. No bulk-approve allowed (Doctrine #1).

Usage:
    python scripts/ingest_prospect_file.py --file prospects.csv --dry-run
    python scripts/ingest_prospect_file.py --file prospects.csv
    python scripts/ingest_prospect_file.py --file prospects.xlsx --channel email
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import uuid
from datetime import UTC, datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

OUTPUT_DIR = REPO / "data" / "prospect_briefs"
LOG_PATH = REPO / "data" / "prospect_ingestion_log.jsonl"

REQUIRED_COLUMNS = ("name_ar", "name_en", "company", "sector_hint")
ALL_COLUMNS = REQUIRED_COLUMNS + (
    "title",
    "linkedin_url",
    "email",
    "phone",
    "referrer_name",
    "warm_consent_yes_no",
    "notes",
    "priority_hint",
)

MAX_ROWS = 500
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_RE = re.compile(r"^\+\d{8,15}$")
LINKEDIN_RE = re.compile(r"^https?://(www\.)?linkedin\.com/in/[A-Za-z0-9_-]+/?$")


def _make_batch_id() -> str:
    return f"BATCH_{uuid.uuid4().hex[:10]}"


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def _read_xlsx(path: Path) -> list[dict]:
    try:
        import openpyxl  # type: ignore[import-untyped]
    except ImportError:
        sys.stderr.write("FATAL: openpyxl required for XLSX. `pip install openpyxl`.\n")
        sys.exit(2)
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    sheet = wb.active
    rows_iter = sheet.iter_rows(values_only=True)
    header = [str(h or "").strip() for h in next(rows_iter)]
    out = []
    for row in rows_iter:
        out.append({header[i]: (str(v) if v is not None else "") for i, v in enumerate(row[: len(header)])})
    return out


def _validate_row(row: dict, row_n: int) -> list[str]:
    errors = []
    for col in REQUIRED_COLUMNS:
        if not row.get(col, "").strip():
            errors.append(f"row {row_n}: missing required column '{col}'")
    li = row.get("linkedin_url", "").strip()
    if li and not LINKEDIN_RE.match(li):
        errors.append(f"row {row_n}: invalid linkedin_url format")
    email = row.get("email", "").strip()
    if email and not EMAIL_RE.match(email):
        errors.append(f"row {row_n}: invalid email format")
    phone = row.get("phone", "").strip()
    if phone and not PHONE_RE.match(phone):
        errors.append(f"row {row_n}: phone must be E.164 (+966...)")
    return errors


def _process_row(row: dict, batch_id: str, channel: str | None) -> dict:
    """Process one validated row → brief + sequence."""
    from scripts.research_prospect import build_brief, render_markdown  # type: ignore[attr-defined]

    brief = build_brief(
        name=row["name_ar"] or row["name_en"],
        company=row["company"],
        sector_hint=row["sector_hint"],
        linkedin_url=row.get("linkedin_url") or None,
        email=row.get("email") or None,
        phone=row.get("phone") or None,
        notes=row.get("notes") or "",
    )
    brief["ingestion"] = {
        "batch_id": batch_id,
        "ingested_at": _now_iso(),
        "row_data": row,
        "doctrine_lawful_basis": "legitimate_interest (founder-provided list)",
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    json_path = OUTPUT_DIR / f"{brief['brief_id']}.json"
    md_path = OUTPUT_DIR / f"{brief['brief_id']}.md"
    json_path.write_text(json.dumps(brief, indent=2, ensure_ascii=False), encoding="utf-8")
    md_path.write_text(render_markdown(brief), encoding="utf-8")

    # Sequence generation
    warm = (row.get("warm_consent_yes_no", "").strip().lower() == "yes")
    chan = channel or ("linkedin_dm" if row.get("linkedin_url") else "email")

    sequence_data = {
        "brief_id": brief["brief_id"],
        "channel": chan,
        "warm_consent": warm,
        "touches": [],
        "note": "Drafts queued separately in approval_center. Founder approves each.",
    }

    try:
        from auto_client_acquisition.agents.personalized_outreach import (
            generate_sequence,
        )
        drafts = generate_sequence(
            prospect_brief=brief,
            channel=chan,
            warm_consent=warm,
        )
        sequence_data["touches"] = [d.to_dict() for d in drafts]
    except Exception as exc:
        sequence_data["error"] = (
            f"sequence generation deferred: {type(exc).__name__}: {exc}"
        )

    seq_path = OUTPUT_DIR / f"{brief['brief_id']}_sequence.json"
    seq_path.write_text(json.dumps(sequence_data, indent=2, ensure_ascii=False), encoding="utf-8")

    return {
        "brief_id": brief["brief_id"],
        "name_en": row["name_en"],
        "company": row["company"],
        "sector_code": brief["identity"]["sector_code"],
        "icp_score": brief["icp_fit"]["score"],
        "channel": chan,
        "touches_generated": len(sequence_data["touches"]),
        "files": {
            "brief_md": str(md_path.relative_to(REPO)),
            "brief_json": str(json_path.relative_to(REPO)),
            "sequence_json": str(seq_path.relative_to(REPO)),
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True, type=Path)
    ap.add_argument(
        "--channel",
        choices=["linkedin_dm", "email", "whatsapp_warm"],
        help="Override default channel (auto: linkedin_dm if URL present else email)",
    )
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not args.file.is_file():
        sys.stderr.write(f"FATAL: file not found: {args.file}\n")
        return 2

    rows = _read_csv(args.file) if args.file.suffix.lower() == ".csv" else _read_xlsx(args.file)

    if len(rows) > MAX_ROWS:
        sys.stderr.write(
            f"FATAL: {len(rows)} rows exceeds MAX_ROWS={MAX_ROWS}. "
            "Split the file into smaller batches.\n"
        )
        return 2

    # Validate all rows first; fail fast on errors
    errors: list[str] = []
    for i, row in enumerate(rows, start=2):  # row 1 = header
        errors.extend(_validate_row(row, i))
    if errors:
        sys.stderr.write("VALIDATION FAILED:\n")
        for e in errors[:20]:
            sys.stderr.write(f"  {e}\n")
        if len(errors) > 20:
            sys.stderr.write(f"  ... and {len(errors) - 20} more errors\n")
        return 1

    batch_id = _make_batch_id()
    summary = {
        "batch_id": batch_id,
        "file": str(args.file.name),
        "rows_total": len(rows),
        "started_at": _now_iso(),
        "rows": [] if args.dry_run else [],
    }

    if args.dry_run:
        summary["rows"] = [
            {
                "name_en": r["name_en"],
                "company": r["company"],
                "sector_hint": r["sector_hint"],
            }
            for r in rows
        ]
        summary["dry_run"] = True
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        print(f"\nDry-run OK: {len(rows)} rows valid. Re-run without --dry-run to ingest.")
        return 0

    # Live ingestion
    print(f"Batch {batch_id} starting: {len(rows)} rows")
    for i, row in enumerate(rows, start=1):
        result = _process_row(row, batch_id, args.channel)
        summary["rows"].append(result)
        print(
            f"  [{i}/{len(rows)}] {result['name_en']} ({result['company']}) → "
            f"{result['brief_id']} (ICP {result['icp_score']}, "
            f"{result['touches_generated']} touches)"
        )

    summary["completed_at"] = _now_iso()
    summary["doctrine_attestation"] = [
        "Doctrine #1: all touches DRAFT only — founder approval required per send",
        "Doctrine #2: whatsapp_warm requires warm_consent_yes_no=yes per row",
        "Doctrine #3: no scraping; founder-provided list (legitimate interest)",
        "Doctrine #5: Source Passport recorded per row with 90-day expiry",
        "Doctrine #10: every ingestion appended to data/prospect_ingestion_log.jsonl",
    ]

    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(summary, ensure_ascii=False) + "\n")

    print(f"\nOK: batch {batch_id} complete.")
    print(f"Log: {LOG_PATH.relative_to(REPO)}")
    print(f"Next: open approval_center filtered by batch_id={batch_id}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
