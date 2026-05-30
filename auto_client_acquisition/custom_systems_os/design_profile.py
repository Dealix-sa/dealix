"""Custom Systems OS — per-client design profile builder.

Builds a client-specific design token bundle by layering, in order:

    Dealix defaults (design_system_loader)  <-  locked visual direction
    (visual_directions)  <-  whitelisted client overrides.

No colors/typography are invented at runtime: client overrides are limited to
a whitelist, and an unknown direction falls back to the conservative default
(recorded in ``overrides_applied``). The Dealix ``forbidden_copy`` guard is
inherited so the spec renderer keeps the same banned phrases.
"""

from __future__ import annotations

from typing import Any

from auto_client_acquisition.custom_systems_os.schemas import CustomDesignProfile
from auto_client_acquisition.designops.design_system_loader import load_design_system
from auto_client_acquisition.designops.visual_directions import get_direction

DEFAULT_DIRECTION = "saudi_executive_trust"

# Only these top-level token groups may be overridden by a client.
_OVERRIDE_WHITELIST: frozenset[str] = frozenset({"colors", "typography", "spacing", "tone"})


def build_design_profile(
    *,
    customer_id: str,
    direction_name: str = DEFAULT_DIRECTION,
    client_overrides: dict[str, Any] | None = None,
) -> CustomDesignProfile:
    if not customer_id:
        raise ValueError("customer_id is required")

    design_system = load_design_system()
    overrides_applied: list[str] = []

    resolved_direction = direction_name
    try:
        direction = get_direction(direction_name)
    except KeyError:
        direction = get_direction(DEFAULT_DIRECTION)
        resolved_direction = DEFAULT_DIRECTION
        overrides_applied.append(f"unknown_direction_fallback:{direction_name}")

    # Layer 1 — Dealix defaults.
    tokens: dict[str, Any] = {
        "colors": dict(design_system.get("colors") or {}),
        "typography": dict(design_system.get("typography") or {}),
        "spacing": design_system.get("spacing"),
        "status_chips": design_system.get("status_chips"),
        "tone": None,
    }

    # Layer 2 — locked visual direction.
    tokens["colors"].update(direction.get("palette") or {})
    if direction.get("typography"):
        tokens["typography"].update(direction["typography"])
    if direction.get("spacing") is not None:
        tokens["spacing"] = direction["spacing"]
    tokens["tone"] = direction.get("tone")

    # Layer 3 — whitelisted client overrides.
    for key, value in (client_overrides or {}).items():
        if key not in _OVERRIDE_WHITELIST:
            overrides_applied.append(f"rejected_override:{key}")
            continue
        if key in ("colors", "typography") and isinstance(value, dict):
            tokens[key].update(value)
        else:
            tokens[key] = value
        overrides_applied.append(f"client_override:{key}")

    forbidden_copy = tuple(design_system.get("forbidden_copy") or ())

    return CustomDesignProfile(
        customer_id=customer_id,
        base_source_path=str(design_system.get("source_path") or ""),
        direction_name=resolved_direction,
        tokens=tokens,
        overrides_applied=tuple(overrides_applied),
        forbidden_copy=forbidden_copy,
    )


__all__ = ["DEFAULT_DIRECTION", "build_design_profile"]
