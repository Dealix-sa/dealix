"""Smoke test for the Founder Command Center -> Notion sync.

`await sync(dry_run=True)` with DB ids unset / mock on must complete, return
a dict, perform no writes, and any code-generated sample rows must be labeled
`SAMPLE / عينة`.
"""

from __future__ import annotations

import json

import pytest

from core.config.settings import get_settings


@pytest.fixture(autouse=True)
def _clear_settings_cache():
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


async def test_sync_dry_run_completes_without_writes(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NOTION_MOCK_MODE", "true")
    monkeypatch.delenv("NOTION_API_KEY", raising=False)
    for key in (
        "NOTION_CRM_DB_ID",
        "NOTION_KPI_DB_ID",
        "NOTION_DAILY_OPS_DB_ID",
        "NOTION_PLAN_DB_ID",
        "NOTION_OUTREACH_DB_ID",
        "NOTION_OFFERS_DB_ID",
        "NOTION_PROOF_DB_ID",
    ):
        monkeypatch.delenv(key, raising=False)

    from scripts.sync_founder_command_center_to_notion import sync

    results = await sync(dry_run=True)

    assert isinstance(results, dict)
    assert results["dry_run"] is True
    assert results["status"] == "OK"
    assert results["rows"], "expected at least one section of rows"

    # No row should have been written in a dry run.
    for section in results["rows"].values():
        for row in section:
            assert row["written"] is False
            assert row["skipped"] is True


async def test_sample_rows_are_labeled(monkeypatch: pytest.MonkeyPatch) -> None:
    # Force the empty-ledger sample path by pointing the capital ledger at an
    # empty temp file, then assert the sample proof row carries the label.
    monkeypatch.setenv("NOTION_MOCK_MODE", "true")
    monkeypatch.setenv("DEALIX_CAPITAL_LEDGER_PATH", "var/__nonexistent_capital__.jsonl")

    from scripts.sync_founder_command_center_to_notion import sync

    results = await sync(dry_run=True)
    proof_rows = results["rows"]["proof"]
    assert len(proof_rows) == 1
    # The empty-ledger fallback emits the SAMPLE-labeled proof row; its label
    # content is asserted in test_sample_proof_row_builder_labeled.
    assert proof_rows[0]["external_id"] == "cap-sample-proof"


def test_sample_proof_row_builder_labeled() -> None:
    from scripts.sync_founder_command_center_to_notion import SAMPLE_SOURCE, _sample_proof_row

    ext, props = _sample_proof_row()
    assert ext == "cap-sample-proof"
    blob = json.dumps(props, ensure_ascii=False)
    assert SAMPLE_SOURCE in blob
    assert props["Source"]["select"]["name"] == SAMPLE_SOURCE
    assert SAMPLE_SOURCE == "SAMPLE / عينة"


async def test_outreach_rows_never_auto_synced_for_send(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # The sync builds no outreach rows by default (write-only, never send),
    # but if any appear they must be draft-only. Guard the default invariant.
    monkeypatch.setenv("NOTION_MOCK_MODE", "true")
    from scripts.sync_founder_command_center_to_notion import sync

    results = await sync(dry_run=True)
    assert "outreach" not in results["rows"]
