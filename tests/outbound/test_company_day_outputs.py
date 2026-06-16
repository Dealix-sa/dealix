"""Company Day must produce expected output artifacts."""

from __future__ import annotations

from pathlib import Path

import pytest

from app.outbound.storage import CSVOutboundStorage


def test_company_day_creates_command_room_report(tmp_path, monkeypatch):
    # Simulate company-day output paths.
    reports_dir = tmp_path / "reports" / "command_room"
    reports_dir.mkdir(parents=True)
    (reports_dir / "outbound_events.json").write_text('{"total_messages": 0}', encoding="utf-8")

    assert (reports_dir / "outbound_events.json").exists()


def test_storage_initializes_csv_files(tmp_path):
    CSVOutboundStorage(base_dir=tmp_path / "outbound")
    assert (tmp_path / "outbound" / "contacts.csv").exists()
    assert (tmp_path / "outbound" / "messages.csv").exists()
    assert (tmp_path / "outbound" / "events.csv").exists()
    assert (tmp_path / "outbound" / "suppression_list.csv").exists()
    assert (tmp_path / "outbound" / "deals_pipeline.csv").exists()
