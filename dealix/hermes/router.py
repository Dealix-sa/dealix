"""Hermes router — maps a task to (sub_agent, gear, LLM config).

Classification is intentionally cheap and deterministic (keyword heuristics +
optional explicit hint). For ambiguous tasks the router defaults to dealix-pm,
which is the supervising sub-agent and can decompose further.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Optional

from ..llm.engine import (
    DealixEngine,
    Gear,
    GearConfig,
    ProviderName,
    TaskType,
    active_provider,
)


class TaskClass(StrEnum):
    """High-level task class → sub-agent."""
    PM = "pm"               # planning, status, milestone reviews
    ENGINEERING = "engineering"  # code, tests, migrations
    CONTENT = "content"     # docs, AR/EN copy, sector reports
    SALES = "sales"         # qualification, proposals, warm-list drafts
    DELIVERY = "delivery"   # 7-day sprint steps


_SUB_AGENT: dict[TaskClass, str] = {
    TaskClass.PM: "dealix-pm",
    TaskClass.ENGINEERING: "dealix-engineer",
    TaskClass.CONTENT: "dealix-content",
    TaskClass.SALES: "dealix-sales",
    TaskClass.DELIVERY: "dealix-delivery",
}


_KEYWORD_TO_CLASS: list[tuple[tuple[str, ...], TaskClass]] = [
    (("code", "fastapi", "router", "migration", "alembic", "pytest", "fix bug",
      "refactor", "type hint", "endpoint"), TaskClass.ENGINEERING),
    (("doc", "case study", "linkedin post", "proposal template",
      "sector report", "markdown", "bilingual"), TaskClass.CONTENT),
    (("qualify", "qualification", "lead", "proposal", "warm-list",
      "outreach draft", "sales", "rung", "offer ladder"), TaskClass.SALES),
    (("sprint", "source passport", "dq score", "account scor",
      "draft pack", "governance review", "proof pack",
      "capital asset", "retainer eligibility", "delivery"),
     TaskClass.DELIVERY),
    (("status", "what next", "milestone", "30 day", "60 day",
      "90 day", "friction", "plan"), TaskClass.PM),
]


_TASK_GEAR_FOR_CLASS: dict[TaskClass, TaskType] = {
    TaskClass.PM: TaskType.POLICY_EVALUATION,
    TaskClass.ENGINEERING: TaskType.NEW_FEATURE,
    TaskClass.CONTENT: TaskType.DOCUMENTATION,
    TaskClass.SALES: TaskType.CLASSIFICATION,
    TaskClass.DELIVERY: TaskType.COMPLIANCE,
}


@dataclass
class Route:
    task_class: TaskClass
    sub_agent: str
    gear: Gear
    gear_config: GearConfig


class HermesRouter:
    """Stateless router; safe to instantiate per request."""

    def __init__(self, provider: Optional[ProviderName] = None) -> None:
        self.provider: ProviderName = provider or active_provider()

    def classify(self, intent_text: str, hint: Optional[TaskClass] = None) -> TaskClass:
        if hint is not None:
            return hint
        low = (intent_text or "").lower()
        for keywords, cls in _KEYWORD_TO_CLASS:
            if any(k in low for k in keywords):
                return cls
        return TaskClass.PM

    def route(self, intent_text: str, hint: Optional[TaskClass] = None) -> Route:
        cls = self.classify(intent_text, hint)
        task_type = _TASK_GEAR_FOR_CLASS[cls]
        gear_config = DealixEngine.get_for_task(task_type, provider=self.provider)
        return Route(
            task_class=cls,
            sub_agent=_SUB_AGENT[cls],
            gear=gear_config.gear,
            gear_config=gear_config,
        )
