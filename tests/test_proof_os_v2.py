"""Tests for the expanded Proof OS — Proof Pack v2, Decision Passport, Evidence Chain."""

from __future__ import annotations

import json

import pytest

from auto_client_acquisition.proof_os import (
    PROOF_PACK_V2_SECTIONS,
    SECTION_LABELS_AR,
    SECTION_LABELS_EN,
    ApprovalLevel,
    Confidence,
    EvidenceChain,
    GENESIS_HASH,
    ProofPackV2,
    Reversibility,
    Sensitivity,
    bilingual_completeness_score,
    build_empty_proof_pack_v2,
    composite_proof_score,
    evidence_depth_score,
    issue_passport,
    merge_proof_pack_v2,
    new_chain,
    new_proof_pack,
    passport_matches_content,
    proof_strength_band,
    render_json,
    render_markdown,
)


class TestProofPackV2:
    def test_canonical_sections_have_bilingual_labels(self) -> None:
        for section in PROOF_PACK_V2_SECTIONS:
            assert section in SECTION_LABELS_AR, f"missing AR label for {section}"
            assert section in SECTION_LABELS_EN, f"missing EN label for {section}"

    def test_empty_pack_has_every_canonical_section(self) -> None:
        pack = build_empty_proof_pack_v2()
        for section in PROOF_PACK_V2_SECTIONS:
            assert section in pack
            assert pack[section] == ""

    def test_merge_drops_unknown_keys(self) -> None:
        base = build_empty_proof_pack_v2()
        merged = merge_proof_pack_v2(base, {"problem": "x", "fake": "y"})
        assert merged["problem"] == "x"
        assert "fake" not in merged

    def test_new_proof_pack_validates_offer_tier(self) -> None:
        with pytest.raises(ValueError, match="unknown offer_tier"):
            new_proof_pack(
                tenant_id="t1",
                customer_handle="cust",
                offer_tier="unknown",
            )

    def test_new_proof_pack_requires_tenant_and_customer(self) -> None:
        with pytest.raises(ValueError, match="tenant_id"):
            new_proof_pack(
                tenant_id="",
                customer_handle="cust",
                offer_tier="free_diagnostic",
            )
        with pytest.raises(ValueError, match="customer_handle"):
            new_proof_pack(
                tenant_id="t1",
                customer_handle="",
                offer_tier="free_diagnostic",
            )

    def test_is_complete_requires_both_languages(self) -> None:
        pack = new_proof_pack(
            tenant_id="t1",
            customer_handle="cust",
            offer_tier="free_diagnostic",
        )
        ok, missing = pack.is_complete()
        assert not ok
        # Empty pack should show all sections missing in BOTH languages.
        assert any("(ar)" in m for m in missing)
        assert any("(en)" in m for m in missing)

    def test_set_section_writes_to_both_languages(self) -> None:
        pack = new_proof_pack(
            tenant_id="t1",
            customer_handle="cust",
            offer_tier="sprint_499",
        )
        pack.set_section("problem", ar="مشكلة", en="problem")
        assert pack.sections_ar["problem"] == "مشكلة"
        assert pack.sections_en["problem"] == "problem"

    def test_set_section_rejects_unknown(self) -> None:
        pack = new_proof_pack(
            tenant_id="t1",
            customer_handle="cust",
            offer_tier="sprint_499",
        )
        with pytest.raises(ValueError, match="unknown section"):
            pack.set_section("fake_section", ar="x", en="y")

    def test_render_markdown_includes_both_languages_for_every_section(self) -> None:
        pack = new_proof_pack(
            tenant_id="t1",
            customer_handle="cust",
            offer_tier="free_diagnostic",
        )
        pack.set_section("problem", ar="مشكلة المبيعات", en="sales problem")
        pack.set_section("executive_summary", ar="ملخص", en="summary")
        md = render_markdown(pack)
        assert "مشكلة المبيعات" in md
        assert "sales problem" in md
        for section in PROOF_PACK_V2_SECTIONS:
            assert SECTION_LABELS_AR[section] in md
            assert SECTION_LABELS_EN[section] in md

    def test_render_json_round_trips(self) -> None:
        pack = new_proof_pack(
            tenant_id="t1",
            customer_handle="cust",
            offer_tier="free_diagnostic",
        )
        pack.set_section("problem", ar="x", en="y")
        as_json = render_json(pack)
        parsed = json.loads(as_json)
        assert parsed["pack_id"] == pack.pack_id
        assert parsed["sections_ar"]["problem"] == "x"
        assert parsed["sections_en"]["problem"] == "y"


class TestDecisionPassport:
    def test_passport_requires_bilingual_summaries(self) -> None:
        with pytest.raises(ValueError, match="summary_ar"):
            issue_passport(
                tenant_id="t1",
                decision_type="icp_classification",
                summary_ar="",
                summary_en="present",
                content={"x": 1},
            )
        with pytest.raises(ValueError, match="summary_en"):
            issue_passport(
                tenant_id="t1",
                decision_type="icp_classification",
                summary_ar="حاضر",
                summary_en="",
                content={"x": 1},
            )

    def test_passport_rejects_unknown_decision_type(self) -> None:
        with pytest.raises(ValueError, match="unknown decision_type"):
            issue_passport(
                tenant_id="t1",
                decision_type="not_a_real_type",
                summary_ar="x",
                summary_en="y",
                content={"x": 1},
            )

    def test_passport_classifies_irreversible_as_founder_approval(self) -> None:
        p = issue_passport(
            tenant_id="t1",
            decision_type="proof_pack_assembly",
            summary_ar="عربي",
            summary_en="english",
            content={"x": 1},
            reversibility=Reversibility.R3_IRREVERSIBLE,
        )
        assert p.approval_level == ApprovalLevel.A2_FOUNDER
        assert p.requires_human
        assert p.is_irreversible

    def test_passport_classifies_regulated_pii_external_as_founder(self) -> None:
        p = issue_passport(
            tenant_id="t1",
            decision_type="outreach_draft",
            summary_ar="عربي",
            summary_en="english",
            content={"x": 1},
            sensitivity=Sensitivity.S3_REGULATED_PII,
            external_action=True,
        )
        assert p.approval_level == ApprovalLevel.A2_FOUNDER
        assert p.is_regulated_pii

    def test_passport_content_hash_matches(self) -> None:
        content = {"hello": "world", "n": 7}
        p = issue_passport(
            tenant_id="t1",
            decision_type="icp_classification",
            summary_ar="ع",
            summary_en="e",
            content=content,
        )
        assert passport_matches_content(p, content)
        assert not passport_matches_content(p, {"hello": "world", "n": 8})


class TestEvidenceChain:
    def test_chain_requires_run_and_tenant(self) -> None:
        with pytest.raises(ValueError, match="run_id"):
            EvidenceChain(run_id="", tenant_id="t1")
        with pytest.raises(ValueError, match="tenant_id"):
            EvidenceChain(run_id="r1", tenant_id="")

    def test_chain_links_use_genesis_hash_for_first_link(self) -> None:
        chain = new_chain(tenant_id="t1")
        link = chain.append(
            layer="L1_source_passport",
            artifact_type="test",
            content={"a": 1},
            summary="first",
        )
        assert link.prev_hash == GENESIS_HASH
        assert len(chain) == 1

    def test_chain_links_chain_correctly(self) -> None:
        chain = new_chain(tenant_id="t1")
        link1 = chain.append(
            layer="L1_source_passport",
            artifact_type="t",
            content={"a": 1},
            summary="one",
        )
        link2 = chain.append(
            layer="L2_data_quality",
            artifact_type="t",
            content={"b": 2},
            summary="two",
        )
        assert link2.prev_hash == link1.chain_hash
        assert link2.chain_hash != link1.chain_hash

    def test_chain_verify_passes_on_pristine_chain(self) -> None:
        chain = new_chain(tenant_id="t1")
        for i in range(5):
            chain.append(
                layer="L7_proof_pack",
                artifact_type="t",
                content={"i": i},
                summary=f"step{i}",
            )
        ok, errors = chain.verify()
        assert ok, errors
        assert errors == ()

    def test_chain_links_for_layer_filters(self) -> None:
        chain = new_chain(tenant_id="t1")
        chain.append(
            layer="L1_source_passport", artifact_type="t",
            content={}, summary="s",
        )
        chain.append(
            layer="L7_proof_pack", artifact_type="t",
            content={}, summary="s",
        )
        chain.append(
            layer="L7_proof_pack", artifact_type="t2",
            content={}, summary="s",
        )
        assert len(chain.links_for_layer("L7_proof_pack")) == 2

    def test_chain_rejects_empty_summary(self) -> None:
        chain = new_chain(tenant_id="t1")
        with pytest.raises(ValueError, match="summary"):
            chain.append(
                layer="L1_source_passport", artifact_type="t",
                content={}, summary="",
            )


class TestProofScore:
    def test_evidence_depth_grows_log_scaled(self) -> None:
        assert evidence_depth_score(0) == 0
        # Each step adds less than the previous (diminishing returns).
        s1 = evidence_depth_score(1)
        s5 = evidence_depth_score(5)
        s10 = evidence_depth_score(10)
        s50 = evidence_depth_score(50)
        assert s1 < s5 < s10 < s50
        assert s50 - s10 < s10 - s1

    def test_composite_score_caps_blocked_governance(self) -> None:
        sections_full = {k: "x" for k in PROOF_PACK_V2_SECTIONS}
        clean = composite_proof_score(
            sections_ar=sections_full,
            sections_en=sections_full,
            evidence_count=20,
            governance_blocked=False,
        )
        blocked = composite_proof_score(
            sections_ar=sections_full,
            sections_en=sections_full,
            evidence_count=20,
            governance_blocked=True,
        )
        assert clean >= 85
        assert blocked <= 69

    def test_bilingual_completeness_is_average(self) -> None:
        full = {k: "x" for k in PROOF_PACK_V2_SECTIONS}
        empty = build_empty_proof_pack_v2()
        # Half AR + full EN → ~50
        half = {k: ("y" if i % 2 == 0 else "") for i, k in enumerate(PROOF_PACK_V2_SECTIONS)}
        score = bilingual_completeness_score(sections_ar=half, sections_en=full)
        assert 60 <= score <= 80, f"unexpected blend score: {score}"
        zero = bilingual_completeness_score(sections_ar=empty, sections_en=empty)
        assert zero == 0

    def test_proof_strength_bands(self) -> None:
        assert proof_strength_band(95) == "case_candidate"
        assert proof_strength_band(75) == "sales_support"
        assert proof_strength_band(60) == "internal_learning"
        assert proof_strength_band(10) == "weak_proof"
