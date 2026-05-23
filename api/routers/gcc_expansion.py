"""
Wave 16.0 — GCC Expansion Intelligence HTTP surface.

Endpoints:
  GET  /api/v1/gcc-expansion/market-scan     — sector pulse for a GCC country
  GET  /api/v1/gcc-expansion/sector-pulse    — pulse detail for a single sector
  GET  /api/v1/gcc-expansion/opportunity-feed — ranked opportunities (empty-input)
  GET  /api/v1/gcc-expansion/hot-cities      — city heat ranking for a country
  POST /api/v1/gcc-expansion/signal-detect   — detect a single signal from raw data
  GET  /api/v1/gcc-expansion/gcc-overview    — summary across all six GCC markets

Hard gates:
  - is_estimate_always_true: all scored outputs carry is_estimate=True
  - no_pii_in_logs: never log company names or contact info
"""
from __future__ import annotations

import json
import os
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parent.parent.parent

router = APIRouter(
    prefix="/api/v1/gcc-expansion",
    tags=["Wave 16 — GCC Expansion Intelligence"],
)

_HARD_GATES: dict[str, bool] = {
    "is_estimate_always_true": True,
    "no_pii_in_logs": True,
}

_VALID_COUNTRIES: tuple[str, ...] = ("SA", "AE", "KW", "BH", "QA", "OM")

_COUNTRY_NAME_AR: dict[str, str] = {
    "SA": "المملكة العربية السعودية",
    "AE": "الإمارات",
    "KW": "الكويت",
    "BH": "البحرين",
    "QA": "قطر",
    "OM": "عُمان",
}

_COUNTRY_NAME_EN: dict[str, str] = {
    "SA": "Saudi Arabia",
    "AE": "United Arab Emirates",
    "KW": "Kuwait",
    "BH": "Bahrain",
    "QA": "Qatar",
    "OM": "Oman",
}

# Sectors used for synthetic pulse generation per country
_COUNTRY_SECTORS: dict[str, list[str]] = {
    "SA": ["real_estate", "clinics", "logistics", "retail", "hospitality", "agencies"],
    "AE": ["real_estate", "fintech", "tourism", "logistics", "agencies", "hospitality"],
    "KW": ["real_estate", "retail", "logistics", "clinics", "construction"],
    "BH": ["fintech", "real_estate", "logistics", "agencies"],
    "QA": ["construction", "hospitality", "logistics", "real_estate"],
    "OM": ["tourism", "logistics", "real_estate", "clinics"],
}

# Ledger for scan records
_DEFAULT_LEDGER = "var/gcc_scans.jsonl"
_lock = threading.Lock()


def _ledger_path() -> Path:
    p = Path(os.environ.get("DEALIX_GCC_LEDGER_PATH", _DEFAULT_LEDGER))
    if not p.is_absolute():
        p = ROOT / p
    return p


def _append_scan(record: dict[str, Any]) -> None:
    path = _ledger_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with _lock:
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


# ── Lazy import helpers ───────────────────────────────────────────────────────
# The market_intelligence module may have transitive dependencies.  Any
# ImportError causes the endpoint to return a degraded (but valid) response
# rather than crashing the application.

def _import_market_intelligence() -> dict[str, Any] | None:
    try:
        from auto_client_acquisition.market_intelligence import (
            build_sector_pulse,
            rank_hot_sectors,
            build_city_heatmap,
            top_hot_cities,
            detect_hiring_signal,
            detect_website_change,
            detect_ads_signal,
            detect_funding_signal,
            detect_tender_signal,
        )
        return {
            "build_sector_pulse": build_sector_pulse,
            "rank_hot_sectors": rank_hot_sectors,
            "build_city_heatmap": build_city_heatmap,
            "top_hot_cities": top_hot_cities,
            "detect_hiring_signal": detect_hiring_signal,
            "detect_website_change": detect_website_change,
            "detect_ads_signal": detect_ads_signal,
            "detect_funding_signal": detect_funding_signal,
            "detect_tender_signal": detect_tender_signal,
        }
    except Exception:  # noqa: BLE001
        return None


def _build_pulses_for_country(country: str, mi: dict[str, Any]) -> list[dict[str, Any]]:
    """Build sector pulses for a country using empty signal lists."""
    build_sector_pulse = mi["build_sector_pulse"]
    sectors = _COUNTRY_SECTORS.get(country, _COUNTRY_SECTORS["SA"])
    pulses = []
    for sector in sectors:
        pulse = build_sector_pulse(
            sector=sector,
            signals_this_week=[],
            signals_prior_week=[],
        )
        pulses.append(pulse)
    return pulses


def _pulse_heat_score(pulse: Any) -> float:
    """Derive a 0..1 heat score from a SectorPulse."""
    trend_weight = {"rising": 1.0, "steady": 0.5, "cooling": 0.1}.get(
        getattr(pulse, "trend", "steady"), 0.3
    )
    signals = getattr(pulse, "active_signals", 0)
    companies = getattr(pulse, "n_companies_with_signals", 0)
    raw = (signals * 0.6 + companies * 0.4) * trend_weight
    # Normalise: cap at 100 signals → score of 100 (percentage-style, consistent with city heat)
    return round(min(100.0, raw), 2)


# ── Endpoints ─────────────────────────────────────────────────────────────────


@router.get("/market-scan")
async def market_scan(
    country: str = Query(default="SA", description="GCC country code"),
    limit: int = Query(default=20, ge=1, le=50),
) -> dict[str, Any]:
    """Build a sector momentum scan for a GCC country.

    Returns top sectors ranked by pulse score.
    All scores carry is_estimate=True.
    """
    country = country.upper()
    if country not in _VALID_COUNTRIES:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "invalid_country",
                "valid_countries": list(_VALID_COUNTRIES),
            },
        )

    mi = _import_market_intelligence()
    if mi is None:
        return {
            "country": country,
            "sectors_hot": [],
            "is_estimate": True,
            "module_available": False,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "hard_gates": _HARD_GATES,
        }

    rank_hot_sectors = mi["rank_hot_sectors"]
    pulses = _build_pulses_for_country(country, mi)
    ranked = rank_hot_sectors(pulses=pulses, top_n=min(limit, len(pulses)))

    sectors_hot = [
        {
            "sector": p.sector,
            "score": _pulse_heat_score(p),
            "trend": p.trend,
            "signal_count": p.active_signals,
        }
        for p in ranked
    ]

    record = {
        "country": country,
        "sectors_scanned": len(pulses),
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    _append_scan(record)

    return {
        "country": country,
        "country_name_ar": _COUNTRY_NAME_AR.get(country, country),
        "country_name_en": _COUNTRY_NAME_EN.get(country, country),
        "sectors_hot": sectors_hot,
        "is_estimate": True,
        "generated_at": record["generated_at"],
        "hard_gates": _HARD_GATES,
    }


@router.get("/sector-pulse")
async def sector_pulse_detail(
    sector: str = Query(..., description="Sector name, e.g. real_estate"),
    country: str = Query(default="SA", description="GCC country code"),
) -> dict[str, Any]:
    """Return pulse detail for a single sector in a given country.

    When the sector is not tracked for that country, returns an empty pulse
    with is_estimate=True and a note.
    """
    country = country.upper()
    if country not in _VALID_COUNTRIES:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "invalid_country",
                "valid_countries": list(_VALID_COUNTRIES),
            },
        )

    mi = _import_market_intelligence()
    if mi is None:
        return {
            "sector": sector,
            "country": country,
            "pulse": None,
            "is_estimate": True,
            "module_available": False,
            "hard_gates": _HARD_GATES,
        }

    build_sector_pulse = mi["build_sector_pulse"]
    pulse = build_sector_pulse(
        sector=sector,
        signals_this_week=[],
        signals_prior_week=[],
    )

    return {
        "sector": sector,
        "country": country,
        "country_name_ar": _COUNTRY_NAME_AR.get(country, country),
        "pulse": pulse.to_dict(),
        "heat_score": _pulse_heat_score(pulse),
        "is_estimate": True,
        "hard_gates": _HARD_GATES,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/opportunity-feed")
async def opportunity_feed(
    country: str = Query(default="SA", description="GCC country code"),
    limit: int = Query(default=10, ge=1, le=50),
) -> dict[str, Any]:
    """Return ranked opportunity list for a country.

    When no live signals are available (empty-input mode), returns an empty
    list with context explaining why. All results carry is_estimate=True.
    """
    country = country.upper()
    if country not in _VALID_COUNTRIES:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "invalid_country",
                "valid_countries": list(_VALID_COUNTRIES),
            },
        )

    # build_opportunity_feed requires a why_now_explainer callable and
    # populated signals.  In empty-input mode we return an empty feed with a
    # note rather than fabricating opportunities.
    return {
        "country": country,
        "country_name_ar": _COUNTRY_NAME_AR.get(country, country),
        "opportunities": [],
        "count": 0,
        "note": (
            "No live signals ingested. Connect a signal adapter to populate "
            "the opportunity feed."
        ),
        "is_estimate": True,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "hard_gates": _HARD_GATES,
    }


@router.get("/hot-cities")
async def hot_cities(
    country: str = Query(default="SA", description="GCC country code"),
    top_n: int = Query(default=5, ge=1, le=20),
) -> dict[str, Any]:
    """Return top cities ranked by buying-intent heat for a country.

    In empty-input mode (no signal data) the city heatmap will be empty.
    All scores carry is_estimate=True.
    """
    country = country.upper()
    if country not in _VALID_COUNTRIES:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "invalid_country",
                "valid_countries": list(_VALID_COUNTRIES),
            },
        )

    mi = _import_market_intelligence()
    if mi is None:
        return {
            "country": country,
            "cities": [],
            "is_estimate": True,
            "module_available": False,
            "hard_gates": _HARD_GATES,
        }

    build_city_heatmap = mi["build_city_heatmap"]
    top_hot_cities_fn = mi["top_hot_cities"]

    # build_city_heatmap needs signals_by_company and company_metadata.
    # With empty dicts the result is an empty heatmap — correct for zero-input mode.
    heatmap = build_city_heatmap(
        signals_by_company={},
        company_metadata={},
    )
    top = top_hot_cities_fn(heatmaps=heatmap, n=top_n)

    cities = [
        {
            "city": h.city,
            "heat_score": h.heat_score,
            "bucket": h.bucket,
            "sector_leaders": h.top_sector,
            "n_signals": h.n_signals,
        }
        for h in top
    ]

    return {
        "country": country,
        "country_name_ar": _COUNTRY_NAME_AR.get(country, country),
        "cities": cities,
        "is_estimate": True,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "hard_gates": _HARD_GATES,
    }


# ── Signal Detect ─────────────────────────────────────────────────────────────

class SignalDetectRequest(BaseModel):
    signal_type: str
    raw_data: dict[str, Any] = {}


def _run_hiring_detector(mi: dict[str, Any], raw_data: dict[str, Any]) -> list[Any]:
    detect = mi["detect_hiring_signal"]
    company_id = raw_data.get("company", "unknown")
    jobs_count = int(raw_data.get("jobs_count", 0))
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    from datetime import timedelta
    job_postings = [
        {
            "title": raw_data.get("title", "sales manager"),
            "posted_at": now - timedelta(days=1),
            "url": raw_data.get("url"),
        }
    ] * max(1, jobs_count)
    return detect(company_id=company_id, job_postings=job_postings)


def _run_website_detector(mi: dict[str, Any], raw_data: dict[str, Any]) -> list[Any]:
    detect = mi["detect_website_change"]
    company_id = raw_data.get("company", "unknown")
    diff = {
        "added_paths": raw_data.get("added_paths", []),
        "added_widgets": raw_data.get("added_widgets", []),
        "major_redesign": raw_data.get("major_redesign", False),
        "homepage_url": raw_data.get("url"),
    }
    return detect(company_id=company_id, diff=diff)


def _run_ads_detector(mi: dict[str, Any], raw_data: dict[str, Any]) -> list[Any]:
    detect = mi["detect_ads_signal"]
    company_id = raw_data.get("company", "unknown")
    history = raw_data.get("weekly_ad_spend_history", [10.0, 10.0, 10.0, 20.0])
    return detect(company_id=company_id, weekly_ad_spend_history=history)


def _run_funding_detector(mi: dict[str, Any], raw_data: dict[str, Any]) -> list[Any]:
    detect = mi["detect_funding_signal"]
    company_id = raw_data.get("company", "unknown")
    from datetime import timedelta
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    announcements = raw_data.get("announcements", [
        {
            "round_type": raw_data.get("round_type", "seed"),
            "amount_sar": raw_data.get("amount_sar", 500000),
            "announced_at": now - timedelta(days=10),
            "url": raw_data.get("url"),
        }
    ])
    # Normalise string dates
    processed: list[dict[str, Any]] = []
    for a in announcements:
        entry = dict(a)
        if isinstance(entry.get("announced_at"), str):
            entry["announced_at"] = datetime.fromisoformat(entry["announced_at"])
            if entry["announced_at"].tzinfo:
                entry["announced_at"] = entry["announced_at"].replace(tzinfo=None)
        processed.append(entry)
    return detect(company_id=company_id, announcements=processed)


def _run_tender_detector(mi: dict[str, Any], raw_data: dict[str, Any]) -> list[Any]:
    detect = mi["detect_tender_signal"]
    company_id = raw_data.get("company", "unknown")
    from datetime import timedelta
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    tenders = raw_data.get("tenders", [
        {
            "title": raw_data.get("title", "General tender"),
            "body": raw_data.get("body", ""),
            "published_at": now - timedelta(days=5),
            "deadline": now + timedelta(days=30),
            "url": raw_data.get("url"),
            "value_sar": raw_data.get("value_sar"),
        }
    ])
    processed: list[dict[str, Any]] = []
    for t in tenders:
        entry = dict(t)
        for key in ("published_at", "deadline"):
            if isinstance(entry.get(key), str):
                entry[key] = datetime.fromisoformat(entry[key])
                if entry[key].tzinfo:
                    entry[key] = entry[key].replace(tzinfo=None)
        processed.append(entry)
    return detect(company_id=company_id, tenders=processed)


_DETECTOR_RUNNERS = {
    "hiring": _run_hiring_detector,
    "website": _run_website_detector,
    "ads": _run_ads_detector,
    "funding": _run_funding_detector,
    "tender": _run_tender_detector,
}


@router.post("/signal-detect")
async def signal_detect(req: SignalDetectRequest) -> dict[str, Any]:
    """Detect a signal from raw data.

    signal_type must be one of: hiring, website, ads, funding, tender.
    Returns detected flag, confidence, and metadata.
    All outputs carry is_estimate=True.
    """
    signal_type = req.signal_type.lower().strip()
    if signal_type not in _DETECTOR_RUNNERS:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "invalid_signal_type",
                "valid_types": list(_DETECTOR_RUNNERS.keys()),
                "received": req.signal_type,
            },
        )

    mi = _import_market_intelligence()
    if mi is None:
        return {
            "signal_type": signal_type,
            "detected": False,
            "confidence": 0.0,
            "metadata": {},
            "is_estimate": True,
            "module_available": False,
            "hard_gates": _HARD_GATES,
        }

    runner = _DETECTOR_RUNNERS[signal_type]
    try:
        detections = runner(mi, req.raw_data)
    except (ValueError, TypeError, KeyError) as exc:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "invalid_raw_data",
                "message": str(exc),
                "signal_type": signal_type,
            },
        ) from exc

    detected = len(detections) > 0
    confidence = (
        sum(d.confidence for d in detections) / len(detections)
        if detections else 0.0
    )
    metadata: dict[str, Any] = {}
    if detections:
        first = detections[0]
        metadata = {
            "detected_signal_type": first.signal_type,
            "source": first.source,
            "payload": first.payload,
            "total_detections": len(detections),
        }

    return {
        "signal_type": signal_type,
        "detected": detected,
        "confidence": round(confidence, 4),
        "metadata": metadata,
        "is_estimate": True,
        "hard_gates": _HARD_GATES,
    }


# ── GCC Overview ──────────────────────────────────────────────────────────────

@router.get("/gcc-overview")
async def gcc_overview() -> dict[str, Any]:
    """Return a summary scan across all six GCC markets.

    For each country: top sector + heat score.
    All scores carry is_estimate=True.
    """
    mi = _import_market_intelligence()

    countries: list[dict[str, Any]] = []
    for country_code in _VALID_COUNTRIES:
        if mi is not None:
            pulses = _build_pulses_for_country(country_code, mi)
            rank_hot_sectors = mi["rank_hot_sectors"]
            ranked = rank_hot_sectors(pulses=pulses, top_n=1)
            if ranked:
                top_sector = ranked[0].sector
                heat_score = _pulse_heat_score(ranked[0])
            else:
                top_sector = None
                heat_score = 0.0
        else:
            top_sector = None
            heat_score = 0.0

        countries.append({
            "country_code": country_code,
            "country_name_ar": _COUNTRY_NAME_AR[country_code],
            "country_name_en": _COUNTRY_NAME_EN[country_code],
            "top_sector": top_sector,
            "heat_score": heat_score,
        })

    return {
        "countries": countries,
        "is_estimate": True,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "hard_gates": _HARD_GATES,
    }
