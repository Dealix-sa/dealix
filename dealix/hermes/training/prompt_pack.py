"""Arabic+English prompt packs — first-class assets."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field


@dataclass
class PromptPack:
    id: str
    name: str
    language: str          # "ar" | "en" | "ar+en"
    prompts: list[str]
    target_audience: str


@dataclass
class PromptPackLibrary:
    _by_id: dict[str, PromptPack] = field(default_factory=dict)

    def add(self, *, name: str, language: str, prompts: list[str], target_audience: str) -> PromptPack:
        if not prompts:
            raise ValueError("PromptPack must contain at least one prompt.")
        p = PromptPack(
            id=f"prm_{uuid.uuid4().hex[:10]}",
            name=name,
            language=language,
            prompts=list(prompts),
            target_audience=target_audience,
        )
        self._by_id[p.id] = p
        return p

    def all(self) -> list[PromptPack]:
        return list(self._by_id.values())


__all__ = ["PromptPack", "PromptPackLibrary"]
