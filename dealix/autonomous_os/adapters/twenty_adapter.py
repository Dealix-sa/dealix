"""
Twenty CRM adapter — read-only pipeline signals for the Growth Engine.

Pulls light commercial counts (warm leads, active conversations, outstanding
proposals, booked sprints) that the GrowthEngine uses to prioritise draft work.

Read-only by design: it never writes to the CRM and never sends anything. When
Twenty is not configured/reachable, it degrades to a local JSON snapshot
(`<runtime>/crm_context.json`) or zeros — so the OS always has a safe signal.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from .base import Adapter, AdapterResult, AdapterStatus

REQUEST_TIMEOUT_SECONDS = 20

_ZERO_CONTEXT = {
    "warm_leads": 0,
    "active_conversations": 0,
    "proposals_outstanding": 0,
    "proof_assets_ready": 0,
    "booked_sprints": 0,
}


class TwentyCRMAdapter(Adapter):
    name = "twenty_crm"

    def __init__(
        self,
        env: dict[str, str] | None = None,
        local_snapshot: Path | str | None = None,
    ) -> None:
        self._env = env if env is not None else dict(os.environ)
        self._snapshot = Path(local_snapshot) if local_snapshot else None

    def _get(self, key: str) -> str:
        return (self._env.get(key) or "").strip()

    @property
    def api_url(self) -> str:
        return self._get("TWENTY_API_URL")

    def is_available(self) -> bool:
        return bool(self.api_url and self._get("TWENTY_API_KEY"))

    def status(self) -> AdapterStatus:
        available = self.is_available()
        source = "live" if available else ("offline_fallback")
        detail = "twenty api configured" if available else "using local snapshot / zeros"
        return AdapterStatus(name=self.name, available=available, mode=source, detail=detail)

    def _local_context(self) -> dict[str, int]:
        if self._snapshot and self._snapshot.exists():
            try:
                data = json.loads(self._snapshot.read_text(encoding="utf-8"))
                return {k: int(data.get(k, 0) or 0) for k in _ZERO_CONTEXT}
            except (json.JSONDecodeError, ValueError, OSError):
                return dict(_ZERO_CONTEXT)
        return dict(_ZERO_CONTEXT)

    def fetch_growth_context(self) -> AdapterResult:
        if not self.is_available():
            return AdapterResult(
                ok=True,
                mode="offline_fallback",
                data=self._local_context(),
                meta={"reason": "twenty not configured"},
            )

        # Twenty exposes a GraphQL API; we query only aggregate counts.
        query = {
            "query": (
                "query OsContext { "
                "warm: opportunities(filter: {stage: {eq: WARM}}) { totalCount } "
                "active: opportunities(filter: {stage: {eq: ACTIVE}}) { totalCount } "
                "proposals: opportunities(filter: {stage: {eq: PROPOSAL}}) { totalCount } "
                "booked: opportunities(filter: {stage: {eq: WON}}) { totalCount } }"
            )
        }
        body = json.dumps(query).encode("utf-8")
        req = urllib.request.Request(  # noqa: S310 - operator-configured API URL
            self.api_url,
            data=body,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._get('TWENTY_API_KEY')}",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT_SECONDS) as resp:  # noqa: S310
                parsed = json.loads(resp.read().decode("utf-8"))
            d = (parsed or {}).get("data", {}) or {}
            ctx = {
                "warm_leads": int((d.get("warm") or {}).get("totalCount", 0) or 0),
                "active_conversations": int((d.get("active") or {}).get("totalCount", 0) or 0),
                "proposals_outstanding": int((d.get("proposals") or {}).get("totalCount", 0) or 0),
                "proof_assets_ready": self._local_context()["proof_assets_ready"],
                "booked_sprints": int((d.get("booked") or {}).get("totalCount", 0) or 0),
            }
            return AdapterResult(ok=True, mode="live", data=ctx)
        except (urllib.error.URLError, ValueError, json.JSONDecodeError, OSError, KeyError) as exc:
            return AdapterResult(
                ok=True,
                mode="offline_fallback",
                data=self._local_context(),
                error=f"{type(exc).__name__}: {exc}",
                meta={"reason": "twenty query failed"},
            )
