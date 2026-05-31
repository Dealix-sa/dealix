"""Verify HMAC intent signing produces consistent, tamper-detectable proofs."""

from __future__ import annotations

from dealix.hermes.authenticated_workflows.intent_proof import IntentProof, sign_intent, verify_intent


def test_sign_and_verify_intent_roundtrip() -> None:
    proof = sign_intent("send_proposal", actor="agent.sales", payload={"deal_id": "d_1"})
    assert verify_intent(proof) is True
    tampered = IntentProof(
        intent=proof.intent,
        actor="agent.evil",
        timestamp=proof.timestamp,
        signature=proof.signature,
        payload=proof.payload,
    )
    assert verify_intent(tampered) is False
