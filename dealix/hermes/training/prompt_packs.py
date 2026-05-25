"""Prompt packs — reusable prompt sets per role."""

from __future__ import annotations

from dataclasses import dataclass, field

from pydantic import BaseModel, ConfigDict, Field


class PromptPack(BaseModel):
    model_config = ConfigDict(extra="forbid")

    pack_id: str
    title: str
    role: str
    prompts: list[str] = Field(default_factory=list)


@dataclass
class PromptPackLibrary:
    _packs: dict[str, PromptPack] = field(default_factory=dict)

    def upsert(self, pack: PromptPack) -> PromptPack:
        self._packs[pack.pack_id] = pack
        return pack

    def list(self) -> list[PromptPack]:
        return list(self._packs.values())
