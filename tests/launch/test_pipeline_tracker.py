"""Tests for dealix.launch_os.pipeline_tracker.

Actual interface:
    PipelineStage: class with string constants RESEARCH/OUTREACH/DISCOVERY/
                   PROPOSAL/NEGOTIATION/WON/LOST and ALL list
    PipelineItem: dataclass with id, account_name, stage, offer_id, value_sar,
                  icp_score, last_touch_date, next_action, owner_notes;
                  to_dict() / from_dict()
    PipelineTracker(path=None):
        .add(account_name, offer_id, value_sar, icp_score, next_action,
             owner_notes, stage) -> PipelineItem
        .get(deal_id) -> PipelineItem   (raises KeyError if not found)
        .update_stage(deal_id, new_stage, next_action, owner_notes) -> PipelineItem
        .list_all() -> list[PipelineItem]  (sorted by icp_score desc)
        .list_by_stage(stage) -> list[PipelineItem]
        .pipeline_summary() -> dict[total_deals, total_arr_sar, by_stage, arr_by_stage]
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from dealix.launch_os.pipeline_tracker import (
    PipelineItem,
    PipelineStage,
    PipelineTracker,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _fresh_tracker(path: Path | None = None) -> PipelineTracker:
    if path is None:
        import tempfile, os
        fd, tmp = tempfile.mkstemp(suffix=".jsonl")
        os.close(fd)
        os.unlink(tmp)
        return PipelineTracker(path=tmp)
    return PipelineTracker(path=path)


def _populated_tracker(path: Path | None = None) -> PipelineTracker:
    t = _fresh_tracker(path)
    t.add("Alpha Corp", "REVENUE_LEAK_AUDIT", value_sar=10_000, icp_score=80, stage=PipelineStage.RESEARCH)
    t.add("Beta Ltd", "SALES_COMMAND_CENTER", value_sar=15_000, icp_score=70, stage=PipelineStage.OUTREACH)
    t.add("Gamma SA", "WHATSAPP_FOLLOWUP_OS", value_sar=8_000, icp_score=60, stage=PipelineStage.DISCOVERY)
    t.add("Delta Inc", "PROPOSAL_PROOF_PACK_OS", value_sar=25_000, icp_score=75, stage=PipelineStage.PROPOSAL)
    t.add("Epsilon Co", "AI_OPERATING_SYSTEM_FOR_SMB", value_sar=50_000, icp_score=85, stage=PipelineStage.WON)
    return t


# ---------------------------------------------------------------------------
# PipelineStage constants
# ---------------------------------------------------------------------------

class TestPipelineStage:
    def test_research_stage_exists(self) -> None:
        assert PipelineStage.RESEARCH == "RESEARCH"

    def test_outreach_stage_exists(self) -> None:
        assert PipelineStage.OUTREACH == "OUTREACH"

    def test_discovery_stage_exists(self) -> None:
        assert PipelineStage.DISCOVERY == "DISCOVERY"

    def test_proposal_stage_exists(self) -> None:
        assert PipelineStage.PROPOSAL == "PROPOSAL"

    def test_negotiation_stage_exists(self) -> None:
        assert PipelineStage.NEGOTIATION == "NEGOTIATION"

    def test_won_stage_exists(self) -> None:
        assert PipelineStage.WON == "WON"

    def test_lost_stage_exists(self) -> None:
        assert PipelineStage.LOST == "LOST"

    def test_all_attribute_contains_all_stages(self) -> None:
        all_stages = PipelineStage.ALL
        assert isinstance(all_stages, list)
        for stage in ["RESEARCH", "OUTREACH", "DISCOVERY", "PROPOSAL", "NEGOTIATION", "WON", "LOST"]:
            assert stage in all_stages


# ---------------------------------------------------------------------------
# PipelineTracker.add
# ---------------------------------------------------------------------------

class TestPipelineTrackerAdd:
    def test_add_returns_pipeline_item(self) -> None:
        t = _fresh_tracker()
        item = t.add("Acme", "REVENUE_LEAK_AUDIT")
        assert isinstance(item, PipelineItem)

    def test_add_stores_account_name(self) -> None:
        t = _fresh_tracker()
        item = t.add("Acme Motors", "REVENUE_LEAK_AUDIT")
        assert item.account_name == "Acme Motors"

    def test_add_stores_offer_id(self) -> None:
        t = _fresh_tracker()
        item = t.add("Acme", "SALES_COMMAND_CENTER")
        assert item.offer_id == "SALES_COMMAND_CENTER"

    def test_add_default_stage_is_research(self) -> None:
        t = _fresh_tracker()
        item = t.add("Acme", "REVENUE_LEAK_AUDIT")
        assert item.stage == PipelineStage.RESEARCH

    def test_add_custom_stage_stored(self) -> None:
        t = _fresh_tracker()
        item = t.add("Acme", "REVENUE_LEAK_AUDIT", stage=PipelineStage.OUTREACH)
        assert item.stage == PipelineStage.OUTREACH

    def test_add_value_sar_stored(self) -> None:
        t = _fresh_tracker()
        item = t.add("Acme", "REVENUE_LEAK_AUDIT", value_sar=20_000)
        assert item.value_sar == 20_000

    def test_add_icp_score_stored(self) -> None:
        t = _fresh_tracker()
        item = t.add("Acme", "REVENUE_LEAK_AUDIT", icp_score=75)
        assert item.icp_score == 75

    def test_add_invalid_stage_raises_value_error(self) -> None:
        t = _fresh_tracker()
        with pytest.raises(ValueError):
            t.add("Acme", "REVENUE_LEAK_AUDIT", stage="INVALID_STAGE")

    def test_add_increments_total_count(self) -> None:
        t = _fresh_tracker()
        t.add("A", "REVENUE_LEAK_AUDIT")
        t.add("B", "REVENUE_LEAK_AUDIT")
        assert len(t.list_all()) == 2

    def test_add_assigns_unique_deal_ids(self) -> None:
        t = _fresh_tracker()
        i1 = t.add("A", "REVENUE_LEAK_AUDIT")
        i2 = t.add("B", "REVENUE_LEAK_AUDIT")
        assert i1.id != i2.id


# ---------------------------------------------------------------------------
# PipelineTracker.get
# ---------------------------------------------------------------------------

class TestPipelineTrackerGet:
    def test_get_returns_item_after_add(self) -> None:
        t = _fresh_tracker()
        item = t.add("Find Me", "REVENUE_LEAK_AUDIT")
        retrieved = t.get(item.id)
        assert retrieved.id == item.id
        assert retrieved.account_name == "Find Me"

    def test_get_unknown_id_raises_key_error(self) -> None:
        t = _fresh_tracker()
        with pytest.raises(KeyError):
            t.get("deal_does_not_exist")


# ---------------------------------------------------------------------------
# Full stage progression RESEARCH -> WON
# ---------------------------------------------------------------------------

class TestFullStageProgression:
    def test_advance_through_all_stages_to_won(self) -> None:
        t = _fresh_tracker()
        item = t.add("Journey Co", "REVENUE_LEAK_AUDIT")

        progression = [
            PipelineStage.OUTREACH,
            PipelineStage.DISCOVERY,
            PipelineStage.PROPOSAL,
            PipelineStage.NEGOTIATION,
            PipelineStage.WON,
        ]
        for stage in progression:
            updated = t.update_stage(item.id, stage)
            assert updated.stage == stage

    def test_item_stage_updated_in_tracker_after_update(self) -> None:
        t = _fresh_tracker()
        item = t.add("Prog Co", "REVENUE_LEAK_AUDIT")
        t.update_stage(item.id, PipelineStage.OUTREACH)
        retrieved = t.get(item.id)
        assert retrieved.stage == PipelineStage.OUTREACH

    def test_update_stage_unknown_deal_raises_key_error(self) -> None:
        t = _fresh_tracker()
        with pytest.raises(KeyError):
            t.update_stage("ghost_deal_id", PipelineStage.WON)

    def test_update_stage_invalid_stage_raises_value_error(self) -> None:
        t = _fresh_tracker()
        item = t.add("Acme", "REVENUE_LEAK_AUDIT")
        with pytest.raises(ValueError):
            t.update_stage(item.id, "NOT_A_STAGE")

    def test_can_move_deal_to_lost(self) -> None:
        t = _fresh_tracker()
        item = t.add("Lost Deal Co", "REVENUE_LEAK_AUDIT", stage=PipelineStage.PROPOSAL)
        updated = t.update_stage(item.id, PipelineStage.LOST, owner_notes="budget_frozen")
        assert updated.stage == PipelineStage.LOST


# ---------------------------------------------------------------------------
# pipeline_summary
# ---------------------------------------------------------------------------

class TestPipelineSummary:
    def test_summary_returns_dict(self) -> None:
        t = _fresh_tracker()
        assert isinstance(t.pipeline_summary(), dict)

    def test_summary_has_total_deals_key(self) -> None:
        t = _fresh_tracker()
        summary = t.pipeline_summary()
        assert "total_deals" in summary

    def test_summary_has_by_stage_key(self) -> None:
        t = _fresh_tracker()
        summary = t.pipeline_summary()
        assert "by_stage" in summary

    def test_summary_has_total_arr_sar_key(self) -> None:
        t = _fresh_tracker()
        summary = t.pipeline_summary()
        assert "total_arr_sar" in summary

    def test_summary_total_deals_zero_on_empty_tracker(self) -> None:
        t = _fresh_tracker()
        summary = t.pipeline_summary()
        assert summary["total_deals"] == 0

    def test_summary_total_deals_matches_add_count(self) -> None:
        t = _fresh_tracker()
        t.add("A", "REVENUE_LEAK_AUDIT")
        t.add("B", "REVENUE_LEAK_AUDIT")
        t.add("C", "REVENUE_LEAK_AUDIT")
        summary = t.pipeline_summary()
        assert summary["total_deals"] == 3

    def test_by_stage_counts_correct_after_adds(self) -> None:
        t = _fresh_tracker()
        t.add("A", "REVENUE_LEAK_AUDIT", stage=PipelineStage.RESEARCH)
        t.add("B", "REVENUE_LEAK_AUDIT", stage=PipelineStage.RESEARCH)
        t.add("C", "REVENUE_LEAK_AUDIT", stage=PipelineStage.OUTREACH)
        summary = t.pipeline_summary()
        by_stage = summary["by_stage"]
        assert by_stage[PipelineStage.RESEARCH] == 2
        assert by_stage[PipelineStage.OUTREACH] == 1

    def test_total_arr_sar_is_sum_of_value_sar(self) -> None:
        t = _fresh_tracker()
        t.add("A", "REVENUE_LEAK_AUDIT", value_sar=10_000)
        t.add("B", "REVENUE_LEAK_AUDIT", value_sar=20_000)
        summary = t.pipeline_summary()
        assert summary["total_arr_sar"] == 30_000

    def test_summary_updates_after_stage_change(self) -> None:
        t = _fresh_tracker()
        item = t.add("Move Me", "REVENUE_LEAK_AUDIT", stage=PipelineStage.RESEARCH)
        before = t.pipeline_summary()["by_stage"][PipelineStage.RESEARCH]
        t.update_stage(item.id, PipelineStage.OUTREACH)
        after = t.pipeline_summary()["by_stage"][PipelineStage.RESEARCH]
        assert after == before - 1


# ---------------------------------------------------------------------------
# JSON save / load roundtrip (via tmp_pipeline_file fixture)
# ---------------------------------------------------------------------------

class TestPipelineJsonRoundtrip:
    def test_data_persisted_to_jsonl_file(self, tmp_pipeline_file: Path) -> None:
        t = PipelineTracker(path=tmp_pipeline_file)
        t.add("Persist Co", "REVENUE_LEAK_AUDIT", value_sar=5_000)
        assert tmp_pipeline_file.exists()
        content = tmp_pipeline_file.read_text(encoding="utf-8").strip()
        assert content  # file is not empty

    def test_load_restores_all_accounts(self, tmp_pipeline_file: Path) -> None:
        t1 = PipelineTracker(path=tmp_pipeline_file)
        t1.add("Alpha", "REVENUE_LEAK_AUDIT", value_sar=10_000, icp_score=80)
        t1.add("Beta", "SALES_COMMAND_CENTER", value_sar=20_000, icp_score=70)

        t2 = PipelineTracker(path=tmp_pipeline_file)
        assert len(t2.list_all()) == 2

    def test_load_restores_stage_correctly(self, tmp_pipeline_file: Path) -> None:
        t1 = PipelineTracker(path=tmp_pipeline_file)
        item = t1.add("Stage Co", "REVENUE_LEAK_AUDIT", stage=PipelineStage.DISCOVERY)

        t2 = PipelineTracker(path=tmp_pipeline_file)
        loaded = t2.get(item.id)
        assert loaded.stage == PipelineStage.DISCOVERY

    def test_save_produces_valid_jsonl(self, tmp_pipeline_file: Path) -> None:
        t = PipelineTracker(path=tmp_pipeline_file)
        t.add("JSON Co", "REVENUE_LEAK_AUDIT")
        lines = tmp_pipeline_file.read_text(encoding="utf-8").strip().splitlines()
        for line in lines:
            parsed = json.loads(line)
            assert isinstance(parsed, dict)

    def test_empty_file_loads_as_empty_tracker(self, tmp_pipeline_file: Path) -> None:
        tmp_pipeline_file.write_text("", encoding="utf-8")
        t = PipelineTracker(path=tmp_pipeline_file)
        assert len(t.list_all()) == 0


# ---------------------------------------------------------------------------
# list_all / list_by_stage
# ---------------------------------------------------------------------------

class TestListMethods:
    def test_list_all_returns_list(self) -> None:
        t = _fresh_tracker()
        assert isinstance(t.list_all(), list)

    def test_list_all_empty_on_new_tracker(self) -> None:
        t = _fresh_tracker()
        assert t.list_all() == []

    def test_list_all_sorted_by_icp_score_descending(self) -> None:
        t = _fresh_tracker()
        t.add("Low", "REVENUE_LEAK_AUDIT", icp_score=40)
        t.add("High", "REVENUE_LEAK_AUDIT", icp_score=85)
        t.add("Mid", "REVENUE_LEAK_AUDIT", icp_score=65)
        items = t.list_all()
        scores = [i.icp_score for i in items]
        assert scores == sorted(scores, reverse=True)

    def test_list_by_stage_returns_correct_items(self) -> None:
        t = _fresh_tracker()
        t.add("R1", "REVENUE_LEAK_AUDIT", stage=PipelineStage.RESEARCH)
        t.add("R2", "REVENUE_LEAK_AUDIT", stage=PipelineStage.RESEARCH)
        t.add("O1", "REVENUE_LEAK_AUDIT", stage=PipelineStage.OUTREACH)
        research = t.list_by_stage(PipelineStage.RESEARCH)
        outreach = t.list_by_stage(PipelineStage.OUTREACH)
        assert len(research) == 2
        assert len(outreach) == 1

    def test_list_by_stage_returns_empty_for_empty_stage(self) -> None:
        t = _fresh_tracker()
        t.add("Acme", "REVENUE_LEAK_AUDIT", stage=PipelineStage.RESEARCH)
        assert t.list_by_stage(PipelineStage.WON) == []


# ---------------------------------------------------------------------------
# PipelineItem.to_dict / from_dict
# ---------------------------------------------------------------------------

class TestPipelineItemSerialization:
    def test_to_dict_returns_dict(self) -> None:
        t = _fresh_tracker()
        item = t.add("Acme", "REVENUE_LEAK_AUDIT")
        assert isinstance(item.to_dict(), dict)

    def test_to_dict_has_required_keys(self) -> None:
        t = _fresh_tracker()
        item = t.add("Acme", "REVENUE_LEAK_AUDIT", value_sar=5_000, icp_score=72)
        d = item.to_dict()
        for key in ("id", "account_name", "stage", "offer_id", "value_sar", "icp_score"):
            assert key in d

    def test_from_dict_roundtrip(self) -> None:
        t = _fresh_tracker()
        item = t.add("Roundtrip Co", "REVENUE_LEAK_AUDIT", value_sar=10_000, icp_score=65)
        reconstructed = PipelineItem.from_dict(item.to_dict())
        assert reconstructed.id == item.id
        assert reconstructed.account_name == item.account_name
        assert reconstructed.stage == item.stage
        assert reconstructed.value_sar == item.value_sar
