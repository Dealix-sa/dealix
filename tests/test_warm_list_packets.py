"""Tests for the batch warm-list Close Packet generator.

Offline: the core builder is a pure function over a dict (no network, no
subprocess). The CSV is built in a temp directory; no founder data is read.

Scenario uses three rows:
  1. clear ACCEPT  — warm + owner-grade role -> packet written
  2. REJECT-grade  — cold + non-owner + no signals -> refer_out, no packet
  3. doctrine row  — notes request a cold WhatsApp blast -> reject, no packet
"""
from __future__ import annotations

import csv
from pathlib import Path

import pytest

from scripts.dealix_warm_list_packets import (
    _row_to_prospect,
    _sanitize_filename,
    build_packets,
    main,
    read_rows,
    write_outputs,
)

_HEADER = [
    "name",
    "role",
    "company",
    "sector",
    "relationship",
    "city",
    "linkedin_url",
    "notes",
]

_ROWS = [
    # 1. clear ACCEPT: warm relationship + CEO (owner-grade) role.
    {
        "name": "Aisha Al-Harbi",
        "role": "CEO",
        "company": "Accept Realty",
        "sector": "real_estate",
        "relationship": "warm",
        "city": "Riyadh",
        "linkedin_url": "https://linkedin.com/in/aisha",
        "notes": "wants ranked revenue opportunities",
    },
    # 2. REJECT-grade: cold relationship + non-owner role + nothing else.
    {
        "name": "Bandar Cold",
        "role": "Analyst",
        "company": "Weak Signal Co",
        "sector": "misc",
        "relationship": "cold",
        "city": "",
        "linkedin_url": "",
        "notes": "",
    },
    # 3. doctrine violation expressed in the notes (cold WhatsApp blast).
    {
        "name": "Khalid Blast",
        "role": "CMO",
        "company": "Blast Marketing",
        "sector": "agencies",
        "relationship": "warm",
        "city": "Jeddah",
        "linkedin_url": "https://linkedin.com/in/khalid",
        "notes": "we want to blast leads via cold whatsapp to everyone",
    },
]


def _write_csv(path: Path, rows: list[dict[str, str]]) -> Path:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=_HEADER)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return path


# ── _sanitize_filename ──
def test_sanitize_filename_collapses_and_lowercases() -> None:
    assert _sanitize_filename("Accept Realty") == "accept_realty"
    assert _sanitize_filename("  A//B  ") == "a_b"
    assert _sanitize_filename("") == "contact"
    assert _sanitize_filename("***") == "contact"


# ── _row_to_prospect: flag inference mirrors warm_list_outreach ──
def test_row_to_prospect_warm_owner_is_accept_grade() -> None:
    prospect = _row_to_prospect(_ROWS[0], channel="whatsapp")
    assert prospect["company"] == "Accept Realty"
    assert prospect["relationship"] == "warm"
    sig = prospect["signals"]
    assert sig["owner_present"] is True
    assert sig["pain_clear"] is True
    assert sig["has_budget"] is True


def test_row_to_prospect_cold_nonowner_is_weak() -> None:
    prospect = _row_to_prospect(_ROWS[1], channel="whatsapp")
    assert prospect["relationship"] == "cold"
    sig = prospect["signals"]
    assert sig["owner_present"] is False
    assert sig["pain_clear"] is False
    assert sig["has_budget"] is False


# ── read_rows ──
def test_read_rows_skips_empty_name_rows(tmp_path: Path) -> None:
    rows_with_blank = _ROWS + [dict.fromkeys(_HEADER, "")]
    csv_path = _write_csv(tmp_path / "warm.csv", rows_with_blank)
    rows = read_rows(csv_path)
    assert len(rows) == 3  # the all-empty row is dropped
    assert rows[0]["name"] == "Aisha Al-Harbi"


# ── build_packets: the three-row scenario ──
def test_build_packets_decisions_and_write_flags() -> None:
    rows = list(_ROWS)
    results = build_packets(rows, channel="whatsapp")
    assert len(results) == 3

    accept, reject, doctrine = results

    # 1. clear ACCEPT -> packet written, no violations.
    assert accept["decision"] == "accept"
    assert accept["write_packet"] is True
    assert accept["doctrine_violations"] == []
    assert accept["score"] == 100

    # 2. REJECT-grade (cold/non-owner) -> refer_out, no packet.
    assert reject["decision"] == "refer_out"
    assert reject["write_packet"] is False
    assert "refer_out" in reject["reason"]

    # 3. doctrine row -> reject + violation, no packet.
    assert doctrine["decision"] == "reject"
    assert "cold_whatsapp" in doctrine["doctrine_violations"]
    assert doctrine["write_packet"] is False
    assert "doctrine_violation" in doctrine["reason"]
    assert "cold_whatsapp" in doctrine["reason"]


def test_build_packets_rejects_invalid_channel() -> None:
    with pytest.raises(ValueError):
        build_packets(list(_ROWS), channel="carrier_pigeon")


# ── write_outputs: files + index reflect the three-row scenario ──
def test_write_outputs_writes_only_accept_packet(tmp_path: Path) -> None:
    results = build_packets(list(_ROWS), channel="whatsapp")
    out_dir = tmp_path / "packets"
    summary = write_outputs(results, out_dir=out_dir, is_demo=False)

    # Exactly one packet (the ACCEPT row); two skipped.
    assert summary["generated"] == 1
    assert summary["skipped"] == 2
    assert len(summary["written_files"]) == 1

    # The packet file is named after the ACCEPT company; the reject/doctrine
    # companies get NO file.
    written_names = {p.name for p in summary["written_files"]}
    assert "accept_realty_close_packet.md" in written_names
    assert not (out_dir / "weak_signal_co_close_packet.md").exists()
    assert not (out_dir / "blast_marketing_close_packet.md").exists()

    # The ACCEPT packet content is a labeled DRAFT and carries the disclaimer.
    packet_text = (out_dir / "accept_realty_close_packet.md").read_text(
        encoding="utf-8"
    )
    assert "Close Packet — Accept Realty" in packet_text
    assert "Outreach DRAFT" in packet_text
    assert "never auto-sent" in packet_text
    assert "النتائج التقديرية ليست نتائج مضمونة" in packet_text


def test_write_outputs_index_lists_all_rows_with_badges(tmp_path: Path) -> None:
    results = build_packets(list(_ROWS), channel="whatsapp")
    out_dir = tmp_path / "packets"
    summary = write_outputs(results, out_dir=out_dir, is_demo=False)

    index_text = summary["index_path"].read_text(encoding="utf-8")

    # Summary counts.
    assert "1 packet(s) generated" in index_text
    assert "2 skipped" in index_text

    # All three contacts are listed.
    assert "Aisha Al-Harbi" in index_text
    assert "Bandar Cold" in index_text
    assert "Khalid Blast" in index_text

    # Correct decision badges (bilingual).
    assert "ACCEPT / مقبول" in index_text
    assert "REFER_OUT / إحالة" in index_text
    assert "REJECT / مرفوض" in index_text

    # ACCEPT row links to its packet; the other two say "no packet" + reason.
    assert "[accept_realty_close_packet.md]" in index_text
    assert "no packet — refer_out" in index_text
    assert "no packet — doctrine_violation: cold_whatsapp" in index_text

    # No packet file exists for the reject/doctrine rows even though they are
    # in the index.
    assert not (out_dir / "blast_marketing_close_packet.md").exists()


def test_write_outputs_demo_banner_when_demo(tmp_path: Path) -> None:
    results = build_packets(list(_ROWS), channel="whatsapp")
    summary = write_outputs(results, out_dir=tmp_path / "p", is_demo=True)
    index_text = summary["index_path"].read_text(encoding="utf-8")
    assert "DEMO DATA" in index_text


# ── main: end-to-end over a temp CSV ──
def test_main_end_to_end(tmp_path: Path) -> None:
    csv_path = _write_csv(tmp_path / "warm.csv", list(_ROWS))
    out_dir = tmp_path / "out"
    rc = main(["--csv", str(csv_path), "--out-dir", str(out_dir), "--channel", "whatsapp"])
    assert rc == 0
    assert (out_dir / "INDEX.md").exists()
    assert (out_dir / "accept_realty_close_packet.md").exists()
    # Only the ACCEPT packet was written.
    packet_files = sorted(p.name for p in out_dir.glob("*_close_packet.md"))
    assert packet_files == ["accept_realty_close_packet.md"]


def test_main_missing_csv_falls_back_to_template(tmp_path: Path) -> None:
    # A non-existent CSV falls back to the repo template and is labeled DEMO.
    out_dir = tmp_path / "demo_out"
    rc = main(
        [
            "--csv",
            str(tmp_path / "does_not_exist.csv"),
            "--out-dir",
            str(out_dir),
        ]
    )
    assert rc == 0
    index_text = (out_dir / "INDEX.md").read_text(encoding="utf-8")
    assert "DEMO DATA" in index_text
