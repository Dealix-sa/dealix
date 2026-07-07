"""
Adapters — real, safe connectors to the Autonomous OS core stack.

Every adapter is:
- **Offline-safe**: if the external service is not configured/reachable, it
  degrades to a deterministic local fallback and never raises.
- **Draft-only**: no adapter here sends any external message. The WhatsApp
  adapter can *format* a draft payload but has no capability to send it.
- **Dependency-light**: uses only the standard library (urllib), so it runs in
  minimal CI/cron with no extra installs.

Core stack mapped here (per the OS brief):
  - Ollama  -> local-first model inference (the "brain")
  - Twenty  -> CRM pipeline signals feeding the growth engine (the "eyes")
  - WhatsApp/Evolution -> draft payload formatting only (the bound "hands")
"""

from __future__ import annotations

from typing import Any

from .base import Adapter, AdapterResult, AdapterStatus  # noqa: F401
from .ollama_adapter import OllamaAdapter  # noqa: F401
from .twenty_adapter import TwentyCRMAdapter  # noqa: F401
from .whatsapp_draft_adapter import WhatsAppDraftAdapter  # noqa: F401

__all__ = [
    "Adapter",
    "AdapterResult",
    "AdapterStatus",
    "OllamaAdapter",
    "TwentyCRMAdapter",
    "WhatsAppDraftAdapter",
    "all_status",
]


def all_status(env: dict[str, str] | None = None) -> list[dict[str, Any]]:
    """Report the availability/mode of every core-stack adapter."""
    adapters: list[Adapter] = [
        OllamaAdapter(env=env),
        TwentyCRMAdapter(env=env),
        WhatsAppDraftAdapter(env=env),
    ]
    return [a.status().to_dict() for a in adapters]
