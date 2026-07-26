"""The production secret guard must keep refusing insecure startups.

``api.main._validate_production_secrets`` is the single thing standing between
a misconfigured deploy and a production app running on placeholder keys. It has
been under pressure before: when a deployment fails to boot, weakening this
check is the fastest way to make the error go away, and the wrong one.

These tests pin each rejection case so that removing or loosening one is a
visible test failure rather than a quiet edit. They also pin the escape hatch —
non-production environments are intentionally exempt — so nobody has to guess
whether that behaviour is deliberate.

Secrets here are obvious placeholders; no real credential appears.
"""

from __future__ import annotations

import pytest

from api.main import _validate_production_secrets

STRONG_SECRET = "a" * 64
STRONG_JWT = "b" * 64


class _FakeSecret:
    """Stands in for pydantic's SecretStr."""

    def __init__(self, value: str) -> None:
        self._value = value

    def get_secret_value(self) -> str:
        return self._value


class _FakeSettings:
    def __init__(
        self,
        *,
        is_production: bool = True,
        app_secret_key: str = STRONG_SECRET,
        jwt_secret_key: str = STRONG_JWT,
    ) -> None:
        self.is_production = is_production
        self.app_secret_key = _FakeSecret(app_secret_key)
        self.jwt_secret_key = _FakeSecret(jwt_secret_key)


@pytest.fixture
def valid_env(monkeypatch):
    monkeypatch.setenv("API_KEYS", "placeholder-api-key")
    monkeypatch.setenv("ADMIN_API_KEYS", "placeholder-admin-key")


def test_accepts_strong_production_config(valid_env):
    _validate_production_secrets(_FakeSettings())


def test_skips_validation_outside_production(monkeypatch):
    """Non-production is exempt by design — local dev must stay runnable."""
    monkeypatch.delenv("API_KEYS", raising=False)
    monkeypatch.delenv("ADMIN_API_KEYS", raising=False)

    _validate_production_secrets(
        _FakeSettings(is_production=False, app_secret_key="change-me", jwt_secret_key="change-me")
    )


@pytest.mark.parametrize(
    "placeholder", ["change-me", "CHANGE_ME_to_64_byte_hex", "", "changeme"]
)
def test_rejects_placeholder_app_secret_key(valid_env, placeholder):
    with pytest.raises(RuntimeError, match="APP_SECRET_KEY"):
        _validate_production_secrets(_FakeSettings(app_secret_key=placeholder))


def test_rejects_jwt_secret_containing_change_me(valid_env):
    with pytest.raises(RuntimeError, match="JWT_SECRET_KEY"):
        _validate_production_secrets(_FakeSettings(jwt_secret_key="change-me-" + "c" * 40))


def test_rejects_short_jwt_secret(valid_env):
    """Length floor is 32; 31 characters must still be refused."""
    with pytest.raises(RuntimeError, match="JWT_SECRET_KEY"):
        _validate_production_secrets(_FakeSettings(jwt_secret_key="d" * 31))


@pytest.mark.parametrize("blank", ["", "   "])
def test_rejects_empty_api_keys(monkeypatch, blank):
    monkeypatch.setenv("API_KEYS", blank)
    monkeypatch.setenv("ADMIN_API_KEYS", "placeholder-admin-key")

    with pytest.raises(RuntimeError, match="API_KEYS"):
        _validate_production_secrets(_FakeSettings())


@pytest.mark.parametrize("blank", ["", "   "])
def test_rejects_empty_admin_api_keys(monkeypatch, blank):
    monkeypatch.setenv("API_KEYS", "placeholder-api-key")
    monkeypatch.setenv("ADMIN_API_KEYS", blank)

    with pytest.raises(RuntimeError, match="ADMIN_API_KEYS"):
        _validate_production_secrets(_FakeSettings())


def test_guard_is_still_called_during_startup():
    """The check is worthless if it stops being wired into lifespan."""
    import inspect

    from api import main

    source = inspect.getsource(main.lifespan)
    assert "_validate_production_secrets" in source, (
        "api.main.lifespan no longer calls _validate_production_secrets — "
        "production could boot on placeholder secrets."
    )
