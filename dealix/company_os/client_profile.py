"""Client profile model for Company OS runs."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class ClientProfile:
    client_id: str
    name: str
    industry: str
    country: str = "Saudi Arabia"
    city: str = "Riyadh"
    language: str = "ar/en"
    goals: list[str] = field(default_factory=list)
    restrictions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
