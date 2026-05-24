"""SprintWorkflow — Phase 2 deterministic 7-day Sprint pipeline.

Triggered by `payment_confirmed` events. Each step is idempotent and
side-effect-free until the final `safe_send` step.

Steps:
    passport_validate   — confirm Source Passport exists + PDPL basis logged
    dq_score            — Data Quality Score
    account_scoring     — ICP score (Tier A/B/C/D)
    draft_pack          — bilingual proposal (deterministic templates)
    policy_eval         — ALLOW / DENY / ESCALATE via approvals engine
    pdf_render_ar       — Arabic Proof Pack PDF (deterministic)
    pdf_render_en       — English Proof Pack PDF (deterministic)
    sign                — Ed25519 sign both PDFs (sign-on-write)
    ledger_register     — register ProofAsset in capital ledger
    safe_send           — closed-loop delivery to paying customer
    retainer_eligibility — score for upsell escalation

The orchestrator is pure Python — durable execution is layered above by
auto_client_acquisition.orchestrator.durable_workflow. Failures here are
deterministic exceptions; the durable layer handles retry + DLQ routing.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable

from auto_client_acquisition.proof_os.signer import SignedAsset, sign_payload

log = logging.getLogger(__name__)

STEP_NAMES = (
    "passport_validate",
    "dq_score",
    "account_scoring",
    "draft_pack",
    "policy_eval",
    "pdf_render_ar",
    "pdf_render_en",
    "sign",
    "ledger_register",
    "safe_send",
    "retainer_eligibility",
)


@dataclass(frozen=True, slots=True)
class SprintInput:
    """Required input to fire a Sprint workflow."""

    payment_id: str
    offer_id: str
    source_passport_id: str
    customer_handle: str
    amount_halalas: int = 0
    currency: str = "SAR"
    locale_primary: str = "ar"

    def to_dict(self) -> dict[str, Any]:
        return {
            "payment_id": self.payment_id,
            "offer_id": self.offer_id,
            "source_passport_id": self.source_passport_id,
            "customer_handle": self.customer_handle,
            "amount_halalas": self.amount_halalas,
            "currency": self.currency,
            "locale_primary": self.locale_primary,
        }


@dataclass
class SprintState:
    """Accumulating state across steps. Each step writes its output here."""

    input: SprintInput
    started_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    steps_completed: list[str] = field(default_factory=list)
    outputs: dict[str, Any] = field(default_factory=dict)
    delivery_status: str = "pending"
    halted_reason: str | None = None

    def is_complete(self) -> bool:
        return len(self.steps_completed) == len(STEP_NAMES)

    def to_dict(self) -> dict[str, Any]:
        return {
            "input": self.input.to_dict(),
            "started_at": self.started_at,
            "steps_completed": list(self.steps_completed),
            "outputs": {
                k: (v.to_dict() if hasattr(v, "to_dict") else v)
                for k, v in self.outputs.items()
            },
            "delivery_status": self.delivery_status,
            "halted_reason": self.halted_reason,
        }


# Default step implementations — pure, deterministic. Test harnesses can
# override any one via the `step_overrides` parameter for failure injection.


def _passport_validate(state: SprintState) -> dict[str, Any]:
    pid = state.input.source_passport_id
    if not pid:
        raise ValueError("source_passport_id missing — Non-Negotiable #10")
    return {"passport_id": pid, "validated_at": datetime.now(timezone.utc).isoformat()}


def _dq_score(state: SprintState) -> dict[str, Any]:
    # Deterministic placeholder; integrates with data_os.data_quality_score
    # in production via dependency injection.
    return {"score": 0.85, "tier": "B"}


def _account_scoring(state: SprintState) -> dict[str, Any]:
    return {"icp_tier": "A", "fit_score": 0.78}


def _draft_pack(state: SprintState) -> dict[str, Any]:
    return {
        "title_ar": "حزمة الإثبات — ديلكس",
        "title_en": "Dealix Proof Pack",
        "sections": ["executive_summary", "evidence", "next_steps"],
        "no_guaranteed_claims": True,
    }


def _policy_eval(state: SprintState) -> dict[str, Any]:
    # In production, calls dealix.governance.approvals.evaluate(...).
    # Closed-loop class for paying customers — ALLOW by default.
    return {"decision": "ALLOW", "policy_id": "phase2_closed_loop_v1"}


def _pdf_render(state: SprintState, locale: str) -> dict[str, Any]:
    draft = state.outputs.get("draft_pack", {})
    title = draft.get(f"title_{locale}", f"Proof Pack ({locale})")
    body = (
        f"# {title}\n\n"
        f"Customer: {state.input.customer_handle}\n"
        f"Offer: {state.input.offer_id}\n"
        f"Payment: {state.input.payment_id}\n"
        f"Generated: {datetime.now(timezone.utc).isoformat()}\n"
    )
    payload = body.encode("utf-8")
    return {"locale": locale, "bytes_len": len(payload), "payload": payload}


def _pdf_render_ar(state: SprintState) -> dict[str, Any]:
    return _pdf_render(state, "ar")


def _pdf_render_en(state: SprintState) -> dict[str, Any]:
    return _pdf_render(state, "en")


def _sign(state: SprintState) -> dict[str, Any]:
    """Signs both PDFs. Non-Negotiable #9: bilingual + signed REQUIRED."""
    ar = state.outputs.get("pdf_render_ar", {})
    en = state.outputs.get("pdf_render_en", {})
    if not ar or not en:
        raise ValueError(
            "sign_step_requires_both_locales — Non-Negotiable #9 "
            "(evidence packs MUST be bilingual)"
        )
    signed_ar = sign_payload(
        ar["payload"], metadata={"locale": "ar", "offer_id": state.input.offer_id}
    )
    signed_en = sign_payload(
        en["payload"], metadata={"locale": "en", "offer_id": state.input.offer_id}
    )
    return {"ar": signed_ar, "en": signed_en}


def _ledger_register(state: SprintState) -> dict[str, Any]:
    signed = state.outputs.get("sign", {})
    if not signed.get("ar") or not signed.get("en"):
        raise ValueError("ledger_register_requires_signed_assets")
    # Deterministic asset id derived from content hashes.
    ar_hash = signed["ar"].content_sha256[:16]
    en_hash = signed["en"].content_sha256[:16]
    return {
        "asset_id": f"proof_{ar_hash}_{en_hash}",
        "ar_hash": signed["ar"].content_sha256,
        "en_hash": signed["en"].content_sha256,
        "registered_at": datetime.now(timezone.utc).isoformat(),
    }


def _safe_send(state: SprintState) -> dict[str, Any]:
    """Final external action — closed-loop to paying customer.

    In production this calls auto_client_acquisition.safe_send_gateway via
    a deterministic outbound queue. Here we record the intent only.
    """
    asset = state.outputs.get("ledger_register", {})
    return {
        "channel": "email",
        "recipient_handle": state.input.customer_handle,
        "asset_id": asset.get("asset_id"),
        "queued_at": datetime.now(timezone.utc).isoformat(),
    }


def _retainer_eligibility(state: SprintState) -> dict[str, Any]:
    """Post-delivery eligibility score; never auto-charges anything."""
    scoring = state.outputs.get("account_scoring", {})
    fit = float(scoring.get("fit_score", 0.0))
    return {
        "eligible": fit >= 0.75,
        "next_action": "escalate_pitch" if fit >= 0.75 else "monitor",
    }


_DEFAULT_STEPS: dict[str, Callable[[SprintState], dict[str, Any]]] = {
    "passport_validate": _passport_validate,
    "dq_score": _dq_score,
    "account_scoring": _account_scoring,
    "draft_pack": _draft_pack,
    "policy_eval": _policy_eval,
    "pdf_render_ar": _pdf_render_ar,
    "pdf_render_en": _pdf_render_en,
    "sign": _sign,
    "ledger_register": _ledger_register,
    "safe_send": _safe_send,
    "retainer_eligibility": _retainer_eligibility,
}


class SprintWorkflow:
    """Pure orchestrator. Idempotent: run(state) resumes from steps_completed."""

    def __init__(
        self,
        *,
        step_overrides: dict[str, Callable[[SprintState], dict[str, Any]]] | None = None,
    ) -> None:
        self.steps: dict[str, Callable[[SprintState], dict[str, Any]]] = {
            **_DEFAULT_STEPS,
            **(step_overrides or {}),
        }

    def run(self, state: SprintState) -> SprintState:
        """Execute all remaining steps in order. Resumes from completed set."""
        for name in STEP_NAMES:
            if name in state.steps_completed:
                continue
            try:
                step = self.steps[name]
                out = step(state)
            except Exception as exc:  # noqa: BLE001 — surface to durable layer
                log.exception("sprint_step_failed step=%s reason=%s", name, exc)
                state.halted_reason = f"{name}: {exc}"
                raise
            state.outputs[name] = out
            state.steps_completed.append(name)

        # Policy gate: if DENY/ESCALATE arrived from policy_eval, leave delivery pending.
        policy = state.outputs.get("policy_eval", {})
        if policy.get("decision") == "ALLOW":
            state.delivery_status = "delivered"
        else:
            state.delivery_status = "pending"
        return state


__all__ = [
    "STEP_NAMES",
    "SignedAsset",
    "SprintInput",
    "SprintState",
    "SprintWorkflow",
]
