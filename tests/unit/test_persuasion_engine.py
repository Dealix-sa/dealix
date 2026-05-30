"""Unit tests for persuasion_engine."""

import pytest

from auto_client_acquisition.sales_os.persuasion_engine import (
    ConvictionStep,
    ObjectionResponse,
    ObjectionType,
    PainSignal,
    PainType,
    PersuasionChain,
    build_persuasion_chain,
    get_objection_response,
    known_icp_tiers,
)


def _pain(pain_type: PainType = PainType.REVENUE_LEAK, severity: int = 70, cost: int = 10000) -> PainSignal:
    return PainSignal(pain_type=pain_type, severity=severity, cost_estimate_sar=cost, frequency="monthly")


class TestBuildPersuasionChain:
    def test_returns_persuasion_chain(self):
        chain = build_persuasion_chain("agency", [_pain()])
        assert isinstance(chain, PersuasionChain)

    def test_conviction_steps_nonempty(self):
        chain = build_persuasion_chain("agency", [_pain()])
        assert len(chain.conviction_sequence) > 0

    def test_all_objection_types_included_by_default(self):
        chain = build_persuasion_chain("agency", [_pain()])
        objection_types = {o.objection_type for o in chain.objection_responses}
        assert ObjectionType.PRICE in objection_types
        assert ObjectionType.TRUST in objection_types
        assert ObjectionType.TIMING in objection_types

    def test_target_objections_filtered(self):
        chain = build_persuasion_chain(
            "agency", [_pain()],
            target_objections=[ObjectionType.PRICE, ObjectionType.TRUST],
        )
        assert len(chain.objection_responses) == 2
        types = {o.objection_type for o in chain.objection_responses}
        assert types == {ObjectionType.PRICE, ObjectionType.TRUST}

    def test_unknown_tier_falls_back_to_default(self):
        chain = build_persuasion_chain("nonexistent_tier", [_pain()])
        assert len(chain.conviction_sequence) > 0

    def test_total_pain_cost_summed(self):
        signals = [_pain(cost=5000), _pain(PainType.DATA_CHAOS, cost=3000)]
        chain = build_persuasion_chain("agency", signals)
        assert chain.total_pain_cost_sar_monthly == 8000

    def test_closing_questions_bilingual(self):
        chain = build_persuasion_chain("b2b_direct", [_pain()])
        assert len(chain.closing_questions_ar) > 0
        assert len(chain.closing_questions_en) > 0

    def test_evidence_anchors_from_pain_signals(self):
        chain = build_persuasion_chain("agency", [_pain(PainType.PROOF_GAP)])
        assert "agency_proof_pack_sample" in chain.evidence_anchors

    def test_empty_pain_signals(self):
        chain = build_persuasion_chain("agency", [])
        assert chain.total_pain_cost_sar_monthly == 0

    def test_icp_tier_stored(self):
        chain = build_persuasion_chain("executive", [_pain()])
        assert chain.icp_tier == "executive"


class TestConvictionSteps:
    def test_steps_have_bilingual_content(self):
        chain = build_persuasion_chain("agency", [_pain()])
        for step in chain.conviction_sequence:
            assert len(step.question_ar) > 0
            assert len(step.question_en) > 0
            assert len(step.purpose_ar) > 0

    def test_steps_numbered_sequentially(self):
        chain = build_persuasion_chain("agency", [_pain()])
        numbers = [s.step_number for s in chain.conviction_sequence]
        assert numbers == list(range(1, len(numbers) + 1))

    def test_last_step_is_decision_prompt(self):
        chain = build_persuasion_chain("agency", [_pain()])
        assert chain.conviction_sequence[-1].step_type == "decision_prompt"


class TestObjectionResponses:
    def test_all_objections_have_bilingual_content(self):
        for ot in ObjectionType:
            resp = get_objection_response(ot)
            assert resp is not None
            assert len(resp.response_ar) > 0
            assert len(resp.response_en) > 0
            assert len(resp.reframe_question_ar) > 0

    def test_unknown_objection_returns_none(self):
        assert get_objection_response("nonexistent") is None  # type: ignore[arg-type]


class TestKnownICPTiers:
    def test_returns_tuple(self):
        tiers = known_icp_tiers()
        assert isinstance(tiers, tuple)
        assert "agency" in tiers
        assert "b2b_direct" in tiers
        assert "executive" in tiers
