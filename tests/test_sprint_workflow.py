"""SprintWorkflow — Phase 2 end-to-end deterministic 7-day Sprint pipeline.

Verifies:
  - all 11 steps run in order on a fresh state
  - workflow is idempotent — re-running a completed state is a no-op
  - the sign step refuses to proceed without BOTH locales (Non-Neg #9)
  - missing source passport halts at passport_validate (Non-Neg #10)
  - signed assets verify against the rendered payloads
  - retainer eligibility is computed at the tail without side effects
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.proof_os.signer import verify_payload
from auto_client_acquisition.proof_os.sprint_workflow import (
    STEP_NAMES,
    SprintInput,
    SprintState,
    SprintWorkflow,
)


def _seed_state() -> SprintState:
    return SprintState(
        input=SprintInput(
            payment_id="pay_001",
            offer_id="sprint_499",
            source_passport_id="passport_001",
            customer_handle="ahmad",
            amount_halalas=49_900,
            currency="SAR",
            locale_primary="ar",
        )
    )


def test_full_run_completes_all_steps():
    state = _seed_state()
    SprintWorkflow().run(state)
    assert state.is_complete()
    assert state.steps_completed == list(STEP_NAMES)
    assert state.delivery_status == "delivered"


def test_idempotent_replay_is_noop():
    state = _seed_state()
    wf = SprintWorkflow()
    wf.run(state)
    # Capture outputs and run again — should not change anything.
    snapshot = list(state.steps_completed)
    wf.run(state)
    assert state.steps_completed == snapshot


def test_missing_passport_halts_at_first_step():
    state = SprintState(
        input=SprintInput(
            payment_id="pay_x",
            offer_id="sprint_499",
            source_passport_id="",  # missing
            customer_handle="x",
        )
    )
    wf = SprintWorkflow()
    with pytest.raises(ValueError) as exc:
        wf.run(state)
    assert "Non-Negotiable #10" in str(exc.value)
    # Pre-failure: passport_validate added nothing.
    assert "passport_validate" not in state.steps_completed
    # Halted reason recorded.
    assert state.halted_reason is not None
    assert state.halted_reason.startswith("passport_validate")


def test_sign_step_requires_both_locales():
    state = _seed_state()
    # Override pdf_render_en to skip — sign must then refuse.
    wf = SprintWorkflow(
        step_overrides={
            "pdf_render_en": lambda _s: {},  # empty output
        }
    )
    with pytest.raises(ValueError) as exc:
        wf.run(state)
    assert "Non-Negotiable #9" in str(exc.value)


def test_signed_pdfs_verify():
    state = _seed_state()
    SprintWorkflow().run(state)
    ar_pdf = state.outputs["pdf_render_ar"]
    en_pdf = state.outputs["pdf_render_en"]
    signed = state.outputs["sign"]
    assert verify_payload(ar_pdf["payload"], signed["ar"]) is True
    assert verify_payload(en_pdf["payload"], signed["en"]) is True


def test_ledger_register_records_both_hashes():
    state = _seed_state()
    SprintWorkflow().run(state)
    ledger = state.outputs["ledger_register"]
    assert ledger["ar_hash"]
    assert ledger["en_hash"]
    assert ledger["asset_id"].startswith("proof_")


def test_safe_send_records_recipient_and_asset_id():
    state = _seed_state()
    SprintWorkflow().run(state)
    send = state.outputs["safe_send"]
    assert send["recipient_handle"] == "ahmad"
    assert send["asset_id"] == state.outputs["ledger_register"]["asset_id"]


def test_retainer_eligibility_uses_account_scoring():
    state = _seed_state()
    SprintWorkflow().run(state)
    eligibility = state.outputs["retainer_eligibility"]
    # Default fit_score is 0.78 (above 0.75 threshold).
    assert eligibility["eligible"] is True
    assert eligibility["next_action"] == "escalate_pitch"


def test_deny_decision_keeps_delivery_pending():
    state = _seed_state()
    wf = SprintWorkflow(
        step_overrides={
            "policy_eval": lambda _s: {"decision": "DENY", "policy_id": "test"},
        }
    )
    wf.run(state)
    assert state.delivery_status == "pending"


def test_partial_run_resumes_from_failure():
    """A step failing mid-run lets a retry resume from where it stopped."""
    state = _seed_state()
    calls = {"draft_pack": 0}

    def flaky_draft(s: SprintState) -> dict:
        calls["draft_pack"] += 1
        if calls["draft_pack"] == 1:
            raise RuntimeError("transient")
        return {"title_ar": "x", "title_en": "x", "sections": [], "no_guaranteed_claims": True}

    wf = SprintWorkflow(step_overrides={"draft_pack": flaky_draft})
    with pytest.raises(RuntimeError):
        wf.run(state)
    # First two steps completed; draft_pack did not.
    assert "passport_validate" in state.steps_completed
    assert "dq_score" in state.steps_completed
    assert "draft_pack" not in state.steps_completed
    # Retry — should pick up exactly at draft_pack.
    wf.run(state)
    assert state.is_complete()
    assert calls["draft_pack"] == 2


def test_state_to_dict_serializable():
    import json

    state = _seed_state()
    SprintWorkflow().run(state)
    json.dumps(state.to_dict(), default=str)


def test_step_names_constant_has_11_steps():
    assert len(STEP_NAMES) == 11
    assert len(set(STEP_NAMES)) == 11
