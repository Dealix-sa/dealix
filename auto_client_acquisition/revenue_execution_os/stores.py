"""JSONL persistence for Revenue Execution OS entities.

One small append-only store per entity, mirroring the ``value_ledger`` pattern:
a ``DEALIX_REVX_*_PATH`` env override with a default under
``data/revenue_execution/``. These are runtime files (gitignored); seed data
lives in ``data/distribution/``.
"""

from __future__ import annotations

import json
import os
from collections.abc import Iterable
from pathlib import Path
from typing import Any, Generic, Protocol, TypeVar

from auto_client_acquisition.revenue_execution_os.models import (
    Draft,
    Followup,
    PaymentHandoff,
    ProofPackRef,
    Proposal,
    Prospect,
    Renewal,
    WinLoss,
)


class _Model(Protocol):
    def to_dict(self) -> dict[str, Any]:
        """Serialize the model to a plain dict."""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Any:
        """Build a model instance from a plain dict."""


T = TypeVar("T", bound=_Model)


class JsonlStore(Generic[T]):
    """Append-only JSONL store with id-keyed read / filter / update."""

    def __init__(self, *, env_var: str, default_path: str, model: type[T], id_field: str) -> None:
        self._env_var = env_var
        self._default_path = default_path
        self._model = model
        self._id_field = id_field

    def path(self) -> Path:
        raw = os.getenv(self._env_var, self._default_path)
        p = Path(raw)
        p.parent.mkdir(parents=True, exist_ok=True)
        return p

    # -- writes ----------------------------------------------------------
    def add(self, obj: T) -> T:
        with self.path().open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(obj.to_dict(), ensure_ascii=False))
            fh.write("\n")
        return obj

    def add_many(self, objs: Iterable[T]) -> list[T]:
        out: list[T] = []
        with self.path().open("a", encoding="utf-8") as fh:
            for obj in objs:
                fh.write(json.dumps(obj.to_dict(), ensure_ascii=False))
                fh.write("\n")
                out.append(obj)
        return out

    # -- reads -----------------------------------------------------------
    def _read_rows(self) -> list[dict[str, Any]]:
        p = self.path()
        if not p.exists():
            return []
        rows: list[dict[str, Any]] = []
        with p.open(encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(json.loads(line))
                except Exception:  # noqa: S112 - skip malformed JSONL lines (best-effort store)
                    continue
        return rows

    def list(self, *, limit: int = 1000, newest_first: bool = True, **filters: Any) -> list[T]:
        rows = self._read_rows()
        if filters:
            rows = [r for r in rows if all(r.get(k) == v for k, v in filters.items())]
        rows.sort(key=lambda r: str(r.get("created_at", "")), reverse=newest_first)
        return [self._model.from_dict(r) for r in rows[: max(0, limit)]]

    def get(self, id_value: str) -> T | None:
        for row in self._read_rows():
            if str(row.get(self._id_field, "")) == str(id_value):
                return self._model.from_dict(row)
        return None

    def count(self, **filters: Any) -> int:
        return len(self.list(limit=10_000_000, **filters))

    # -- update (rewrite-in-place by id) ---------------------------------
    def update(self, id_value: str, **changes: Any) -> T | None:
        rows = self._read_rows()
        updated: T | None = None
        for i, row in enumerate(rows):
            if str(row.get(self._id_field, "")) == str(id_value):
                merged = {**row, **changes}
                rows[i] = merged
                updated = self._model.from_dict(merged)
                break
        if updated is None:
            return None
        with self.path().open("w", encoding="utf-8") as fh:
            for row in rows:
                fh.write(json.dumps(row, ensure_ascii=False))
                fh.write("\n")
        return updated

    def clear_for_test(self) -> None:
        p = self.path()
        if p.exists():
            p.unlink()


# One store per entity. Defaults live under data/revenue_execution/ (gitignored).
PROSPECTS: JsonlStore[Prospect] = JsonlStore(
    env_var="DEALIX_REVX_PROSPECTS_PATH",
    default_path="data/revenue_execution/prospects.jsonl",
    model=Prospect,
    id_field="prospect_id",
)
DRAFTS: JsonlStore[Draft] = JsonlStore(
    env_var="DEALIX_REVX_DRAFTS_PATH",
    default_path="data/revenue_execution/drafts.jsonl",
    model=Draft,
    id_field="draft_id",
)
FOLLOWUPS: JsonlStore[Followup] = JsonlStore(
    env_var="DEALIX_REVX_FOLLOWUPS_PATH",
    default_path="data/revenue_execution/followups.jsonl",
    model=Followup,
    id_field="followup_id",
)
PROPOSALS: JsonlStore[Proposal] = JsonlStore(
    env_var="DEALIX_REVX_PROPOSALS_PATH",
    default_path="data/revenue_execution/proposals.jsonl",
    model=Proposal,
    id_field="proposal_id",
)
PROOF_PACKS: JsonlStore[ProofPackRef] = JsonlStore(
    env_var="DEALIX_REVX_PROOF_PACKS_PATH",
    default_path="data/revenue_execution/proof_packs.jsonl",
    model=ProofPackRef,
    id_field="proof_pack_id",
)
PAYMENT_HANDOFFS: JsonlStore[PaymentHandoff] = JsonlStore(
    env_var="DEALIX_REVX_PAYMENT_HANDOFFS_PATH",
    default_path="data/revenue_execution/payment_handoffs.jsonl",
    model=PaymentHandoff,
    id_field="handoff_id",
)
RENEWALS: JsonlStore[Renewal] = JsonlStore(
    env_var="DEALIX_REVX_RENEWALS_PATH",
    default_path="data/revenue_execution/renewals.jsonl",
    model=Renewal,
    id_field="renewal_id",
)
WIN_LOSS: JsonlStore[WinLoss] = JsonlStore(
    env_var="DEALIX_REVX_WIN_LOSS_PATH",
    default_path="data/revenue_execution/win_loss.jsonl",
    model=WinLoss,
    id_field="record_id",
)

ALL_STORES: tuple[JsonlStore, ...] = (
    PROSPECTS,
    DRAFTS,
    FOLLOWUPS,
    PROPOSALS,
    PROOF_PACKS,
    PAYMENT_HANDOFFS,
    RENEWALS,
    WIN_LOSS,
)


def clear_all_for_test() -> None:
    """Delete every store file — test helper only."""
    for store in ALL_STORES:
        store.clear_for_test()


__all__ = [
    "ALL_STORES",
    "DRAFTS",
    "FOLLOWUPS",
    "PAYMENT_HANDOFFS",
    "PROOF_PACKS",
    "PROPOSALS",
    "PROSPECTS",
    "RENEWALS",
    "WIN_LOSS",
    "JsonlStore",
    "clear_all_for_test",
]
