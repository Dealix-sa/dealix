"""Delivery handoff: paid → full customer folder with proof pack + governance."""

from __future__ import annotations

import pytest

from scripts.targeting_delivery_handoff import CUSTOMER_FILES, create_handoff


def _paid_company() -> dict:
    return {
        "company_name": "Manar Performance Agency",
        "website": "https://manar.example.sa",
        "city": "riyadh",
        "sector": "marketing_agency",
        "no_case_studies": True,
        "source_urls": ["https://manar.example.sa", "https://manar.example.sa/clients"],
        "evidence_count": 2,
    }


def test_handoff_creates_all_canonical_files(tmp_path) -> None:
    result = create_handoff(_paid_company(), base_dir=tmp_path)
    folder = tmp_path / result["slug"]
    assert folder.is_dir()
    for filename, _ in CUSTOMER_FILES:
        assert (folder / filename).exists(), f"missing {filename}"


def test_handoff_produces_a_proof_pack(tmp_path) -> None:
    result = create_handoff(_paid_company(), base_dir=tmp_path)
    proof = tmp_path / result["slug"] / "09_proof_pack.md"
    assert proof.exists()
    text = proof.read_text(encoding="utf-8")
    assert "L1" in text and "L3" in text  # proof levels present


def test_every_file_carries_governance_front_matter(tmp_path) -> None:
    result = create_handoff(_paid_company(), base_dir=tmp_path)
    folder = tmp_path / result["slug"]
    required = [
        "source:",
        "evidence:",
        "assumption:",
        "confidence:",
        "recommendation:",
        "approval_required:",
        "next_action:",
        "owner:",
        "due_date:",
    ]
    for filename, _ in CUSTOMER_FILES:
        text = (folder / filename).read_text(encoding="utf-8")
        for key in required:
            assert key in text, f"{filename} missing front-matter key {key}"


def test_intake_records_offer_and_paid_date(tmp_path) -> None:
    result = create_handoff(_paid_company(), offer_id="command_sprint", base_dir=tmp_path)
    intake = (tmp_path / result["slug"] / "00_intake.md").read_text(encoding="utf-8")
    assert "Command Sprint" in intake
    assert "Paid date:" in intake


def test_handoff_requires_a_company_name(tmp_path) -> None:
    with pytest.raises(ValueError):
        create_handoff({"company_name": ""}, base_dir=tmp_path)


def test_slug_is_filesystem_safe(tmp_path) -> None:
    result = create_handoff(
        {**_paid_company(), "company_name": "ACME / Saudi Co. (٢)"}, base_dir=tmp_path
    )
    assert "/" not in result["slug"]
    assert (tmp_path / result["slug"]).is_dir()
