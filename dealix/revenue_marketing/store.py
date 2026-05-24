"""JSON persistence for the Dealix Revenue Marketing Engine.

Follows the JSON store pattern used by ``dealix/marketing_factory/store.py``:
atomic write, threading lock, optional YAML seed load, singleton accessor,
test reset helper. Default location ``var/revenue_marketing.json``, override
via the ``DEALIX_REVENUE_MARKETING_STORE`` env var.
"""

from __future__ import annotations

import json
import os
import threading
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml
from pydantic import TypeAdapter

from dealix.revenue_marketing.schemas import (
    Audience,
    CaseStudyDraft,
    Lead,
    MarketingCampaign,
    MarketingExperiment,
    MarketingTouch,
    MarketSignal,
    MessageVariant,
    Offer,
    RevenueAttribution,
)

_DEFAULT_PATH_ENV = "DEALIX_REVENUE_MARKETING_STORE"

_SIGNALS_TA = TypeAdapter(list[MarketSignal])
_AUDIENCES_TA = TypeAdapter(list[Audience])
_OFFERS_TA = TypeAdapter(list[Offer])
_MESSAGES_TA = TypeAdapter(list[MessageVariant])
_CAMPAIGNS_TA = TypeAdapter(list[MarketingCampaign])
_TOUCHES_TA = TypeAdapter(list[MarketingTouch])
_ATTR_TA = TypeAdapter(list[RevenueAttribution])
_EXP_TA = TypeAdapter(list[MarketingExperiment])
_CASE_TA = TypeAdapter(list[CaseStudyDraft])
_LEADS_TA = TypeAdapter(list[Lead])


def default_store_path() -> Path:
    raw = os.environ.get(_DEFAULT_PATH_ENV, "")
    if raw.strip():
        p = Path(raw)
    else:
        p = Path(__file__).resolve().parents[2] / "var" / "revenue_marketing.json"
    if not p.is_absolute():
        p = Path(__file__).resolve().parents[2] / p
    return p


def _seeds_dir() -> Path:
    return Path(__file__).resolve().parent / "seeds"


def uid(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


_EMPTY_KEYS = (
    "signals",
    "audiences",
    "offers",
    "messages",
    "campaigns",
    "touches",
    "attributions",
    "experiments",
    "case_studies",
    "leads",
)


class RevenueMarketingStore:
    """JSON-backed store for the Revenue Marketing Engine."""

    def __init__(self, path: Path | None = None) -> None:
        self._path = path or default_store_path()
        self._lock = threading.Lock()

    # ────────────────────────── internal io ─────────────────────────
    def _empty_blob(self) -> dict[str, Any]:
        blob: dict[str, Any] = {"version": 1}
        for k in _EMPTY_KEYS:
            blob[k] = []
        return blob

    def _read_raw(self) -> dict[str, Any]:
        if not self._path.exists():
            return self._empty_blob()
        try:
            data = json.loads(self._path.read_text(encoding="utf-8"))
        except Exception:
            return self._empty_blob()
        for k in _EMPTY_KEYS:
            data.setdefault(k, [])
        return data

    def _write_atomic(self, data: dict[str, Any]) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self._path.with_suffix(".tmp")
        data["generated_at"] = datetime.now(UTC).isoformat()
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

    # ────────────────────────── seed loader ─────────────────────────
    def ensure_seed_loaded(self) -> dict[str, int]:
        """Load YAML seeds for offers + messages once if store is empty."""

        def _fn(blob: dict[str, Any]) -> dict[str, int]:
            added = {"offers": 0, "messages": 0}
            offers = _OFFERS_TA.validate_python(blob.get("offers") or [])
            if not offers:
                seed_file = _seeds_dir() / "offers.seed.yaml"
                if seed_file.exists():
                    raw = yaml.safe_load(seed_file.read_text(encoding="utf-8")) or {}
                    for row in raw.get("offers") or []:
                        offer = Offer(
                            id=str(row.get("id") or uid("off")),
                            name_ar=str(row.get("name_ar") or ""),
                            name_en=str(row.get("name_en") or ""),
                            rung=row.get("rung") or "entry",
                            price_min_sar=float(row.get("price_min_sar") or 0.0),
                            price_max_sar=float(row.get("price_max_sar") or 0.0),
                            target_segment=str(row.get("target_segment") or ""),
                            pain_addressed=str(row.get("pain_addressed") or ""),
                            deliverables_ar=list(row.get("deliverables_ar") or []),
                            deliverables_en=list(row.get("deliverables_en") or []),
                            success_metric=str(row.get("success_metric") or ""),
                            scale_kill_rule=str(row.get("scale_kill_rule") or ""),
                        )
                        offers.append(offer)
                        added["offers"] += 1
                    blob["offers"] = [x.model_dump(mode="json") for x in offers]

            messages = _MESSAGES_TA.validate_python(blob.get("messages") or [])
            if not messages:
                seed_file = _seeds_dir() / "messages.seed.yaml"
                if seed_file.exists():
                    raw = yaml.safe_load(seed_file.read_text(encoding="utf-8")) or {}
                    for row in raw.get("messages") or []:
                        msg = MessageVariant(
                            id=str(row.get("id") or uid("msg")),
                            offer_id=str(row.get("offer_id") or ""),
                            angle=str(row.get("angle") or ""),
                            headline_ar=str(row.get("headline_ar") or ""),
                            headline_en=str(row.get("headline_en") or ""),
                            body_ar=str(row.get("body_ar") or ""),
                            body_en=str(row.get("body_en") or ""),
                            cta_ar=str(row.get("cta_ar") or ""),
                            cta_en=str(row.get("cta_en") or ""),
                            status=row.get("status") or "draft",
                        )
                        messages.append(msg)
                        added["messages"] += 1
                    blob["messages"] = [x.model_dump(mode="json") for x in messages]
            return added

        return self._mutate(_fn)

    # ────────────────────────── signals ─────────────────────────────
    def list_signals(self, *, limit: int = 200) -> list[MarketSignal]:
        blob = self._read_raw()
        rows = _SIGNALS_TA.validate_python(blob.get("signals") or [])
        rows.sort(key=lambda x: x.observed_at, reverse=True)
        return rows[:limit]

    def upsert_signal(self, signal: MarketSignal) -> MarketSignal:
        def _fn(blob: dict[str, Any]) -> MarketSignal:
            rows = _SIGNALS_TA.validate_python(blob.get("signals") or [])
            rest = [x for x in rows if x.id != signal.id]
            rest.append(signal)
            blob["signals"] = [x.model_dump(mode="json") for x in rest]
            return signal

        return self._mutate(_fn)

    # ────────────────────────── audiences ───────────────────────────
    def list_audiences(self, *, limit: int = 200) -> list[Audience]:
        blob = self._read_raw()
        return _AUDIENCES_TA.validate_python(blob.get("audiences") or [])[:limit]

    def upsert_audience(self, audience: Audience) -> Audience:
        def _fn(blob: dict[str, Any]) -> Audience:
            rows = _AUDIENCES_TA.validate_python(blob.get("audiences") or [])
            rest = [x for x in rows if x.id != audience.id]
            rest.append(audience)
            blob["audiences"] = [x.model_dump(mode="json") for x in rest]
            return audience

        return self._mutate(_fn)

    # ────────────────────────── offers ──────────────────────────────
    def list_offers(self, *, limit: int = 200) -> list[Offer]:
        blob = self._read_raw()
        return _OFFERS_TA.validate_python(blob.get("offers") or [])[:limit]

    def upsert_offer(self, offer: Offer) -> Offer:
        def _fn(blob: dict[str, Any]) -> Offer:
            rows = _OFFERS_TA.validate_python(blob.get("offers") or [])
            rest = [x for x in rows if x.id != offer.id]
            rest.append(offer)
            blob["offers"] = [x.model_dump(mode="json") for x in rest]
            return offer

        return self._mutate(_fn)

    # ────────────────────────── messages ────────────────────────────
    def list_messages(self, *, limit: int = 400) -> list[MessageVariant]:
        blob = self._read_raw()
        return _MESSAGES_TA.validate_python(blob.get("messages") or [])[:limit]

    def upsert_message(self, message: MessageVariant) -> MessageVariant:
        def _fn(blob: dict[str, Any]) -> MessageVariant:
            rows = _MESSAGES_TA.validate_python(blob.get("messages") or [])
            rest = [x for x in rows if x.id != message.id]
            rest.append(message)
            blob["messages"] = [x.model_dump(mode="json") for x in rest]
            return message

        return self._mutate(_fn)

    # ────────────────────────── campaigns ───────────────────────────
    def list_campaigns(self, *, limit: int = 200) -> list[MarketingCampaign]:
        blob = self._read_raw()
        rows = _CAMPAIGNS_TA.validate_python(blob.get("campaigns") or [])
        rows.sort(key=lambda x: x.created_at, reverse=True)
        return rows[:limit]

    def upsert_campaign(self, campaign: MarketingCampaign) -> MarketingCampaign:
        def _fn(blob: dict[str, Any]) -> MarketingCampaign:
            rows = _CAMPAIGNS_TA.validate_python(blob.get("campaigns") or [])
            rest = [x for x in rows if x.id != campaign.id]
            rest.append(campaign)
            blob["campaigns"] = [x.model_dump(mode="json") for x in rest]
            return campaign

        return self._mutate(_fn)

    # ────────────────────────── touches ─────────────────────────────
    def list_touches(self, *, limit: int = 1000) -> list[MarketingTouch]:
        blob = self._read_raw()
        rows = _TOUCHES_TA.validate_python(blob.get("touches") or [])
        rows.sort(key=lambda x: x.occurred_at)
        return rows[:limit]

    def append_touch(self, touch: MarketingTouch) -> MarketingTouch:
        def _fn(blob: dict[str, Any]) -> MarketingTouch:
            rows = _TOUCHES_TA.validate_python(blob.get("touches") or [])
            rows.append(touch)
            blob["touches"] = [x.model_dump(mode="json") for x in rows]
            return touch

        return self._mutate(_fn)

    # ────────────────────────── attribution ─────────────────────────
    def list_attributions(self, *, limit: int = 1000) -> list[RevenueAttribution]:
        blob = self._read_raw()
        rows = _ATTR_TA.validate_python(blob.get("attributions") or [])
        rows.sort(key=lambda x: x.created_at, reverse=True)
        return rows[:limit]

    def append_attribution(self, attribution: RevenueAttribution) -> RevenueAttribution:
        def _fn(blob: dict[str, Any]) -> RevenueAttribution:
            rows = _ATTR_TA.validate_python(blob.get("attributions") or [])
            rows.append(attribution)
            # exclude the computed `is_real_revenue` so the persisted JSON
            # round-trips cleanly through TypeAdapter (extra='forbid').
            blob["attributions"] = [
                x.model_dump(mode="json", exclude={"is_real_revenue"}) for x in rows
            ]
            return attribution

        return self._mutate(_fn)

    # ────────────────────────── experiments ─────────────────────────
    def list_experiments(self, *, limit: int = 200) -> list[MarketingExperiment]:
        blob = self._read_raw()
        rows = _EXP_TA.validate_python(blob.get("experiments") or [])
        rows.sort(key=lambda x: x.created_at, reverse=True)
        return rows[:limit]

    def upsert_experiment(self, experiment: MarketingExperiment) -> MarketingExperiment:
        def _fn(blob: dict[str, Any]) -> MarketingExperiment:
            rows = _EXP_TA.validate_python(blob.get("experiments") or [])
            rest = [x for x in rows if x.id != experiment.id]
            rest.append(experiment)
            blob["experiments"] = [x.model_dump(mode="json") for x in rest]
            return experiment

        return self._mutate(_fn)

    # ────────────────────────── case studies ────────────────────────
    def list_case_studies(self, *, limit: int = 200) -> list[CaseStudyDraft]:
        blob = self._read_raw()
        rows = _CASE_TA.validate_python(blob.get("case_studies") or [])
        rows.sort(key=lambda x: x.created_at, reverse=True)
        return rows[:limit]

    def upsert_case_study(self, case_study: CaseStudyDraft) -> CaseStudyDraft:
        def _fn(blob: dict[str, Any]) -> CaseStudyDraft:
            rows = _CASE_TA.validate_python(blob.get("case_studies") or [])
            rest = [x for x in rows if x.id != case_study.id]
            rest.append(case_study)
            blob["case_studies"] = [x.model_dump(mode="json") for x in rest]
            return case_study

        return self._mutate(_fn)

    # ────────────────────────── leads ───────────────────────────────
    def list_leads(self, *, limit: int = 500) -> list[Lead]:
        blob = self._read_raw()
        rows = _LEADS_TA.validate_python(blob.get("leads") or [])
        rows.sort(key=lambda x: x.created_at, reverse=True)
        return rows[:limit]

    def upsert_lead(self, lead: Lead) -> Lead:
        def _fn(blob: dict[str, Any]) -> Lead:
            rows = _LEADS_TA.validate_python(blob.get("leads") or [])
            rest = [x for x in rows if x.id != lead.id]
            rest.append(lead)
            # exclude the computed `overall_score` so the persisted JSON
            # round-trips through TypeAdapter (extra='forbid').
            blob["leads"] = [x.model_dump(mode="json", exclude={"overall_score"}) for x in rest]
            return lead

        return self._mutate(_fn)

    # ────────────────────────── stats ───────────────────────────────
    def stats(self) -> dict[str, Any]:
        signals = self.list_signals(limit=10_000)
        audiences = self.list_audiences(limit=10_000)
        offers = self.list_offers(limit=10_000)
        messages = self.list_messages(limit=10_000)
        campaigns = self.list_campaigns(limit=10_000)
        touches = self.list_touches(limit=100_000)
        attributions = self.list_attributions(limit=100_000)
        experiments = self.list_experiments(limit=10_000)
        case_studies = self.list_case_studies(limit=10_000)
        leads = self.list_leads(limit=100_000)

        active_campaigns = sum(1 for c in campaigns if c.status == "active")
        running_experiments = sum(1 for x in experiments if x.status == "running")
        unattributed_revenue_count = sum(
            1 for a in attributions if not a.campaign_id and not a.offer_id
        )

        vanity_only = 0
        for camp in campaigns:
            if camp.status != "active":
                continue
            has_revenue = any(a.campaign_id == camp.id and a.is_real_revenue for a in attributions)
            has_leads = any(L.campaign_id == camp.id for L in leads)
            if not has_revenue and not has_leads:
                vanity_only += 1

        return {
            "signals_total": len(signals),
            "audiences_total": len(audiences),
            "offers_total": len(offers),
            "messages_total": len(messages),
            "campaigns_total": len(campaigns),
            "touches_total": len(touches),
            "attributions_total": len(attributions),
            "experiments_total": len(experiments),
            "case_studies_total": len(case_studies),
            "leads_total": len(leads),
            "active_campaigns": active_campaigns,
            "running_experiments": running_experiments,
            "unattributed_revenue_count": unattributed_revenue_count,
            "vanity_only_campaigns": vanity_only,
        }


_default_singleton: RevenueMarketingStore | None = None
_singleton_lock = threading.Lock()


def get_revenue_marketing_store() -> RevenueMarketingStore:
    global _default_singleton
    if _default_singleton is None:
        with _singleton_lock:
            if _default_singleton is None:
                st = RevenueMarketingStore()
                st.ensure_seed_loaded()
                _default_singleton = st
    return _default_singleton


def reset_revenue_marketing_store_for_tests(
    path: Path | None = None,
) -> RevenueMarketingStore:
    global _default_singleton
    st = RevenueMarketingStore(path=path)
    _default_singleton = st
    return st
