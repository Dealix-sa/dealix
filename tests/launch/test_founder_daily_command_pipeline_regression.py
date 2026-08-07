"""Regression tests: generate_daily_command() crashed with AttributeError for any
pipeline item outside RESEARCH stage.

PipelineItem only ever exposed .id and .account_name; founder_daily_command.py
read .account_id and .company_name instead, which don't exist on the dataclass.
"""
from __future__ import annotations

import os
import tempfile

import pytest

from dealix.launch_os.founder_daily_command import generate_daily_command
from dealix.launch_os.pipeline_tracker import PipelineStage, PipelineTracker


@pytest.fixture
def tracker():
    with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
        tmp = f.name
    t = PipelineTracker(path=tmp)
    yield t
    if os.path.exists(tmp):
        os.unlink(tmp)


def test_outreach_queue_uses_item_id_and_account_name_for_research_stage(tracker):
    item = tracker.add("Acme Motors", offer_id="REVENUE_LEAK_AUDIT", next_action="Send intro email")

    cmd = generate_daily_command(tracker, [])

    assert len(cmd.outreach_queue) == 1
    entry = cmd.outreach_queue[0]
    assert entry["account_id"] == item.id
    assert entry["account_name"] == "Acme Motors"
    assert entry["offer_id"] == "REVENUE_LEAK_AUDIT"


@pytest.mark.parametrize(
    "stage",
    [
        PipelineStage.OUTREACH,
        PipelineStage.DISCOVERY,
        PipelineStage.PROPOSAL,
        PipelineStage.NEGOTIATION,
    ],
)
def test_pipeline_review_items_does_not_crash_for_non_research_stages(tracker, stage):
    item = tracker.add("Golden Realty Co", offer_id="SALES_COMMAND_CENTER", value_sar=9000)
    tracker.update_stage(item.id, stage)

    cmd = generate_daily_command(tracker, [])

    assert len(cmd.pipeline_review_items) == 1
    entry = cmd.pipeline_review_items[0]
    assert entry["account_id"] == item.id
    assert entry["account_name"] == "Golden Realty Co"
    assert entry["stage"] == stage


def test_api_daily_command_endpoint_does_not_crash_with_live_pipeline(tracker, monkeypatch):
    """Regression for GET /launch/daily-command — same underlying bug."""
    import api.routers.launch_os as launch_os_router

    tracker.add("Clinic Care Network", offer_id="WHATSAPP_FOLLOWUP_OS")
    monkeypatch.setattr(launch_os_router, "_get_tracker", lambda: tracker)

    import asyncio

    result = asyncio.run(launch_os_router.get_daily_command())

    assert result["outreach_queue"][0]["account_name"] == "Clinic Care Network"
