"""Bulk lead intake (M9).

The ``raw_lead_imports`` / ``raw_lead_rows`` tables existed as staged
infrastructure, but nothing turned a raw row into a real ``LeadRecord`` —
so an uploaded list went nowhere. This module closes that gap: it
normalizes the pending rows of an import into ``leads`` rows at lifecycle
stage ``captured``, deduplicates, and updates the import counters.

Enrichment / qualification stay the job of ``AcquisitionPipeline`` — bulk
intake's only job is to land raw rows in the leads table truthfully.
Session-injected so it tests cleanly against sqlite.
"""
from __future__ import annotations

import hashlib
import uuid
from datetime import UTC, datetime
from typing import Any

# Liberal key aliases — uploaded CSVs use many header conventions.
_FIELD_ALIASES: dict[str, tuple[str, ...]] = {
    "company_name": ("company_name", "company", "organisation", "organization", "اسم الشركة"),
    "contact_name": ("contact_name", "name", "contact", "full_name", "الاسم"),
    "contact_email": ("contact_email", "email", "e-mail", "البريد"),
    "contact_phone": ("contact_phone", "phone", "mobile", "tel", "الجوال"),
    "sector": ("sector", "industry", "vertical", "القطاع"),
    "region": ("region", "city", "location", "المدينة"),
    "message": ("message", "notes", "note", "ملاحظات"),
}


def _pick(raw: dict[str, Any], field: str) -> str:
    for alias in _FIELD_ALIASES.get(field, (field,)):
        for key in raw:
            if str(key).strip().lower() == alias.lower():
                value = raw[key]
                if value is not None and str(value).strip():
                    return str(value).strip()
    return ""


def _dedup_hash(email: str, company: str) -> str:
    basis = f"{email}|{company}".lower()
    return hashlib.md5(basis.encode("utf-8")).hexdigest()  # noqa: S324 — non-crypto dedup key


def normalize_import(
    session: Any,
    import_id: str,
    *,
    tenant_id: str | None = None,
) -> dict[str, Any]:
    """Normalize every pending row of one import into ``leads`` rows.

    Returns ``{import_id, ok, rejected, duplicate, total}``. Caller commits.
    """
    from sqlalchemy import select

    from db.models import LeadRecord, RawLeadImport, RawLeadRow

    imp = session.get(RawLeadImport, import_id)
    if imp is None:
        raise ValueError(f"raw_lead_import {import_id} not found")

    imp.status = "normalizing"
    rows = list(
        session.execute(
            select(RawLeadRow).where(
                RawLeadRow.import_id == import_id,
                RawLeadRow.normalized_status == "pending",
            )
        ).scalars().all()
    )

    # Existing dedup hashes — skip leads already in the system.
    known: set[str] = {
        h for (h,) in session.execute(select(LeadRecord.dedup_hash)).all() if h
    }

    ok = rejected = duplicate = 0
    now = datetime.now(UTC)

    for row in rows:
        raw = dict(row.raw_json or {})
        company = _pick(raw, "company_name")
        email = _pick(raw, "contact_email")
        if not company and not email:
            row.normalized_status = "rejected"
            row.error = "row has neither a company name nor an email"
            rejected += 1
            continue

        dedup = _dedup_hash(email, company)
        if dedup in known:
            row.normalized_status = "duplicate"
            duplicate += 1
            continue

        lead_id = f"lead_{uuid.uuid4().hex[:16]}"
        session.add(
            LeadRecord(
                id=lead_id,
                tenant_id=tenant_id,
                source=str(imp.source_type or "manual")[:32],
                company_name=company[:255],
                contact_name=_pick(raw, "contact_name")[:255],
                contact_email=email[:255] or None,
                contact_phone=(_pick(raw, "contact_phone")[:32] or None),
                sector=(_pick(raw, "sector")[:64] or None),
                region=(_pick(raw, "region")[:128] or None),
                status="new",
                lifecycle_stage="captured",
                message=_pick(raw, "message") or None,
                dedup_hash=dedup,
                meta_json={"raw_lead_import_id": import_id},
                created_at=now,
                updated_at=now,
            )
        )
        row.normalized_status = "ok"
        row.account_id = lead_id
        known.add(dedup)
        ok += 1

    imp.rows_normalized = (imp.rows_normalized or 0) + ok
    imp.rows_rejected = (imp.rows_rejected or 0) + rejected
    imp.rows_duplicate = (imp.rows_duplicate or 0) + duplicate
    imp.status = "normalized"
    imp.updated_at = now

    return {
        "import_id": import_id,
        "ok": ok,
        "rejected": rejected,
        "duplicate": duplicate,
        "total": len(rows),
    }


__all__ = ["normalize_import"]
