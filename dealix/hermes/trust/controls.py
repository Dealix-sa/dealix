"""Trust controls — named safety mechanisms with on/off state and owner."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class ControlState(StrEnum):
    active = "active"
    paused = "paused"
    removed = "removed"


class Control(BaseModel):
    model_config = ConfigDict(extra="forbid")

    control_id: str
    name: str
    owner: str = "Sami"
    description: str = ""
    state: ControlState = ControlState.active
    framework_refs: list[str] = []  # e.g. NIST_AI_RMF.MANAGE.4


@dataclass
class ControlCatalog:
    _controls: dict[str, Control] = field(default_factory=dict)

    def register(self, control: Control) -> Control:
        self._controls[control.control_id] = control
        return control

    def get(self, control_id: str) -> Control:
        return self._controls[control_id]

    def list(self) -> list[Control]:
        return list(self._controls.values())
