"""Local conftest for `tests/api/`.

The repo-wide `async_client` fixture imports `api.main`, which in this
sandbox triggers an unrelated pyo3 panic from `cryptography` (see the
Wave 2 spec note on the pre-existing CI failure). To exercise the
Hermes router in isolation we mount it on a minimal FastAPI app and
expose an `async_hermes_client` fixture.

This is the only safe way to actually test the router end-to-end given
the current environment; if/when the upstream pyo3 issue is fixed,
swap to the global `async_client` fixture.
"""

from __future__ import annotations

import os
from collections.abc import AsyncGenerator
from pathlib import Path

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient


@pytest.fixture(autouse=True)
def _hermes_dev_admin_key(monkeypatch: pytest.MonkeyPatch) -> None:
    """Pin the admin key to a known value so tests are deterministic."""
    monkeypatch.setenv("DEALIX_ADMIN_API_KEY", "test-admin-key")


@pytest.fixture
def hermes_app(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> FastAPI:
    """A minimal FastAPI app with only the Hermes router mounted."""
    # Force persistence under tmp_path so tests are isolated.
    monkeypatch.setenv(
        "DEALIX_HERMES_APPROVAL_PATH",
        str(tmp_path / "approvals.jsonl"),
    )
    monkeypatch.setenv(
        "DEALIX_HERMES_EVIDENCE_PATH",
        str(tmp_path / "evidence.jsonl"),
    )
    from api.routers import hermes as hermes_router

    hermes_router.reset_state_for_tests(
        approval_path=tmp_path / "approvals.jsonl",
        evidence_path=tmp_path / "evidence.jsonl",
    )
    app = FastAPI()
    app.include_router(hermes_router.router)
    return app


@pytest_asyncio.fixture
async def async_hermes_client(hermes_app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=hermes_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
