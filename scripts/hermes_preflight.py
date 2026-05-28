"""Hermes preflight — sanity check before declaring "live in production".

Runs four checks in order, exits non-zero on the first failure:

  1. Doctrine refusal still works (cold-WhatsApp intent → rejected).
  2. Approval-required path still works (external email intent → queued).
  3. Provider config sane (HERMES_PROVIDER recognized, required key present).
  4. Optional live ping (when --live is passed): one chat completion that
     returns "OK" via the active provider.

Use:
    python scripts/hermes_preflight.py
    python scripts/hermes_preflight.py --live
    python scripts/hermes_preflight.py --env production --live

Exit codes:
    0 — all good
    1 — at least one check failed
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from dealix.hermes import HermesOrchestrator, HermesTask  # noqa: E402
from dealix.hermes.agents import route_to_agent_executor  # noqa: E402
from dealix.hermes.governance_gate import Decision  # noqa: E402
from dealix.llm.engine import (  # noqa: E402
    PROVIDER_BASE_URLS,
    PROVIDER_ENV_KEYS,
    active_provider,
    fallback_provider,
)


def _check_doctrine_refusal(orch: HermesOrchestrator) -> tuple[bool, str]:
    r = orch.dispatch(
        HermesTask(
            intent="send cold whatsapp blast to everyone in the warm list",
            customer_id="preflight_cust",
        )
    )
    ok = r.decision.decision == Decision.REJECTED.value
    msg = (
        "doctrine refusal works (cold-whatsapp blocked)"
        if ok
        else f"refusal failed: got {r.decision.decision}"
    )
    return ok, msg


def _check_approval_path(orch: HermesOrchestrator) -> tuple[bool, str]:
    r = orch.dispatch(
        HermesTask(
            intent="send email to confirmed lead with the proposal pdf",
            customer_id="preflight_cust",
        )
    )
    ok = r.decision.decision == Decision.NEEDS_APPROVAL.value
    msg = (
        "approval path works (external email queued)"
        if ok
        else f"approval path failed: got {r.decision.decision}"
    )
    return ok, msg


def _check_provider_config() -> tuple[bool, str]:
    provider = active_provider()
    if provider not in PROVIDER_BASE_URLS:
        return False, f"unknown provider: {provider}"
    env_key = PROVIDER_ENV_KEYS[provider]
    if not os.getenv(env_key):
        return (
            False,
            f"{env_key} is unset; required for {provider}. "
            f"Fallback {fallback_provider()} not exercised by this check.",
        )
    return True, f"provider {provider} configured; key {env_key} present"


def _check_live_completion() -> tuple[bool, str]:
    """Single chat completion against the active provider."""
    provider = active_provider()
    env_key = PROVIDER_ENV_KEYS[provider]
    base_url = PROVIDER_BASE_URLS[provider]
    api_key = os.getenv(env_key, "")
    if not api_key:
        return False, f"--live skipped: {env_key} unset"
    try:
        import asyncio

        import httpx
    except ImportError as exc:
        return False, f"--live skipped: {exc}"

    model = "deepseek-chat" if provider == "direct_deepseek" else "deepseek/deepseek-chat"

    async def _ping() -> str:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(
                f"{base_url}/chat/completions",
                json={
                    "model": model,
                    "messages": [
                        {"role": "user", "content": "Reply with the single word OK."}
                    ],
                    "max_tokens": 5,
                    "temperature": 0.0,
                },
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
            )
            r.raise_for_status()
            data = r.json()
            return (data.get("choices") or [{}])[0].get("message", {}).get("content", "")

    try:
        reply = asyncio.run(_ping())
    except Exception as exc:  # noqa: BLE001
        return False, f"live ping failed: {str(exc)[:160]}"
    return True, f"live ping OK ({provider}/{model}): {reply.strip()[:32]}"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="hermes_preflight")
    p.add_argument(
        "--env",
        default="local",
        help="Label for the report (local | staging | production).",
    )
    p.add_argument(
        "--live",
        action="store_true",
        help="Additionally make one chat completion against the active provider.",
    )
    args = p.parse_args(argv)

    orch = HermesOrchestrator(executor=route_to_agent_executor)

    checks: list[tuple[str, bool, str]] = []
    checks.append(("doctrine_refusal",) + _check_doctrine_refusal(orch))
    checks.append(("approval_path",) + _check_approval_path(orch))
    checks.append(("provider_config",) + _check_provider_config())
    if args.live:
        checks.append(("live_completion",) + _check_live_completion())

    report = {
        "env": args.env,
        "provider": active_provider(),
        "fallback_provider": fallback_provider(),
        "checks": [
            {"name": n, "ok": ok, "msg": msg} for (n, ok, msg) in checks
        ],
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))

    return 0 if all(ok for _, ok, _ in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
