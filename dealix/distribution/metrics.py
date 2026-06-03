"""Distribution Metrics — the funnel cockpit across every ledger.

Pure aggregation over the JSONL ledgers (drafts → follow-ups → proposals →
proof packs → payments → renewals) plus win/loss. No external calls, no PII in
the output (company names only where needed; contact fields are never emitted).
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from dealix.distribution.ledger import read_records
from dealix.distribution.paths import (
    DRAFTS_LEDGER,
    FOLLOWUPS_LEDGER,
    PAYMENTS_LEDGER,
    PROOF_PACKS_LEDGER,
    PROPOSALS_LEDGER,
    RENEWALS_LEDGER,
    WIN_LOSS_LEDGER,
)
from dealix.distribution.win_loss import learning_summary


def _status_counts(records: list[dict[str, Any]]) -> dict[str, int]:
    return dict(Counter(str(r.get("status") or "unknown") for r in records))


def compute_metrics(*, ledgers: dict[str, Path] | None = None) -> dict[str, Any]:
    """Compute the full distribution funnel snapshot."""
    paths = {
        "drafts": DRAFTS_LEDGER,
        "followups": FOLLOWUPS_LEDGER,
        "proposals": PROPOSALS_LEDGER,
        "proof_packs": PROOF_PACKS_LEDGER,
        "payments": PAYMENTS_LEDGER,
        "renewals": RENEWALS_LEDGER,
        "win_loss": WIN_LOSS_LEDGER,
    }
    if ledgers:
        paths.update(ledgers)

    data = {name: read_records(p) for name, p in paths.items()}

    drafts = data["drafts"]
    proposals = data["proposals"]
    payments = data["payments"]

    drafts_by_status = _status_counts(drafts)
    proposals_by_status = _status_counts(proposals)
    payments_by_status = _status_counts(payments)

    approved_drafts = drafts_by_status.get("approved", 0) + drafts_by_status.get(
        "copied_manual_send", 0
    )
    accepted_proposals = proposals_by_status.get("accepted", 0)
    paid = payments_by_status.get("paid", 0)

    def _pct(num: int, den: int) -> float | None:
        return round(100 * num / den, 1) if den else None

    funnel = {
        "drafts": len(drafts),
        "approved_drafts": approved_drafts,
        "proposals": len(proposals),
        "accepted_proposals": accepted_proposals,
        "payments": len(payments),
        "paid": paid,
        "draft_approval_rate_pct": _pct(approved_drafts, len(drafts)),
        "proposal_accept_rate_pct": _pct(accepted_proposals, len(proposals)),
        "payment_close_rate_pct": _pct(paid, len(payments)),
    }

    return {
        "kpis": {
            "pending_drafts": drafts_by_status.get("draft_pending_approval", 0),
            "approved_drafts": approved_drafts,
            "due_followups": sum(1 for f in data["followups"] if f.get("status") == "due"),
            "proposal_drafts": proposals_by_status.get("draft_pending_approval", 0),
            "proof_packs": len(data["proof_packs"]),
            "payment_handoffs": len(payments),
            "upcoming_renewals": sum(1 for r in data["renewals"] if r.get("status") == "upcoming"),
            "won_deals": Counter(str(r.get("outcome") or "") for r in data["win_loss"]).get(
                "won", 0
            ),
            "lost_deals": Counter(str(r.get("outcome") or "") for r in data["win_loss"]).get(
                "lost", 0
            ),
        },
        "by_status": {
            "drafts": drafts_by_status,
            "proposals": proposals_by_status,
            "payments": payments_by_status,
            "proof_packs": _status_counts(data["proof_packs"]),
            "renewals": _status_counts(data["renewals"]),
        },
        "funnel": funnel,
        "sector_performance": dict(
            Counter(str(d.get("sector") or "") for d in drafts if d.get("sector"))
        ),
        "channel_performance": dict(
            Counter(str(d.get("channel") or "") for d in drafts if d.get("channel"))
        ),
        "win_loss": learning_summary(data["win_loss"]),
    }


__all__ = ["compute_metrics"]
