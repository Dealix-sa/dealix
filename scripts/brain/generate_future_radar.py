"""Generate a Future Radar — scenario-based, non-deterministic.

The radar covers 30, 90, and 365-day horizons. For each horizon and each focus
area, three scenarios are produced: base, upside, downside. Every scenario
carries an explicit confidence level (low/medium/high). No scenario is a
prediction or a guarantee — it is a structured hypothesis about a possible
future state.

IMPORTANT: This module must never emit statements like "X will happen" or
"guaranteed ROI". Use "could", "may", "scenario", "confidence" language.
"""
from __future__ import annotations

from datetime import UTC, datetime, timezone
from typing import Any

HORIZONS = (30, 90, 365)
SCENARIO_KEYS = ("base", "upside", "downside")
CONFIDENCE_LEVELS = ("low", "medium", "high")

# Phrases that imply deterministic futures — guarded against in tests.
DETERMINISTIC_PHRASES = (
    "will happen",
    "is guaranteed",
    "guaranteed roi",
    "certain to",
    "definitely",
    "must happen",
    "inevitable",
    "100% chance",
    "zero risk",
    "risk-free",
)


def _scenario(text: str, confidence: str) -> dict[str, str]:
    if confidence not in CONFIDENCE_LEVELS:
        raise ValueError(f"confidence must be one of {CONFIDENCE_LEVELS}, got {confidence}")
    # Defensive check: never let a deterministic phrase through.
    lowered = text.lower()
    for phrase in DETERMINISTIC_PHRASES:
        if phrase in lowered:
            raise ValueError(
                f"Future radar scenario contains deterministic phrase '{phrase}': {text!r}"
            )
    return {"scenario": text, "confidence": confidence}


def generate_future_radar(
    focus_areas: list[str] | None = None,
    profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Generate a scenario-based future radar.

    Parameters
    ----------
    focus_areas : list of focus-area names. If None, uses profile's focus
        areas or a sensible default set.
    profile : optional company profile (used to derive focus areas).

    Returns a mapping of horizon -> focus_area -> {base,upside,downside}
    each with scenario text and a confidence level.
    """
    if focus_areas is None:
        focus_areas = (profile or {}).get("focus_areas") or ["growth", "product", "operations"]

    radar: dict[str, Any] = {
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "horizons": {},
        "note": (
            "Scenarios are structured hypotheses, not predictions. "
            "Each carries an explicit confidence level. No guaranteed outcomes."
        ),
    }

    for horizon in HORIZONS:
        horizon_key = f"{horizon}_day"
        radar["horizons"][horizon_key] = {}
        for area in focus_areas:
            radar["horizons"][horizon_key][area] = {
                "base": _scenario(
                    f"If current trajectory holds, {area} may stabilise at current pace over {horizon} days.",
                    "medium",
                ),
                "upside": _scenario(
                    f"If key assumptions hold and execution is strong, {area} could accelerate over {horizon} days.",
                    "low",
                ),
                "downside": _scenario(
                    f"If key assumptions break, {area} may regress over {horizon} days.",
                    "medium",
                ),
            }

    return radar


if __name__ == "__main__":
    import json

    print(json.dumps(generate_future_radar(), indent=2))
