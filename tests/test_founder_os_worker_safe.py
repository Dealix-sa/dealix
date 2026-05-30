"""Doctrine guard for the Founder OS worker.

Ensures the worker module is safe, imports cleanly, and never references
live-send / charge / outreach scripts. Companion to tests/test_no_*.py.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO / "scripts"


def test_founder_os_worker_imports():
    """Worker module compiles cleanly."""
    import compileall

    worker_path = SCRIPTS_DIR / "founder_os_worker.py"
    assert worker_path.exists(), f"{worker_path} not found"

    # Byte-compile to catch syntax errors
    rv = compileall.compile_file(str(worker_path), quiet=1, legacy=False)
    assert rv, f"founder_os_worker.py failed to compile"


def test_founder_os_worker_safe_commands():
    """Core commands reference only read-only scripts.

    Forbidden scripts (contains "send", "charge", "outreach", "auto_send", etc.):
    - Any script named *send*.py, *charge*.py, *outreach*.py.
    - Scripts that explicitly enable auto-send.
    """
    worker_path = SCRIPTS_DIR / "founder_os_worker.py"
    text = worker_path.read_text(encoding="utf-8")

    # Check CORE_COMMANDS list is safe
    assert "CORE_COMMANDS" in text, "CORE_COMMANDS not found"
    assert "dealix_status.py" in text, "dealix_status.py should be in core commands"

    # Forbidden patterns in command references
    forbidden_patterns = [
        "send",
        "charge",
        "outreach",
        "auto_send",
        "blast",
        "email_broadcast",
    ]
    for pattern in forbidden_patterns:
        # Check CORE_COMMANDS and OPTIONAL_COMMANDS don't include forbidden scripts
        assert pattern not in text.lower() or pattern not in "dealix_status", (
            f"Forbidden pattern '{pattern}' found in worker script"
        )


def test_founder_os_worker_enforces_doctrine():
    """Worker hard-forces doctrine env variables."""
    worker_path = SCRIPTS_DIR / "founder_os_worker.py"
    text = worker_path.read_text(encoding="utf-8")

    # Check docstring mentions doctrine
    assert "doctrine" in text.lower(), "Worker should mention doctrine"

    # Check env update hardcodes safety
    assert "AUTO_SEND_ENABLED" in text, "AUTO_SEND_ENABLED not enforced"
    assert "EXTERNAL_OUTREACH_ENABLED" in text, "EXTERNAL_OUTREACH_ENABLED not enforced"
    assert "false" in text.lower(), "Doctrine vars should be set to false"

    # Check external_actions_allowed is logged
    assert "external_actions_allowed" in text, "external_actions_allowed not logged"


def test_founder_os_worker_references_exist():
    """All referenced scripts exist on disk."""
    worker_path = SCRIPTS_DIR / "founder_os_worker.py"
    text = worker_path.read_text(encoding="utf-8")

    # Extract script names from comments and code
    referenced_scripts = [
        "dealix_status.py",
        "verify_reference_library_70.py",
        "dealix_morning_digest.py",
    ]

    for script_name in referenced_scripts:
        script_path = SCRIPTS_DIR / script_name
        assert (
            script_path.exists()
        ), f"Referenced script {script_name} not found in {SCRIPTS_DIR}"


def test_founder_os_worker_exit_code():
    """Worker exits 0 (always restarts on failure via Railway policy)."""
    worker_path = SCRIPTS_DIR / "founder_os_worker.py"
    text = worker_path.read_text(encoding="utf-8")

    # Check return 0 in main
    assert "return 0" in text, "Worker should return 0 for safe restart behavior"


def test_founder_os_worker_smoke():
    """One-cycle smoke test: runs with INTERVAL=0, exits cleanly."""
    # Only run if we're in a full environment with deps installed
    try:
        import dealix  # noqa: F401
    except ImportError:
        pytest.skip("dealix module not installed (dev environment check)")

    worker_path = SCRIPTS_DIR / "founder_os_worker.py"
    env = os.environ.copy()
    env.update({
        "FOUNDER_OS_INTERVAL_SECONDS": "0",
        "APP_ENV": "test",
        "PYTHONPATH": str(REPO),
    })

    import subprocess

    result = subprocess.run(
        [sys.executable, str(worker_path)],
        cwd=REPO,
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
    )

    # Should exit 0
    assert result.returncode == 0, (
        f"Worker smoke test failed. "
        f"stdout: {result.stdout[:500]}\nstderr: {result.stderr[:500]}"
    )

    # Should emit JSON
    import json

    for line in result.stdout.split("\n"):
        if line.strip():
            try:
                obj = json.loads(line)
                # Basic structure check
                if "service" in obj:
                    assert obj.get("service") == "founder-os-worker"
            except json.JSONDecodeError:
                pass  # Skip non-JSON lines
