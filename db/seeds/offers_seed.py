"""Hermes offer registry seed.

Re-exports the canonical ``DEFAULT_OFFERS`` tuple from the Hermes
product module and exposes a serialisable ``OFFERS`` list of dicts for
database seeding.
"""

from __future__ import annotations

import dataclasses
from typing import Any

from dealix.hermes.products.offer_registry import DEFAULT_OFFERS

OFFERS: list[dict[str, Any]] = [dataclasses.asdict(o) for o in DEFAULT_OFFERS]


__all__ = ["DEFAULT_OFFERS", "OFFERS"]
