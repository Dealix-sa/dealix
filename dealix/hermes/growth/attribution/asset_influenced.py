"""Asset-influenced attribution: add a 10% bump per asset that touched the deal."""

from __future__ import annotations


def apply(weights: dict[str, float], assets: tuple[str, ...]) -> dict[str, float]:
    if not assets:
        return weights
    out = dict(weights)
    bump = 0.1
    for a in assets:
        out[f"asset:{a}"] = out.get(f"asset:{a}", 0.0) + bump
    return out
