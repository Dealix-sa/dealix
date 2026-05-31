"""Custom Systems OS — core + doctrine tests.

Mirrors the repo's ``test_no_*`` doctrine style: Source Passport gate, no
guaranteed claims (governance block + score cap), Proof Pack required, and at
least one Capital Asset per engagement. Ledgers are redirected to ``tmp_path``.
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.capital_os import capital_ledger
from auto_client_acquisition.custom_systems_os import ledger as cs_ledger
from auto_client_acquisition.custom_systems_os.design_profile import build_design_profile
from auto_client_acquisition.custom_systems_os.engagement_runner import (
    run_custom_system_engagement,
)
from auto_client_acquisition.custom_systems_os.proof_sections import build_proof_sections
from auto_client_acquisition.custom_systems_os.structure_blueprint import (
    build_structure_blueprint,
)
from auto_client_acquisition.data_os.source_passport import SourcePassport
from auto_client_acquisition.designops.exporter import export_artifact
from auto_client_acquisition.proof_architecture_os.proof_pack_v2 import PROOF_PACK_V2_SECTIONS
from auto_client_acquisition.proof_os.proof_pack import proof_pack_v2_sections_complete


@pytest.fixture
def tmp_ledgers(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_CUSTOM_SYSTEMS_PATH", str(tmp_path / "cs.jsonl"))
    monkeypatch.setenv("DEALIX_CAPITAL_LEDGER_PATH", str(tmp_path / "cap.jsonl"))
    cs_ledger.clear_for_test()
    capital_ledger.clear_for_test()
    yield tmp_path


def _valid_passport() -> SourcePassport:
    return SourcePassport(
        source_id="s1",
        source_type="client_upload",
        owner="o",
        allowed_use=frozenset({"internal_analysis"}),
        contains_pii=False,
        sensitivity="medium",
        retention_policy="project_duration",
        ai_access_allowed=True,
        external_use_allowed=False,
    )


def _run(tmp_path, **over):
    kwargs = {
        "customer_id": "c1",
        "customer_name": "Acme Corp",
        "engagement_id": "e1",
        "passport": _valid_passport(),
        "paid_pilots_completed": 3,
        "declared_modules": ["sales_inbox"],
        "declared_workflows": ["weekly_growth"],
        "workflow_owner_present": True,
        "adoption_score": 75.0,
        "out_dir": str(tmp_path / "exports"),
    }
    kwargs.update(over)
    return run_custom_system_engagement(**kwargs)


def test_no_source_passport_blocks_engagement(tmp_ledgers):
    bad = SourcePassport(
        source_id="",
        source_type="x",
        owner="",
        allowed_use=frozenset(),
        contains_pii=False,
        sensitivity="low",
        retention_policy="",
        ai_access_allowed=False,
        external_use_allowed=False,
    )
    res = _run(tmp_ledgers, passport=bad)
    assert res.passport_valid is False
    assert res.next_step == "blocked_source_passport"
    assert res.spec_written_files == ()  # NO build before the passport passes


def test_entry_gate_blocks_under_three_pilots(tmp_ledgers):
    res = _run(tmp_ledgers, paid_pilots_completed=1)
    assert res.next_step == "blocked_entry_gate"
    assert "no_customization_before_3_paid_pilots" in res.blocked_reasons
    assert res.spec_written_files == ()


def test_missing_context_asks_first(tmp_ledgers):
    res = _run(tmp_ledgers, declared_modules=[], declared_workflows=[])
    assert res.next_step == "ask_founder_for_missing_context"
    assert res.spec_written_files == ()


def test_happy_path_assembles_and_is_governed(tmp_ledgers):
    res = _run(tmp_ledgers)
    assert res.passport_valid is True
    assert res.governance_decision in {"allow", "allow_with_monitoring"}
    assert res.governance_blocked is False
    assert res.safety_passed is True
    assert res.proof_complete is True
    assert res.next_step == "deliver_for_founder_review"
    assert len(res.capital_assets) >= 1
    assert res.spec_written_files  # non-empty
    assert res.delivery_mode == "founder_assisted"


def test_proof_pack_all_14_sections(tmp_ledgers):
    profile = build_design_profile(customer_id="c1")
    blueprint = build_structure_blueprint(
        customer_id="c1", declared_modules=["m"], declared_workflows=["w"]
    )
    sections = build_proof_sections(
        customer_name="Acme",
        passport_valid=True,
        governance_decision="allow",
        profile=profile,
        blueprint=blueprint,
        spec_artifact_ref="x.md",
        capital_asset_refs=["cap_1"],
        retainer_recommendation="proof_pilot",
    )
    complete, missing = proof_pack_v2_sections_complete(sections)
    assert complete is True
    assert missing == ()
    assert set(sections) == set(PROOF_PACK_V2_SECTIONS)


def test_at_least_one_capital_asset(tmp_ledgers):
    res = _run(tmp_ledgers)
    assert len(res.capital_assets) >= 1
    assert capital_ledger.list_assets(engagement_id="e1")


def test_no_guaranteed_claims_blocks_and_caps_score(tmp_ledgers):
    # A guaranteed-outcome claim rendered into the spec must be governance-blocked,
    # never exported, and the proof score capped below case-ready.
    res = _run(
        tmp_ledgers,
        customer_name="we guarantee revenue results",
        engagement_id="e_poison",
    )
    assert res.governance_blocked is True
    assert res.governance_decision in {"block", "escalate"}
    assert res.proof_score <= 69
    assert res.spec_written_files == ()
    assert res.next_step in {"blocked_governance", "blocked_safety_gate"}


def test_pdf_format_is_deferred():
    with pytest.raises(NotImplementedError):
        export_artifact(manifest={"artifact_id": "x"}, content={"markdown": "# x"}, formats=["pdf"])


def test_design_profile_override_and_unknown_direction_fallback(tmp_ledgers):
    fallback = build_design_profile(customer_id="c1", direction_name="not-a-real-direction")
    assert any("unknown_direction_fallback" in o for o in fallback.overrides_applied)
    assert fallback.forbidden_copy  # inherits the Dealix forbidden-copy guard

    overridden = build_design_profile(customer_id="c1", client_overrides={"tone": "custom_tone"})
    assert overridden.tokens["tone"] == "custom_tone"
    assert "client_override:tone" in overridden.overrides_applied


def test_ledger_roundtrip(tmp_ledgers):
    _run(tmp_ledgers, engagement_id="e_ledger")
    records = cs_ledger.list_engagements(customer_id="c1")
    assert any(r.engagement_id == "e_ledger" for r in records)
