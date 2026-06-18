"""
Knowledge graph — in-memory triple store with subject/object indices.
رسم المعرفة — مخزن ثلاثيات بفهارس على الموضوع والمفعول.

Lightweight enough to live next to a customer brain. Supports:
    - upsert / delete triples
    - SPO / SP / PO / S / P / O pattern queries
    - per-entity neighborhood traversal (BFS, max depth)
    - JSON serialization for persistence
"""

from __future__ import annotations

import json
import threading
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable


@dataclass(frozen=True)
class Triple:
    subject: str
    predicate: str
    object: str
    confidence: float = 1.0
    source: str = ""
    metadata: tuple[tuple[str, Any], ...] = field(default_factory=tuple)
    created_at: float = field(default_factory=time.time)


class KnowledgeGraph:
    """Triple store with bidirectional indices."""

    def __init__(self) -> None:
        self._triples: dict[tuple[str, str, str], Triple] = {}
        self._spo: dict[str, set[tuple[str, str]]] = {}  # s -> {(p,o)}
        self._pos: dict[str, set[tuple[str, str]]] = {}  # p -> {(s,o)}
        self._osp: dict[str, set[tuple[str, str]]] = {}  # o -> {(s,p)}
        self._lock = threading.RLock()

    # ── CRUD ──────────────────────────────────────────────────────
    def add(
        self,
        subject: str,
        predicate: str,
        object_: str,
        *,
        confidence: float = 1.0,
        source: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> Triple:
        if not subject or not predicate or not object_:
            raise ValueError("subject/predicate/object required")
        meta_tuple = tuple(sorted((metadata or {}).items()))
        triple = Triple(
            subject=subject,
            predicate=predicate,
            object=object_,
            confidence=confidence,
            source=source,
            metadata=meta_tuple,
        )
        key = (subject, predicate, object_)
        with self._lock:
            self._triples[key] = triple
            self._spo.setdefault(subject, set()).add((predicate, object_))
            self._pos.setdefault(predicate, set()).add((subject, object_))
            self._osp.setdefault(object_, set()).add((subject, predicate))
        return triple

    def add_many(self, triples: Iterable[tuple[str, str, str]]) -> int:
        count = 0
        for s, p, o in triples:
            self.add(s, p, o)
            count += 1
        return count

    def delete(self, subject: str, predicate: str, object_: str) -> bool:
        key = (subject, predicate, object_)
        with self._lock:
            existed = key in self._triples
            self._triples.pop(key, None)
            if existed:
                self._spo.get(subject, set()).discard((predicate, object_))
                self._pos.get(predicate, set()).discard((subject, object_))
                self._osp.get(object_, set()).discard((subject, predicate))
        return existed

    # ── Query ─────────────────────────────────────────────────────
    def query(
        self,
        subject: str | None = None,
        predicate: str | None = None,
        object_: str | None = None,
    ) -> list[Triple]:
        with self._lock:
            if subject and predicate and object_:
                t = self._triples.get((subject, predicate, object_))
                return [t] if t else []
            if subject:
                pairs = self._spo.get(subject, set())
                out = []
                for p, o in pairs:
                    if (predicate and p != predicate) or (object_ and o != object_):
                        continue
                    t = self._triples.get((subject, p, o))
                    if t:
                        out.append(t)
                return out
            if predicate:
                pairs = self._pos.get(predicate, set())
                out = []
                for s, o in pairs:
                    if object_ and o != object_:
                        continue
                    t = self._triples.get((s, predicate, o))
                    if t:
                        out.append(t)
                return out
            if object_:
                pairs = self._osp.get(object_, set())
                return [self._triples[(s, p, object_)] for s, p in pairs]
            return list(self._triples.values())

    def neighbors(
        self, subject: str, *, max_depth: int = 2, max_results: int = 64
    ) -> list[Triple]:
        if max_depth < 1:
            return []
        seen: set[str] = {subject}
        frontier: list[str] = [subject]
        out: list[Triple] = []
        for _ in range(max_depth):
            next_frontier: list[str] = []
            for node in frontier:
                with self._lock:
                    for p, o in self._spo.get(node, set()):
                        t = self._triples.get((node, p, o))
                        if t and len(out) < max_results:
                            out.append(t)
                        if o not in seen:
                            seen.add(o)
                            next_frontier.append(o)
                    for s, p in self._osp.get(node, set()):
                        t = self._triples.get((s, p, node))
                        if t and len(out) < max_results:
                            out.append(t)
                        if s not in seen:
                            seen.add(s)
                            next_frontier.append(s)
            if not next_frontier or len(out) >= max_results:
                break
            frontier = next_frontier
        return out

    # ── Stats ─────────────────────────────────────────────────────
    def stats(self) -> dict[str, Any]:
        with self._lock:
            return {
                "triples": len(self._triples),
                "subjects": len(self._spo),
                "predicates": len(self._pos),
                "objects": len(self._osp),
            }

    # ── Persistence ───────────────────────────────────────────────
    def to_json(self) -> str:
        with self._lock:
            return json.dumps(
                [self._triple_to_dict(t) for t in self._triples.values()],
                ensure_ascii=False,
            )

    def save(self, path: str | Path) -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(self.to_json(), encoding="utf-8")

    def load(self, path: str | Path) -> int:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        count = 0
        for item in data:
            self.add(
                item["subject"],
                item["predicate"],
                item["object"],
                confidence=float(item.get("confidence", 1.0)),
                source=item.get("source", ""),
                metadata=dict(item.get("metadata", []) or []),
            )
            count += 1
        return count

    @staticmethod
    def _triple_to_dict(t: Triple) -> dict[str, Any]:
        d = asdict(t)
        d["metadata"] = list(t.metadata)
        return d
