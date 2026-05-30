#!/usr/bin/env python3
"""Dealix Founder OS / Hermes Agents worker.

A long-running Railway *worker* service (not a Cron job) that keeps the
founder operating loop warm 24/7. Each cycle runs a small set of read-only
diagnostics and prints a structured JSON heartbeat to stdout so Railway log
drains, alerting, and the founder digest can observe it.

Production-safe by construction — honors the Dealix non-negotiables:
- Never sends external outreach (AUTO_SEND_ENABLED / EXTERNAL_OUTREACH_ENABLED
  are forced to "false" for child processes).
- Never performs destructive actions; only invokes read-only status scripts.
- Approval mode is "required" by default; surfaced in every heartbeat.

Run locally:
    python scripts/founder_os_worker.py

Run on Railway (Worker service, no public domain):
    Start Command: python scripts/founder_os_worker.py
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

INTERVAL_SECONDS = int(os.getenv("FOUNDER_OS_INTERVAL_SECONDS", "900"))
APPROVAL_MODE = os.getenv("AGENT_APPROVAL_MODE", "required").lower()
COMMAND_TIMEOUT = int(os.getenv("FOUNDER_OS_COMMAND_TIMEOUT_SECONDS", "240"))

# Read-only diagnostics. Each entry is argv with cmd[1] = relative script path.
COMMANDS: list[list[str]] = [
    [sys.executable, "scripts/dealix_status.py"],
    [sys.executable, "scripts/dealix_morning_digest.py", "--print"],
    [sys.executable, "scripts/verify_reference_library_70.py"],
]


def _child_env() -> dict[str, str]:
    """Environment for child diagnostics — outreach hard-disabled."""
    return {
        **os.environ,
        "PYTHONUTF8": "1",
        "PYTHONIOENCODING": "utf-8",
        "AUTO_SEND_ENABLED": "false",
        "EXTERNAL_OUTREACH_ENABLED": "false",
        "AGENT_APPROVAL_MODE": APPROVAL_MODE,
    }


def run_command(cmd: list[str]) -> dict[str, object]:
    started = time.time()
    script_path = ROOT / cmd[1]
    if not script_path.exists():
        return {"cmd": cmd, "skipped": "file_not_found"}
    try:
        proc = subprocess.run(
            cmd,
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=COMMAND_TIMEOUT,
            env=_child_env(),
            check=False,
        )
        return {
            "cmd": cmd,
            "returncode": proc.returncode,
            "latency_ms": round((time.time() - started) * 1000),
            "stdout_tail": proc.stdout[-4000:],
            "stderr_tail": proc.stderr[-4000:],
        }
    except subprocess.TimeoutExpired:
        return {
            "cmd": cmd,
            "error": "timeout",
            "latency_ms": round((time.time() - started) * 1000),
        }
    except Exception as exc:
        return {
            "cmd": cmd,
            "error": repr(exc),
            "latency_ms": round((time.time() - started) * 1000),
        }


def founder_cycle() -> dict[str, object]:
    return {
        "service": "founder-os-worker",
        "timestamp": datetime.now(UTC).isoformat(),
        "approval_mode": APPROVAL_MODE,
        "external_actions_allowed": False,
        "auto_send_enabled": os.getenv("AUTO_SEND_ENABLED", "false"),
        "results": [run_command(cmd) for cmd in COMMANDS],
    }


def main() -> int:
    print(
        json.dumps(
            {
                "service": "founder-os-worker",
                "status": "started",
                "interval_seconds": INTERVAL_SECONDS,
                "approval_mode": APPROVAL_MODE,
                "external_actions_allowed": False,
            },
            ensure_ascii=False,
        ),
        flush=True,
    )
    while True:
        print(json.dumps(founder_cycle(), ensure_ascii=False, indent=2), flush=True)
        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    raise SystemExit(main())
