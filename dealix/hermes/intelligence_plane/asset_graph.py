"""
Asset Graph — كل نتيجة تجارية ناجحة تتحول إلى أصل قابل لإعادة الاستخدام
(template, playbook, evidence pack). الـ Asset Library يُربط بـ outcome_graph
لمعرفة "أي أصل دفع الـ revenue الأكثر".
"""

from __future__ import annotations

import threading
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import Any


class AssetKind(StrEnum):
    PROPOSAL_TEMPLATE = "proposal_template"
    MESSAGE_TEMPLATE = "message_template"
    PLAYBOOK = "playbook"
    EVIDENCE_PACK = "evidence_pack"
    CASE_STUDY = "case_study"
    PARTNER_PITCH = "partner_pitch"
    MARKET_REPORT = "market_report"


@dataclass
class Asset:
    asset_id: str
    kind: AssetKind
    title: str
    body: dict[str, Any]  # arbitrary structured payload
    source_execution_id: str | None = None
    source_outcome_id: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    tags: list[str] = field(default_factory=list)
    revenue_attributed_sar: int = 0


class AssetGraph:
    def __init__(self) -> None:
        self._assets: dict[str, Asset] = {}
        self._by_kind: dict[AssetKind, list[str]] = defaultdict(list)
        self._lock = threading.Lock()

    def add(self, asset: Asset) -> Asset:
        with self._lock:
            self._assets[asset.asset_id] = asset
            self._by_kind[asset.kind].append(asset.asset_id)
            return asset

    def attribute_revenue(self, asset_id: str, amount_sar: int) -> None:
        with self._lock:
            asset = self._assets.get(asset_id)
            if asset is None:
                raise KeyError(asset_id)
            asset.revenue_attributed_sar += amount_sar

    def by_kind(self, kind: AssetKind) -> list[Asset]:
        with self._lock:
            return [self._assets[aid] for aid in self._by_kind.get(kind, [])]

    def top_by_revenue(self, n: int = 10) -> list[Asset]:
        with self._lock:
            return sorted(
                self._assets.values(),
                key=lambda a: a.revenue_attributed_sar,
                reverse=True,
            )[:n]


__all__ = ["Asset", "AssetGraph", "AssetKind"]
