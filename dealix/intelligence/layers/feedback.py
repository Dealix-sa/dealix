"""
Feedback / active-learning store — thumbs + structured labels.
ذاكرة التغذية الراجعة — تخزين تقييمات وتسميات نشطة.

Designed for "human-in-the-loop" loops: agents emit a prediction,
operators thumbs-up/down with a free-text reason, the store buckets and
returns ranked candidates for re-labeling. Persists to JSONL on demand.
"""

from __future__ import annotations

import json
import threading
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable, Literal

Verdict = Literal["positive", "negative", "neutral"]


@dataclass
class Feedback:
    item_id: str
    layer: str
    prediction: Any
    verdict: Verdict
    reason: str = ""
    actor: str = "anonymous"
    score: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


@dataclass(frozen=True)
class FeedbackSummary:
    layer: str
    total: int
    positives: int
    negatives: int
    neutrals: int
    accuracy: float  # positives / (positives+negatives)
    avg_score: float | None
    recent_negatives: tuple[Feedback, ...]


class FeedbackStore:
    """Thread-safe feedback store with simple analytics."""

    def __init__(self, *, persist_path: str | Path | None = None) -> None:
        self._items: list[Feedback] = []
        self._lock = threading.RLock()
        self._persist_path = Path(persist_path) if persist_path else None
        if self._persist_path and self._persist_path.exists():
            self._load()

    # ── CRUD ──────────────────────────────────────────────────────
    def add(
        self,
        item_id: str,
        layer: str,
        prediction: Any,
        verdict: Verdict,
        *,
        reason: str = "",
        actor: str = "anonymous",
        score: float | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Feedback:
        if not item_id or not layer:
            raise ValueError("item_id and layer required")
        if verdict not in ("positive", "negative", "neutral"):
            raise ValueError("verdict must be positive | negative | neutral")
        fb = Feedback(
            item_id=item_id,
            layer=layer,
            prediction=prediction,
            verdict=verdict,
            reason=reason,
            actor=actor,
            score=score,
            metadata=metadata or {},
        )
        with self._lock:
            self._items.append(fb)
            self._persist_append(fb)
        return fb

    def add_many(self, items: Iterable[dict[str, Any]]) -> int:
        count = 0
        for item in items:
            self.add(
                item_id=str(item["item_id"]),
                layer=str(item["layer"]),
                prediction=item.get("prediction"),
                verdict=item.get("verdict", "neutral"),
                reason=item.get("reason", ""),
                actor=item.get("actor", "anonymous"),
                score=item.get("score"),
                metadata=item.get("metadata"),
            )
            count += 1
        return count

    def list(
        self,
        *,
        layer: str | None = None,
        verdict: Verdict | None = None,
        limit: int = 100,
    ) -> list[Feedback]:
        with self._lock:
            out = list(self._items)
        if layer:
            out = [f for f in out if f.layer == layer]
        if verdict:
            out = [f for f in out if f.verdict == verdict]
        return out[-limit:]

    # ── Analytics ─────────────────────────────────────────────────
    def summary(self, layer: str) -> FeedbackSummary:
        with self._lock:
            items = [f for f in self._items if f.layer == layer]
        pos = sum(1 for f in items if f.verdict == "positive")
        neg = sum(1 for f in items if f.verdict == "negative")
        neu = sum(1 for f in items if f.verdict == "neutral")
        scores = [f.score for f in items if f.score is not None]
        avg = round(sum(scores) / len(scores), 4) if scores else None
        accuracy = pos / (pos + neg) if (pos + neg) else 0.0
        recent_neg = tuple(reversed([f for f in items if f.verdict == "negative"][-5:]))
        return FeedbackSummary(
            layer=layer,
            total=len(items),
            positives=pos,
            negatives=neg,
            neutrals=neu,
            accuracy=round(accuracy, 4),
            avg_score=avg,
            recent_negatives=recent_neg,
        )

    def candidates_for_relabel(self, layer: str, *, limit: int = 20) -> list[Feedback]:
        """Items most likely to benefit from manual relabel — recent negatives + low scores."""
        with self._lock:
            items = [f for f in self._items if f.layer == layer]
        scored: list[tuple[float, Feedback]] = []
        for f in items:
            score = 0.0
            if f.verdict == "negative":
                score += 1.0
            if f.score is not None and f.score < 0.5:
                score += 0.5
            if not f.reason:
                score += 0.1
            scored.append((score, f))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [f for _, f in scored[:limit]]

    # ── Persistence (JSONL append-only) ───────────────────────────
    def _persist_append(self, fb: Feedback) -> None:
        if not self._persist_path:
            return
        try:
            self._persist_path.parent.mkdir(parents=True, exist_ok=True)
            with self._persist_path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(asdict(fb), default=str, ensure_ascii=False) + "\n")
        except Exception:  # pragma: no cover
            pass

    def _load(self) -> None:
        try:
            with self._persist_path.open("r", encoding="utf-8") as fh:  # type: ignore[union-attr]
                for line in fh:
                    if not line.strip():
                        continue
                    data = json.loads(line)
                    self._items.append(Feedback(**data))
        except Exception:  # pragma: no cover
            pass
