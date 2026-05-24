#!/usr/bin/env python3
"""
Verify MiniMax-first Dealix LLM configuration (never prints API keys).

Usage:
  python3 scripts/verify_minimax_dealix.py
  python3 scripts/verify_minimax_dealix.py --ping   # live chat (costs quota)
"""
from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.config.models import effective_dealix_llm_profile
from core.config.settings import get_settings
from core.llm.runtime_router import get_runtime_router, reset_runtime_router


def main() -> int:
    parser = argparse.ArgumentParser(description="MiniMax-first Dealix verify")
    parser.add_argument(
        "--ping",
        action="store_true",
        help="Send minimal chat via runtime router (incurs MiniMax quota)",
    )
    args = parser.parse_args()

    get_settings.cache_clear()
    reset_runtime_router()
    import core.llm.router as router_mod

    router_mod._router_instance = None

    settings = get_settings()
    profile = effective_dealix_llm_profile(settings)
    print(f"DEALIX_LLM_PROFILE_RESOLVED={profile}")
    print(f"AI_PRIMARY_PROVIDER={settings.ai_primary_provider}")
    print(f"AI_FALLBACK_PROVIDER={settings.ai_fallback_provider}")
    print(f"MINIMAX_MODEL={settings.minimax_model}")
    print(f"MINIMAX_CONFIGURED={settings.has_llm_provider('minimax')}")

    if not settings.has_llm_provider("minimax"):
        print("DEALIX_MINIMAX_VERDICT=FAIL (MINIMAX_API_KEY missing)")
        return 1

    key = settings.minimax_api_key.get_secret_value() if settings.minimax_api_key else ""
    if key.startswith("sk-user-"):
        print("DEALIX_MINIMAX_VERDICT=FAIL (use sk-api Token Plan key, not sk-user)")
        return 1

    runtime = get_runtime_router()
    status = runtime.status()
    print(f"RUNTIME_PRIMARY={status.get('primary_provider')}")
    print(f"TOKEN_PLAN_HINT={status.get('token_plan_hint')}")

    if settings.ai_primary_provider.lower() != "minimax" and profile != "minimax":
        print(
            "DEALIX_MINIMAX_VERDICT=WARN "
            "(MiniMax keyed but AI_PRIMARY/DEALIX_LLM_PROFILE not minimax-first)"
        )

    if not args.ping:
        print("DEALIX_MINIMAX_VERDICT=PASS (config only; use --ping for live call)")
        return 0

    async def _ping() -> None:
        response = await runtime.chat(
            "Reply with exactly: DEALIX_MINIMAX_OK",
            system="Health check. One short line only.",
            max_tokens=32,
            temperature=0.0,
        )
        print(f"DEALIX_MINIMAX_PING_PROVIDER={response.provider}")
        print(f"DEALIX_MINIMAX_PING_MODEL={response.model}")
        print(f"DEALIX_MINIMAX_PING_CONTENT={response.content[:200]!r}")

    try:
        asyncio.run(_ping())
    except Exception as exc:
        err = str(exc)
        if "insufficient_balance" in err or "1008" in err:
            print(
                "DEALIX_MINIMAX_VERDICT=FAIL "
                "(insufficient_balance — add Credits at platform.minimax.io)"
            )
        else:
            print(f"DEALIX_MINIMAX_VERDICT=FAIL (ping: {err[:300]})")
        return 1

    print("DEALIX_MINIMAX_VERDICT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
