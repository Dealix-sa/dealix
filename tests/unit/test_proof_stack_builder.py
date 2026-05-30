"""Unit tests for proof_stack_builder."""

import pytest

from auto_client_acquisition.proof_os.proof_stack_builder import (
    ProofAsset,
    ProofStack,
    ProofType,
    build_proof_stack,
    score_proof_readiness,
)


def _event(event_type: str, evidence_level: int = 3, consent: str = "granted", approval: str = "approved") -> dict:
    return {
        "event_type": event_type,
        "evidence_level": evidence_level,
        "consent_status": consent,
        "approval_status": approval,
    }


class TestBuildProofStack:
    def test_returns_proof_stack(self):
        stack = build_proof_stack("acct_1", [])
        assert isinstance(stack, ProofStack)

    def test_empty_events_zero_completeness(self):
        stack = build_proof_stack("acct_1", [])
        assert stack.completeness_score == 0

    def test_all_assets_present_in_stack(self):
        stack = build_proof_stack("acct_1", [])
        assert len(stack.assets) == len(ProofType)

    def test_payment_event_sets_payment_asset_available(self):
        stack = build_proof_stack("acct_1", [_event("payment_confirmed")])
        payment_assets = [a for a in stack.assets if a.proof_type == ProofType.PAYMENT and a.is_available]
        assert len(payment_assets) == 1

    def test_completeness_increases_with_events(self):
        stack_empty = build_proof_stack("acct_1", [])
        stack_one = build_proof_stack("acct_1", [_event("payment_confirmed")])
        assert stack_one.completeness_score > stack_empty.completeness_score

    def test_unknown_event_type_ignored(self):
        stack = build_proof_stack("acct_1", [_event("unknown_event_xyz")])
        assert stack.completeness_score == 0

    def test_duplicate_event_type_counted_once(self):
        events = [_event("payment_confirmed"), _event("payment_confirmed")]
        stack = build_proof_stack("acct_1", events)
        payment_assets = [a for a in stack.assets if a.proof_type == ProofType.PAYMENT and a.is_available]
        assert len(payment_assets) == 1

    def test_account_id_preserved(self):
        stack = build_proof_stack("my_account", [])
        assert stack.account_id == "my_account"


class TestPublishability:
    def test_l4_granted_approved_is_publishable(self):
        stack = build_proof_stack("acct_1", [_event("payment_confirmed", evidence_level=4)])
        pub_assets = [a for a in stack.assets if a.is_publishable]
        assert len(pub_assets) >= 1

    def test_l3_not_publishable(self):
        stack = build_proof_stack("acct_1", [_event("payment_confirmed", evidence_level=3)])
        payment_asset = next(a for a in stack.assets if a.proof_type == ProofType.PAYMENT and a.is_available)
        assert not payment_asset.is_publishable

    def test_no_consent_not_publishable(self):
        stack = build_proof_stack("acct_1", [_event("payment_confirmed", evidence_level=4, consent="internal_only")])
        payment_asset = next(a for a in stack.assets if a.proof_type == ProofType.PAYMENT and a.is_available)
        assert not payment_asset.is_publishable

    def test_case_study_ready_requires_high_publishable_score(self):
        # With only one payment event at L4, publishable score = 25 < 60 threshold
        stack = build_proof_stack("acct_1", [_event("payment_confirmed", evidence_level=4)])
        assert not stack.is_ready_for_case_study

    def test_private_sales_uses_l3(self):
        stack = build_proof_stack("acct_1", [_event("payment_confirmed", evidence_level=3)])
        # L3 = customer_approved, weight=25
        assert stack.private_sales_score >= 25


class TestGapAnalysis:
    def test_empty_stack_has_all_gaps(self):
        stack = build_proof_stack("acct_1", [])
        assert len(stack.gaps_ar) == len(ProofType)

    def test_filled_asset_removes_its_gap(self):
        stack = build_proof_stack("acct_1", [_event("payment_confirmed")])
        # Payment gap should no longer be in gaps
        payment_gaps = [g for g in stack.gaps_ar if "دفع" in g or "فاتورة" in g]
        assert len(payment_gaps) == 0

    def test_recommended_next_event_nonempty_when_gaps_exist(self):
        stack = build_proof_stack("acct_1", [])
        assert len(stack.recommended_next_event_ar) > 0
        assert len(stack.recommended_next_event_en) > 0

    def test_full_stack_no_more_gaps(self):
        # Provide all mapped event types
        events = [
            _event("payment_confirmed", evidence_level=4),
            _event("proof_pack_assembled", evidence_level=4),
            _event("deliverable_completed", evidence_level=4),
            _event("expansion_offered", evidence_level=4),
            _event("demo_booked", evidence_level=4),
        ]
        stack = build_proof_stack("acct_1", events)
        assert stack.completeness_score > 0


class TestScoreProofReadiness:
    def test_returns_dict(self):
        stack = build_proof_stack("acct_1", [])
        report = score_proof_readiness(stack)
        assert isinstance(report, dict)

    def test_all_required_keys_present(self):
        stack = build_proof_stack("acct_1", [])
        report = score_proof_readiness(stack)
        required_keys = {
            "account_id", "completeness_score", "publishable_score",
            "private_sales_score", "is_ready_for_case_study",
            "is_ready_for_private_sales", "recommended_next_event_ar",
            "recommended_next_event_en", "gaps", "gaps_en",
        }
        assert required_keys.issubset(report.keys())

    def test_account_id_matches(self):
        stack = build_proof_stack("test_acct", [])
        report = score_proof_readiness(stack)
        assert report["account_id"] == "test_acct"
