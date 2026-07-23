"""Deployment identity precedence for health and release evidence."""

from __future__ import annotations

import pytest

from core.config.settings import Settings


@pytest.fixture(autouse=True)
def _clear_deploy_identity(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in ("VERCEL_GIT_COMMIT_SHA", "RAILWAY_GIT_COMMIT_SHA", "GIT_SHA"):
        monkeypatch.delenv(name, raising=False)


def test_vercel_commit_beats_stale_generic_git_sha(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GIT_SHA", "stale-build")
    monkeypatch.setenv("VERCEL_GIT_COMMIT_SHA", "vercel-current")

    assert Settings(_env_file=None).git_sha == "vercel-current"


def test_railway_commit_beats_stale_generic_git_sha(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GIT_SHA", "stale-build")
    monkeypatch.setenv("RAILWAY_GIT_COMMIT_SHA", "railway-current")

    assert Settings(_env_file=None).git_sha == "railway-current"


def test_generic_git_sha_remains_the_build_fallback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GIT_SHA", "docker-build")

    assert Settings(_env_file=None).git_sha == "docker-build"
