"""
automation — Automation Readiness scoring. The platform refuses to
turn on autonomy until a workflow has earned it through measurable
trust, outcomes, and low incident rate.
"""

from dealix.hermes.automation.readiness_score import (
    AutomationDecision,
    AutomationReadinessScore,
    score_automation_readiness,
)

__all__ = ["AutomationDecision", "AutomationReadinessScore", "score_automation_readiness"]
