#!/usr/bin/env python3
"""Dealix Founder OS / Railway worker — persistent doctrine-safe heartbeat.

A long-running loop for a Railway **worker** service. Each cycle runs
**read-only** diagnostics and emits one structured JSON log line, then sleeps.

Philosophy:
- Default cycle: run dealix_status.py (cheap, read-only, exit 0 always).
- Opt-in extras via env flags (off by default): verify ref lib, morning digest (print-only).
- Hard-forces doctrine env in every subprocess: AUTO_SEND_ENABLED=false,
  EXTERNAL_OUTREACH_ENABLED=false, AGENT_APPROVAL_MODE=required.
- Never imports/sends. Logs external_actions_allowed: false. Gracefully skips
  missing referenced scripts rather than crashing.

Exit code: 0 (process should restart on failure; Railway handles that).

Usage:
    FOUNDER_OS_INTERVAL_SECONDS=900 python scripts/founder_os_worker.py
    FOUNDER_OS_INTERVAL_SECONDS=0 python scripts/founder_os_worker.py  # one cycle, exit

Environment Variables:
  FOUNDER_OS_INTERVAL_SECONDS  Seconds between cycles. Default 900 (15 min).
  FOUNDER_OS_RUN_VERIFY        1 = run verify_reference_library_70.py each cycle.
  FOUNDER_OS_RUN_DIGEST        1 = run dealix_morning_digest.py --print each cycle.
  APP_ENV, ENVIRONMENT, DATABASE_URL, etc. — forwarded from container.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTERVAL_SECONDS = int(os.getenv("FOUNDER_OS_INTERVAL_SECONDS", "900"))
RUN_VERIFY = os.getenv("FOUNDER_OS_RUN_VERIFY", "").lower() in ("1", "true")
RUN_DIGEST = os.getenv("FOUNDER_OS_RUN_DIGEST", "").lower() in ("1", "true")

# Core commands: always run (if exist)
CORE_COMMANDS = [
    [sys.executable, "scripts/dealix_status.py"],
]

# Optional extras (off by default, cheaper)
OPTIONAL_COMMANDS = []
if RUN_VERIFY:
    OPTIONAL_COMMANDS.append([sys.executable, "scripts/verify_reference_library_70.py"])
if RUN_DIGEST:
    OPTIONAL_COMMANDS.append(
        [sys.executable, "scripts/dealix_morning_digest.py", "--print"]
    )

APPROVAL_MODE = os.getenv("AGENT_APPROVAL_MODE", "required").lower()


def run_command(cmd: list[str]) -> dict[str, object]:
    """Run a command with doctrine-enforced env + timeout.

    Returns metadata dict, never raises.
    """
    started = time.time()
    script_path = ROOT / cmd[1]

    # Graceful skip if file doesn't exist
    if not script_path.exists():
        return {
            "cmd": cmd,
            "skipped": True,
            "reason": "file_not_found",
            "path": str(script_path),
        }

    try:
        # Build env: inherit parent, override doctrine flags to guarantee safety
        env = os.environ.copy()
        env.update(
            {
                "AUTO_SEND_ENABLED": "false",
                "EXTERNAL_OUTREACH_ENABLED": "false",
                "AGENT_APPROVAL_MODE": APPROVAL_MODE,
            }
        )

        proc = subprocess.run(
            cmd,
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=240,
            env=env,
        )

        return {
            "cmd": cmd,
            "returncode": proc.returncode,
            "latency_ms": round((time.time() - started) * 1000),
            # Tail to avoid bloat
            "stdout_lines": (proc.stdout or "").split("\n")[-20:],
            "stderr_lines": (proc.stderr or "").split("\n")[-10:],
        }

    except subprocess.TimeoutExpired:
        return {
            "cmd": cmd,
            "timeout": True,
            "timeout_seconds": 240,
            "latency_ms": round((time.time() - started) * 1000),
        }
    except Exception as exc:
        return {
            "cmd": cmd,
            "error": repr(exc),
            "latency_ms": round((time.time() - started) * 1000),
        }


def founder_cycle() -> dict[str, object]:
    """Run one cycle: core + optional commands, return metadata."""
    results = []
    for cmd in CORE_COMMANDS + OPTIONAL_COMMANDS:
        results.append(run_command(cmd))

    return {
        "service": "founder-os-worker",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "cycle": {
            "approval_mode": APPROVAL_MODE,
            "external_actions_allowed": False,  # Hard guarantee
            "auto_send_enabled": "false",
            "doctrine_enforced": True,
        },
        "results": results,
    }


def main() -> int:
    """Long-running heartbeat loop."""
    # Log startup
    print(
        json.dumps(
            {
                "service": "founder-os-worker",
                "status": "started",
                "interval_seconds": INTERVAL_SECONDS,
                "approval_mode": APPROVAL_MODE,
                "run_verify": RUN_VERIFY,
                "run_digest": RUN_DIGEST,
                "external_actions_allowed": False,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
            ensure_ascii=False,
        ),
        flush=True,
    )

    # Main loop
    while True:
        cycle_result = founder_cycle()
        print(json.dumps(cycle_result, ensure_ascii=False, indent=2), flush=True)

        # Exit after one cycle if interval is 0 (smoke test mode)
        if INTERVAL_SECONDS == 0:
            return 0

        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    raise SystemExit(main())
