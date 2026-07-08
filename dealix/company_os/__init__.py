"""Dealix Self-Improving Autonomous Company OS foundation.

This package is intentionally draft-only and approval-first. It prepares
internal reports, queues, drafts, and proof logs without sending, publishing,
charging, merging, or mutating production.
"""

from .company_brain import CompanyBrain, build_default_dealix_brain
from .daily_planner import build_daily_company_os_plan
from .report_generator import render_daily_report

__all__ = [
    "CompanyBrain",
    "build_default_dealix_brain",
    "build_daily_company_os_plan",
    "render_daily_report",
]
