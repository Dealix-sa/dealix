"""Base types shared by all Autonomous OS adapters."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class AdapterStatus:
    name: str
    available: bool
    mode: str  # "live" | "offline_fallback" | "draft_only"
    detail: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "available": self.available,
            "mode": self.mode,
            "detail": self.detail,
        }


@dataclass
class AdapterResult:
    ok: bool
    mode: str  # "live" | "offline_fallback" | "draft_only"
    data: Any = None
    error: str = ""
    meta: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "mode": self.mode,
            "data": self.data,
            "error": self.error,
            "meta": self.meta,
        }


class Adapter:
    """Common contract. Subclasses must be offline-safe and never send."""

    name: str = "adapter"

    def is_available(self) -> bool:  # pragma: no cover - overridden
        return False

    def status(self) -> AdapterStatus:  # pragma: no cover - overridden
        return AdapterStatus(name=self.name, available=self.is_available(), mode="offline_fallback")
