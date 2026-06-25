#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "data" / "commercial" / "lead_pipeline.csv"
FIELDS = [
    "company_name",
    "sector",
    "city",
    "website",
    "source_url",
    "contact_channel",
    "pain_hypothesis",
    "recommended_offer",
    "stage",
    "next_action",
    "owner_decision",
    "notes",
]


def row_id(row: dict[str, str]) -> str:
    website = (row.get("website") or "").strip().lower().rstrip("/")
    name = (row.get("company_name") or "").strip().lower()
    return website or name


def clean(row: dict[str, str]) -> dict[str, str]:
    out = {field: (row.get(field) or "").strip() for field in FIELDS}
    out["city"] = out["city"] or "Riyadh"
    out["source_url"] = out["source_url"] or out["website"] or "manual_review_required"
    out["contact_channel"] = out["contact_channel"] or "manual_review"
    out["stage"] = out["stage"] or "research"
    out["next_action"] = out["next_action"] or "review source"
    out["owner_decision"] = out["owner_decision"] or "review"
    out["notes"] = out["notes"] or "imported research account"
    return out


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path")
    args = parser.parse_args()

    current = [clean(row) for row in read_csv(TARGET)]
    incoming = [clean(row) for row in read_csv(Path(args.csv_path))]
    seen = {row_id(row) for row in current if row_id(row)}
    added = 0
    for row in incoming:
        ident = row_id(row)
        if not ident or ident in seen:
            continue
        current.append(row)
        seen.add(ident)
        added += 1
    write_csv(TARGET, current)
    print(f"ACCOUNTS_IMPORTED={added}")
    print(f"TOTAL_ACCOUNTS={len(current)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
