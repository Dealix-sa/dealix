"""Tests for bulk lead intake normalization (M9)."""
from __future__ import annotations

import uuid

import pytest

sa = pytest.importorskip("sqlalchemy")
import sqlalchemy.orm  # noqa: E402,F401

from auto_client_acquisition.sales_os.bulk_intake import normalize_import  # noqa: E402


@pytest.fixture()
def session():
    from db.models import Base

    engine = sa.create_engine("sqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    with sa.orm.Session(engine, future=True) as s:
        yield s


def _make_import(session, rows: list[dict]) -> str:
    from db.models import RawLeadImport, RawLeadRow

    imp_id = f"imp_{uuid.uuid4().hex[:8]}"
    session.add(
        RawLeadImport(
            id=imp_id, source_name="upload.csv", source_type="owned",
            rows_total=len(rows),
        )
    )
    for raw in rows:
        session.add(
            RawLeadRow(id=f"row_{uuid.uuid4().hex[:8]}", import_id=imp_id, raw_json=raw)
        )
    session.commit()
    return imp_id


def _leads(session) -> list:
    from db.models import LeadRecord

    return list(session.execute(sa.select(LeadRecord)).scalars().all())


def test_normalizes_valid_rows_into_leads(session) -> None:
    imp_id = _make_import(
        session,
        [
            {"company": "Foodics", "email": "ops@foodics.sa", "industry": "saas"},
            {"company_name": "Sary", "name": "Buyer", "phone": "+966500000000"},
        ],
    )
    result = normalize_import(session, imp_id)
    session.commit()

    assert result["ok"] == 2
    leads = _leads(session)
    assert len(leads) == 2
    assert all(lead.lifecycle_stage == "captured" for lead in leads)
    assert {lead.company_name for lead in leads} == {"Foodics", "Sary"}


def test_duplicate_rows_are_flagged_not_double_created(session) -> None:
    imp_id = _make_import(
        session,
        [
            {"company": "Lean", "email": "hi@lean.sa"},
            {"company": "Lean", "email": "hi@lean.sa"},  # exact dup
        ],
    )
    result = normalize_import(session, imp_id)
    session.commit()

    assert result["ok"] == 1
    assert result["duplicate"] == 1
    assert len(_leads(session)) == 1


def test_empty_row_is_rejected(session) -> None:
    imp_id = _make_import(session, [{"industry": "saas"}])  # no company, no email
    result = normalize_import(session, imp_id)
    session.commit()

    assert result["rejected"] == 1
    assert result["ok"] == 0
    assert _leads(session) == []


def test_import_counters_and_status_updated(session) -> None:
    imp_id = _make_import(session, [{"company": "Hakbah", "email": "x@hakbah.sa"}])
    normalize_import(session, imp_id)
    session.commit()

    from db.models import RawLeadImport

    imp = session.get(RawLeadImport, imp_id)
    assert imp.status == "normalized"
    assert imp.rows_normalized == 1


def test_missing_import_raises(session) -> None:
    with pytest.raises(ValueError):
        normalize_import(session, "imp_does_not_exist")
