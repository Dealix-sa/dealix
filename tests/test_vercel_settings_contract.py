from __future__ import annotations

from core.config.settings import Settings


def test_vercel_production_env_sets_dealix_production() -> None:
    settings = Settings(
        VERCEL_ENV="production",
        VERCEL_GIT_COMMIT_SHA="abc123vercelsha",
    )

    assert settings.app_env == "production"
    assert settings.is_production is True
    assert settings.git_sha == "abc123vercelsha"


def test_vercel_preview_env_maps_to_staging() -> None:
    settings = Settings(VERCEL_ENV="preview")

    assert settings.app_env == "staging"
    assert settings.is_production is False


def test_explicit_app_env_wins_over_vercel_env() -> None:
    settings = Settings(
        APP_ENV="test",
        VERCEL_ENV="production",
        GIT_SHA="localsha",
        VERCEL_GIT_COMMIT_SHA="vercelsha",
    )

    assert settings.app_env == "test"
    assert settings.git_sha == "localsha"
