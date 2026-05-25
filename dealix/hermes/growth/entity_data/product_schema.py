from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ProductEntity:
    name: str
    description: str
    url: str
    brand: str
    category: str = ""


def product_jsonld(p: ProductEntity) -> dict[str, object]:
    if not p.name or not p.url:
        raise ValueError("ProductEntity requires name and url")
    return {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": p.name,
        "description": p.description,
        "url": p.url,
        "brand": {"@type": "Brand", "name": p.brand},
        "category": p.category,
    }
