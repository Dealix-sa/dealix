"""Content type / CTA matrix integrity tests."""

from __future__ import annotations

from dealix.growth_os.content_engine.content_types import (
    CONTENT_TYPE_DESCRIPTIONS,
    CONTENT_TYPES,
)
from dealix.growth_os.content_engine.cta_matrix import CONTENT_TO_CASH, cta_for


def test_five_content_types_present() -> None:
    expected = {"trust", "revenue", "partner", "executive", "market_radar"}
    assert set(CONTENT_TYPES) == expected
    assert set(CONTENT_TYPE_DESCRIPTIONS.keys()) == expected


def test_every_content_type_maps_to_cta_and_offer() -> None:
    for key in CONTENT_TYPES:
        mapping = cta_for(key)
        assert mapping.cta_label_ar
        assert mapping.cta_label_en
        assert mapping.cta_path.startswith("/")
        assert mapping.offer_key
        assert mapping.offer_label_ar
        assert mapping.offer_label_en


def test_cta_paths_are_unique() -> None:
    paths = [m.cta_path for m in CONTENT_TO_CASH.values()]
    assert len(paths) == len(set(paths))
