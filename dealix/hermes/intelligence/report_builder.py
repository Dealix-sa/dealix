"""Report Builder — composes a sector / market report from collected signals."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


class ReportBuilder:
    def build(self, *, title: str, sector: str, signals: list[dict[str, Any]]) -> dict[str, Any]:
        return {
            "title": title,
            "sector": sector,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "summary": (
                f"{len(signals)} signals analysed for {sector}. "
                "Highest-confidence items lead the recommendations."
            ),
            "signals": sorted(signals, key=lambda s: s.get("confidence", 0.0), reverse=True)[:10],
            "draft_only": True,
            "external_publish": False,
        }
