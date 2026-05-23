"""
Approval matrix.

Reads `dealix/registers/approval_classes.yaml` and provides the lookup
the control plane and agents use to determine which approval class a
given action requires.

This module is intentionally pure (no I/O outside the YAML file) so it
is trivial to test and impossible to bypass.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

REGISTER_PATH = Path(__file__).resolve().parent.parent / "registers" / "approval_classes.yaml"


@dataclass(frozen=True, slots=True)
class ActionPolicy:
    action: str
    approval_class: str
    notes: str = ""


class ApprovalMatrix:
    """Lookup approval class for an action.

    The register format is intentionally minimal so the YAML can be
    parsed without a full YAML library if needed.
    """

    DEFAULT_CLASS = "founder"
    BLOCKED_KEYWORDS = (
        "auto_send_external",
        "auto-execute outbound",
        "auto execute outbound",
    )

    def __init__(self, register: Mapping[str, str] | None = None) -> None:
        self._register: dict[str, str] = dict(register or {})

    @classmethod
    def from_register(cls, path: Path = REGISTER_PATH) -> "ApprovalMatrix":
        register: dict[str, str] = {}
        if not path.exists():
            return cls(register)
        for raw in path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if ":" not in line:
                continue
            key, _, value = line.partition(":")
            key = key.strip().strip('"').strip("'")
            value = value.strip().strip('"').strip("'")
            if key and value and value not in {"|", ">", "{}", "[]"}:
                register[key] = value
        return cls(register)

    def classify(self, action: str) -> ActionPolicy:
        lowered = action.lower()
        for blocked in self.BLOCKED_KEYWORDS:
            if blocked in lowered:
                return ActionPolicy(action=action, approval_class="blocked",
                                    notes="Permanently blocked by doctrine.")
        approval_class = self._register.get(action, self.DEFAULT_CLASS)
        return ActionPolicy(action=action, approval_class=approval_class)

    def is_auto(self, action: str) -> bool:
        return self.classify(action).approval_class == "auto"

    def requires_founder(self, action: str) -> bool:
        return self.classify(action).approval_class.startswith("founder")

    def is_blocked(self, action: str) -> bool:
        return self.classify(action).approval_class == "blocked"
