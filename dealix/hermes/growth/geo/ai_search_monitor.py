"""
AI-search monitor — records observations of how the brand appears in
generative answers over time.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field


@dataclass
class AISearchObservation:
    engine: str             # "perplexity" | "google_ai_overview" | "chatgpt_search" | ...
    query: str
    appeared: bool
    cited_as: str = ""
    cited_url: str = ""
    snippet: str = ""
    captured_at: float = field(default_factory=time.time)


class AISearchMonitor:
    def __init__(self) -> None:
        self._observations: list[AISearchObservation] = []

    def record(self, observation: AISearchObservation) -> None:
        self._observations.append(observation)

    def appearance_rate(self, *, engine: str | None = None) -> float:
        observations = (
            [o for o in self._observations if o.engine == engine]
            if engine
            else self._observations
        )
        if not observations:
            return 0.0
        appeared = sum(1 for o in observations if o.appeared)
        return round(appeared / len(observations), 4)

    def __len__(self) -> int:
        return len(self._observations)

    def __iter__(self):
        return iter(self._observations)
