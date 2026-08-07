#!/usr/bin/env python3
"""Import a large XLSX company directory into governed targeting staging.

The original workbook is never modified. Raw email/phone values are never
stored by this importer; only masked values and optional keyed HMACs are kept.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from sqlalchemy import create_engine, delete, select
from sqlalchemy.orm import Session

from db.models import Base
from db.models_company_targeting import (
    CompanyDirectoryEntryRecord,
    CompanyDirectoryImportRecord,
)
from dealix.company_os.company_directory import analyze_company_directory


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Import a Saudi company XLSX into governed staging."
    )
    parser.add_argument("workbook", type=Path)
    parser.add_argument("--tenant-id", default="dealix")
    parser.add_argument("--sheet", default="داتا كاملة")
    parser.add_argument("--source-name", default="provided_saudi_company_directory")
    parser.add_argument(
        "--database-url",
        default="sqlite:///outputs/company_targeting/dealix_company_targeting.sqlite3",
    )
    parser.add_argument(
        "--analysis-json",
        type=Path,
        default=Path("outputs/company_targeting/company_directory_analysis.json"),
    )
    parser.add_argument(
        "--workbook-staging-json",
        type=Path,
        default=Path("outputs/company_targeting/company_targeting_workbook.json"),
    )
    parser.add_argument(
        "--source-terms-verified",
        action="store_true",
        help="Set only after documenting the dataset license/allowed use.",
    )
    parser.add_argument(
        "--retention-days",
        type=int,
        default=180,
        help="Research staging retention window.",
    )
    parser.add_argument(
        "--hash-key-env",
        default="DEALIX_CONTACT_HASH_KEY",
        help="Optional env var containing a secret HMAC key for contact dedupe.",
    )
    return parser.parse_args()


def _ensure_sqlite_parent(database_url: str) -> None:
    prefix = "sqlite:///"
    if database_url.startswith(prefix):
        Path(database_url.removeprefix(prefix)).parent.mkdir(parents=True, exist_ok=True)


def _sync_database_url(database_url: str) -> str:
    """Use the sync psycopg driver for this batch import command."""
    if database_url.startswith("postgresql+asyncpg://"):
        return database_url.replace(
            "postgresql+asyncpg://",
            "postgresql+psycopg://",
            1,
        )
    return database_url


def main() -> int:
    args = _parse_args()
    if not args.workbook.exists():
        raise SystemExit(f"workbook_not_found:{args.workbook}")
    if not 1 <= args.retention_days <= 365:
        raise SystemExit("retention_days_must_be_1_to_365")

    hash_value = os.getenv(args.hash_key_env, "")
    hash_key = hash_value.encode("utf-8") if hash_value else None
    analysis, candidates = analyze_company_directory(
        args.workbook,
        sheet_name=args.sheet,
        source_terms_verified=args.source_terms_verified,
        hash_key=hash_key,
    )
    args.analysis_json.parent.mkdir(parents=True, exist_ok=True)
    args.analysis_json.write_text(
        json.dumps(analysis.to_dict(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    args.workbook_staging_json.parent.mkdir(parents=True, exist_ok=True)
    args.workbook_staging_json.write_text(
        json.dumps(
            {
                "analysis": analysis.to_dict(),
                "candidates": [
                    {
                        "company_name": candidate.company_name,
                        "city": candidate.city,
                        "activity": candidate.activity,
                        "has_valid_email": candidate.has_valid_email,
                        "has_valid_phone": candidate.has_valid_phone,
                        "data_quality_score": candidate.data_quality_score,
                        "fit_score": candidate.fit_score,
                        "research_priority_score": candidate.research_priority_score,
                        "priority": candidate.priority,
                        "recommended_offer_id": candidate.recommended_offer_id,
                        "value_angle_ar": candidate.value_angle_ar,
                        "targeting_status": candidate.targeting_status,
                        "suppression_reasons": list(candidate.suppression_reasons),
                        "source_sheet": candidate.source_sheet,
                        "source_row_number": candidate.source_row_number,
                    }
                    for candidate in candidates
                ],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    database_url = _sync_database_url(args.database_url)
    _ensure_sqlite_parent(database_url)
    engine = create_engine(database_url)
    tables = [
        CompanyDirectoryImportRecord.__table__,
        CompanyDirectoryEntryRecord.__table__,
    ]
    Base.metadata.create_all(engine, tables=tables)
    import_id = (
        f"cdi_{args.tenant_id}_{analysis.source_sha256[:16]}_"
        f"{analysis.source_sheet.encode('utf-8').hex()[:8]}"
    )
    now = datetime.now(UTC).replace(tzinfo=None)
    terms_status = "verified" if args.source_terms_verified else "unverified"
    with Session(engine) as session:
        import_record = session.execute(
            select(CompanyDirectoryImportRecord).where(
                CompanyDirectoryImportRecord.id == import_id
            )
        ).scalar_one_or_none()
        values = {
            "tenant_id": args.tenant_id,
            "source_name": args.source_name,
            "source_file_name": analysis.source_file,
            "source_file_sha256": analysis.source_sha256,
            "source_sheet": analysis.source_sheet,
            "source_type": "provided_directory",
            "allowed_use": "company_research_and_ranking_only",
            "source_terms_status": terms_status,
            "consent_status": "unknown",
            "retention_until": now + timedelta(days=args.retention_days),
            "status": "imported_research_only",
            "rows_total": analysis.populated_rows,
            "rows_unique": analysis.unique_candidates,
            "rows_duplicate": analysis.duplicate_rows,
            "rows_research_only": analysis.research_only_rows,
            "rows_target_ready": analysis.target_ready_rows,
            "stats_json": analysis.to_dict(),
            "updated_at": now,
        }
        if import_record is None:
            import_record = CompanyDirectoryImportRecord(
                id=import_id,
                created_at=now,
                **values,
            )
            session.add(import_record)
        else:
            for key, value in values.items():
                setattr(import_record, key, value)

        # Idempotent refresh: the source hash identifies this same import, so
        # replace only its derived entries before rebuilding normalized rows.
        session.execute(
            delete(CompanyDirectoryEntryRecord).where(
                CompanyDirectoryEntryRecord.import_id == import_id
            )
        )

        for candidate in candidates:
            session.merge(
                CompanyDirectoryEntryRecord(
                    id=f"{args.tenant_id}_{candidate.id}",
                    tenant_id=args.tenant_id,
                    import_id=import_id,
                    company_name=candidate.company_name[:255],
                    normalized_name=candidate.normalized_name[:255],
                    city=candidate.city[:128] or None,
                    activity=candidate.activity[:255] or None,
                    has_valid_email=candidate.has_valid_email,
                    has_valid_phone=candidate.has_valid_phone,
                    email_masked=candidate.email_masked,
                    phone_masked=candidate.phone_masked,
                    email_hmac=candidate.email_hmac,
                    phone_hmac=candidate.phone_hmac,
                    source_sheet=candidate.source_sheet,
                    source_row_number=candidate.source_row_number,
                    source_fingerprint=candidate.source_fingerprint,
                    data_quality_score=candidate.data_quality_score,
                    fit_score=candidate.fit_score,
                    research_priority_score=candidate.research_priority_score,
                    priority=candidate.priority,
                    recommended_offer_id=candidate.recommended_offer_id,
                    value_angle_ar=candidate.value_angle_ar,
                    relationship_status=candidate.relationship_status,
                    consent_status=candidate.consent_status,
                    targeting_status=candidate.targeting_status,
                    suppression_reasons_json=list(candidate.suppression_reasons),
                    created_at=now,
                    updated_at=now,
                )
            )
        session.commit()

    output = {
        "status": "imported_research_only",
        "database_url": args.database_url,
        "import_id": import_id,
        "source_terms_status": terms_status,
        "raw_contact_values_stored": False,
        "contact_hmac_enabled": bool(hash_key),
        "analysis": analysis.to_dict(),
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
