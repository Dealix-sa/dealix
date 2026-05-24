"""Tests for `dealix.products.offer_library.OfferLibrary`."""

from __future__ import annotations

import pytest

from dealix.products.offer_library import OfferLibrary


def test_seeded_library_contains_five_offers() -> None:
    library = OfferLibrary()
    names = {o.name for o in library.all()}
    assert "Revenue Hunter Pilot" in names
    assert "AI Trust Kit" in names
    assert "Agency White-label Kit" in names
    assert "Vertical Launch Sprint" in names
    assert "Renewal & Upsell Pack" in names
    assert len(library.all()) >= 5


def test_list_for_buyer_filters_substring_match() -> None:
    library = OfferLibrary()
    agency_offers = library.list_for_buyer("Agency")
    assert agency_offers
    assert any("White-label" in o.name for o in agency_offers)


def test_duplicate_registration_raises() -> None:
    library = OfferLibrary()
    existing = library.get("AI Trust Kit")
    with pytest.raises(ValueError):
        library.register(existing)


def test_get_unknown_raises_key_error() -> None:
    library = OfferLibrary()
    with pytest.raises(KeyError):
        library.get("does not exist")
