"""Dealix LLM Strategy - Fallback chains per task type."""

import os
from enum import Enum
from typing import Literal, Optional

from pydantic import BaseModel, Field


def _env_first(*names: str, default: str = "") -> str:
    for name in names:
        value = os.getenv(name, "")
        if value:
            return value
    return default


def _env_first(*names: str, default: str = "") -> str:
    for name in names:
        value = os.getenv(name, "")
        if value:
            return value
    return default


def _env_first(*names: str, default: str = "") -> str:
    for name in names:
        value = os.getenv(name, "")
        if value:
            return value
    return default


def _env_first(*names: str, default: str = "") -> str:
    for name in names:
def _env_first(*keys: str, default: str = "") -> str:
    for key in keys:
        value = os.getenv(key, "").strip()
        if value:
            return value
    return default


        value = os.getenv(name, "")
        if value:
            return value
    return default


class ModelTier(str, Enum):
    PRIMARY = "primary"
    ARCHITECT = "architect"
    LIGHT = "light"
    FALLBACK = "fallback"


class TaskType(str, Enum):_env_first("PRIMARY_MODEL", "GEAR2_MODEL", "OPENROUTER_MODEL", default="minimax/minimax-m2.5"),
        ModelTier.ARCHITECT: _env_first("ARCHITECT_MODEL", "GEAR3_MODEL", "OPENROUTER_MODEL", default="minimax/minimax-m2.7"),
        ModelTier.LIGHT: _env_first("LIGHT_MODEL", "GEAR1_MODEL", "OPENROUTER_MODEL", default="deepseek/deepseek-chat"),
        ModelTier.FALLBACK: _env_first("FALLBACK_MODEL", "LIGHT_MODEL", "GEAR1_MODEL", "OPENROUTER_MODEL", default="deepseek/deepseek-chat"),
    }

    _TIMEOUTS = {
        ModelTier.PRIMARY: int(_env_first("PRIMARY_TIMEOUT", "GEAR2_TIMEOUT", "OPENROUTER_TIMEOUT", default="120")),
        ModelTier.ARCHITECT: int(_env_first("ARCHITECT_TIMEOUT", "GEAR3_TIMEOUT", "OPENROUTER_TIMEOUT", default="180")),
        ModelTier.LIGHT: int(_env_first("LIGHT_TIMEOUT", "GEAR1_TIMEOUT", "OPENROUTER_TIMEOUT", default="90")),
        ModelTier.FALLBACK: int(_env_first("FALLBACK_TIMEOUT", "LIGHT_TIMEOUT", "GEAR1_TIMEOUT", "OPENROUTER_TIMEOUT", default=
class ModelConfig(BaseModel):
    provider: Literal["openrouter"] = "openrouter"
    model_id: str
    timeout: int = Field(default=120, ge=30, le=300)
    max_retries: int = Field(default=2, ge=0, le=5)
    reasoning_preserved: bo_env_first("GEAR2_MODEL", "PRIMARY_MODEL", default="minimax/minimax-m2.5"),
        ModelTier.ARCHITECT: _env_first("GEAR3_MODEL", "ARCHITECT_MODEL", default="minimax/minimax-m2.7"),
        ModelTier.LIGHT: _env_first("GEAR1_MODEL", "LIGHT_MODEL", "OPENROUTER_MODEL", default="deepseek/deepseek-chat"),
        ModelTier.FALLBACK: _env_first("GEAR1_MODEL", "FALLBACK_MODEL", "OPENROUTER_MODEL", default="deepseek/deepseek-chat"),
    }

    _TIMEOUTS = {
        ModelTier.PRIMARY: int(_env_first("GEAR2_TIMEOUT", "PRIMARY_TIMEOUT", default="120")),
        ModelTier.ARCHITECT: int(_env_first("GEAR3_TIMEOUT", "ARCHITECT_TIMEOUT", default="180")),
        ModelTier.LIGHT: int(_env_first("GEAR1_TIMEOUT", "LIGHT_TIMEOUT", "OPENROUTER_TIMEOUT", default="90")),
        ModelTier.FALLBACK: int(_env_first("GEAR1_TIMEOUT", "FALLBACK_TIMEOUT", "OPENROUTER_TIMEOUT", default=r.PRIMARY, ModelTier.FALLBACK],
        TaskType.CONTENT_CREATION: [ModelTier.PRIMARY, ModelTier.ARCHITECT, ModelTier.FALLBACK],
        TaskType.COMPLIANCE_ANALYSIS: [ModelTier.ARCHITECT, ModelTier.PRIMARY, ModelTier.FALLBACK],
    }

    _MODEL_IDS = {
        ModelTier.PRIMARY: _env_first("GEAR2_MODEL", "PRIMARY_MODEL", default="minimax/minimax-m2.5"),
        ModelTier.ARCHITECT: _env_first("GEAR3_MODEL", "ARCHITECT_MODEL", default="minimax/minimax-m2.7"),
        ModelTier.LIGHT: _env_first("GEAR1_MODEL", "LIGHT_MODEL", "OPENROUTER_MODEL", default="deepseek/deepseek-chat"),
        ModelTier.FALLBACK: _env_first("GEAR1_MODEL", "FALLBACK_MODEL", "OPENROUTER_MODEL", default="deepseek/deepseek-chat"),
    }

    _TIMEOUTS = {
        ModelTier.PRIMARY: int(_env_first("GEAR2_TIMEOUT", "PRIMARY_TIMEOUT", default="120")),
        ModelTier.ARCHITECT: int(_env_first("GEAR3_TIMEOUT", "ARCHITECT_TIMEOUT", default="180")),
        ModelTier.LIGHT: int(_env_first("GEAR1_TIMEOUT", "LIGHT_TIMEOUT", "OPENROUTER_TIMEOUT", default="90")),
        ModelTier.FALLBACK: int(_env_first("GEAR1_TIMEOUT", "FALLBACK_TIMEOUT", "OPENROUTER_TIMEOUT", default="90")),
    }

    def resolve(self, task: TaskType, prefer_cheap: bool = False):
        tiers = self._TASK_MAP.get(task, [ModelTier.PRIMARY, ModelTier.FALLBACK])
        if prefer_cheap:
            order = {ModelTier.LIGHT: 0, ModelTier.FALLBACK: 1, ModelTier.PRIMARY: 2, ModelTier.ARCHITECT: 3}
            tiers = sorted(tiers, key=lambda t: order[t])
        return [
            ModelConfig(
                model_id=self._MODEL_IDS[tier],
                timeout=self._TIMEOUTS[tier],
                reasoning_preserved=(tier != ModelTier.FALLBACK),
            )
            for tier in tiers
        ]


router = LLMStrategyRouter()
