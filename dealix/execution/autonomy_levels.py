"""Autonomy levels for safe Company OS execution."""

from __future__ import annotations

from enum import IntEnum


class AutonomyLevel(IntEnum):
    OBSERVE = 0
    ANALYZE = 1
    DRAFT = 2
    INTERNAL_EXECUTE = 3
    REPO_EXECUTE = 4
    EXTERNAL_EXECUTE = 5


EXTERNAL_ACTIONS = {
    "send_email",
    "send_whatsapp",
    "send_sms",
    "post_content",
    "capture_payment",
    "merge_pr",
    "modify_production",
}


def classify_action(action_type: str) -> AutonomyLevel:
    normalized = action_type.strip().lower()
    if normalized in EXTERNAL_ACTIONS:
        return AutonomyLevel.EXTERNAL_EXECUTE
    if normalized in {"create_pr", "run_tests", "create_branch"}:
        return AutonomyLevel.REPO_EXECUTE
    if normalized in {"write_report", "write_queue", "write_proof", "update_local_file"}:
        return AutonomyLevel.INTERNAL_EXECUTE
    if normalized in {"draft_message", "draft_proposal", "draft_content"}:
        return AutonomyLevel.DRAFT
    if normalized in {"score", "classify", "prioritize"}:
        return AutonomyLevel.ANALYZE
    return AutonomyLevel.OBSERVE


def requires_human_approval(action_type: str) -> bool:
    return classify_action(action_type) >= AutonomyLevel.EXTERNAL_EXECUTE
