"""Unit tests for the Brand & Growth Operating Layer internal API.

These tests exercise the read-only endpoints under
``/api/v1/internal/{brand,growth,marketing,product}`` directly, without
spinning up the full FastAPI app. They cover the success path (seed CSVs +
brand tokens present) and the source-provenance contract (``source=signal``
when data is found, ``source=fallback`` when not).
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path


def _run(coro):
    """Drive a coroutine to completion without leaking a loop.

    Using ``asyncio.run`` instead of ``asyncio.get_event_loop()`` so the
    test works under pytest-asyncio's auto mode and on Python 3.10+
    where ``get_event_loop()`` with no running loop is deprecated.
    """
    return asyncio.run(coro)


def test_brand_summary_returns_pillars_and_palette() -> None:
    from api.routers.brand_growth_internal import brand_summary

    payload = _run(brand_summary())

    assert payload["brand"]["name"] == "DEALIX"
    assert payload["brand"]["tagline"] == "INTELLIGENT DEALS. REAL GROWTH."
    assert "Saudi B2B Revenue Operating System" in payload["brand"]["positioning"]
    assert payload["brand"]["pillars"] == [
        "Built on Trust",
        "Driven by Growth",
        "Closing Deals",
        "Focused on Results",
        "Global Mindset, Local Impact",
    ]

    palette = payload["palette"]
    assert palette["bg_primary"] == "#0B1220"
    assert palette["accent_primary"] == "#00D1A1"
    assert palette["text_secondary"] == "#B2BBC6"


def test_brand_summary_tokens_source_provenance() -> None:
    from api.routers.brand_growth_internal import brand_summary

    payload = _run(brand_summary())
    # When tokens JSON exists, source must be "signal".
    assert payload["tokens_source"] in {"signal", "fallback"}
    # In a normal checkout, brand-tokens.json is present.
    repo_root = Path(__file__).resolve().parents[2]
    tokens_present = (repo_root / "docs" / "brand" / "brand-tokens.json").exists()
    if tokens_present:
        assert payload["tokens_source"] == "signal"
        assert payload["tokens_meta"], "tokens meta should be populated when JSON exists"


def test_brand_summary_assets_registry_listed() -> None:
    from api.routers.brand_growth_internal import brand_summary

    payload = _run(brand_summary())
    assets = payload["assets"]
    assert isinstance(assets, list)
    if assets:
        # Every row must carry source provenance.
        for row in assets:
            assert "source" in row


def test_growth_targeting_payload_contains_required_sections() -> None:
    from api.routers.brand_growth_internal import growth_targeting

    payload = _run(growth_targeting())
    for key in ("sectors", "segments", "accounts", "machines"):
        assert key in payload, f"missing section: {key}"
        assert isinstance(payload[key], list)
        assert f"{key}_source" in payload
        assert payload[f"{key}_source"] in {"signal", "fallback"}


def test_growth_targeting_trust_note_present() -> None:
    from api.routers.brand_growth_internal import growth_targeting

    payload = _run(growth_targeting())
    note = payload["trust_note"]
    assert "decision support" in note.lower()
    assert "approval" in note.lower()


def test_marketing_summary_payload() -> None:
    from api.routers.brand_growth_internal import marketing_summary

    payload = _run(marketing_summary())
    for key in ("calendar", "campaigns", "ideas"):
        assert key in payload
        assert isinstance(payload[key], list)
        assert f"{key}_source" in payload
    assert "brand check" in payload["trust_note"].lower()


def test_product_distribution_payload() -> None:
    from api.routers.brand_growth_internal import product_distribution

    payload = _run(product_distribution())
    assert "offer_ladder" in payload
    assert "product_distribution" in payload
    assert payload["pricing_guardrails_doc"] == "docs/product/PRICING_GUARDRAILS.md"
    assert isinstance(payload["offer_ladder"], list)
    assert isinstance(payload["product_distribution"], list)
    # If the seed CSV is present we expect all 7 rungs.
    if payload["offer_ladder"]:
        rungs = {row.get("rung") for row in payload["offer_ladder"]}
        assert {"1", "2", "3", "4", "5", "6", "7"}.issubset(rungs)


def test_no_guaranteed_claims_in_payloads() -> None:
    """The trust contract: no payload should contain guarantee language."""
    from api.routers.brand_growth_internal import (
        brand_summary,
        growth_targeting,
        marketing_summary,
        product_distribution,
    )

    banned = (
        "guaranteed revenue",
        "guaranteed sales",
        "guaranteed leads",
        "guaranteed results",
        "auto-pilot growth",
    )
    payloads = [
        _run(brand_summary()),
        _run(growth_targeting()),
        _run(marketing_summary()),
        _run(product_distribution()),
    ]
    for payload in payloads:
        serialised = json.dumps(payload, ensure_ascii=False).lower()
        for phrase in banned:
            assert phrase not in serialised, f"banned claim '{phrase}' present in payload"


def test_router_registers_expected_paths() -> None:
    from api.routers.brand_growth_internal import router

    paths = {route.path for route in router.routes}
    assert "/api/v1/internal/brand/summary" in paths
    assert "/api/v1/internal/growth/targeting" in paths
    assert "/api/v1/internal/marketing/summary" in paths
    assert "/api/v1/internal/product/distribution" in paths


def test_csv_loader_handles_missing_file(tmp_path, monkeypatch) -> None:
    """The CSV loader returns [] for missing paths instead of raising."""
    import api.routers.brand_growth_internal as mod

    missing = tmp_path / "does-not-exist.csv"
    assert mod._load_csv(missing) == []
