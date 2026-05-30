"""Contract: the Founder-OS worker stays inside the 11 non-negotiables.

The worker (scripts/founder_os_worker.py) runs as a persistent Railway service.
It must only invoke read-only diagnostics and must never enable a live send /
charge / external outreach. These tests are the CI guard for that promise.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
WORKER_PATH = REPO_ROOT / "scripts" / "founder_os_worker.py"


def _load_worker():
    spec = importlib.util.spec_from_file_location("founder_os_worker", WORKER_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def worker():
    return _load_worker()


def test_worker_module_exists() -> None:
    assert WORKER_PATH.exists(), "scripts/founder_os_worker.py must exist"


def test_subprocess_env_forces_hard_gates_off(worker) -> None:
    env = worker.subprocess_env()
    assert env["AUTO_SEND_ENABLED"] == "false"
    assert env["EXTERNAL_OUTREACH_ENABLED"] == "false"
    assert env["AGENT_APPROVAL_MODE"] == "required"


def test_default_commands_are_read_only(worker) -> None:
    # Default cycle (no opt-in flags) must contain only the status diagnostic.
    commands = worker.build_commands()
    assert commands, "worker must run at least one diagnostic"
    flat = " ".join(token for cmd in commands for token in cmd).lower()
    for forbidden in worker.FORBIDDEN_COMMAND_TOKENS:
        assert forbidden not in flat, f"worker command must not contain {forbidden!r}"


def test_optional_digest_is_print_only(worker) -> None:
    # The only digest command the worker may ever run is print-only.
    assert "--print" in worker.DIGEST_COMMAND
    flat = " ".join(worker.DIGEST_COMMAND).lower()
    assert "--live" not in flat


def test_referenced_scripts_exist(worker) -> None:
    # Every script the worker can invoke must be present on disk.
    candidates = [
        worker.BASE_COMMANDS[0],
        worker.VERIFY_COMMAND,
        worker.DIGEST_COMMAND,
    ]
    for cmd in candidates:
        script_rel = cmd[1]
        assert (REPO_ROOT / script_rel).exists(), f"missing {script_rel}"
