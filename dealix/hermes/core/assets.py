"""Asset Builder — every reusable artifact lives here.

Assets are the compounding output of the system: each outcome should be
inspected for asset potential (template / playbook / case study / dataset /
offer). If none, that is itself recorded — explicit "no asset" is fine,
silent "we forgot to ask" is not.
"""

from __future__ import annotations

from collections.abc import Iterable

from dealix.hermes.core.schemas import Asset, AssetKind, Outcome


class AssetBuilder:
    def __init__(self) -> None:
        self._store: dict[str, Asset] = {}

    def register(
        self,
        *,
        kind: AssetKind,
        title: str,
        summary: str,
        body: str,
        created_by: str,
        derived_from: Iterable[Outcome] | None = None,
        tags: Iterable[str] | None = None,
        reusable: bool = True,
    ) -> Asset:
        asset = Asset(
            kind=kind,
            title=title,
            summary=summary,
            body=body,
            created_by=created_by,
            derived_from_outcome_ids=[o.outcome_id for o in (derived_from or [])],
            tags=list(tags or []),
            reusable=reusable,
        )
        self._store[asset.asset_id] = asset
        return asset

    def revise(self, asset_id: str, *, body: str, summary: str | None = None) -> Asset:
        a = self._store.get(asset_id)
        if a is None:
            raise KeyError(asset_id)
        a = a.model_copy(
            update={
                "body": body,
                "summary": summary or a.summary,
                "version": a.version + 1,
            }
        )
        self._store[asset_id] = a
        return a

    def get(self, asset_id: str) -> Asset | None:
        return self._store.get(asset_id)

    def by_kind(self, kind: AssetKind) -> list[Asset]:
        return [a for a in self._store.values() if a.kind is kind]

    def all(self) -> list[Asset]:
        return list(self._store.values())


__all__ = ["AssetBuilder"]
