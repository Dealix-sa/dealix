"""
ICP Registry — كل ICP يحدد القطاع، الحجم، الـ pain، شخصية المشتري، والقنوات
المناسبة. يُستخدم في scoring وفي workflows مثل Revenue Hunter.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field


@dataclass
class ICP:
    icp_id: str
    name: str
    sector: str
    company_size_min: int
    company_size_max: int
    geography: str
    primary_pain: str
    buyer_persona: str
    preferred_channels: list[str] = field(default_factory=list)
    excluded_industries: list[str] = field(default_factory=list)


class ICPRegistry:
    def __init__(self) -> None:
        self._icps: dict[str, ICP] = {}
        self._lock = threading.Lock()

    def register(self, icp: ICP) -> ICP:
        with self._lock:
            if icp.icp_id in self._icps:
                raise ValueError(f"icp `{icp.icp_id}` already registered")
            self._icps[icp.icp_id] = icp
        return icp

    def get(self, icp_id: str) -> ICP | None:
        with self._lock:
            return self._icps.get(icp_id)

    def all(self) -> list[ICP]:
        with self._lock:
            return list(self._icps.values())


__all__ = ["ICP", "ICPRegistry"]
