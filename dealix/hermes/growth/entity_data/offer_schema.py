from __future__ import annotations

from dataclasses import dataclass


@dataclass
class OfferEntity:
    name: str
    price_sar: float
    price_currency: str = "SAR"
    availability: str = "https://schema.org/InStock"
    url: str = ""
    description: str = ""


def offer_jsonld(o: OfferEntity) -> dict[str, object]:
    if o.price_sar < 0:
        raise ValueError("price_sar must be >= 0")
    return {
        "@context": "https://schema.org",
        "@type": "Offer",
        "name": o.name,
        "price": o.price_sar,
        "priceCurrency": o.price_currency,
        "availability": o.availability,
        "url": o.url,
        "description": o.description,
    }
