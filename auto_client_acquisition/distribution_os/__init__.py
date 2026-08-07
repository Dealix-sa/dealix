"""Distribution OS — the Revenue Execution layer.

An approval-first orchestration layer over the existing OS modules
(``governance_os``, ``proof_os``, ``sales_os``, ``payment_ops``,
``autonomous_growth.product_catalog``). It turns a prospect into a tracked
chain: qualify -> draft (quality-gated) -> follow-up -> proposal -> proof ->
payment handoff -> delivery handoff -> renewal/upsell -> win/loss -> metrics.

Doctrine (non-negotiable, enforced by tests):
- AI drafts; the founder approves; the system tracks.
- No external sends in v1 (no send capability exists in this package).
- No cold WhatsApp / LinkedIn automation / scraping.
- All drafts start pending approval; guaranteed-outcome claims are blocked.
- Every offer / proposal / handoff links to a real catalog product (no
  invented prices).
- Every commercial claim carries an evidence level (L0–L5).
"""

from __future__ import annotations

from auto_client_acquisition.distribution_os import (
    catalog,
    delivery_handoff,
    draft_factory,
    draft_quality,
    followup,
    metrics,
    payment_handoff,
    proof_pack,
    proposal,
    prospect,
    renewal,
    win_loss,
)

__all__ = [
    "catalog",
    "delivery_handoff",
    "draft_factory",
    "draft_quality",
    "followup",
    "metrics",
    "payment_handoff",
    "proof_pack",
    "proposal",
    "prospect",
    "renewal",
    "win_loss",
]
