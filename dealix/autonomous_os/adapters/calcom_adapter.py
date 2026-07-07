"""
Cal.com adapter — booking-link preparation (read-only).

Provides a shareable booking link and event-type metadata so the OS can draft
"book a Free Diagnostic / Sprint call" prompts. It never creates a booking and
never sends anything — it only *prepares* a link a founder can include in an
approved message.

Offline-safe: if Cal.com is not configured/reachable, it returns a configured
default booking URL (`CALCOM_BOOKING_URL`) or a clearly-labelled placeholder.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any

from .base import Adapter, AdapterResult, AdapterStatus

REQUEST_TIMEOUT_SECONDS = 20
PLACEHOLDER_URL = "https://cal.com/dealix/diagnostic"  # labelled default, replace in config


class CalComAdapter(Adapter):
    name = "calcom"

    def __init__(self, env: dict[str, str] | None = None) -> None:
        self._env = env if env is not None else dict(os.environ)

    def _get(self, key: str) -> str:
        return (self._env.get(key) or "").strip()

    def is_available(self) -> bool:
        return bool(self._get("CALCOM_API_KEY"))

    @property
    def default_url(self) -> str:
        return self._get("CALCOM_BOOKING_URL") or PLACEHOLDER_URL

    def status(self) -> AdapterStatus:
        available = self.is_available()
        return AdapterStatus(
            name=self.name,
            available=available,
            mode="live" if available else "offline_fallback",
            detail="prepares booking links; never creates bookings or sends",
        )

    def booking_link(self, event_slug: str | None = None) -> AdapterResult:
        """Return a booking link draft. Read-only; no booking is created."""
        if not self.is_available():
            url = self.default_url if not event_slug else f"{self.default_url}/{event_slug}"
            return AdapterResult(
                ok=True,
                mode="offline_fallback",
                data={"booking_url": url, "event_slug": event_slug, "creates_booking": False},
                meta={"reason": "cal.com not configured — using default/placeholder URL"},
            )

        req = urllib.request.Request(
            "https://api.cal.com/v2/event-types",
            headers={"Authorization": f"Bearer {self._get('CALCOM_API_KEY')}"},
            method="GET",
        )
        try:
            with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT_SECONDS) as resp:
                parsed = json.loads(resp.read().decode("utf-8"))
            types = (parsed or {}).get("data", []) or []
            chosen: dict[str, Any] | None = None
            for t in types:
                if not event_slug or str(t.get("slug")) == event_slug:
                    chosen = t
                    break
            slug = str((chosen or {}).get("slug", event_slug or ""))
            url = f"{self.default_url}/{slug}" if slug else self.default_url
            return AdapterResult(
                ok=True,
                mode="live",
                data={"booking_url": url, "event_slug": slug, "creates_booking": False},
            )
        except (urllib.error.URLError, ValueError, json.JSONDecodeError, OSError) as exc:
            return AdapterResult(
                ok=True,
                mode="offline_fallback",
                data={"booking_url": self.default_url, "creates_booking": False},
                error=f"{type(exc).__name__}: {exc}",
                meta={"reason": "cal.com request failed"},
            )
