#!/usr/bin/env python3
"""Dealix Founder-OS worker — persistent, doctrine-safe heartbeat.

Runs as a long-lived Railway *worker* service (no public domain). Each cycle
runs **read-only** founder diagnostics and emits one structured JSON log line,
then sleeps ``FOUNDER_OS_INTERVAL_SECONDS`` (default 900s / 15min).

Hard doctrine guarantees (the 11 non-negotiables):
  * Never sends anything externally and never charges. Every subprocess is run
    with ``AUTO_SEND_ENABLED=false`` and ``EXTERNAL_OUTREACH_ENABLED=false``
    forced into its environment, and ``AGENT_APPROVAL_MODE=required``.
  * Only invokes read-only diagnostics. The optional digest is run with
    ``--print`` so it renders to stdout and never sends email.
  * Missing scripts are skipped (logged), never crash the loop.

Usage:
    python scripts/founder_os_worker.py            # loop forever (Railway worker)
    python scripts/founder_os_worker.py --once     # run a single cycle and exit
    FOUNDER_OS_INTERVAL_SECONDS=0 python scripts/founder_os_worker.py  # one cycle

Environment:
    FOUNDER_OS_INTERVAL_SECONDS   sleep between cycles, seconds (default 900).
                                  0 (or --once) runs exactly one cycle and exits.
    FOUNDER_OS_RUN_VERIFY=1       also run verify_reference_library_70.py.
    FOUNDER_OS_RUN_DIGEST=1       also run dealix_morning_digest.py --print
                                  (print-only; never sends).
    FOUNDER_OS_COMMAND_TIMEOUT    per-command timeout, seconds (default 240).
    AGENT_APPROVAL_MODE           surfaced in logs (default "required").

Designed to pair with scripts/watchdog_drift_check.py (Railway cron).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# The optional digest is print-only (`--print` renders to stdout, never sends).
DIGEST_COMMAND = [sys.executable, "scripts/dealix_morning_digest.py", "--print"]

# Read-only diagnostics that are always safe to run. Order matters only for logs.
BASE_COMMANDS: list[list[str]] = [
    [sys.executable, "scripts/dealix_status.py", "--json"],
]
VERIFY_COMMAND = [sys.executable, "scripts/verify_reference_library_70.py"]

# Tokens that, if they appeared in a command, would signal a live external
# action. The worker must never invoke any of these — asserted by
# tests/test_founder_os_worker_safe.py.
FORBIDDEN_COMMAND_TOKENS = (
    "send",
    "outreach",
    "whatsapp",
    "charge",
    "invoice_pay",
    "blast",
    "--live",
)


def _truthy(name: str, default: str = "0") -> bool:
    return os.getenv(name, default).strip().lower() in ("1", "true", "yes", "on")


def interval_seconds() -> int:
    try:
        return max(0, int(os.getenv("FOUNDER_OS_INTERVAL_SECONDS", "900")))
    except ValueError:
        return 900


def command_timeout() -> int:
    try:
        return max(1, int(os.getenv("FOUNDER_OS_COMMAND_TIMEOUT", "240")))
    except ValueError:
        return 240


def build_commands() -> list[list[str]]:
    """Return the read-only commands for one cycle, honoring opt-in env flags."""
    commands = [list(cmd) for cmd in BASE_COMMANDS]
    if _truthy("FOUNDER_OS_RUN_VERIFY"):
        commands.append(list(VERIFY_COMMAND))
    if _truthy("FOUNDER_OS_RUN_DIGEST"):
        # Always print-only — the worker never sends email.
        commands.append(list(DIGEST_COMMAND))
    return commands


def subprocess_env() -> dict[str, str]:
    """Environment forced onto every subprocess — doctrine-safe, no live actions."""
    return {
        **os.environ,
        "PYTHONUTF8": "1",
        "PYTHONIOENCODING": "utf-8",
        # Hard gates: never flip these on from the worker.
        "AUTO_SEND_ENABLED": "false",
        "EXTERNAL_OUTREACH_ENABLED": "false",
        "AGENT_APPROVAL_MODE": os.getenv("AGENT_APPROVAL_MODE", "required").lower(),
    }


def run_command(cmd: list[str], env: dict[str, str], timeout: int) -> dict[str, object]:
    started = time.time()
    script_rel = cmd[1] if len(cmd) > 1 else cmd[0]
    script_path = REPO_ROOT / script_rel
    if not script_path.exists():
        return {"cmd": cmd, "skipped": "file_not_found"}
    try:
        proc = subprocess.run(  # noqa: S603 - fixed, repo-local diagnostics only
            cmd,
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            timeout=timeout,
            env=env,
        )
        return {
            "cmd": cmd,
            "returncode": proc.returncode,
            "latency_ms": round((time.time() - started) * 1000),
            "stdout_tail": proc.stdout[-2000:],
            "stderr_tail": proc.stderr[-2000:],
        }
    except subprocess.TimeoutExpired:
        return {
            "cmd": cmd,
            "error": "timeout",
            "latency_ms": round((time.time() - started) * 1000),
        }
    except Exception as exc:  # pragma: no cover - defensive; loop must survive
        return {
            "cmd": cmd,
            "error": repr(exc),
            "latency_ms": round((time.time() - started) * 1000),
        }


def run_cycle() -> dict[str, object]:
    env = subprocess_env()
    timeout = command_timeout()
    return {
        "service": "founder-os-worker",
        "timestamp": datetime.now(UTC).isoformat(),
        "approval_mode": env["AGENT_APPROVAL_MODE"],
        "external_actions_allowed": False,
        "auto_send_enabled": env["AUTO_SEND_ENABLED"],
        "results": [run_command(cmd, env, timeout) for cmd in build_commands()],
    }


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    once = "--once" in argv or interval_seconds() == 0
    interval = interval_seconds()

    print(
        json.dumps(
            {
                "service": "founder-os-worker",
                "status": "started",
                "interval_seconds": interval,
                "once": once,
                "approval_mode": os.getenv("AGENT_APPROVAL_MODE", "required").lower(),
                "external_actions_allowed": False,
            },
            ensure_ascii=False,
        ),
        flush=True,
    )

    while True:
        print(json.dumps(run_cycle(), ensure_ascii=False, indent=2), flush=True)
        if once:
            return 0
        time.sleep(interval)


if __name__ == "__main__":
    raise SystemExit(main())
