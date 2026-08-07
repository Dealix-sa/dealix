"""Regression tests for the lead-import CLI authentication contract."""

from __future__ import annotations

import pytest

from scripts import import_leads


def test_build_auth_headers_sends_both_explicit_credentials(monkeypatch):
    monkeypatch.setenv("DEALIX_API_KEY", "environment-api")
    monkeypatch.setenv("DEALIX_ADMIN_API_KEY", "environment-admin")

    headers = import_leads.build_auth_headers("explicit-api", "explicit-admin")

    assert headers == {
        "X-API-Key": "explicit-api",
        "X-Admin-API-Key": "explicit-admin",
    }


def test_build_auth_headers_uses_environment_fallbacks(monkeypatch):
    monkeypatch.setenv("DEALIX_API_KEY", "environment-api")
    monkeypatch.setenv("DEALIX_ADMIN_API_KEY", "environment-admin")

    headers = import_leads.build_auth_headers()

    assert headers == {
        "X-API-Key": "environment-api",
        "X-Admin-API-Key": "environment-admin",
    }


@pytest.mark.parametrize(
    ("api_key", "admin_key", "missing_name"),
    [
        ("", "admin", "DEALIX_API_KEY"),
        ("api", "", "DEALIX_ADMIN_API_KEY"),
        ("", "", "DEALIX_API_KEY"),
    ],
)
def test_build_auth_headers_fails_closed_when_a_credential_is_missing(
    monkeypatch,
    api_key,
    admin_key,
    missing_name,
):
    monkeypatch.delenv("DEALIX_API_KEY", raising=False)
    monkeypatch.delenv("DEALIX_ADMIN_API_KEY", raising=False)

    with pytest.raises(ValueError, match=missing_name):
        import_leads.build_auth_headers(api_key, admin_key)
