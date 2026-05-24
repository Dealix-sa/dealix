"""Layer 4 — Decision passport assembly (per-decision evidence chain)."""
from __future__ import annotations

import hashlib
from typing import Any

from auto_client_acquisition.ai_layers.schemas import LayerContext, LayerResult


def _passport_id(customer_id: str, action: str) -> str:
    raw = f"{customer_id}:{action}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:16]


def run(ctx: LayerContext) -> LayerResult:
    """Assemble a decision passport for an action.

    Expected payload keys:
        action: str — what is being decided (e.g., "send_warm_outreach").
        evidence_refs: list[str] — pointers to value_os events / source refs.
        risk_class: str — "L0"-"L5" (claim_safety scale).
    """
    action = str(ctx.payload.get("action", "unspecified_action"))
    evidence_refs = list(ctx.payload.get("evidence_refs", []) or [])
    risk_class = str(ctx.payload.get("risk_class", "L1"))

    # Combine context source_refs and evidence_refs; uniq-preserve order.
    seen: set[str] = set()
    chain: list[str] = []
    for ref in (*ctx.source_refs, *evidence_refs):
        if ref not in seen:
            seen.add(ref)
            chain.append(ref)

    if not chain:
        return LayerResult(
            layer="decision_passport",
            customer_id=ctx.customer_id,
            ok=False,
            governance_decision="BLOCK",
            output={"reason": "no_evidence_chain", "action": action},
            notes=("Decision passport needs at least one evidence ref",),
        )

    pid = _passport_id(ctx.customer_id, action)
    decision = "ALLOW"
    if risk_class in ("L3", "L4", "L5") or ctx.external_action_requested:
        decision = "REQUIRE_APPROVAL"

    return LayerResult(
        layer="decision_passport",
        customer_id=ctx.customer_id,
        ok=True,
        governance_decision=decision,
        output={
            "passport_id": pid,
            "action": action,
            "evidence_chain": chain,
            "risk_class": risk_class,
            "issued_to": ctx.actor,
        },
        notes=(f"passport {pid} risk {risk_class}",),
    )
