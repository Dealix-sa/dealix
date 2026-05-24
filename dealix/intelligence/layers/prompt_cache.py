"""
Prompt cache — content-addressable LLM response cache with TTL + LRU.
ذاكرة طلبات النموذج — حفظ ردود LLM لتفادي تكرار الاستدعاء.

Pure Python, thread-safe, optional disk persistence. No external deps.
"""

from __future__ import annotations

import hashlib
import json
import threading
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class CacheEntry:
    key: str
    value: Any
    created_at: float
    expires_at: float | None
    hits: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)


class PromptCache:
    """LRU + TTL cache, optional persistence."""

    def __init__(
        self,
        *,
        max_size: int = 512,
        default_ttl: float | None = 60 * 60,
        persist_path: str | Path | None = None,
    ) -> None:
        if max_size < 1:
            raise ValueError("max_size must be >= 1")
        self.max_size = max_size
        self.default_ttl = default_ttl
        self._store: OrderedDict[str, CacheEntry] = OrderedDict()
        self._lock = threading.RLock()
        self._persist_path = Path(persist_path) if persist_path else None
        self._hits = 0
        self._misses = 0
        if self._persist_path and self._persist_path.exists():
            self._load()

    # ── Key helpers ───────────────────────────────────────────────
    @staticmethod
    def make_key(*parts: Any) -> str:
        payload = json.dumps(parts, sort_keys=True, default=str, ensure_ascii=False)
        return hashlib.blake2b(payload.encode("utf-8"), digest_size=16).hexdigest()

    # ── CRUD ──────────────────────────────────────────────────────
    def get(self, key: str) -> Any | None:
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                self._misses += 1
                return None
            if entry.expires_at is not None and entry.expires_at < time.time():
                self._store.pop(key, None)
                self._misses += 1
                return None
            entry.hits += 1
            self._store.move_to_end(key)
            self._hits += 1
            return entry.value

    def set(
        self,
        key: str,
        value: Any,
        *,
        ttl: float | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        ttl = self.default_ttl if ttl is None else ttl
        expires_at = (time.time() + ttl) if ttl is not None else None
        with self._lock:
            entry = CacheEntry(
                key=key,
                value=value,
                created_at=time.time(),
                expires_at=expires_at,
                metadata=metadata or {},
            )
            if key in self._store:
                self._store.move_to_end(key)
            self._store[key] = entry
            while len(self._store) > self.max_size:
                self._store.popitem(last=False)
            self._persist()

    def get_or_set(self, key: str, factory, *, ttl: float | None = None) -> Any:
        cached = self.get(key)
        if cached is not None:
            return cached
        value = factory()
        self.set(key, value, ttl=ttl)
        return value

    def invalidate(self, key: str) -> bool:
        with self._lock:
            existed = key in self._store
            self._store.pop(key, None)
            if existed:
                self._persist()
            return existed

    def clear(self) -> None:
        with self._lock:
            self._store.clear()
            self._hits = 0
            self._misses = 0
            self._persist()

    # ── Stats ─────────────────────────────────────────────────────
    def stats(self) -> dict[str, Any]:
        with self._lock:
            total = self._hits + self._misses
            return {
                "size": len(self._store),
                "max_size": self.max_size,
                "hits": self._hits,
                "misses": self._misses,
                "hit_rate": round(self._hits / total, 4) if total else 0.0,
                "persistent": self._persist_path is not None,
            }

    # ── Persistence (best-effort, JSON) ───────────────────────────
    def _persist(self) -> None:
        if not self._persist_path:
            return
        try:
            self._persist_path.parent.mkdir(parents=True, exist_ok=True)
            payload = [
                {
                    "key": e.key,
                    "value": e.value,
                    "created_at": e.created_at,
                    "expires_at": e.expires_at,
                    "hits": e.hits,
                    "metadata": e.metadata,
                }
                for e in self._store.values()
            ]
            tmp = self._persist_path.with_suffix(self._persist_path.suffix + ".tmp")
            tmp.write_text(json.dumps(payload, default=str), encoding="utf-8")
            tmp.replace(self._persist_path)
        except Exception:  # pragma: no cover
            pass

    def _load(self) -> None:
        try:
            data = json.loads(self._persist_path.read_text(encoding="utf-8"))  # type: ignore[union-attr]
            for item in data:
                self._store[item["key"]] = CacheEntry(
                    key=item["key"],
                    value=item.get("value"),
                    created_at=float(item.get("created_at", time.time())),
                    expires_at=item.get("expires_at"),
                    hits=int(item.get("hits", 0)),
                    metadata=item.get("metadata", {}),
                )
        except Exception:  # pragma: no cover
            pass
