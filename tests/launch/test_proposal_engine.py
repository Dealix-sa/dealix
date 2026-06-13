"""Tests for dealix.launch_os.proposal_engine.

Actual interface:
    ProposalPack: dataclass with id, account_name, offer_id, offer_name_ar,
                  value_prop_ar, scope_items, timeline_weeks, investment_sar,
                  roi_narrative_ar, proof_references, next_step_ar, problem_ar,
                  out_of_scope, pricing_status, approval_required, evidence_level,
                  created_at_iso

    build_proposal(account, offer_id, discovery_notes, *, pricing_status,
                   approval_required, evidence_level) -> ProposalPack

    render_markdown(pack: ProposalPack) -> str

Canonical offer IDs from _OFFER_CATALOGUE:
    REVENUE_LEAK_AUDIT, WHATSAPP_FOLLOWUP_OS, SALES_COMMAND_CENTER,
    PROPOSAL_PROOF_PACK_OS, AI_OPERATING_SYSTEM_FOR_SMB, CUSTOM_ENTERPRISE_OS
"""

from __future__ import annotations

from typing import Any

import pytest

from dealix.launch_os.proposal_engine import (
    ProposalPack,
    build_proposal,
    render_markdown,
)


# ---------------------------------------------------------------------------
# Canonical offer IDs from the catalogue
# ---------------------------------------------------------------------------

VALID_OFFER_IDS = [
    "REVENUE_LEAK_AUDIT",
    "WHATSAPP_FOLLOWUP_OS",
    "SALES_COMMAND_CENTER",
    "PROPOSAL_PROOF_PACK_OS",
    "AI_OPERATING_SYSTEM_FOR_SMB",
    "CUSTOM_ENTERPRISE_OS",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _account(**overrides: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "account_id": "acc_001",
        "account_name": "شركة النخبة للتقنية",
        "sector": "automotive",
    }
    base.update(overrides)
    return base


def _build(
    offer_id: str = "REVENUE_LEAK_AUDIT",
    discovery_notes: dict[str, Any] | None = None,
    **account_overrides: Any,
) -> ProposalPack:
    return build_proposal(
        _account(**account_overrides),
        offer_id=offer_id,
        discovery_notes=discovery_notes or {},
    )


# ---------------------------------------------------------------------------
# build_proposal — offer catalogue coverage
# ---------------------------------------------------------------------------

class TestBuildProposalOffers:
    @pytest.mark.parametrize("offer_id", VALID_OFFER_IDS)
    def test_build_proposal_for_each_offer_returns_proposal_pack(self, offer_id: str) -> None:
        pack = _build(offer_id=offer_id)
        assert isinstance(pack, ProposalPack)

    @pytest.mark.parametrize("offer_id", VALID_OFFER_IDS)
    def test_offer_id_recorded_in_pack(self, offer_id: str) -> None:
        pack = _build(offer_id=offer_id)
        assert pack.offer_id == offer_id

    @pytest.mark.parametrize("offer_id", VALID_OFFER_IDS)
    def test_pack_has_non_empty_offer_name_ar(self, offer_id: str) -> None:
        pack = _build(offer_id=offer_id)
        assert pack.offer_name_ar.strip(), f"{offer_id} has empty offer_name_ar"

    @pytest.mark.parametrize("offer_id", VALID_OFFER_IDS)
    def test_pack_has_non_empty_scope_items(self, offer_id: str) -> None:
        pack = _build(offer_id=offer_id)
        assert isinstance(pack.scope_items, list)
        assert len(pack.scope_items) > 0, f"{offer_id} has no scope_items"

    def test_unknown_offer_id_falls_back_gracefully(self) -> None:
        """An unrecognised offer ID should not crash — it falls back to empty catalogue data."""
        pack = _build(offer_id="NONEXISTENT_OFFER")
        assert isinstance(pack, ProposalPack)
        # offer_id must still be preserved
        assert pack.offer_id == "NONEXISTENT_OFFER"


# ---------------------------------------------------------------------------
# Required pack fields
# ---------------------------------------------------------------------------

class TestProposalPackFields:
    def test_pack_has_id(self) -> None:
        pack = _build()
        assert pack.id and isinstance(pack.id, str)

    def test_pack_id_starts_with_prop(self) -> None:
        pack = _build()
        assert pack.id.startswith("prop_")

    def test_pack_has_account_name(self) -> None:
        pack = _build()
        assert pack.account_name == "شركة النخبة للتقنية"

    def test_pack_has_investment_sar_as_int(self) -> None:
        pack = _build()
        assert isinstance(pack.investment_sar, int)

    def test_pack_has_value_prop_ar(self) -> None:
        pack = _build()
        assert hasattr(pack, "value_prop_ar")
        assert isinstance(pack.value_prop_ar, str)

    def test_pack_has_timeline_weeks_as_int(self) -> None:
        pack = _build()
        assert isinstance(pack.timeline_weeks, int)
        assert pack.timeline_weeks > 0

    def test_pack_has_roi_narrative_ar(self) -> None:
        pack = _build()
        assert hasattr(pack, "roi_narrative_ar")
        assert isinstance(pack.roi_narrative_ar, str)

    def test_pack_has_proof_references_as_list(self) -> None:
        pack = _build()
        assert isinstance(pack.proof_references, list)

    def test_pack_has_next_step_ar(self) -> None:
        pack = _build()
        assert pack.next_step_ar.strip()

    def test_pack_has_out_of_scope_as_list(self) -> None:
        pack = _build()
        assert isinstance(pack.out_of_scope, list)

    def test_pack_has_pricing_status(self) -> None:
        pack = _build()
        assert hasattr(pack, "pricing_status")

    def test_pack_has_evidence_level(self) -> None:
        pack = _build()
        assert hasattr(pack, "evidence_level")

    def test_pack_has_created_at_iso(self) -> None:
        pack = _build()
        assert "T" in pack.created_at_iso  # ISO timestamp contains T separator


# ---------------------------------------------------------------------------
# Arabic content presence
# ---------------------------------------------------------------------------

class TestArabicContent:
    @pytest.mark.parametrize("offer_id", VALID_OFFER_IDS)
    def test_value_prop_ar_contains_arabic_characters(self, offer_id: str) -> None:
        pack = _build(offer_id=offer_id)
        has_arabic = any(ord(c) > 127 for c in pack.value_prop_ar)
        assert has_arabic, f"{offer_id} value_prop_ar has no Arabic characters"

    def test_offer_name_ar_is_non_empty_and_has_arabic(self) -> None:
        pack = _build(offer_id="REVENUE_LEAK_AUDIT")
        assert pack.offer_name_ar.strip()
        assert any(ord(c) > 127 for c in pack.offer_name_ar)


# ---------------------------------------------------------------------------
# Discovery notes integration
# ---------------------------------------------------------------------------

class TestDiscoveryNotesIntegration:
    def test_leakage_sar_appears_in_roi_narrative(self) -> None:
        pack = _build(
            offer_id="REVENUE_LEAK_AUDIT",
            discovery_notes={"leakage_sar": 200_000},
        )
        # 200000 should appear in some form in the narrative
        assert "200" in pack.roi_narrative_ar or "200,000" in pack.roi_narrative_ar

    def test_pain_ar_from_notes_used_as_problem_ar(self) -> None:
        pain = "فقدان العملاء المحتملين بعد الزيارة"
        pack = _build(
            offer_id="REVENUE_LEAK_AUDIT",
            discovery_notes={"pain_ar": pain},
        )
        assert pack.problem_ar == pain

    def test_extra_proof_ref_prepended_to_list(self) -> None:
        pack = _build(
            offer_id="REVENUE_LEAK_AUDIT",
            discovery_notes={"proof_ref": "عميل X حقق نتيجة Y"},
        )
        assert pack.proof_references[0] == "عميل X حقق نتيجة Y"

    def test_empty_discovery_notes_does_not_crash(self) -> None:
        pack = _build(discovery_notes={})
        assert isinstance(pack, ProposalPack)

    def test_zero_leakage_gives_pending_roi_narrative(self) -> None:
        pack = _build(discovery_notes={"leakage_sar": 0})
        assert pack.roi_narrative_ar.strip()


# ---------------------------------------------------------------------------
# render_markdown
# ---------------------------------------------------------------------------

class TestRenderMarkdown:
    def test_render_markdown_returns_string(self) -> None:
        pack = _build()
        md = render_markdown(pack)
        assert isinstance(md, str)

    def test_render_markdown_is_non_empty(self) -> None:
        pack = _build()
        md = render_markdown(pack)
        assert md.strip()

    def test_render_markdown_contains_h1_heading(self) -> None:
        pack = _build()
        md = render_markdown(pack)
        assert "# " in md

    def test_render_markdown_contains_account_name(self) -> None:
        pack = _build(account_name="Acme Motors")
        md = render_markdown(pack)
        assert "Acme Motors" in md

    def test_render_markdown_contains_offer_id(self) -> None:
        pack = _build(offer_id="REVENUE_LEAK_AUDIT")
        md = render_markdown(pack)
        assert "REVENUE_LEAK_AUDIT" in md

    def test_render_markdown_contains_sar_or_arabic_currency(self) -> None:
        pack = _build()
        md = render_markdown(pack)
        assert "ريال" in md or "SAR" in md

    def test_render_markdown_contains_scope_section(self) -> None:
        pack = _build()
        md = render_markdown(pack)
        assert "نطاق" in md or "scope" in md.lower()

    def test_render_markdown_contains_roi_narrative(self) -> None:
        pack = _build(discovery_notes={"leakage_sar": 50_000})
        md = render_markdown(pack)
        assert pack.roi_narrative_ar[:20] in md

    def test_render_markdown_contains_next_step(self) -> None:
        pack = _build()
        md = render_markdown(pack)
        assert pack.next_step_ar in md

    @pytest.mark.parametrize("offer_id", VALID_OFFER_IDS)
    def test_render_markdown_valid_for_all_offers(self, offer_id: str) -> None:
        pack = _build(offer_id=offer_id)
        md = render_markdown(pack)
        assert isinstance(md, str) and md.strip()
