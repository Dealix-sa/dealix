"""Load founder Saudi targeting profiles from YAML config."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from auto_client_acquisition.revenue_os.saudi_targeting_profile import SaudiTargetingProfile

_CONFIG = Path(__file__).resolve().parents[2] / "data" / "config" / "saudi_targeting_profiles.yaml"


@lru_cache(maxsize=1)
def load_targeting_profiles_config() -> dict[str, Any]:
    if not _CONFIG.is_file():
        return {"schema_version": 1, "profiles": []}
    raw = yaml.safe_load(_CONFIG.read_text(encoding="utf-8")) or {}
    return raw if isinstance(raw, dict) else {"profiles": []}


def list_configured_profiles() -> list[dict[str, Any]]:
    cfg = load_targeting_profiles_config()
    profiles = cfg.get("profiles") or []
    out: list[dict[str, Any]] = []
    for p in profiles:
        if not isinstance(p, dict):
            continue
        try:
            from auto_client_acquisition.revenue_os.saudi_targeting_profile import (
                build_local_discover_body,
            )

            profile = SaudiTargetingProfile(
                industry_key=str(p.get("industry_key") or ""),
                city_key=str(p.get("city_key") or ""),
                max_results=int(p.get("max_results") or 20),
                signal_keywords=list(p.get("signal_keywords") or []),
            )

            out.append({
                "id": p.get("id"),
                "label_ar": p.get("label_ar"),
                "label_en": p.get("label_en"),
                "tier1_source": p.get("tier1_source", "google_places"),
                "targeting_profile": profile.model_dump(),
                "discover_body": build_local_discover_body(profile),
            })
        except Exception as exc:  # noqa: BLE001
            out.append({
                "id": p.get("id"),
                "error": str(exc)[:200],
            })
    return out
