"""Layer 5 — Compliance reasoning across PDPL / ZATCA / SAMA / NCA.

Returns a deterministic reasoning chain (not a free-form LLM answer). Each
framework contributes a verdict; the layer's overall decision is the strictest
verdict across frameworks.

Frameworks:
    - PDPL (Saudi PDPL): personal-data handling, consent, cross-border, retention.
    - ZATCA: e-invoicing posture (relevant only for payment actions).
    - SAMA: financial-data handling (only for fintech / payments).
    - NCA: data classification (public/internal/confidential/top-secret) +
      sovereignty (Saudi region).
"""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.ai_layers.schemas import LayerContext, LayerResult

_STRICTNESS = {
    "ALLOW": 0,
    "ALLOW_WITH_REVIEW": 1,
    "DRAFT_ONLY": 2,
    "REQUIRE_APPROVAL": 3,
    "REDACT": 4,
    "BLOCK": 5,
    "ESCALATE": 6,
}


def _strictest(*decisions: str) -> str:
    return max(decisions, key=lambda d: _STRICTNESS.get(d, 0))


def _pdpl(ctx: LayerContext) -> tuple[str, list[str]]:
    chain: list[str] = []
    decision = "ALLOW"
    contains_pii = bool(ctx.contains_pii_hint) or bool(
        ctx.payload.get("contains_pii", False)
    )
    lawful_basis = ctx.payload.get("lawful_basis")
    cross_border = bool(ctx.payload.get("cross_border", False))

    if contains_pii:
        chain.append("PDPL:Article-5 — personal data present")
        if not lawful_basis:
            chain.append("PDPL:Article-6 — no lawful basis declared → BLOCK")
            decision = _strictest(decision, "BLOCK")
        else:
            chain.append(f"PDPL:Article-6 — lawful basis '{lawful_basis}' declared")
        if ctx.external_action_requested:
            chain.append("PDPL:Article-21 — external use requires approval")
            decision = _strictest(decision, "REQUIRE_APPROVAL")
        if cross_border:
            chain.append("PDPL:Article-29 — cross-border transfer flagged")
            decision = _strictest(decision, "REQUIRE_APPROVAL")
    else:
        chain.append("PDPL:Article-5 — no personal data → ALLOW")
    return decision, chain


def _zatca(ctx: LayerContext) -> tuple[str, list[str]]:
    chain: list[str] = []
    action = str(ctx.payload.get("action", ""))
    is_invoice = bool(ctx.payload.get("is_invoice", False)) or "invoice" in action
    if not is_invoice:
        return "ALLOW", ["ZATCA:not-applicable"]
    has_vat_id = bool(ctx.payload.get("vat_id"))
    has_uuid = bool(ctx.payload.get("invoice_uuid"))
    if has_vat_id and has_uuid:
        chain.append("ZATCA:e-invoice — VAT ID + UUID present")
        return "ALLOW", chain
    chain.append("ZATCA:e-invoice — missing VAT ID or UUID → BLOCK")
    return "BLOCK", chain


def _sama(ctx: LayerContext) -> tuple[str, list[str]]:
    chain: list[str] = []
    handles_financial = bool(ctx.payload.get("handles_financial_data", False))
    if not handles_financial:
        return "ALLOW", ["SAMA:not-applicable"]
    tokenized = bool(ctx.payload.get("financial_data_tokenized", False))
    if not tokenized:
        chain.append("SAMA: raw financial data without tokenization → BLOCK")
        return "BLOCK", chain
    chain.append("SAMA: financial data tokenized")
    if ctx.external_action_requested:
        chain.append("SAMA: external action on financial data → REQUIRE_APPROVAL")
        return "REQUIRE_APPROVAL", chain
    return "ALLOW", chain


def _nca(ctx: LayerContext) -> tuple[str, list[str]]:
    chain: list[str] = []
    classification = str(ctx.payload.get("data_classification", "internal")).lower()
    region = str(ctx.payload.get("processing_region", "sa")).lower()
    chain.append(f"NCA:classification='{classification}', region='{region}'")
    if region != "sa":
        chain.append("NCA:sovereignty — non-Saudi region → BLOCK")
        return "BLOCK", chain
    if classification in ("confidential", "secret", "top-secret"):
        if ctx.external_action_requested:
            chain.append(
                f"NCA:{classification} class with external action → REQUIRE_APPROVAL"
            )
            return "REQUIRE_APPROVAL", chain
        chain.append(f"NCA:{classification} class internal use only")
        return "ALLOW_WITH_REVIEW", chain
    return "ALLOW", chain


def run(ctx: LayerContext) -> LayerResult:
    """Reason across PDPL / ZATCA / SAMA / NCA for the action in payload."""
    if not ctx.source_refs and ctx.external_action_requested:
        return LayerResult(
            layer="compliance_reasoning",
            customer_id=ctx.customer_id,
            ok=False,
            governance_decision="BLOCK",
            output={"reason": "external_action_needs_source_ref"},
            notes=("External action without source_ref blocked",),
        )

    pdpl_dec, pdpl_chain = _pdpl(ctx)
    zatca_dec, zatca_chain = _zatca(ctx)
    sama_dec, sama_chain = _sama(ctx)
    nca_dec, nca_chain = _nca(ctx)

    overall = _strictest(pdpl_dec, zatca_dec, sama_dec, nca_dec)

    return LayerResult(
        layer="compliance_reasoning",
        customer_id=ctx.customer_id,
        ok=overall != "BLOCK",
        governance_decision=overall,
        output={
            "frameworks": {
                "PDPL": {"decision": pdpl_dec, "chain": pdpl_chain},
                "ZATCA": {"decision": zatca_dec, "chain": zatca_chain},
                "SAMA": {"decision": sama_dec, "chain": sama_chain},
                "NCA": {"decision": nca_dec, "chain": nca_chain},
            },
            "overall": overall,
        },
        notes=(f"PDPL={pdpl_dec}", f"ZATCA={zatca_dec}", f"SAMA={sama_dec}", f"NCA={nca_dec}"),
        capital_asset_candidates=("governance_rule",) if overall == "ALLOW" else (),
    )
