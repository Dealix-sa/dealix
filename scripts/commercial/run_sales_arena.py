#!/usr/bin/env python3
"""Run the live-model Dealix Sales Arena and print its proof report."""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from core.llm.inference import NoLLMProviderConfigured
from dealix.commercial.sales_arena import run_sales_arena


async def _run() -> int:
    try:
        report = await run_sales_arena()
    except NoLLMProviderConfigured:
        print("blocked: no_llm_provider_configured")
        return 2
    except TimeoutError:
        print("blocked: llm_timeout")
        return 2
    except Exception as exc:
        print(f"blocked: sales_arena_unavailable:{type(exc).__name__}")
        return 2

    print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
    return 0 if report.success else 1


def main() -> int:
    return asyncio.run(_run())


if __name__ == "__main__":
    raise SystemExit(main())
