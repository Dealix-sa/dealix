from __future__ import annotations

import zipfile
from pathlib import Path

from dealix.company_os.campaign_planner import (
    ContactPermission,
    build_campaign_plan,
)
from dealix.company_os.company_directory import (
    analyze_company_directory,
    build_directory_candidate,
)
from scripts.commercial.import_company_directory import _sync_database_url


def _minimal_xlsx(path: Path) -> None:
    workbook = """<?xml version="1.0" encoding="UTF-8"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets><sheet name="داتا كاملة" sheetId="1" r:id="rId1"/></sheets>
</workbook>"""
    rels = """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Target="worksheets/sheet1.xml"
    Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet"/>
</Relationships>"""
    sheet = """<?xml version="1.0" encoding="UTF-8"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <sheetData>
    <row r="1">
      <c r="A1" t="inlineStr"><is><t>اسم الشركة</t></is></c>
      <c r="B1" t="inlineStr"><is><t>المدينة</t></is></c>
      <c r="C1" t="inlineStr"><is><t>الإيميل</t></is></c>
      <c r="D1" t="inlineStr"><is><t>رقم التواصل</t></is></c>
      <c r="E1" t="inlineStr"><is><t>وظيفة الشركة</t></is></c>
    </row>
    <row r="2">
      <c r="A2" t="inlineStr"><is><t>شركة ألف</t></is></c>
      <c r="B2" t="inlineStr"><is><t>الرياض</t></is></c>
      <c r="C2" t="inlineStr"><is><t>sales@alef.sa</t></is></c>
      <c r="D2" t="inlineStr"><is><t>0551234567</t></is></c>
      <c r="E2" t="inlineStr"><is><t>مقاولات</t></is></c>
    </row>
    <row r="3">
      <c r="A3" t="inlineStr"><is><t>شركة ألف</t></is></c>
      <c r="B3" t="inlineStr"><is><t>الرياض</t></is></c>
      <c r="C3" t="inlineStr"><is><t>bad</t></is></c>
      <c r="D3" t="inlineStr"><is><t>0551234567</t></is></c>
      <c r="E3" t="inlineStr"><is><t>مقاولات</t></is></c>
    </row>
    <row r="1048576"></row>
  </sheetData>
</worksheet>"""
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("xl/workbook.xml", workbook)
        archive.writestr("xl/_rels/workbook.xml.rels", rels)
        archive.writestr("xl/worksheets/sheet1.xml", sheet)


def test_directory_analysis_ignores_formatted_empty_rows_and_dedupes(tmp_path: Path) -> None:
    workbook = tmp_path / "companies.xlsx"
    _minimal_xlsx(workbook)
    analysis, candidates = analyze_company_directory(workbook)
    assert analysis.populated_rows == 2
    assert analysis.unique_candidates == 1
    assert analysis.duplicate_rows == 1
    assert analysis.invalid_email_rows == 1
    assert analysis.target_ready_rows == 0
    assert len(candidates) == 1


def test_batch_import_converts_async_postgres_url_to_sync_driver() -> None:
    assert _sync_database_url(
        "postgresql+asyncpg://user:pass@db.example/dealix"
    ) == "postgresql+psycopg://user:pass@db.example/dealix"


def test_directory_candidate_masks_contacts_and_never_infers_consent() -> None:
    candidate = build_directory_candidate(
        {
            "اسم الشركة": "مصنع الاختبار",
            "المدينة": "الدمام",
            "الإيميل": "owner@example.sa",
            "رقم التواصل": "0551234567",
            "وظيفة الشركة": "صناعة المنتجات الغذائية",
        },
        source_sheet="داتا كاملة",
        source_row_number=2,
    )
    assert candidate.email_masked == "o***@example.sa"
    assert candidate.phone_masked == "+***4567"
    assert candidate.email_hmac is None
    assert candidate.targeting_status == "research_only"
    assert candidate.consent_status == "unknown"
    assert "consent_not_proven" in candidate.suppression_reasons


def test_campaign_is_research_only_without_permission() -> None:
    candidate = build_directory_candidate(
        {
            "اسم الشركة": "شركة اختبار",
            "المدينة": "الرياض",
            "الإيميل": "sales@example.sa",
            "رقم التواصل": "0551234567",
            "وظيفة الشركة": "مقاولات",
        },
        source_sheet="داتا كاملة",
        source_row_number=2,
    )
    plan = build_campaign_plan([candidate])
    assert plan.research_only_count == 1
    assert plan.draft_ready_count == 0
    assert plan.external_actions_performed == 0
    assert plan.items[0].external_action_permitted is False


def test_campaign_can_prepare_draft_for_evidenced_relationship_but_not_send() -> None:
    candidate = build_directory_candidate(
        {
            "اسم الشركة": "شركة اختبار",
            "المدينة": "الرياض",
            "الإيميل": "sales@example.sa",
            "رقم التواصل": "0551234567",
            "وظيفة الشركة": "مقاولات",
        },
        source_sheet="داتا كاملة",
        source_row_number=2,
    )
    permission = ContactPermission(
        relationship_status="inbound",
        channel="email",
        consent_status="existing_relationship",
        evidence_id="ev_inbound_001",
    )
    plan = build_campaign_plan(
        [candidate],
        permissions={candidate.id: permission},
    )
    assert plan.draft_ready_count == 1
    assert plan.items[0].channel == "email_draft"
    assert plan.items[0].external_action_permitted is False
