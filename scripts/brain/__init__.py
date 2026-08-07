"""Company Brain OS — shared helpers.

This package contains the Company Brain OS engine scripts. The engine is
strictly non-deterministic about the future: every forward-looking output is
expressed as a *scenario* (base / upside / downside) with an explicit
confidence level. No function in this package claims guaranteed outcomes or
ROI.

Modules
-------
ingest_company_profile        — load company profile data into the brain
build_company_brain_map        — assemble a knowledge map of signals, decisions,
                                 assumptions, experiments, risks, opportunities
detect_bottlenecks             — surface friction points from the brain map
generate_future_radar           — scenario-based 30/90/365-day radar (no
                                 deterministic predictions)
generate_daily_decision         — produce a decision record with all required
                                 fields (logged to ledgers/decisions_log.csv)
generate_weekly_board_memo      — weekly memo summarising signal movement and
                                 open decisions
generate_30_day_action_plan     — rolling 30-day scenario plan with confidence
run_brain_day                   — orchestrator: runs a full brain day cycle
seed_demo_brain_data            — populates ledgers with demo data for testing
"""
from __future__ import annotations

__all__ = [
    "ingest_company_profile",
    "build_company_brain_map",
    "detect_bottlenecks",
    "generate_future_radar",
    "generate_daily_decision",
    "generate_weekly_board_memo",
    "generate_30_day_action_plan",
    "run_brain_day",
    "seed_demo_brain_data",
]

# Guard rails advertised to every consumer.
GUARDRAILS = [
    "No deterministic future predictions — every forward statement is a scenario.",
    "Every scenario carries an explicit confidence level (low/medium/high).",
    "No guaranteed ROI claims.",
    "No automatic external action — the brain only recommends; humans act.",
]

# Required fields for every decision record produced by the brain.
DECISION_REQUIRED_FIELDS = [
    "decision",
    "why_now",
    "assumption",
    "confidence",
    "owner",
    "next_action",
    "success_metric",
    "review_date",
    "risk_if_delayed",
]
