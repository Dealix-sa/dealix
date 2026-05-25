"""
Package — the canonical shape of a Dealix offer.

This module also houses the package registry. ``products.packages``
populates it.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from dealix.hermes.control_plane.sovereignty_gate import SovereigntyLevel


@dataclass(frozen=True)
class Package:
    package_id: str
    name: str
    buyer: str
    pain: str
    deliverables: tuple[str, ...]
    price_range_sar: tuple[int, int]
    upsell: str | None
    trust_risks: tuple[str, ...]
    required_approval: SovereigntyLevel
    delivery_playbook_id: str
    tags: tuple[str, ...] = field(default_factory=tuple)


PRODUCT_REGISTRY: dict[str, Package] = {}


def register_package(package: Package) -> Package:
    PRODUCT_REGISTRY[package.package_id] = package
    return package
