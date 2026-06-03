"""Personalization levels P0–P4 and the cold-send floor.

P0 sector only · P1 company+sector · P2 pain from their site ·
P3 trigger/event · P4 proof angle. No cold draft below P1 may be sent
unless it is a warm / press / general relationship message.
"""

from __future__ import annotations

LEVELS: tuple[str, ...] = ("P0", "P1", "P2", "P3", "P4")


def level_rank(level: str) -> int:
    try:
        return LEVELS.index((level or "P0").upper())
    except ValueError:
        return 0


def personalization_floor_ok(level: str, touch_type: str, *, is_warm: bool = False) -> bool:
    """A cold draft must be at least P1. Warm contexts are exempt.

    ``touch_type`` is accepted for future per-type policy; today every cold
    touch shares the same P1 floor.
    """
    if is_warm:
        return True
    _ = touch_type
    return level_rank(level) >= 1


def infer_level(
    *,
    has_company: bool = False,
    has_sector: bool = False,
    has_pain_from_site: bool = False,
    has_trigger: bool = False,
    has_proof_angle: bool = False,
) -> str:
    if has_proof_angle:
        return "P4"
    if has_trigger:
        return "P3"
    if has_pain_from_site:
        return "P2"
    if has_company and has_sector:
        return "P1"
    return "P0"
