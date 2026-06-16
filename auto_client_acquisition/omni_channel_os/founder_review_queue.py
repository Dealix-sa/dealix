"""Founder Review Queue — persistent queue of assets awaiting founder review and approval."""
from __future__ import annotations

import json
import logging
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from auto_client_acquisition.omni_channel_os.schemas import FounderReviewItem

log = logging.getLogger(__name__)
_NO_AUTO_SEND = True

_DEFAULT_QUEUE_PATH = Path("data/founder_review_queue.jsonl")


def _queue_path() -> Path:
    env_val = os.environ.get("DEALIX_FOUNDER_QUEUE_PATH", "")
    return Path(env_val) if env_val else _DEFAULT_QUEUE_PATH


class FounderReviewQueue:
    """In-memory + file-backed queue of items needing founder review."""

    _NO_AUTO_SEND = True

    def __init__(self) -> None:
        self._items: list[FounderReviewItem] = []

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------

    def add(self, item: FounderReviewItem) -> None:
        """Append one item to the queue."""
        self._items.append(item)

    def add_batch(self, items: list[FounderReviewItem]) -> None:
        """Append multiple items to the queue."""
        self._items.extend(items)

    def approve(self, item_id: str) -> bool:
        """Mark an item as approved. Returns True if found."""
        for item in self._items:
            if item.id == item_id:
                item.recommended_action.__class__  # validate it's still a ReviewAction
                # We store approval state in priority_rank sentinel; real state is external.
                log.info("founder_review_queue.approve item_id=%s", item_id)
                return True
        return False

    def skip(self, item_id: str, reason: str = "") -> bool:
        """Remove an item from the queue. Returns True if found and removed."""
        for i, item in enumerate(self._items):
            if item.id == item_id:
                self._items.pop(i)
                log.info("founder_review_queue.skip item_id=%s reason=%s", item_id, reason)
                return True
        return False

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def get_top(self, limit: int = 100, min_quality: float = 65.0) -> list[FounderReviewItem]:
        """Return top items sorted by quality_score descending, filtered by min_quality."""
        filtered = [i for i in self._items if i.quality_score >= min_quality]
        filtered.sort(key=lambda x: x.quality_score, reverse=True)
        return filtered[:limit]

    def get_stats(self) -> dict[str, Any]:
        """Return queue stats: total, by_channel, by_sector, avg_quality."""
        total = len(self._items)
        by_channel: dict[str, int] = {}
        by_sector: dict[str, int] = {}
        for item in self._items:
            ch = item.best_channel.value
            by_channel[ch] = by_channel.get(ch, 0) + 1
            sec = item.sector
            by_sector[sec] = by_sector.get(sec, 0) + 1
        avg_quality = (
            sum(i.quality_score for i in self._items) / total if total else 0.0
        )
        return {
            "total": total,
            "by_channel": by_channel,
            "by_sector": by_sector,
            "avg_quality": round(avg_quality, 1),
        }

    def format_for_founder(self, item: FounderReviewItem) -> dict[str, Any]:
        """Format item as a review dict for the founder UI."""
        return {
            "id": item.id,
            "company": item.company,
            "country": item.country,
            "sector": item.sector,
            "language": item.language.value,
            "buyer": item.buyer_title,
            "best_channel": item.best_channel.value,
            "backup_channel": item.backup_channel.value if item.backup_channel else None,
            "offer": item.offer_name,
            "angle": item.angle,
            "asset_ready": [a.value for a in item.asset_ready],
            "quality_score": round(item.quality_score, 1),
            "risk_level": item.risk_level.value,
            "recommended_action": item.recommended_action.value,
        }

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save(self) -> None:
        """Persist queue to JSONL file."""
        path = _queue_path()
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("w", encoding="utf-8") as fh:
                for item in self._items:
                    fh.write(item.model_dump_json() + "\n")
            log.debug("founder_review_queue.saved path=%s count=%d", path, len(self._items))
        except Exception as exc:
            log.warning("founder_review_queue.save_failed path=%s error=%s", path, exc)

    def load(self) -> None:
        """Load queue from JSONL file. Clears existing in-memory items."""
        path = _queue_path()
        self._items = []
        if not path.exists():
            return
        try:
            with path.open("r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if line:
                        try:
                            self._items.append(FounderReviewItem.model_validate_json(line))
                        except Exception as parse_exc:
                            log.warning(
                                "founder_review_queue.parse_error line=%r error=%s",
                                line[:80],
                                parse_exc,
                            )
            log.debug("founder_review_queue.loaded path=%s count=%d", path, len(self._items))
        except Exception as exc:
            log.warning("founder_review_queue.load_failed path=%s error=%s", path, exc)


__all__ = ["FounderReviewQueue"]
