"""Approval matrix — deterministic risk routing.

Maps a free-text action description to a (risk, approval_route) pair. This is
the single source of truth used by the agent governance layer to decide
whether an action can run autonomously, needs human/founder approval, or is
blocked outright. It is intentionally keyword-driven and conservative: when in
doubt the safer (higher-risk) classification wins, and a human stays in the
loop. Nothing here ever sends anything — it only routes for approval.
"""

from __future__ import annotations

from typing import Literal

Risk = Literal["low", "medium", "high", "critical"]


def approval_for_action(action: str) -> tuple[Risk, str]:
    a = action.lower().strip()

    # Credentials / secrets — most sensitive. Founder-only, effectively blocked
    # for autonomous agents.
    if any(k in a for k in ("secret", "credential", "api key", "api_key", "private key")):
        return "critical", "blocked_founder_only"

    # WhatsApp — always high risk and requires human approval + explicit consent.
    if "whatsapp" in a:
        return "high", "human+consent"

    # LinkedIn automation / scraping — blocked outright.
    if "linkedin" in a and ("automation" in a or "automate" in a or "scrap" in a):
        return "high", "blocked"

    # Drafts are low/medium regardless of topic — a human reviews before any send.
    if "draft" in a:
        return "medium", "human_review"

    # Email send — medium risk, human approval before it leaves the workspace.
    if "send" in a and "email" in a:
        return "medium", "human"

    # Payments / billing / invoicing / refunds — high risk, founder approval.
    if any(k in a for k in ("payment", "refund", "invoice", "charge", "billing")):
        return "high", "human_founder"

    # Pricing / discounts / quotes / negotiation — high risk, founder sets the
    # final price. Drafts are caught earlier so "draft pricing" stays medium.
    if any(k in a for k in ("pricing", "price", "discount", "quote", "negotiat")):
        return "high", "founder"

    # Contracts / legal / agreements / signatures — high risk, human/legal review.
    if any(k in a for k in ("contract", "legal", "agreement", "signature", "sign-off")):
        return "high", "human_legal"

    # Any other external send / outbound message — high risk, human approval.
    if "external" in a or ("send" in a and "message" in a) or "outbound" in a:
        return "high", "human"

    # PII / personal data handling — high risk, lawful basis required.
    if "pii" in a or "personal data" in a:
        return "high", "lawful_basis_required"

    # Publishing / public marketing claims — medium risk, claim QA gate.
    if "publish" in a or "claim" in a:
        return "medium", "claim_qa"

    return "low", "auto"
