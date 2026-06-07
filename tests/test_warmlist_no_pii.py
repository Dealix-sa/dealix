"""Constitution guard — the warm-list builder must never emit PII.

The daily warm-list seed is projected from the public Saudi lead graph. Even if
the source file ever gains contact names / emails / pre-drafted messages, the
builder must strip them: contact columns blank, no '@' anywhere, no private
notes copied (Article 4 — IMMUTABLE).
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.dealix_build_warmlist import OUT_HEADER, build_rows, write_warmlist


def _write_source_with_pii(tmp_path: Path) -> Path:
    """A source graph that DELIBERATELY contains PII + pre-drafted outreach,
    to prove the builder strips all of it."""
    src = tmp_path / "graph.csv"
    src.write_text(
        "company,sector,website,country,decision_roles,first_message_angle,notes,contact_name\n"
        "Foodics,SaaS,https://foodics.com,SA,CEO,"
        "\"مرحباً أحمد، رأيت...\",surname connection ahmad@foodics.com,Ahmad Al-Zaini\n"
        "Lucidya,CXM,https://lucidya.com,SA,CEO,"
        "\"أهلاً عبدالله\",priority,Abdullah Asiri\n",
        encoding="utf-8",
    )
    return src


def test_builder_blanks_contact_columns(tmp_path: Path) -> None:
    rows = build_rows(_write_source_with_pii(tmp_path))
    assert rows, "expected non-empty rows"
    for r in rows:
        assert r["contact_name"] == ""
        assert r["contact_title"] == ""


def test_builder_emits_no_emails_or_messages(tmp_path: Path) -> None:
    rows = build_rows(_write_source_with_pii(tmp_path))
    for r in rows:
        for value in r.values():
            assert "@" not in value, f"email leaked into warm-list: {value!r}"
        # the pre-drafted Arabic message must not be copied into notes
        assert r["notes"] == ""


def test_builder_uses_honest_tier1_source(tmp_path: Path) -> None:
    """Public-info targets are NOT marked warm (would be dishonest)."""
    rows = build_rows(_write_source_with_pii(tmp_path))
    for r in rows:
        assert r["source"] == "public_business_info_allowed"
        assert r["source"] not in ("warm_intro", "partner_referral", "founder_intro")


def test_written_file_has_stable_header_and_no_pii(tmp_path: Path) -> None:
    rows = build_rows(_write_source_with_pii(tmp_path))
    out = tmp_path / "candidates.csv"
    write_warmlist(rows, out)
    with out.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == OUT_HEADER
        for r in reader:
            assert r["contact_name"] == "" and r["contact_title"] == ""
            assert "@" not in ",".join(v or "" for v in r.values())
