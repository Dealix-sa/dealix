"""Local-first model routing policy for Dealix strategy execution."""

from __future__ import annotations

from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class ModelRoute:
    task: str
    preferred_route: str
    reason: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


def route_task(task: str) -> ModelRoute:
    lowered = task.lower()
    if any(word in lowered for word in ("classify", "score", "summary", "summarize")):
        return ModelRoute(task=task, preferred_route="local_small_model", reason="low risk deterministic support task")
    if any(word in lowered for word in ("draft", "copy", "arabic", "english")):
        return ModelRoute(task=task, preferred_route="local_or_low_cost_fallback", reason="quality can be reviewed before use")
    if any(word in lowered for word in ("code", "test", "refactor")):
        return ModelRoute(task=task, preferred_route="coding_agent_or_stronger_model", reason="repo changes need higher accuracy")
    return ModelRoute(task=task, preferred_route="local_first", reason="default lowest-cost safe route")
