"""
Strategy Registry — loads declarative strategy definitions from YAML.

A strategy is a named, ordered set of steps that advance one commercial or
operational objective (revenue sprint, Saudi market access, technical trust,
content factory, proof pack). Strategies are data, not code, so the founder
can review and edit them without touching the engine.

Strategy YAML contract (see dealix/autonomous_os/strategies/*.yaml):

    id: revenue_sprint            # required, unique
    name: Revenue Command Room Sprint
    objective_en: "..."
    objective_ar: "..."
    language: ar                  # default output language
    enabled: true                 # inactive strategies are skipped
    priority: 90                  # higher runs first
    kpis: [qualified_leads, proposals_drafted]
    guardrails: [draft_only, approval_first, no_cold_outreach]
    steps:
      - action: draft_proof_pack
        kind: internal            # internal | external_draft
        risk: 0.1                 # 0..1
        channel: null             # whatsapp|email|... for external drafts
        offer: transformation_diagnostic_sprint
        requires_approval: false
        output: proof_pack_draft
        description: "..."
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

DEFAULT_STRATEGIES_DIR = Path(__file__).resolve().parent / "strategies"


@dataclass
class StrategyStep:
    action: str
    kind: str = "internal"
    risk: float = 0.0
    channel: str | None = None
    offer: str | None = None
    requires_approval: bool = False
    output: str | None = None
    description: str = ""

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> StrategyStep:
        return cls(
            action=str(d["action"]),
            kind=str(d.get("kind", "internal")),
            risk=float(d.get("risk", 0.0) or 0.0),
            channel=(str(d["channel"]) if d.get("channel") else None),
            offer=(str(d["offer"]) if d.get("offer") else None),
            requires_approval=bool(d.get("requires_approval", False)),
            output=(str(d["output"]) if d.get("output") else None),
            description=str(d.get("description", "")),
        )


@dataclass
class Strategy:
    id: str
    name: str
    objective_en: str = ""
    objective_ar: str = ""
    language: str = "ar"
    enabled: bool = True
    priority: int = 50
    kpis: list[str] = field(default_factory=list)
    guardrails: list[str] = field(default_factory=list)
    steps: list[StrategyStep] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Strategy:
        if not d.get("id"):
            raise ValueError("strategy is missing required 'id'")
        return cls(
            id=str(d["id"]),
            name=str(d.get("name", d["id"])),
            objective_en=str(d.get("objective_en", "")),
            objective_ar=str(d.get("objective_ar", "")),
            language=str(d.get("language", "ar")),
            enabled=bool(d.get("enabled", True)),
            priority=int(d.get("priority", 50)),
            kpis=[str(k) for k in d.get("kpis", []) or []],
            guardrails=[str(g) for g in d.get("guardrails", []) or []],
            steps=[StrategyStep.from_dict(s) for s in d.get("steps", []) or []],
        )


class StrategyRegistry:
    """Loads and indexes strategy YAML files from a directory."""

    def __init__(self, strategies_dir: Path | str | None = None) -> None:
        self.dir = Path(strategies_dir) if strategies_dir else DEFAULT_STRATEGIES_DIR
        self._by_id: dict[str, Strategy] = {}

    def load(self) -> StrategyRegistry:
        self._by_id.clear()
        if not self.dir.exists():
            return self
        for path in sorted(self.dir.glob("*.yaml")):
            raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            if not isinstance(raw, dict):
                raise ValueError(f"{path.name}: top-level YAML must be a mapping")
            strategy = Strategy.from_dict(raw)
            if strategy.id in self._by_id:
                raise ValueError(f"duplicate strategy id '{strategy.id}' in {path.name}")
            self._by_id[strategy.id] = strategy
        return self

    def all(self) -> list[Strategy]:
        return list(self._by_id.values())

    def active(self) -> list[Strategy]:
        """Enabled strategies, highest priority first."""
        return sorted(
            (s for s in self._by_id.values() if s.enabled),
            key=lambda s: (-s.priority, s.id),
        )

    def get(self, strategy_id: str) -> Strategy | None:
        return self._by_id.get(strategy_id)

    def __len__(self) -> int:
        return len(self._by_id)
