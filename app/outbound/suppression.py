"""Suppression list — recipients who must never receive outbound messages.

A suppressed recipient blocks ALL channels by default. The list is in-memory
and intentionally simple; production deployments may back it with a database
table, but the interface (``is_suppressed`` / ``add_suppression`` /
``remove_suppression``) stays the same.

Suppression covers:
  - opt-outs (unsubscribe)
  - hard bounces
  - complaints
  - manual do-not-contact
  - legal/regulatory blocks (e.g. PDPL DSAR erasure)
"""

from __future__ import annotations

from threading import Lock
from typing import Any

_LOCK = Lock()
# _SUPPRESSED[identifier] = set(channels) | {"__all__"}
_SUPPRESSED: "dict[str, set[str]]" = {}

ALL_CHANNELS = "__all__"


def _norm(identifier: str) -> str:
    return (identifier or "").strip().lower()


def is_suppressed(identifier: str, channel: str = "email") -> bool:
    """True if `identifier` is suppressed for `channel` (or globally)."""
    ident = _norm(identifier)
    if not ident:
        return False
    with _LOCK:
        entry = _SUPPRESSED.get(ident)
        if not entry:
            return False
        return ALL_CHANNELS in entry or channel in entry


def add_suppression(identifier: str, channel: str = ALL_CHANNELS, reason: str = "") -> None:
    """Add `identifier` to the suppression list. Defaults to all channels."""
    ident = _norm(identifier)
    if not ident:
        return
    with _LOCK:
        entry = _SUPPRESSED.setdefault(ident, set())
        entry.add(channel or ALL_CHANNELS)


def remove_suppression(identifier: str, channel: str | None = None) -> None:
    """Remove a suppression entry. If channel is None, remove entirely."""
    ident = _norm(identifier)
    with _LOCK:
        if channel is None:
            _SUPPRESSED.pop(ident, None)
            return
        entry = _SUPPRESSED.get(ident)
        if entry:
            entry.discard(channel)
            if not entry:
                _SUPPRESSED.pop(ident, None)


def suppressed_channels(identifier: str) -> set[str]:
    """Return the set of channels suppressed for `identifier` (may include __all__)."""
    ident = _norm(identifier)
    with _LOCK:
        return set(_SUPPRESSED.get(ident, set()))


def clear_suppressions() -> None:
    """Clear all suppression state (used by tests)."""
    with _LOCK:
        _SUPPRESSED.clear()


def load_suppressions(items: list[dict[str, Any]]) -> None:
    """Bulk-load suppression entries from a list of dicts.

    Each dict should have: identifier (str), optional channel (str),
    optional reason (str).
    """
    for item in items:
        add_suppression(
            str(item.get("identifier", "")),
            channel=str(item.get("channel", ALL_CHANNELS)),
            reason=str(item.get("reason", "")),
        )