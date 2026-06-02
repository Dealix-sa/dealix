"""Dealix WhatsApp Client OS (client-facing).

A governed, menu-driven **business workflow assistant** delivered over
WhatsApp for Saudi B2B companies — NOT a general-purpose chatbot. It guides a
client through: readiness assessment → product recommendation → permissions →
drafts → proposals → proof → payment/onboarding → support → human handoff.

This is distinct from the internal, founder-only ``whatsapp_decision_bot``.

Doctrine (enforced in code + tests):
- No API keys / secrets in WhatsApp text — secure portal links instead.
- No cold WhatsApp, no LinkedIn automation, no scraping, no blasts.
- Human approval for any external commitment.
- Human handoff for ambiguity, sensitive data, pricing, contracts, complaints.
- Every recommendation ties to ``service_catalog`` + an evidence level.
- All actions logged to the JSONL ledgers.
"""

from auto_client_acquisition.whatsapp_client_os.assessment import (
    build_assessment,
    recommend_offer,
    score_assessment,
)
from auto_client_acquisition.whatsapp_client_os.conversation_state import advance, transition
from auto_client_acquisition.whatsapp_client_os.engine import (
    ClientOSResponse,
    handle_inbound,
    new_session,
)
from auto_client_acquisition.whatsapp_client_os.intent_router import classify
from auto_client_acquisition.whatsapp_client_os.metrics import compute_metrics
from auto_client_acquisition.whatsapp_client_os.whatsapp_policy_guard import (
    guard_inbound,
    scan_for_secrets,
    scan_for_unsafe_request,
)

__all__ = [
    "ClientOSResponse",
    "advance",
    "build_assessment",
    "classify",
    "compute_metrics",
    "guard_inbound",
    "handle_inbound",
    "new_session",
    "recommend_offer",
    "scan_for_secrets",
    "scan_for_unsafe_request",
    "score_assessment",
    "transition",
]
