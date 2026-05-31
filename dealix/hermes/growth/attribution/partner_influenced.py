"""Partner-influenced attribution: a sourcing partner gets up to 0.5."""

from __future__ import annotations


def apply(weights: dict[str, float], partner: str | None) -> dict[str, float]:
    if not partner:
        return weights
    out = dict(weights)
    out[f"partner:{partner}"] = out.get(f"partner:{partner}", 0.0) + 0.5
    return out
