#!/usr/bin/env python3
"""Report which founder env vars are set — never prints secret values."""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Load .env.local if present (settings also reads it)
try:
    from dotenv import load_dotenv

    load_dotenv(ROOT / ".env")
    load_dotenv(ROOT / ".env.local", override=True)
except ImportError:
    pass

CHECKS: list[tuple[str, tuple[str, ...]]] = [
    ("llm_runtime", ("DEEPSEEK_API_KEY", "MINIMAX_API_KEY", "OPENAI_API_KEY")),
    ("admin", ("ADMIN_API_KEYS",)),
    ("posthog", ("POSTHOG_API_KEY",)),
    ("calendly", ("CALENDLY_URL", "CALENDLY_PAT", "CALENDLY_WEBHOOK_SECRET")),
    ("calendly_oauth", ("CALENDLY_OAUTH_CLIENT_ID", "CALENDLY_OAUTH_CLIENT_SECRET")),
    ("hubspot", ("HUBSPOT_ACCESS_TOKEN",)),
    ("github_optional", ("GITHUB_TOKEN",)),
]


def _set(name: str) -> bool:
    v = (os.getenv(name) or "").strip()
    if not v or v.startswith("REPLACE_ME"):
        return False
    return True


def main() -> int:
    print("FOUNDER_ENV_CONFIGURED_REPORT")
    any_fail = False
    for group, keys in CHECKS:
        status = {k: _set(k) for k in keys}
        ready = any(status.values()) if group != "calendly" else (
            status.get("CALENDLY_URL", False)
            and (status.get("CALENDLY_PAT", False) or status.get("CALENDLY_WEBHOOK_SECRET", False))
        )
        if group in {"llm_runtime", "admin"} and not ready:
            any_fail = True
        line = " ".join(f"{k}={'OK' if status[k] else 'MISSING'}" for k in keys)
        print(f"  {group}: {'PASS' if ready else 'PARTIAL'} — {line}")

    try:
        from core.config.settings import get_settings

        get_settings.cache_clear()
        s = get_settings()
        print(
            "  settings_calendly_webhook:",
            "OK" if s.calendly_webhook_secret else "MISSING",
        )
        print(
            "  settings_hubspot:",
            "OK" if s.hubspot_access_token else "MISSING",
        )
    except Exception as exc:
        print(f"  settings_check: SKIP ({exc})")

    if any_fail:
        print("FOUNDER_ENV_VERDICT=INCOMPLETE")
        return 1
    print("FOUNDER_ENV_VERDICT=OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
