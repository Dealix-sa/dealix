"""Repository path constants for commercial_ops scripts."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = REPO_ROOT / "data"
FOUNDER_BRIEFS_DIR = DATA_DIR / "founder_briefs"
FOUNDER_WEEKLY_DIR = DATA_DIR / "founder_weekly"
FOUNDER_AGENT_STATE_DIR = DATA_DIR / "founder_agent"

WAR_ROOM_TODAY_JSON = DATA_DIR / "war_room_today.json"
FOUNDER_DAILY_ANCHOR_JSON = DATA_DIR / "founder_briefs" / "daily_anchor_latest.json"

FOUNDER_AGENT_QUEUE_JSON = FOUNDER_AGENT_STATE_DIR / "queue_today.json"
FOUNDER_AGENT_LEARNING_YAML = FOUNDER_AGENT_STATE_DIR / "weekly_learning.yaml"
FOUNDER_AGENT_TASK_QUEUE_YAML = REPO_ROOT / "dealix" / "config" / "founder_agent_task_queue.yaml"

FOUNDER_WEEKLY_ONE_DECISION_YAML = (
    REPO_ROOT / "dealix" / "config" / "founder_weekly_one_decision.yaml"
)

EVIDENCE_TRACKER_CSV = (
    REPO_ROOT / "docs" / "commercial" / "operations" / "evidence_events_tracker.csv"
)
AGENCY_TARGETS_CSV = (
    REPO_ROOT / "docs" / "commercial" / "operations" / "targeting" / "agency_accounts_seed.csv"
)

ICP_AGENCY_YAML = REPO_ROOT / "dealix" / "config" / "icp_agency_wedge.yaml"
GTM_ABM_WAVE1_YAML = REPO_ROOT / "dealix" / "config" / "gtm_abm_wave1.yaml"
