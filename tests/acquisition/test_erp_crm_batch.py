"""Tests for the ERP/CRM done-for-you acquisition batch."""

from __future__ import annotations

import csv
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
BATCH_PATH = REPO_ROOT / "acquisition" / "lead_batches" / "2026-05-23-erp-crm-seed.csv"
LIBRARY_PATH = REPO_ROOT / "acquisition" / "outreach_messages" / "erp_crm_v1.md"
APPROVAL_PATH = REPO_ROOT / "acquisition" / "approvals" / "2026-05-23-erp-crm-seed.md"

REQUIRED_COLS = {
    "company",
    "sector",
    "website",
    "fit_score",
    "priority",
    "verification_status",
    "suggested_message_id",
    "approval_status",
}


def _load_rows() -> list[dict[str, str]]:
    with BATCH_PATH.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_batch_file_exists() -> None:
    assert BATCH_PATH.exists(), f"missing batch file: {BATCH_PATH}"


def test_batch_has_required_columns() -> None:
    with BATCH_PATH.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        cols = set(reader.fieldnames or [])
    missing = REQUIRED_COLS - cols
    assert not missing, f"missing required columns: {missing}"


def test_batch_has_25_rows() -> None:
    rows = _load_rows()
    assert len(rows) == 25, f"expected 25 leads, got {len(rows)}"


def test_priority_matches_fit_score() -> None:
    for row in _load_rows():
        score = int(row["fit_score"])
        priority = row["priority"]
        if score >= 80:
            expected = "A"
        elif score >= 70:
            expected = "B"
        else:
            expected = "C"
        assert priority == expected, (
            f"{row['company']}: fit_score={score} but priority={priority} (expected {expected})"
        )


def test_verified_rows_have_websites() -> None:
    for row in _load_rows():
        if row["verification_status"] == "URL_VERIFIED":
            assert row["website"].startswith("http"), (
                f"{row['company']} is URL_VERIFIED but website is empty"
            )


def test_unverified_rows_block_send() -> None:
    """Unverified rows must not have an Approved status until a URL is added."""
    for row in _load_rows():
        if row["verification_status"] == "URL_NEEDS_VERIFICATION":
            assert row["approval_status"] != "Approved", (
                f"{row['company']} is unverified but already Approved"
            )


def test_all_rows_pending_at_seed_time() -> None:
    for row in _load_rows():
        assert row["approval_status"] == "Pending", (
            f"{row['company']} should start as Pending (founder approves)"
        )


def test_no_guarantee_language_in_messages() -> None:
    text = LIBRARY_PATH.read_text(encoding="utf-8")
    body = text.split("## Copy Rules", 1)[0].lower()
    banned = ["guarantee", "guaranteed", "promised", "promise revenue"]
    for phrase in banned:
        assert phrase not in body, (
            f"banned phrase '{phrase}' found in outreach copy (not in policy block)"
        )


def test_messages_have_single_cta() -> None:
    """First-touch messages should ask exactly one question."""
    text = LIBRARY_PATH.read_text(encoding="utf-8")
    for mid in ("erp_crm_v1_en", "erp_crm_v1_ar"):
        match = re.search(
            rf"^## {mid}[^\n]*\n+```\n(.*?)```", text, re.DOTALL | re.MULTILINE
        )
        assert match, f"missing message body for {mid}"
        body = match.group(1)
        en_q = body.count("?")
        ar_q = body.count("؟")
        assert en_q + ar_q <= 2, (
            f"{mid}: expected <=2 question marks, found en={en_q} ar={ar_q}"
        )


def test_approval_file_present() -> None:
    assert APPROVAL_PATH.exists(), f"missing approval queue: {APPROVAL_PATH}"
    content = APPROVAL_PATH.read_text(encoding="utf-8")
    assert "Sami Decision" in content
    assert "Pending" in content


def test_message_id_resolves_in_library() -> None:
    library = LIBRARY_PATH.read_text(encoding="utf-8")
    ids = set(re.findall(r"^## ([a-z0-9_]+)", library, re.MULTILINE))
    for row in _load_rows():
        mid = row.get("suggested_message_id")
        if mid:
            assert mid in ids, f"{row['company']} references unknown message_id {mid}"


@pytest.mark.parametrize(
    "doc",
    [
        "docs/acquisition/DONE_FOR_YOU_ACQUISITION_OS.md",
        "docs/acquisition/CONTACT_DISCOVERY_POLICY.md",
        "docs/delivery/REVENUE_SPRINT_SAMPLE_TEMPLATE.md",
        "docs/revenue/PROPOSAL_TRIGGER_RULES.md",
    ],
)
def test_supporting_docs_present(doc: str) -> None:
    path = REPO_ROOT / doc
    assert path.exists(), f"missing supporting doc: {doc}"
    assert path.stat().st_size > 200, f"supporting doc too short: {doc}"
