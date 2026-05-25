"""Shared Playbook dataclass — every delivery file produces one of these."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class PlaybookStep:
    name: str
    owner: str  # "agent:..." | "sami" | "customer" | "partner"
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    quality_gates: tuple[str, ...] = field(default_factory=tuple)
    approval_gates: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class Playbook:
    playbook_id: str
    package_id: str
    steps: tuple[PlaybookStep, ...]
    outcome_metrics: tuple[str, ...]
    upsell_path: str
