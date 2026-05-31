"""Offer composition utilities."""

from __future__ import annotations

from dealix.hermes.products.offer_library import Offer, check_readiness


def build_offer(**fields) -> Offer:
    offer = Offer(**fields)
    readiness = check_readiness(offer)
    if not readiness.ready:
        raise ValueError(f"offer missing fields: {readiness.missing_fields}")
    return offer
