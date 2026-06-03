"""Dealix Revenue Execution OS — governed product distribution layer.

This package turns Dealix into a **practical, daily product-distribution machine**
without ever becoming a spam bot or an unsafe agent. Every surface here is:

  - **draft-only** — nothing is sent externally; the founder approves and sends
    manually (see :mod:`dealix.distribution.doctrine`);
  - **approval-first** — drafts/proposals/payments/renewals all start
    ``*_pending_approval`` and require an explicit human transition;
  - **evidence-aware** — claims are tagged with the canonical L0–L5 evidence
    level (:mod:`auto_client_acquisition.proof_engine.evidence`); public proof
    needs L4+;
  - **doctrine-bound** — it reuses the canonical non-negotiables from
    :mod:`auto_client_acquisition.safe_send_gateway` (no cold WhatsApp, no
    LinkedIn automation, no scraping, no bulk outreach, no guaranteed claims,
    no fake proof, no external send without approval).

The daily flow (see :mod:`dealix.distribution.day`)::

    prospects → drafts → quality gate → queue review → follow-ups
             → proposals → proof packs → payment handoff → renewals
             → metrics → win/loss learning → founder summary

Logic lives here (unit-tested); thin CLIs in ``scripts/`` expose Makefile
targets (``make distribution-day`` etc.).
"""

from __future__ import annotations

SCHEMA_VERSION = "1.0"

__all__ = ["SCHEMA_VERSION"]
