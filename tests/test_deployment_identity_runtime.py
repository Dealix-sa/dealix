"""Deployment identity must match platform metadata, not stale build fallback."""

from __future__ import annotations

from pathlib import Path

import pytest

from core.config.deployment_identity import resolve_deployment_git_sha


@pytest.fixture(autouse=True)
def _clear_identity(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in ("VERCEL_GIT_COMMIT_SHA", "RAILWAY_GIT_COMMIT_SHA", "GIT_SHA"):
        monkeypatch.delenv(name, raising=False)


def test_vercel_identity_has_highest_precedence(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GIT_SHA", "stale-generic")
    monkeypatch.setenv("RAILWAY_GIT_COMMIT_SHA", "railway-current")
    monkeypatch.setenv("VERCEL_GIT_COMMIT_SHA", "vercel-current")

    assert resolve_deployment_git_sha("settings-fallback") == "vercel-current"


def test_railway_identity_beats_generic_fallback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GIT_SHA", "stale-generic")
    monkeypatch.setenv("RAILWAY_GIT_COMMIT_SHA", "railway-current")

    assert resolve_deployment_git_sha("settings-fallback") == "railway-current"


def test_generic_and_settings_fallbacks_remain_supported(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GIT_SHA", "docker-current")
    assert resolve_deployment_git_sha("settings-fallback") == "docker-current"

    monkeypatch.delenv("GIT_SHA")
    assert resolve_deployment_git_sha("settings-fallback") == "settings-fallback"
    assert resolve_deployment_git_sha("") == "unknown"


def test_public_trust_surfaces_use_runtime_identity_resolver() -> None:
    root = Path(__file__).resolve().parents[1]
    for relative in ("api/routers/health.py", "api/routers/platform_meta.py"):
        source = (root / relative).read_text(encoding="utf-8")
        assert "resolve_deployment_git_sha" in source
        assert '"git_sha": settings.git_sha' not in source
        assert "git_sha=settings.git_sha" not in source
