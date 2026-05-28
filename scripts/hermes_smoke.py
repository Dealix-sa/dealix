"""Hermes smoke check — verifies provider routing + governance gate end-to-end.

Run after a key rotation or a config change:

    python scripts/hermes_smoke.py
    python scripts/hermes_smoke.py --provider direct_deepseek

The smoke does NOT make a network call by default — it exercises the
orchestrator dispatch pipeline (gate + router + audit + friction bridge)
with a built-in offline executor. Pass --live to additionally make a single
chat completion call against the active provider; --live requires either
OPENROUTER_API_KEY or DEEPSEEK_API_KEY in the environment.

Exit codes:
  0 — smoke passed
  1 — smoke failed
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from dealix.hermes import HermesOrchestrator, HermesTask  # noqa: E402
from dealix.hermes.agents import route_to_agent_executor  # noqa: E402
from dealix.llm.engine import (  # noqa: E402
    PROVIDER_BASE_URLS,
    PROVIDER_ENV_KEYS,
    active_provider,
)


def _run_offline_phase(provider_override: str | None) -> dict[str, Any]:
    if provider_override:
        os.environ["HERMES_PROVIDER"] = provider_override

    orch = HermesOrchestrator(executor=route_to_agent_executor)

    cases = [
        ("approved engineering", "refactor the FastAPI router for /leads", "approved"),
        ("approved delivery", "run source passport for customer ACME", "approved"),
        ("refusal cold whatsapp", "send cold whatsapp blast to warm list", "rejected"),
        ("refusal scraping", "scrape saudi yellow pages for emails", "rejected"),
        ("needs approval email", "send email to confirmed lead", "needs_approval"),
    ]

    results: list[dict[str, Any]] = []
    failures: list[str] = []
    for label, intent, expected in cases:
        out = orch.dispatch(HermesTask(intent=intent, customer_id="smoke_001"))
        got = out.decision.decision
        ok = got == expected
        results.append(
            {
                "case": label,
                "expected": expected,
                "got": got,
                "ok": ok,
                "run_id": out.run_id,
            }
        )
        if not ok:
            failures.append(f"{label}: expected={expected} got={got}")
    return {"results": results, "failures": failures}


def _run_live_phase() -> dict[str, Any]:
    """Optional: a single chat completion against the active provider."""
    provider = active_provider()
    env_key = PROVIDER_ENV_KEYS[provider]
    base_url = PROVIDER_BASE_URLS[provider]
    api_key = os.getenv(env_key)
    if not api_key:
        return {
            "skipped": True,
            "reason": f"{env_key} not set; cannot run live check.",
            "provider": provider,
        }
    try:
        from openai import OpenAI  # type: ignore[import-not-found]
    except ImportError:
        return {
            "skipped": True,
            "reason": "openai SDK not installed; pip install openai",
            "provider": provider,
        }
    try:
        client = OpenAI(api_key=api_key, base_url=base_url)
        model = (
            "deepseek-chat" if provider == "direct_deepseek" else "deepseek/deepseek-chat"
        )
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Reply with the word OK."}],
            max_tokens=5,
        )
        text = resp.choices[0].message.content or ""
        return {
            "provider": provider,
            "base_url": base_url,
            "model": model,
            "reply_excerpt": text[:50],
            "ok": True,
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "provider": provider,
            "ok": False,
            "error": str(exc)[:300],
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--provider",
        choices=["openrouter", "direct_deepseek"],
        help="Override HERMES_PROVIDER for this smoke run.",
    )
    parser.add_argument(
        "--live", action="store_true", help="Additionally make one chat completion call."
    )
    args = parser.parse_args()

    offline = _run_offline_phase(args.provider)
    live: dict[str, Any] | None = _run_live_phase() if args.live else None

    report: dict[str, Any] = {
        "provider_resolved": active_provider(),
        "offline": offline,
    }
    if live is not None:
        report["live"] = live

    print(json.dumps(report, ensure_ascii=False, indent=2))

    if offline["failures"]:
        return 1
    if live is not None and not live.get("ok") and not live.get("skipped"):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
