"""Evidence Chain — append-only, hash-linked evidence ledger for AI Stack runs.

Every artifact the AI Stack produces (passport, draft, query, retrieval set,
governance verdict, ledger entry) is registered here with a SHA-256 hash that
chains back to the previous entry. The chain gives auditors a tamper-evident
trail: if any single link is mutated, every later link's ``prev_hash`` no
longer reconciles.

The chain is **per-run** and lives in memory by default. Persistent backends
can be added (JSONL / Postgres) without changing the surface; existing tests
should depend only on the public functions in ``__all__``.
"""

from __future__ import annotations

import hashlib
import json
import threading
import uuid
from collections.abc import Iterator, Mapping
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime, timezone
from typing import Any

# Sentinel "genesis" hash placed before the first real link in a chain.
GENESIS_HASH: str = "0" * 64


@dataclass(frozen=True, slots=True)
class EvidenceLink:
    """A single link in a per-run evidence chain."""

    link_id: str
    run_id: str
    layer: str
    artifact_type: str
    content_hash: str
    prev_hash: str
    chain_hash: str
    summary: str
    metadata: Mapping[str, Any] = field(default_factory=dict)
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["metadata"] = dict(self.metadata)
        return data


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _hash(payload: str | Mapping[str, Any]) -> str:
    if isinstance(payload, Mapping):
        serialized = json.dumps(payload, sort_keys=True, ensure_ascii=False, default=str)
    else:
        serialized = str(payload)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def _compute_chain_hash(prev_hash: str, content_hash: str, layer: str) -> str:
    """Each chain hash binds (prev_hash || content_hash || layer)."""
    return hashlib.sha256(
        f"{prev_hash}|{content_hash}|{layer}".encode(),
    ).hexdigest()


class EvidenceChain:
    """Per-run evidence chain.

    Thread-safe append + verification. The chain is identified by ``run_id``;
    callers should keep one chain per AI Stack run and pass it to each layer.
    """

    __slots__ = ("_links", "_lock", "run_id", "tenant_id")

    def __init__(self, *, run_id: str, tenant_id: str) -> None:
        if not run_id or not run_id.strip():
            raise ValueError("run_id is required")
        if not tenant_id or not tenant_id.strip():
            raise ValueError("tenant_id is required")
        self.run_id = run_id.strip()
        self.tenant_id = tenant_id.strip()
        self._links: list[EvidenceLink] = []
        self._lock = threading.RLock()

    def __len__(self) -> int:
        with self._lock:
            return len(self._links)

    def __iter__(self) -> Iterator[EvidenceLink]:
        with self._lock:
            return iter(list(self._links))

    @property
    def head(self) -> EvidenceLink | None:
        with self._lock:
            return self._links[-1] if self._links else None

    def append(
        self,
        *,
        layer: str,
        artifact_type: str,
        content: str | Mapping[str, Any],
        summary: str,
        metadata: Mapping[str, Any] | None = None,
    ) -> EvidenceLink:
        """Append a new evidence link bound to the previous chain hash."""
        if not layer or not layer.strip():
            raise ValueError("layer is required")
        if not artifact_type or not artifact_type.strip():
            raise ValueError("artifact_type is required")
        if not summary or not summary.strip():
            raise ValueError("summary is required (audit-readability)")
        content_hash = _hash(content)
        with self._lock:
            prev_hash = self._links[-1].chain_hash if self._links else GENESIS_HASH
            chain_hash = _compute_chain_hash(prev_hash, content_hash, layer.strip())
            link = EvidenceLink(
                link_id=f"ev_{uuid.uuid4().hex[:16]}",
                run_id=self.run_id,
                layer=layer.strip(),
                artifact_type=artifact_type.strip(),
                content_hash=content_hash,
                prev_hash=prev_hash,
                chain_hash=chain_hash,
                summary=summary.strip(),
                metadata=dict(metadata or {}),
                created_at=_now_iso(),
            )
            self._links.append(link)
            return link

    def verify(self) -> tuple[bool, tuple[str, ...]]:
        """Re-walk the chain and confirm every link's hash reconciles.

        Returns ``(ok, errors)``. An empty error tuple means the chain has not
        been tampered with since each ``append`` call.
        """
        errors: list[str] = []
        with self._lock:
            prev = GENESIS_HASH
            for idx, link in enumerate(self._links):
                if link.prev_hash != prev:
                    errors.append(
                        f"link {idx} ({link.link_id}) prev_hash mismatch "
                        f"(got {link.prev_hash[:8]}, expected {prev[:8]})"
                    )
                expected = _compute_chain_hash(link.prev_hash, link.content_hash, link.layer)
                if link.chain_hash != expected:
                    errors.append(
                        f"link {idx} ({link.link_id}) chain_hash mismatch "
                        f"(got {link.chain_hash[:8]}, expected {expected[:8]})"
                    )
                prev = link.chain_hash
        return not errors, tuple(errors)

    def links(self) -> tuple[EvidenceLink, ...]:
        with self._lock:
            return tuple(self._links)

    def links_for_layer(self, layer: str) -> tuple[EvidenceLink, ...]:
        with self._lock:
            return tuple(link for link in self._links if link.layer == layer)

    def to_dict(self) -> dict[str, Any]:
        with self._lock:
            return {
                "run_id": self.run_id,
                "tenant_id": self.tenant_id,
                "links": [link.to_dict() for link in self._links],
                "head_hash": self._links[-1].chain_hash if self._links else GENESIS_HASH,
            }


def new_chain(*, tenant_id: str, run_id: str | None = None) -> EvidenceChain:
    """Construct a fresh evidence chain for a single AI Stack run."""
    rid = (run_id or f"run_{uuid.uuid4().hex[:16]}").strip()
    return EvidenceChain(run_id=rid, tenant_id=tenant_id)


__all__ = [
    "GENESIS_HASH",
    "EvidenceChain",
    "EvidenceLink",
    "new_chain",
]
