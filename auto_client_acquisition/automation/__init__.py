"""Automation package — shared daily-motion logic.

The daily sales motion (lead-prep, top-50 targeting, follow-ups, founder
brief, stale-approval sweep) lives here as plain async functions so that
BOTH the HTTP endpoints in ``api/routers/automation.py`` AND the ARQ cron
worker in ``core/tasks/worker.py`` call one implementation — no duplication.

Doctrine: nothing in this package auto-sends prospect outreach. Targeting
and follow-up runners only QUEUE drafts (approval_required=True) into the
durable approval queue. The founder's approval tap is the only send
trigger for prospect channels.
"""

from __future__ import annotations

from auto_client_acquisition.automation.daily_runner import (
    expire_stale_approvals,
    run_daily_targeting_core,
    run_followups_core,
)

__all__ = [
    "expire_stale_approvals",
    "run_daily_targeting_core",
    "run_followups_core",
]
