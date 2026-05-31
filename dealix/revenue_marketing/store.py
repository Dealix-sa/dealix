"""JSON-backed store for the Revenue Marketing Engine.

Mirrors the SQL contract; JSON is the local-dev / test fallback so the
engine works without Postgres. Production paths can switch to the SQL
tables defined in migrations/versions/20260525_014_revenue_marketing.py.
"""

from __future__ import annotations

import json
import os
import threading
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable

import yaml
from pydantic import TypeAdapter

from dealix.revenue_marketing.schemas import (
    CampaignRecord,
    ContentCardRecord,
    FunnelSnapshotRecord,
    MarketingExperimentRecord,
    MarketingTouchRecord,
    MarketSignalRecord,
    OfferRecord,
    RevenueAttributionRecord,
)

_DEFAULT_PATH_ENV = "DEALIX_REVENUE_MARKETING_STORE"
_SEED_FILENAME = "seed.yaml"

_SIGNALS_TA = TypeAdapter(list[MarketSignalRecord])
_OFFERS_TA = TypeAdapter(list[OfferRecord])
_CAMPAIGNS_TA = TypeAdapter(list[CampaignRecord])
_TOUCHES_TA = TypeAdapter(list[MarketingTouchRecord])
_ATTRIB_TA = TypeAdapter(list[RevenueAttributionRecord])
_EXP_TA = TypeAdapter(list[MarketingExperimentRecord])
_CONTENT_TA = TypeAdapter(list[ContentCardRecord])
_SNAPSHOT_TA = TypeAdapter(list[FunnelSnapshotRecord])


def default_store_path() -> Path:
    raw = os.environ.get(_DEFAULT_PATH_ENV, "")
    if raw.strip():
        p = Path(raw)
    else:
        p = Path(__file__).resolve().parents[2] / "var" / "revenue_marketing.json"
    if not p.is_absolute():
        p = Path(__file__).resolve().parents[2] / p
    return p


def _seed_path() -> Path:
    return Path(__file__).resolve().parent / _SEED_FILENAME


def uid(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


class RevenueMarketingStore:
    def __init__(self, path: Path | None = None) -> None:
        self._path = path or default_store_path()
        self._lock = threading.Lock()

    def _empty(self) -> dict[str, Any]:
        return {
            "version": 1,
            "signals": [],
            "offers": [],
            "campaigns": [],
            "touches": [],
            "attributions": [],
            "experiments": [],
            "content_cards": [],
            "funnel_snapshots": [],
        }

    def _read_raw(self) -> dict[str, Any]:
        if not self._path.exists():
            return self._empty()
        try:
            return json.loads(self._path.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            return self._empty()

    def _write_atomic(self, data: dict[str, Any]) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self._path.with_suffix(".tmp")
        data["generated_at"] = datetime.now(UTC).isoformat()
        tmp.write_text(
            json.dumps(data, ensure_ascii=False, indent=2, default=str),
            encoding="utf-8",
        )
        tmp.replace(self._path)

    def _mutate(self, fn: Callable[[dict[str, Any]], Any]) -> Any:
        with self._lock:
            blob = self._read_raw()
            out = fn(blob)
            self._write_atomic(blob)
            return out

    def ensure_seed_loaded(self) -> dict[str, int]:
        """Load YAML seed once if store is empty. Returns counts loaded per section."""

        def _fn(blob: dict[str, Any]) -> dict[str, int]:
            counts = {"offers": 0, "signals": 0, "content_cards": 0}
            existing_offers = _OFFERS_TA.validate_python(blob.get("offers") or [])
            if existing_offers:
                return counts

            seed_file = _seed_path()
            if not seed_file.exists():
                return counts

            seed = yaml.safe_load(seed_file.read_text(encoding="utf-8")) or {}

            offers: list[OfferRecord] = []
            for row in seed.get("offers") or []:
                offers.append(OfferRecord(**row))
            blob["offers"] = [o.model_dump(mode="json") for o in offers]
            counts["offers"] = len(offers)

            signals: list[MarketSignalRecord] = []
            for row in seed.get("signals") or []:
                rid = row.pop("id", uid("sig"))
                signals.append(MarketSignalRecord(id=rid, **row))
            blob["signals"] = [s.model_dump(mode="json") for s in signals]
            counts["signals"] = len(signals)

            cards: list[ContentCardRecord] = []
            for row in seed.get("content_cards") or []:
                rid = row.pop("id", uid("cnt"))
                cards.append(ContentCardRecord(id=rid, **row))
            blob["content_cards"] = [c.model_dump(mode="json") for c in cards]
            counts["content_cards"] = len(cards)

            return counts

        return self._mutate(_fn)

    # ── Signals ──────────────────────────────────────────────────
    def list_signals(self) -> list[MarketSignalRecord]:
        return _SIGNALS_TA.validate_python(self._read_raw().get("signals") or [])

    def append_signal(self, sig: MarketSignalRecord) -> MarketSignalRecord:
        def _fn(blob: dict[str, Any]) -> MarketSignalRecord:
            rows = _SIGNALS_TA.validate_python(blob.get("signals") or [])
            rows.append(sig)
            blob["signals"] = [r.model_dump(mode="json") for r in rows]
            return sig

        return self._mutate(_fn)

    # ── Offers ───────────────────────────────────────────────────
    def list_offers(self) -> list[OfferRecord]:
        return _OFFERS_TA.validate_python(self._read_raw().get("offers") or [])

    def get_offer(self, offer_id: str) -> OfferRecord | None:
        for o in self.list_offers():
            if o.id == offer_id:
                return o
        return None

    def upsert_offer(self, offer: OfferRecord) -> OfferRecord:
        def _fn(blob: dict[str, Any]) -> OfferRecord:
            rows = _OFFERS_TA.validate_python(blob.get("offers") or [])
            rest = [r for r in rows if r.id != offer.id]
            rest.append(offer)
            blob["offers"] = [r.model_dump(mode="json") for r in rest]
            return offer

        return self._mutate(_fn)

    # ── Campaigns ────────────────────────────────────────────────
    def list_campaigns(self) -> list[CampaignRecord]:
        return _CAMPAIGNS_TA.validate_python(self._read_raw().get("campaigns") or [])

    def upsert_campaign(self, c: CampaignRecord) -> CampaignRecord:
        def _fn(blob: dict[str, Any]) -> CampaignRecord:
            rows = _CAMPAIGNS_TA.validate_python(blob.get("campaigns") or [])
            rest = [r for r in rows if r.id != c.id]
            c.updated_at = datetime.now(UTC)
            rest.append(c)
            blob["campaigns"] = [r.model_dump(mode="json") for r in rest]
            return c

        return self._mutate(_fn)

    # ── Touches ──────────────────────────────────────────────────
    def list_touches(self, *, lead_id: str | None = None) -> list[MarketingTouchRecord]:
        rows = _TOUCHES_TA.validate_python(self._read_raw().get("touches") or [])
        if lead_id:
            rows = [t for t in rows if t.lead_id == lead_id]
        rows.sort(key=lambda t: t.occurred_at)
        return rows

    def append_touch(self, t: MarketingTouchRecord) -> MarketingTouchRecord:
        def _fn(blob: dict[str, Any]) -> MarketingTouchRecord:
            rows = _TOUCHES_TA.validate_python(blob.get("touches") or [])
            rows.append(t)
            blob["touches"] = [r.model_dump(mode="json") for r in rows]
            return t

        return self._mutate(_fn)

    # ── Attribution ──────────────────────────────────────────────
    def list_attributions(self) -> list[RevenueAttributionRecord]:
        return _ATTRIB_TA.validate_python(self._read_raw().get("attributions") or [])

    def append_attribution(self, a: RevenueAttributionRecord) -> RevenueAttributionRecord:
        def _fn(blob: dict[str, Any]) -> RevenueAttributionRecord:
            rows = _ATTRIB_TA.validate_python(blob.get("attributions") or [])
            rows.append(a)
            blob["attributions"] = [r.model_dump(mode="json") for r in rows]
            return a

        return self._mutate(_fn)

    # ── Experiments ──────────────────────────────────────────────
    def list_experiments(self) -> list[MarketingExperimentRecord]:
        return _EXP_TA.validate_python(self._read_raw().get("experiments") or [])

    def upsert_experiment(self, e: MarketingExperimentRecord) -> MarketingExperimentRecord:
        def _fn(blob: dict[str, Any]) -> MarketingExperimentRecord:
            rows = _EXP_TA.validate_python(blob.get("experiments") or [])
            rest = [r for r in rows if r.id != e.id]
            e.updated_at = datetime.now(UTC)
            rest.append(e)
            blob["experiments"] = [r.model_dump(mode="json") for r in rest]
            return e

        return self._mutate(_fn)

    # ── Content cards ────────────────────────────────────────────
    def list_content_cards(self) -> list[ContentCardRecord]:
        return _CONTENT_TA.validate_python(self._read_raw().get("content_cards") or [])

    def upsert_content_card(self, c: ContentCardRecord) -> ContentCardRecord:
        def _fn(blob: dict[str, Any]) -> ContentCardRecord:
            rows = _CONTENT_TA.validate_python(blob.get("content_cards") or [])
            rest = [r for r in rows if r.id != c.id]
            rest.append(c)
            blob["content_cards"] = [r.model_dump(mode="json") for r in rest]
            return c

        return self._mutate(_fn)

    # ── Funnel snapshots ─────────────────────────────────────────
    def list_funnel_snapshots(self, limit: int = 60) -> list[FunnelSnapshotRecord]:
        rows = _SNAPSHOT_TA.validate_python(self._read_raw().get("funnel_snapshots") or [])
        rows.sort(key=lambda s: s.captured_at, reverse=True)
        return rows[:limit]

    def append_funnel_snapshot(self, s: FunnelSnapshotRecord) -> FunnelSnapshotRecord:
        def _fn(blob: dict[str, Any]) -> FunnelSnapshotRecord:
            rows = _SNAPSHOT_TA.validate_python(blob.get("funnel_snapshots") or [])
            rows.append(s)
            blob["funnel_snapshots"] = [r.model_dump(mode="json") for r in rows]
            return s

        return self._mutate(_fn)

    def stats(self) -> dict[str, int]:
        blob = self._read_raw()
        return {
            "signals": len(blob.get("signals") or []),
            "offers": len(blob.get("offers") or []),
            "campaigns": len(blob.get("campaigns") or []),
            "touches": len(blob.get("touches") or []),
            "attributions": len(blob.get("attributions") or []),
            "experiments": len(blob.get("experiments") or []),
            "content_cards": len(blob.get("content_cards") or []),
            "funnel_snapshots": len(blob.get("funnel_snapshots") or []),
        }


_singleton: RevenueMarketingStore | None = None
_singleton_lock = threading.Lock()


def get_revenue_marketing_store() -> RevenueMarketingStore:
    global _singleton
    if _singleton is None:
        with _singleton_lock:
            if _singleton is None:
                st = RevenueMarketingStore()
                st.ensure_seed_loaded()
                _singleton = st
    return _singleton


def reset_revenue_marketing_store_for_tests(path: Path | None = None) -> RevenueMarketingStore:
    global _singleton
    st = RevenueMarketingStore(path=path)
    st.ensure_seed_loaded()
    _singleton = st
    return st
