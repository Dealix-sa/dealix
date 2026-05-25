"""
JSON-backed persistence for Revenue Marketing OS.

Mirrors the pattern used by ``dealix.marketing_factory.store`` and
``dealix.revenue_ops_autopilot.store``: a single JSON blob on disk
with atomic writes, validated by Pydantic ``TypeAdapter`` on read.

The blob lives at ``var/revenue_marketing_os.json`` by default; the
``DEALIX_REVENUE_MARKETING_STORE`` env var overrides the path so
tests can swap to a tmpdir.
"""

from __future__ import annotations

import json
import os
import threading
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pydantic import TypeAdapter

from dealix.revenue_marketing_os.schemas import (
    AttributionRecord,
    CampaignRecord,
    ExperimentRecord,
    ICPRecord,
    LeadRecord,
    MessageRecord,
    OfferRecord,
    RevenueRecord,
    ScaleKillDecision,
    TouchRecord,
)

_STORE_PATH_ENV = "DEALIX_REVENUE_MARKETING_STORE"

_ICP_TA = TypeAdapter(list[ICPRecord])
_OFFERS_TA = TypeAdapter(list[OfferRecord])
_MESSAGES_TA = TypeAdapter(list[MessageRecord])
_CAMPAIGNS_TA = TypeAdapter(list[CampaignRecord])
_LEADS_TA = TypeAdapter(list[LeadRecord])
_TOUCHES_TA = TypeAdapter(list[TouchRecord])
_REVENUE_TA = TypeAdapter(list[RevenueRecord])
_ATTRIBUTION_TA = TypeAdapter(list[AttributionRecord])
_EXPERIMENTS_TA = TypeAdapter(list[ExperimentRecord])
_DECISIONS_TA = TypeAdapter(list[ScaleKillDecision])


def default_revenue_marketing_store_path() -> Path:
    raw = os.environ.get(_STORE_PATH_ENV, "")
    if raw.strip():
        p = Path(raw)
    else:
        p = Path(__file__).resolve().parents[2] / "var" / "revenue_marketing_os.json"
    if not p.is_absolute():
        p = Path(__file__).resolve().parents[2] / p
    return p


def uid(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def _utcnow_iso() -> str:
    return datetime.now(UTC).isoformat()


class RevenueMarketingStore:
    """Thread-safe single-blob JSON store for the Money Loop."""

    def __init__(self, path: Path | None = None) -> None:
        self._path = path or default_revenue_marketing_store_path()
        self._lock = threading.Lock()

    @staticmethod
    def _empty_blob() -> dict[str, Any]:
        return {
            "version": 1,
            "generated_at": _utcnow_iso(),
            "icps": [],
            "offers": [],
            "messages": [],
            "campaigns": [],
            "leads": [],
            "touches": [],
            "revenue": [],
            "attribution": [],
            "experiments": [],
            "scale_kill_decisions": [],
        }

    # ── low-level IO ────────────────────────────────────────────────

    def _read_raw(self) -> dict[str, Any]:
        if not self._path.exists():
            return self._empty_blob()
        try:
            data = json.loads(self._path.read_text(encoding="utf-8"))
        except Exception:
            return self._empty_blob()
        if not isinstance(data, dict):
            return self._empty_blob()
        # backfill any missing sections so older snapshots stay readable
        for key, default in self._empty_blob().items():
            data.setdefault(key, default)
        return data

    def _write_atomic(self, data: dict[str, Any]) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        data["generated_at"] = _utcnow_iso()
        tmp = self._path.with_suffix(".tmp")
        tmp.write_text(
            json.dumps(data, ensure_ascii=False, indent=2, default=str),
            encoding="utf-8",
        )
        tmp.replace(self._path)

    def _mutate(self, fn: Any) -> Any:
        with self._lock:
            blob = self._read_raw()
            out = fn(blob)
            self._write_atomic(blob)
            return out

    # ── ICP ─────────────────────────────────────────────────────────

    def list_icps(self) -> list[ICPRecord]:
        return _ICP_TA.validate_python(self._read_raw().get("icps") or [])

    def upsert_icp(self, rec: ICPRecord) -> ICPRecord:
        def _fn(blob: dict[str, Any]) -> ICPRecord:
            rows = _ICP_TA.validate_python(blob.get("icps") or [])
            rest = [x for x in rows if x.id != rec.id]
            rest.append(rec)
            blob["icps"] = [r.model_dump(mode="json") for r in rest]
            return rec

        return self._mutate(_fn)

    # ── Offer ───────────────────────────────────────────────────────

    def list_offers(self) -> list[OfferRecord]:
        return _OFFERS_TA.validate_python(self._read_raw().get("offers") or [])

    def upsert_offer(self, rec: OfferRecord) -> OfferRecord:
        def _fn(blob: dict[str, Any]) -> OfferRecord:
            rows = _OFFERS_TA.validate_python(blob.get("offers") or [])
            rest = [x for x in rows if x.id != rec.id]
            rest.append(rec)
            blob["offers"] = [r.model_dump(mode="json") for r in rest]
            return rec

        return self._mutate(_fn)

    # ── Message ─────────────────────────────────────────────────────

    def list_messages(self) -> list[MessageRecord]:
        return _MESSAGES_TA.validate_python(self._read_raw().get("messages") or [])

    def upsert_message(self, rec: MessageRecord) -> MessageRecord:
        def _fn(blob: dict[str, Any]) -> MessageRecord:
            rows = _MESSAGES_TA.validate_python(blob.get("messages") or [])
            rest = [x for x in rows if x.id != rec.id]
            rest.append(rec)
            blob["messages"] = [r.model_dump(mode="json") for r in rest]
            return rec

        return self._mutate(_fn)

    # ── Campaign ────────────────────────────────────────────────────

    def list_campaigns(self) -> list[CampaignRecord]:
        return _CAMPAIGNS_TA.validate_python(self._read_raw().get("campaigns") or [])

    def get_campaign(self, campaign_id: str) -> CampaignRecord | None:
        for c in self.list_campaigns():
            if c.id == campaign_id:
                return c
        return None

    def upsert_campaign(self, rec: CampaignRecord) -> CampaignRecord:
        def _fn(blob: dict[str, Any]) -> CampaignRecord:
            rows = _CAMPAIGNS_TA.validate_python(blob.get("campaigns") or [])
            rest = [x for x in rows if x.id != rec.id]
            rec_updated = rec.model_copy(update={"updated_at": datetime.now(UTC)})
            rest.append(rec_updated)
            blob["campaigns"] = [r.model_dump(mode="json") for r in rest]
            return rec_updated

        return self._mutate(_fn)

    # ── Lead ────────────────────────────────────────────────────────

    def list_leads(
        self, *, campaign_id: str | None = None, limit: int = 500
    ) -> list[LeadRecord]:
        rows = _LEADS_TA.validate_python(self._read_raw().get("leads") or [])
        if campaign_id is not None:
            rows = [x for x in rows if x.campaign_id == campaign_id]
        rows.sort(key=lambda x: x.created_at, reverse=True)
        return rows[:limit]

    def get_lead(self, lead_id: str) -> LeadRecord | None:
        for x in self.list_leads(limit=10_000):
            if x.id == lead_id:
                return x
        return None

    def upsert_lead(self, rec: LeadRecord) -> LeadRecord:
        def _fn(blob: dict[str, Any]) -> LeadRecord:
            rows = _LEADS_TA.validate_python(blob.get("leads") or [])
            rest = [x for x in rows if x.id != rec.id]
            updated = rec.model_copy(update={"updated_at": datetime.now(UTC)})
            rest.append(updated)
            blob["leads"] = [r.model_dump(mode="json") for r in rest]
            return updated

        return self._mutate(_fn)

    # ── Touch ───────────────────────────────────────────────────────

    def list_touches(
        self, *, lead_id: str | None = None, campaign_id: str | None = None
    ) -> list[TouchRecord]:
        rows = _TOUCHES_TA.validate_python(self._read_raw().get("touches") or [])
        if lead_id is not None:
            rows = [x for x in rows if x.lead_id == lead_id]
        if campaign_id is not None:
            rows = [x for x in rows if x.campaign_id == campaign_id]
        rows.sort(key=lambda x: x.occurred_at, reverse=True)
        return rows

    def append_touch(self, rec: TouchRecord) -> TouchRecord:
        def _fn(blob: dict[str, Any]) -> TouchRecord:
            rows = _TOUCHES_TA.validate_python(blob.get("touches") or [])
            rows.append(rec)
            blob["touches"] = [r.model_dump(mode="json") for r in rows]
            return rec

        return self._mutate(_fn)

    # ── Revenue ─────────────────────────────────────────────────────

    def list_revenue(self) -> list[RevenueRecord]:
        return _REVENUE_TA.validate_python(self._read_raw().get("revenue") or [])

    def get_revenue(self, revenue_id: str) -> RevenueRecord | None:
        for r in self.list_revenue():
            if r.id == revenue_id:
                return r
        return None

    def upsert_revenue(self, rec: RevenueRecord) -> RevenueRecord:
        def _fn(blob: dict[str, Any]) -> RevenueRecord:
            rows = _REVENUE_TA.validate_python(blob.get("revenue") or [])
            rest = [x for x in rows if x.id != rec.id]
            rest.append(rec)
            blob["revenue"] = [r.model_dump(mode="json") for r in rest]
            return rec

        return self._mutate(_fn)

    # ── Attribution ─────────────────────────────────────────────────

    def list_attribution(
        self, *, revenue_id: str | None = None, campaign_id: str | None = None
    ) -> list[AttributionRecord]:
        rows = _ATTRIBUTION_TA.validate_python(
            self._read_raw().get("attribution") or []
        )
        if revenue_id is not None:
            rows = [x for x in rows if x.revenue_id == revenue_id]
        if campaign_id is not None:
            rows = [x for x in rows if x.campaign_id == campaign_id]
        return rows

    def append_attribution(self, rec: AttributionRecord) -> AttributionRecord:
        def _fn(blob: dict[str, Any]) -> AttributionRecord:
            rows = _ATTRIBUTION_TA.validate_python(blob.get("attribution") or [])
            rows.append(rec)
            blob["attribution"] = [r.model_dump(mode="json") for r in rows]
            return rec

        return self._mutate(_fn)

    # ── Experiments ─────────────────────────────────────────────────

    def list_experiments(self) -> list[ExperimentRecord]:
        return _EXPERIMENTS_TA.validate_python(
            self._read_raw().get("experiments") or []
        )

    def upsert_experiment(self, rec: ExperimentRecord) -> ExperimentRecord:
        def _fn(blob: dict[str, Any]) -> ExperimentRecord:
            rows = _EXPERIMENTS_TA.validate_python(blob.get("experiments") or [])
            rest = [x for x in rows if x.id != rec.id]
            rest.append(rec)
            blob["experiments"] = [r.model_dump(mode="json") for r in rest]
            return rec

        return self._mutate(_fn)

    # ── Scale/Kill decisions ────────────────────────────────────────

    def list_decisions(self) -> list[ScaleKillDecision]:
        return _DECISIONS_TA.validate_python(
            self._read_raw().get("scale_kill_decisions") or []
        )

    def append_decision(self, rec: ScaleKillDecision) -> ScaleKillDecision:
        def _fn(blob: dict[str, Any]) -> ScaleKillDecision:
            rows = _DECISIONS_TA.validate_python(
                blob.get("scale_kill_decisions") or []
            )
            rows.append(rec)
            blob["scale_kill_decisions"] = [r.model_dump(mode="json") for r in rows]
            return rec

        return self._mutate(_fn)

    # ── Snapshot ────────────────────────────────────────────────────

    def snapshot(self) -> dict[str, Any]:
        """Read everything for the dashboard endpoint."""
        return self._read_raw()


# ── Singleton ──────────────────────────────────────────────────────

_default_singleton: RevenueMarketingStore | None = None
_singleton_lock = threading.Lock()


def get_revenue_marketing_store() -> RevenueMarketingStore:
    global _default_singleton
    if _default_singleton is None:
        with _singleton_lock:
            if _default_singleton is None:
                _default_singleton = RevenueMarketingStore()
    return _default_singleton


def reset_revenue_marketing_store_for_tests(
    path: Path | None = None,
) -> RevenueMarketingStore:
    global _default_singleton
    st = RevenueMarketingStore(path=path)
    _default_singleton = st
    return st
