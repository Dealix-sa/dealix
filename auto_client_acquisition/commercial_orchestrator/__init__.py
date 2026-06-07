"""Commercial orchestrator — chains existing primitives into the daily
prospects → ICP score → consent gate → bilingual draft → approval queue loop.

This package is the connective tissue the repo was missing. It adds no new
business primitive; it composes:
  - icp_scorer (fit score)
  - commercial_orchestrator.outreach (bilingual, doctrine-safe draft)
  - commercial_orchestrator.draft_queue (durable founder approval queue)

NOTHING in this package sends anything externally. Drafts are company-level and
always queued with approval_required=True.
"""
from __future__ import annotations

from auto_client_acquisition.commercial_orchestrator.outreach import (
    OutreachContext,
    render_outreach_draft,
)
from auto_client_acquisition.commercial_orchestrator.pipeline import (
    DEFAULT_ICP,
    ChainResult,
    dataset_path,
    load_prospects,
    run_acquisition_to_drafts,
)

from auto_client_acquisition.commercial_orchestrator import draft_queue

__all__ = [
    "ChainResult",
    "DEFAULT_ICP",
    "OutreachContext",
    "dataset_path",
    "draft_queue",
    "load_prospects",
    "render_outreach_draft",
    "run_acquisition_to_drafts",
]
