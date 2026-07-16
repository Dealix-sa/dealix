"""Contract tests for the founder-approved Pilot launch pack."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPLIANCE = ROOT / "docs" / "compliance"
COMMERCIAL = ROOT / "docs" / "commercial"


def test_data_flow_register_has_required_governance_columns() -> None:
    path = COMPLIANCE / "PILOT_DATA_FLOW_REGISTER.csv"
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) >= 10
    required = {
        "Flow ID",
        "Status",
        "Data Category",
        "Personal Data",
        "Source",
        "Purpose",
        "Permission or Lawful-Basis Evidence",
        "Current Region",
        "Retention",
        "Cross-Border Decision",
        "Owner",
        "Launch Gate",
    }
    assert required <= set(rows[0])
    assert all(row["Owner"] for row in rows)
    assert any("US West" in row["Current Region"] for row in rows)
    assert not any(row["Status"].strip().lower() == "approved" for row in rows)


def test_privacy_pack_is_fail_closed_and_source_bound() -> None:
    text = (COMPLIANCE / "PILOT_DATA_PROCESSING_AND_SECURITY_PACK_AR.md").read_text(
        encoding="utf-8"
    )
    for marker in (
        "counsel_approval_required",
        "NO_REAL_CUSTOMER_DATA",
        "https://dgp.sdaia.gov.sa/",
        "https://whatsappbusiness.com/policy/",
        "https://www.linkedin.com/legal/user-agreement",
        "Tenant isolation",
        "suppression",
    ):
        assert marker in text


def test_sow_has_no_approved_price_or_guaranteed_outcome() -> None:
    text = (COMMERCIAL / "PILOT_SOW_AND_ACCEPTANCE_TEMPLATE_AR.md").read_text(
        encoding="utf-8"
    )
    assert "[FOUNDER_APPROVED_SAR]" in text
    assert "لا يضمن مبيعات أو إيرادًا أو ROI" in text
    assert "https://zatca.gov.sa/en/E-Invoicing/" in text
    assert "NO_LIVE_SEND" not in text  # human-readable contract, not a false status claim
    assert "14900" not in text
    assert "499" not in text


def test_five_conversation_template_contains_no_fabricated_company_data() -> None:
    path = COMMERCIAL / "QUALIFIED_CONVERSATION_EVIDENCE_TEMPLATE.csv"
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert [row["Interview ID"] for row in rows] == [
        "QC-001",
        "QC-002",
        "QC-003",
        "QC-004",
        "QC-005",
    ]
    for row in rows:
        assert row["Company Alias"] == ""
        assert row["Price Range Mentioned by Prospect"] == ""
        assert row["Decision"] == "pending"
