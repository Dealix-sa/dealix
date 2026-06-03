"""WhatsApp Client OS.

The client-facing WhatsApp operating experience for Dealix: a controlled set
of business flows (not an open chatbot) that lets a Saudi B2B client start on
WhatsApp, run a readiness scan, receive a recommended service tied to the
canonical catalog, grant permissions safely (secrets only via the Secure
Portal), review drafts/proposals/proof, and escalate to a human when needed.

Doctrine (enforced by tests in ``tests/test_no_secrets_in_whatsapp.py`` and
the canonical ``tests/test_no_*`` guards):
- No secrets or API keys are ever requested or stored in WhatsApp text.
- No cold WhatsApp / LinkedIn automation, no scraping, no guaranteed claims.
- No live external send or charge originates here.
- Every client-facing object carries a ``governance_decision``.
- No raw PII is persisted; message text is redacted and the WhatsApp id is
  stored only as a salted hash handle.

Entry points:
- ``brain.handle_message`` — the controlled pipeline for one inbound message.
- ``readiness_scan.score_assessment`` / ``quick_triage`` — readiness scoring.
- ``recommendation.recommend_offer`` — best next offer from the catalog.
- ``action_cards`` — structured card builders.
- ``metrics.compute_metrics`` — founder-facing aggregation.
"""

from auto_client_acquisition.whatsapp_client_os.schemas import (
    ActionCard,
    ActionCardKind,
    ClientAssessment,
    ClientPermission,
    ClientSession,
    EvidenceLevel,
    FlowId,
    HandoffReason,
    Intent,
    MessageEvent,
    PermissionLevel,
    SupportCategory,
    hash_wa_id,
)

__all__ = [
    "ActionCard",
    "ActionCardKind",
    "ClientAssessment",
    "ClientPermission",
    "ClientSession",
    "EvidenceLevel",
    "FlowId",
    "HandoffReason",
    "Intent",
    "MessageEvent",
    "PermissionLevel",
    "SupportCategory",
    "hash_wa_id",
]
