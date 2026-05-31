"""Tests for dealix-marketing-os scripts — public functions only, no API calls."""

from __future__ import annotations

import json
import tempfile
from datetime import date, timedelta
from pathlib import Path
from unittest.mock import MagicMock, patch
import sys
import types

import pytest

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

BASE = Path(__file__).parent.parent / "dealix-marketing-os"
SCRIPTS = BASE / "scripts"


def _load_module(name: str):
    """Load a script module by path without executing its main block."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)  # type: ignore
    spec.loader.exec_module(mod)  # type: ignore
    return mod


# ---------------------------------------------------------------------------
# market_scanner
# ---------------------------------------------------------------------------

class TestMarketScanner:
    def test_load_existing_names_empty_file(self, tmp_path):
        ms = _load_module("market_scanner")
        empty = tmp_path / "raw_leads.jsonl"
        empty.write_text("")
        # Patch the path used by the function
        original = ms.RAW_LEADS_PATH
        ms.RAW_LEADS_PATH = empty
        try:
            names = ms.load_existing_names()
            assert isinstance(names, set)
            assert len(names) == 0
        finally:
            ms.RAW_LEADS_PATH = original

    def test_load_existing_names_with_records(self, tmp_path):
        ms = _load_module("market_scanner")
        leads_file = tmp_path / "raw_leads.jsonl"
        leads_file.write_text(
            json.dumps({"id": "x", "company_name": "Acme Corp", "status": "raw"}) + "\n"
            + json.dumps({"id": "y", "company_name": "Beta Ltd", "status": "raw"}) + "\n"
        )
        original = ms.RAW_LEADS_PATH
        ms.RAW_LEADS_PATH = leads_file
        try:
            names = ms.load_existing_names()
            assert "acme corp" in names
            assert "beta ltd" in names
        finally:
            ms.RAW_LEADS_PATH = original

    def test_load_existing_names_skips_invalid_json(self, tmp_path):
        ms = _load_module("market_scanner")
        leads_file = tmp_path / "raw_leads.jsonl"
        leads_file.write_text("not json\n" + json.dumps({"company_name": "Good Co"}) + "\n")
        original = ms.RAW_LEADS_PATH
        ms.RAW_LEADS_PATH = leads_file
        try:
            names = ms.load_existing_names()
            assert "good co" in names
        finally:
            ms.RAW_LEADS_PATH = original

    def test_run_deduplication(self, tmp_path):
        ms = _load_module("market_scanner")
        leads_file = tmp_path / "raw_leads.jsonl"
        leads_file.write_text(
            json.dumps({"id": "existing", "company_name": "Existing Corp", "status": "raw"}) + "\n"
        )

        fake_stubs = [
            {"company_name": "Existing Corp", "website_hint": "existing.com", "sector": "facilities_management", "country": "Saudi Arabia", "source": "market_scanner_ai"},
            {"company_name": "New Corp", "website_hint": "new.com", "sector": "facilities_management", "country": "Saudi Arabia", "source": "market_scanner_ai"},
        ]

        original_leads = ms.RAW_LEADS_PATH
        original_config = ms.CONFIG_DIR
        ms.RAW_LEADS_PATH = leads_file
        ms.MEMORY_DIR = tmp_path

        with patch.object(ms, "scan_via_claude", return_value=fake_stubs), \
             patch.object(ms, "load_config", return_value={
                 "sectors": [{"id": "facilities_management", "label": "FM", "keywords": ["FM"], "min_employees": 50, "priority": 1}],
                 "regions": [{"name": "Saudi Arabia", "code": "SA", "priority": 1}],
             }):
            ms.run(sector_id="facilities_management", count=5)

        lines = [l for l in leads_file.read_text().strip().splitlines() if l]
        companies = [json.loads(l)["company_name"] for l in lines]
        assert "Existing Corp" in companies
        assert "New Corp" in companies
        assert companies.count("Existing Corp") == 1

        ms.RAW_LEADS_PATH = original_leads
        ms.CONFIG_DIR = original_config


# ---------------------------------------------------------------------------
# company_researcher
# ---------------------------------------------------------------------------

class TestCompanyResearcher:
    def test_compute_fit_score_high(self):
        cr = _load_module("company_researcher")
        scoring = {
            "dimensions": [
                {"id": "operational_complexity", "levels": {"high": 25, "medium": 15, "low": 5}},
                {"id": "data_intensity", "levels": {"high": 20, "medium": 12, "low": 4}},
                {"id": "sector_priority", "levels": {"priority_1": 20, "priority_2": 14, "priority_3": 8}},
                {"id": "buyer_accessibility", "levels": {"high": 15, "medium": 9, "low": 3}},
                {"id": "pain_signal_strength", "levels": {"strong": 10, "moderate": 6, "weak": 2}},
                {"id": "deal_size_potential", "levels": {"high": 10, "medium": 6, "low": 2}},
            ]
        }
        brief = {
            "operations_complexity": "high",
            "data_intensity": "high",
            "_sector_priority": 1,
            "_buyer_accessibility": "high",
            "_pain_signal_strength": "strong",
            "_deal_size_potential": "high",
        }
        score = cr.compute_fit_score(brief, scoring)
        assert score == 100

    def test_compute_fit_score_low(self):
        cr = _load_module("company_researcher")
        scoring = {
            "dimensions": [
                {"id": "operational_complexity", "levels": {"high": 25, "medium": 15, "low": 5}},
                {"id": "data_intensity", "levels": {"high": 20, "medium": 12, "low": 4}},
                {"id": "sector_priority", "levels": {"priority_1": 20, "priority_2": 14, "priority_3": 8}},
                {"id": "buyer_accessibility", "levels": {"high": 15, "medium": 9, "low": 3}},
                {"id": "pain_signal_strength", "levels": {"strong": 10, "moderate": 6, "weak": 2}},
                {"id": "deal_size_potential", "levels": {"high": 10, "medium": 6, "low": 2}},
            ]
        }
        brief = {
            "operations_complexity": "low",
            "data_intensity": "low",
            "_sector_priority": 3,
            "_buyer_accessibility": "low",
            "_pain_signal_strength": "weak",
            "_deal_size_potential": "low",
        }
        score = cr.compute_fit_score(brief, scoring)
        assert score == 24

    def test_compute_fit_score_capped_at_100(self):
        cr = _load_module("company_researcher")
        scoring = {
            "dimensions": [
                {"id": "operational_complexity", "levels": {"high": 60}},
                {"id": "data_intensity", "levels": {"high": 60}},
                {"id": "sector_priority", "levels": {"priority_1": 60}},
                {"id": "buyer_accessibility", "levels": {"high": 60}},
                {"id": "pain_signal_strength", "levels": {"strong": 60}},
                {"id": "deal_size_potential", "levels": {"high": 60}},
            ]
        }
        brief = {
            "operations_complexity": "high",
            "data_intensity": "high",
            "_sector_priority": 1,
            "_buyer_accessibility": "high",
            "_pain_signal_strength": "strong",
            "_deal_size_potential": "high",
        }
        score = cr.compute_fit_score(brief, scoring)
        assert score == 100

    def test_best_offer_for_sector_match(self):
        cr = _load_module("company_researcher")
        offers_config = {
            "offers": [
                {"id": "maintenance_intelligence_os", "target_sectors": ["facilities_management"]},
                {"id": "logistics_control_tower", "target_sectors": ["logistics_transport"]},
            ],
            "default_offer": "field_ops_intelligence",
        }
        assert cr.best_offer_for_sector("facilities_management", offers_config) == "maintenance_intelligence_os"

    def test_best_offer_for_sector_fallback(self):
        cr = _load_module("company_researcher")
        offers_config = {
            "offers": [{"id": "maintenance_intelligence_os", "target_sectors": ["facilities_management"]}],
            "default_offer": "field_ops_intelligence",
        }
        assert cr.best_offer_for_sector("unknown_sector", offers_config) == "field_ops_intelligence"

    def test_read_jsonl_empty(self, tmp_path):
        cr = _load_module("company_researcher")
        empty = tmp_path / "empty.jsonl"
        empty.write_text("")
        result = cr.read_jsonl(empty)
        assert result == []

    def test_read_jsonl_missing_file(self, tmp_path):
        cr = _load_module("company_researcher")
        result = cr.read_jsonl(tmp_path / "nonexistent.jsonl")
        assert result == []

    def test_rewrite_jsonl(self, tmp_path):
        cr = _load_module("company_researcher")
        path = tmp_path / "test.jsonl"
        records = [{"id": "1", "name": "A"}, {"id": "2", "name": "B"}]
        cr.rewrite_jsonl(path, records)
        lines = [l for l in path.read_text().strip().splitlines() if l]
        assert len(lines) == 2
        assert json.loads(lines[0])["id"] == "1"


# ---------------------------------------------------------------------------
# offer_router
# ---------------------------------------------------------------------------

class TestOfferRouter:
    def test_tier_for_score_a(self):
        router = _load_module("offer_router")
        scoring = {"tiers": {"A": {"min_score": 80}, "B": {"min_score": 60}}}
        assert router.tier_for_score(85, scoring) == "A"
        assert router.tier_for_score(80, scoring) == "A"

    def test_tier_for_score_b(self):
        router = _load_module("offer_router")
        scoring = {"tiers": {"A": {"min_score": 80}, "B": {"min_score": 60}}}
        assert router.tier_for_score(65, scoring) == "B"
        assert router.tier_for_score(60, scoring) == "B"

    def test_tier_for_score_nurture(self):
        router = _load_module("offer_router")
        scoring = {"tiers": {"A": {"min_score": 80}, "B": {"min_score": 60}}}
        assert router.tier_for_score(45, scoring) == "nurture"
        assert router.tier_for_score(0, scoring) == "nurture"


# ---------------------------------------------------------------------------
# draft_writer
# ---------------------------------------------------------------------------

class TestDraftWriter:
    def test_draft_types_for_tier_a(self):
        dw = _load_module("draft_writer")
        types = dw.draft_types_for_tier("A")
        assert "cold_email" in types
        assert "linkedin_message" in types
        assert "discovery_call_agenda" in types
        assert "proposal_seed" in types
        assert len(types) == 8

    def test_draft_types_for_tier_b(self):
        dw = _load_module("draft_writer")
        types = dw.draft_types_for_tier("B")
        assert "cold_email" in types
        assert "linkedin_message" in types
        assert len(types) == 4
        assert "discovery_call_agenda" not in types

    def test_draft_types_for_nurture(self):
        dw = _load_module("draft_writer")
        types = dw.draft_types_for_tier("nurture")
        assert types == ["cold_email", "linkedin_message"]

    def test_offer_label_for_id(self):
        dw = _load_module("draft_writer")
        offers_config = {
            "offers": [
                {"id": "maintenance_intelligence_os", "label": "Maintenance Intelligence OS"},
            ]
        }
        assert dw.offer_label_for_id("maintenance_intelligence_os", offers_config) == "Maintenance Intelligence OS"

    def test_offer_label_for_id_missing(self):
        dw = _load_module("draft_writer")
        offers_config = {"offers": []}
        assert dw.offer_label_for_id("unknown_offer", offers_config) == "unknown_offer"

    def test_read_jsonl(self, tmp_path):
        dw = _load_module("draft_writer")
        f = tmp_path / "test.jsonl"
        f.write_text(json.dumps({"id": "1"}) + "\n" + json.dumps({"id": "2"}) + "\n")
        result = dw.read_jsonl(f)
        assert len(result) == 2


# ---------------------------------------------------------------------------
# draft_quality_gate
# ---------------------------------------------------------------------------

class TestDraftQualityGate:
    def test_read_jsonl_valid(self, tmp_path):
        dqg = _load_module("draft_quality_gate")
        f = tmp_path / "drafts.jsonl"
        f.write_text(json.dumps({"id": "d1", "status": "draft_generated"}) + "\n")
        records = dqg.read_jsonl(f)
        assert records[0]["id"] == "d1"

    def test_rewrite_jsonl_overwrites(self, tmp_path):
        dqg = _load_module("draft_quality_gate")
        f = tmp_path / "drafts.jsonl"
        f.write_text(json.dumps({"id": "old"}) + "\n")
        dqg.rewrite_jsonl(f, [{"id": "new"}])
        result = dqg.read_jsonl(f)
        assert len(result) == 1
        assert result[0]["id"] == "new"

    def test_run_no_eligible_drafts(self, tmp_path):
        dqg = _load_module("draft_quality_gate")
        original = dqg.DRAFT_QUEUE_PATH
        f = tmp_path / "drafts.jsonl"
        f.write_text(json.dumps({"id": "d1", "status": "approved_for_review"}) + "\n")
        dqg.DRAFT_QUEUE_PATH = f
        # Should not raise; should print nothing meaningful
        with patch.object(dqg, "evaluate_draft_via_claude") as mock_eval:
            dqg.run()
            mock_eval.assert_not_called()
        dqg.DRAFT_QUEUE_PATH = original


# ---------------------------------------------------------------------------
# reply_processor
# ---------------------------------------------------------------------------

class TestReplyProcessor:
    def test_next_actions_complete(self):
        rp = _load_module("reply_processor")
        for cls in rp.REPLY_CLASSIFICATIONS:
            assert cls in rp.NEXT_ACTIONS, f"Missing next action for: {cls}"

    def test_opt_out_triggers_suppression(self, tmp_path):
        rp = _load_module("reply_processor")
        supp_file = tmp_path / "suppression.jsonl"
        replies_file = tmp_path / "replies.jsonl"
        opps_file = tmp_path / "opportunities.jsonl"
        supp_file.write_text("")
        replies_file.write_text("")
        opps_file.write_text("")

        original_supp = rp.SUPPRESSION_PATH
        original_replies = rp.REPLIES_PATH
        original_opps = rp.OPPORTUNITIES_PATH
        rp.SUPPRESSION_PATH = supp_file
        rp.REPLIES_PATH = replies_file
        rp.OPPORTUNITIES_PATH = opps_file

        classification_result = {
            "classification": "opt_out",
            "key_signal": "please remove me",
            "sentiment": "negative",
            "urgency": "high",
            "reasoning": "Explicit opt-out request",
        }

        with patch.object(rp, "classify_reply_via_claude", return_value=classification_result):
            rp.process_reply_record({
                "company_id": "test-001",
                "company_name": "Test Co",
                "reply_text": "Please remove me from your list.",
            })

        suppressed = [json.loads(l) for l in supp_file.read_text().strip().splitlines() if l]
        assert len(suppressed) == 1
        assert suppressed[0]["company_id"] == "test-001"
        assert suppressed[0]["reason"] == "opt_out"

        rp.SUPPRESSION_PATH = original_supp
        rp.REPLIES_PATH = original_replies
        rp.OPPORTUNITIES_PATH = original_opps

    def test_reply_classifications_list(self):
        rp = _load_module("reply_processor")
        assert "interested" in rp.REPLY_CLASSIFICATIONS
        assert "opt_out" in rp.REPLY_CLASSIFICATIONS
        assert "not_interested" in rp.REPLY_CLASSIFICATIONS
        assert len(rp.REPLY_CLASSIFICATIONS) == 8


# ---------------------------------------------------------------------------
# suppression_manager
# ---------------------------------------------------------------------------

class TestSuppressionManager:
    def test_is_suppressed_false_when_empty(self, tmp_path):
        sm = _load_module("suppression_manager")
        f = tmp_path / "suppression.jsonl"
        f.write_text("")
        original = sm.SUPPRESSION_PATH
        sm.SUPPRESSION_PATH = f
        try:
            assert sm.is_suppressed("company-xyz") is False
        finally:
            sm.SUPPRESSION_PATH = original

    def test_add_suppression(self, tmp_path):
        sm = _load_module("suppression_manager")
        f = tmp_path / "suppression.jsonl"
        f.write_text("")
        original = sm.SUPPRESSION_PATH
        sm.SUPPRESSION_PATH = f
        try:
            sm.add_suppression("cid-001", "Test Co", "opt_out")
            records = sm.read_jsonl(f)
            assert len(records) == 1
            assert records[0]["company_id"] == "cid-001"
        finally:
            sm.SUPPRESSION_PATH = original

    def test_add_suppression_idempotent(self, tmp_path):
        sm = _load_module("suppression_manager")
        f = tmp_path / "suppression.jsonl"
        f.write_text("")
        original = sm.SUPPRESSION_PATH
        sm.SUPPRESSION_PATH = f
        try:
            sm.add_suppression("cid-001", "Test Co", "opt_out")
            sm.add_suppression("cid-001", "Test Co", "opt_out")
            records = sm.read_jsonl(f)
            assert len(records) == 1
        finally:
            sm.SUPPRESSION_PATH = original

    def test_is_suppressed_true_after_add(self, tmp_path):
        sm = _load_module("suppression_manager")
        f = tmp_path / "suppression.jsonl"
        f.write_text("")
        original = sm.SUPPRESSION_PATH
        sm.SUPPRESSION_PATH = f
        try:
            sm.add_suppression("cid-002", "Corp B", "manual")
            assert sm.is_suppressed("cid-002") is True
            assert sm.is_suppressed("cid-999") is False
        finally:
            sm.SUPPRESSION_PATH = original

    def test_check_batch(self, tmp_path):
        sm = _load_module("suppression_manager")
        f = tmp_path / "suppression.jsonl"
        f.write_text(json.dumps({"company_id": "cid-A", "reason": "opt_out"}) + "\n")
        original = sm.SUPPRESSION_PATH
        sm.SUPPRESSION_PATH = f
        try:
            result = sm.check_batch(["cid-A", "cid-B", "cid-C"])
            assert result["cid-A"] is True
            assert result["cid-B"] is False
            assert result["cid-C"] is False
        finally:
            sm.SUPPRESSION_PATH = original


# ---------------------------------------------------------------------------
# follow_up_manager
# ---------------------------------------------------------------------------

class TestFollowUpManager:
    def test_compute_followup_dates(self):
        fm = _load_module("follow_up_manager")
        base = "2026-05-31"
        schedule = fm.compute_followup_dates(base)
        assert "followup_1" in schedule
        assert "followup_2" in schedule
        assert "referral_request" in schedule
        from datetime import date, timedelta
        base_date = date.fromisoformat(base)
        assert schedule["followup_1"] == (base_date + timedelta(days=5)).isoformat()
        assert schedule["followup_2"] == (base_date + timedelta(days=12)).isoformat()
        assert schedule["referral_request"] == (base_date + timedelta(days=21)).isoformat()

    def test_compute_followup_dates_invalid_input(self):
        fm = _load_module("follow_up_manager")
        schedule = fm.compute_followup_dates("not-a-date")
        assert "followup_1" in schedule

    def test_list_due_followups_empty(self, tmp_path):
        fm = _load_module("follow_up_manager")
        f = tmp_path / "approved_sends.jsonl"
        f.write_text("")
        original_sends = fm.APPROVED_SENDS_PATH
        original_drafts = fm.DRAFT_QUEUE_PATH
        fm.APPROVED_SENDS_PATH = f
        fm.DRAFT_QUEUE_PATH = tmp_path / "draft_queue.jsonl"
        (tmp_path / "draft_queue.jsonl").write_text("")
        try:
            due = fm.list_due_followups()
            assert due == []
        finally:
            fm.APPROVED_SENDS_PATH = original_sends
            fm.DRAFT_QUEUE_PATH = original_drafts


# ---------------------------------------------------------------------------
# founder_marketing_report
# ---------------------------------------------------------------------------

class TestFounderMarketingReport:
    def test_build_stats_empty_memory(self, tmp_path):
        fmr = _load_module("founder_marketing_report")
        original_memory = fmr.MEMORY_DIR
        fmr.MEMORY_DIR = tmp_path
        for fname in ["raw_leads.jsonl", "company_briefs.jsonl", "opportunities.jsonl",
                      "draft_queue.jsonl", "approved_sends.jsonl", "replies.jsonl", "learning_log.jsonl"]:
            (tmp_path / fname).write_text("")
        try:
            stats = fmr.build_stats()
            assert "date" in stats
            assert "tier_a_companies" in stats
            assert stats["tier_a_companies"] == 0
            assert stats["ready_for_review"] == 0
        finally:
            fmr.MEMORY_DIR = original_memory

    def test_render_markdown_structure(self):
        fmr = _load_module("founder_marketing_report")
        stats = {
            "date": "2026-05-31",
            "raw_scanned": 5,
            "qualified_companies": 3,
            "tier_a_companies": 2,
            "briefs_completed": 3,
            "drafts_generated": 8,
            "drafts_passed_gate": 5,
            "ready_for_review": 5,
            "interested_count": 1,
            "top_companies": [],
            "top_angles": ["Specific observation about reactive maintenance costs"],
            "total_opportunities": 3,
            "total_replies": 1,
            "total_approved_sends": 0,
        }
        persuasion_config = {"daily_limits": {"sends_per_day": 20}}
        md = fmr.render_markdown(stats, persuasion_config)
        assert "# Dealix Daily Marketing Report" in md
        assert "2026-05-31" in md
        assert "Tier A companies" in md
        assert "Founder Actions Today" in md


# ---------------------------------------------------------------------------
# learning_agent
# ---------------------------------------------------------------------------

class TestLearningAgent:
    def test_render_learning_report(self):
        la = _load_module("learning_agent")
        analysis = {
            "top_performing_angles": ["Reactive maintenance cost angle"],
            "high_response_sectors": ["facilities_management"],
            "best_performing_subjects": ["Operations question for {company}"],
            "ctas_that_generate_meetings": ["30-minute diagnostic call"],
            "offers_opening_conversation": ["Maintenance Intelligence OS"],
            "phrases_to_avoid": ["world-class", "paradigm shift"],
            "followup_timing_insight": "Day 5 follow-ups outperform day 3 by 2x",
            "overall_response_rate_estimate": "12%",
            "key_insights": ["FM sector responds best to cost-of-inaction framing"],
            "persuasion_yml_suggestions": ["Strengthen the pain amplification step with cost data"],
        }
        data_summary = {
            "total_replies": 10,
            "total_drafts": 50,
            "total_opportunities": 20,
            "reply_classifications": {"interested": 3, "not_now": 5, "opt_out": 2},
        }
        report = la.render_learning_report(analysis, data_summary)
        assert "# Dealix Learning Agent Report" in report
        assert "Reactive maintenance cost angle" in report
        assert "persuasion.yml" in report
        assert "Strengthen the pain amplification" in report

    def test_read_jsonl_empty(self, tmp_path):
        la = _load_module("learning_agent")
        f = tmp_path / "empty.jsonl"
        f.write_text("")
        assert la.read_jsonl(f) == []


# ---------------------------------------------------------------------------
# pipeline_runner
# ---------------------------------------------------------------------------

class TestPipelineRunner:
    def test_pipeline_steps_list(self):
        pr = _load_module("pipeline_runner")
        step_ids = [s[0] for s in pr.PIPELINE_STEPS]
        assert "scan" in step_ids
        assert "research" in step_ids
        assert "route" in step_ids
        assert "draft" in step_ids
        assert "gate" in step_ids
        assert "report" in step_ids
        assert len(step_ids) == 6

    def test_run_dry_run_completes(self, capsys):
        pr = _load_module("pipeline_runner")
        pr.run(["scan", "report"], dry_run=True, company_limit=5)
        captured = capsys.readouterr()
        assert "Pipeline complete" in captured.out

    def test_run_skips_unselected_steps(self, capsys):
        pr = _load_module("pipeline_runner")
        pr.run(["report"], dry_run=True, company_limit=5)
        captured = capsys.readouterr()
        assert "Pipeline complete" in captured.out


# ---------------------------------------------------------------------------
# Doctrine guard: draft content must pass governance check
# ---------------------------------------------------------------------------

class TestDraftGovernanceGuard:
    """Ensure generated draft content passes the governance policy check."""

    def test_seed_draft_passes_policy_check(self):
        """The seed draft in draft_queue.jsonl must not contain forbidden patterns."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from auto_client_acquisition.governance_os import policy_check_draft
        draft_queue = BASE / "memory" / "draft_queue.jsonl"
        if not draft_queue.exists():
            pytest.skip("No draft_queue.jsonl present")
        with open(draft_queue) as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                record = json.loads(line)
                text = f"{record.get('subject', '')} {record.get('body', '')}"
                result = policy_check_draft(text)
                assert result.allowed, (
                    f"Seed draft {record.get('id')} failed governance: {result.issues}"
                )
