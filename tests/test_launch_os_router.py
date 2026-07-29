"""Regression tests for api/routers/launch_os.py pipeline endpoints.

POST /launch/pipeline/accounts called PipelineTracker.add() with
account_id/company_name kwargs it doesn't accept (TypeError on every call).
GET /launch/pipeline nested the full pipeline_summary() dict under "by_stage"
instead of the stage-count sub-dict.
"""
from __future__ import annotations

import os
import tempfile

import pytest

import api.routers.launch_os as launch_os_router
from dealix.launch_os.pipeline_tracker import PipelineStage, PipelineTracker


@pytest.fixture
def tracker(monkeypatch):
    with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
        tmp = f.name
    t = PipelineTracker(path=tmp)
    monkeypatch.setattr(launch_os_router, "_get_tracker", lambda: t)
    yield t
    if os.path.exists(tmp):
        os.unlink(tmp)


@pytest.mark.asyncio
async def test_add_to_pipeline_does_not_raise_type_error(tracker):
    account = launch_os_router.PipelineAccountIn(
        account_id="acme_001",
        company_name="Acme Motors",
        offer_id="REVENUE_LEAK_AUDIT",
        value_sar=15000,
        icp_score=82,
        next_action="Send intro email",
    )

    result = await launch_os_router.add_to_pipeline(account)

    assert result["account_name"] == "Acme Motors"
    assert result["offer_id"] == "REVENUE_LEAK_AUDIT"
    assert result["stage"] == PipelineStage.RESEARCH


@pytest.mark.asyncio
async def test_pipeline_summary_by_stage_is_flat_stage_count_map(tracker):
    tracker.add("Acme Motors", offer_id="REVENUE_LEAK_AUDIT", value_sar=15000)

    summary = await launch_os_router.get_pipeline_summary()

    assert summary["by_stage"] == {stage: (1 if stage == PipelineStage.RESEARCH else 0) for stage in PipelineStage.ALL}
    assert summary["total_deals"] == 1
    assert summary["total_arr_sar"] == 15000
