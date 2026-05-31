"""WorkflowDefinition — load YAML configs into typed workflow objects."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass(frozen=True)
class WorkflowStep:
    agent: str
    output: str


@dataclass(frozen=True)
class WorkflowDefinition:
    workflow_id: str
    steps: tuple[WorkflowStep, ...]
    gates: tuple[str, ...]
    outcome_required: bool
    asset_review_required: bool


WORKFLOW_REGISTRY: dict[str, WorkflowDefinition] = {}
_CONFIG_DIR = Path(__file__).resolve().parent / "configs"


def _load_one(path: Path) -> WorkflowDefinition:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    steps = tuple(WorkflowStep(agent=s["agent"], output=s["output"]) for s in data.get("steps", []))
    return WorkflowDefinition(
        workflow_id=data["workflow_id"],
        steps=steps,
        gates=tuple(data.get("gates", [])),
        outcome_required=bool(data.get("outcome_required", True)),
        asset_review_required=bool(data.get("asset_review_required", False)),
    )


def load_all(config_dir: Path | None = None) -> dict[str, WorkflowDefinition]:
    directory = config_dir or _CONFIG_DIR
    WORKFLOW_REGISTRY.clear()
    for path in sorted(directory.glob("*.yaml")):
        wf = _load_one(path)
        WORKFLOW_REGISTRY[wf.workflow_id] = wf
    return WORKFLOW_REGISTRY


# Eager-load so importing the package gives you the registry.
try:
    load_all()
except FileNotFoundError:
    pass
