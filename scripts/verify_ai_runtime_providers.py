#!/usr/bin/env python3
"""
Verify Dealix AI runtime provider configuration (no secrets printed).

Usage:
  python3 scripts/verify_ai_runtime_providers.py
  python3 scripts/verify_ai_runtime_providers.py --ping   # optional live chat ping (costs $)
"""
from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.config.settings import get_settings
from core.llm.runtime_router import get_runtime_router, reset_runtime_router


def main() -> int:
    parser = argparse.ArgumentParser(description="Dealix AI runtime provider check")
    parser.add_argument(
        "--ping",
        action="store_true",
        help="Send a minimal chat to primary (and fallback if needed)",
    )
    args = parser.parse_args()

    get_settings.cache_clear()
    reset_runtime_router()
    import core.llm.router as router_mod

    router_mod._router_instance = None

    runtime = get_runtime_router()
    status = runtime.status()
    print("DEALIX_AI_RUNTIME_STATUS=" + str(status))

    chain = status["provider_chain"]
    ready = status.get("router_ready", {})
    if not any(ready.get(p, False) for p in chain):
        print("DEALIX_AI_RUNTIME_VERDICT=FAIL (no providers ready in chain)")
        return 1

    if not args.ping:
        print("DEALIX_AI_RUNTIME_VERDICT=PASS (config only; use --ping for live call)")
        return 0

    async def _ping() -> None:
        response = await runtime.chat(
            "Reply with exactly: DEALIX_OK",
            system="You are a health-check bot. One short line only.",
            max_tokens=32,
            temperature=0.0,
        )
        print(f"DEALIX_AI_RUNTIME_PING_PROVIDER={response.provider}")
        print(f"DEALIX_AI_RUNTIME_PING_MODEL={response.model}")
        print(f"DEALIX_AI_RUNTIME_PING_CONTENT={response.content[:200]!r}")

    try:
        asyncio.run(_ping())
    except Exception as exc:
        print(f"DEALIX_AI_RUNTIME_VERDICT=FAIL (ping error: {exc})")
        return 1

    print("DEALIX_AI_RUNTIME_VERDICT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
