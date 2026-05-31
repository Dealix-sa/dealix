"""ICP definitions."""

from __future__ import annotations

from dataclasses import dataclass, field

from pydantic import BaseModel, ConfigDict, Field


class ICP(BaseModel):
    model_config = ConfigDict(extra="forbid")

    icp_id: str
    name: str
    sector: str
    buyer_role: str
    pain_points: list[str] = Field(default_factory=list)
    geography: str = "Saudi Arabia"
    avg_deal_sar: float = 0.0


@dataclass
class ICPLibrary:
    _icps: dict[str, ICP] = field(default_factory=dict)

    def upsert(self, icp: ICP) -> ICP:
        self._icps[icp.icp_id] = icp
        return icp

    def get(self, icp_id: str) -> ICP:
        return self._icps[icp_id]

    def list(self) -> list[ICP]:
        return list(self._icps.values())
