"""Local conftest for hermes tests: isolated ledger paths and no network deps."""

from __future__ import annotations

import os
import tempfile
from collections.abc import Iterator
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def _isolated_ledgers(tmp_path: Path) -> Iterator[None]:
    """Redirect every hermes JSONL ledger to a per-test temp directory."""
    overrides = {
        "DEALIX_HERMES_ESCALATION_PATH": str(tmp_path / "escalation.jsonl"),
        "DEALIX_HERMES_AGENT_AUDIT_PATH": str(tmp_path / "agent_audit.jsonl"),
        "DEALIX_HERMES_OUTREACH_PATH": str(tmp_path / "outreach.jsonl"),
        "DEALIX_HERMES_VERIFIED_REVENUE_PATH": str(tmp_path / "verified_revenue.jsonl"),
        "DEALIX_HERMES_SECRET": "hermes-test-secret",
    }
    previous = {k: os.environ.get(k) for k in overrides}
    os.environ.update(overrides)
    try:
        yield
    finally:
        for k, v in previous.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


@pytest.fixture
def evidence_pack_id() -> str:
    return "ep_test_0001"


@pytest.fixture(autouse=True)
def _disable_network(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    """Block accidental socket.connect — function-scoped, restored automatically so it never leaks to non-hermes tests."""
    import socket

    def _blocked(self, *args, **kwargs):  # type: ignore[no-untyped-def]
        raise RuntimeError("network disabled in hermes tests")

    monkeypatch.setattr(socket.socket, "connect", _blocked, raising=True)
    yield
