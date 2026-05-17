"""Content OS — deterministic social content drafting + the daily engine.

Public surface:
  - ``CADENCE_THEMES`` / ``theme_for`` — the 6 content pillars + schedule
  - ``SocialPostDraft`` / ``draft_daily_social_posts`` — drafting engine
  - ``enqueue_social_drafts`` — bridge drafts into the approval queue

The heavier orchestration entrypoints (``run_daily_engine``,
``build_action_list``, ``route_and_draft_proposal``) are imported directly
from their submodules to keep this package free of import cycles.
"""
from __future__ import annotations

from auto_client_acquisition.content_os.cadence import CADENCE_THEMES, theme_for
from auto_client_acquisition.content_os.drafting import (
    SocialPostDraft,
    draft_daily_social_posts,
)
from auto_client_acquisition.content_os.queue_bridge import enqueue_social_drafts

__all__ = [
    "CADENCE_THEMES",
    "SocialPostDraft",
    "draft_daily_social_posts",
    "enqueue_social_drafts",
    "theme_for",
]
