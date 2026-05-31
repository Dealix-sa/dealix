"""Per-vertical kill/scale evaluation."""

from __future__ import annotations

from enum import StrEnum


class VentureVerdict(StrEnum):
    scale = "scale"
    keep = "keep"
    kill = "kill"


def evaluate_vertical(
    *,
    paid_pilots: int,
    qualified_replies: int,
    days_since_launch: int,
) -> VentureVerdict:
    if paid_pilots >= 2:
        return VentureVerdict.scale
    if days_since_launch >= 45 and qualified_replies == 0:
        return VentureVerdict.kill
    return VentureVerdict.keep
