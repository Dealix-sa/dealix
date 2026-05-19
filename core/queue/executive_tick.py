"""Scheduled executive orchestrator tick.

Run with::

    python -m core.queue.executive_tick

No-op (prints a skip line, exits 0) when the feature flag is off. On a
live run it executes one tick, best-effort spawns internal jobs, prints
the result as JSON, and exits 0 on success / 1 on failure. The tick
itself queues and prepares — it never sends and never charges.
"""

from __future__ import annotations

import asyncio
import json
import sys


def _enabled() -> bool:
    from core.config.settings import get_settings

    return bool(get_settings().executive_orchestrator_enabled)


async def _amain() -> int:
    if not _enabled():
        print(json.dumps({"ok": True, "skipped": "flag_off"}))
        return 0

    from auto_client_acquisition.executive_os import (
        run_executive_tick,
        spawn_internal_jobs,
    )

    result = run_executive_tick(dry_run=False)
    spawned: list[dict] = []
    if result.ok and result.intended_jobs:
        spawned = await spawn_internal_jobs(result.intended_jobs)
    out = result.to_dict()
    out["spawned_jobs_result"] = spawned
    print(json.dumps(out, ensure_ascii=False))
    return 0 if result.ok else 1


def main() -> int:
    return asyncio.run(_amain())


if __name__ == "__main__":
    sys.exit(main())
