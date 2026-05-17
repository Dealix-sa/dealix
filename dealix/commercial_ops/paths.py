"""Repository paths for commercial operations."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

EVIDENCE_TRACKER_CSV = (
    REPO_ROOT / "docs/commercial/operations/evidence_events_tracker.csv"
)
AGENCY_TARGETS_CSV = (
    REPO_ROOT / "docs/commercial/operations/targeting/agency_accounts_seed.csv"
)
SOCIAL_QUEUE_YAML = REPO_ROOT / "dealix/config/social_content_queue.yaml"
ICP_AGENCY_YAML = REPO_ROOT / "dealix/config/icp_agency_wedge.yaml"
WAR_ROOM_TODAY_JSON = REPO_ROOT / "data/war_room_today.json"
FOUNDER_BRIEFS_DIR = REPO_ROOT / "data/founder_briefs"
