"""Notion Command Center settings — mirrors test_settings_whatsapp.py."""

from __future__ import annotations

import pytest

from core.config.settings import Settings, get_settings


@pytest.fixture(autouse=True)
def _clear_settings_cache():
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


def test_notion_mock_mode_default_false(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("NOTION_MOCK_MODE", raising=False)
    s = Settings()
    assert s.notion_mock_mode is False


def test_notion_mock_mode_env_true(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NOTION_MOCK_MODE", "true")
    s = Settings()
    assert s.notion_mock_mode is True


def test_notion_api_key_parses_as_secret(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NOTION_API_KEY", "secret_value_123")
    s = Settings()
    assert s.notion_api_key is not None
    # SecretStr does not leak in repr; the value is only via get_secret_value().
    assert "secret_value_123" not in repr(s.notion_api_key)
    assert s.notion_api_key.get_secret_value() == "secret_value_123"


def test_notion_version_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("NOTION_VERSION", raising=False)
    s = Settings()
    assert s.notion_version == "2022-06-28"


def test_notion_db_ids_default_none(monkeypatch: pytest.MonkeyPatch) -> None:
    for key in (
        "NOTION_CRM_DB_ID",
        "NOTION_KPI_DB_ID",
        "NOTION_DAILY_OPS_DB_ID",
        "NOTION_PLAN_DB_ID",
        "NOTION_OUTREACH_DB_ID",
        "NOTION_OFFERS_DB_ID",
        "NOTION_PROOF_DB_ID",
    ):
        monkeypatch.delenv(key, raising=False)
    s = Settings()
    assert s.notion_crm_db_id is None
    assert s.notion_kpi_db_id is None
    assert s.notion_daily_ops_db_id is None
    assert s.notion_plan_db_id is None
    assert s.notion_outreach_db_id is None
    assert s.notion_offers_db_id is None
    assert s.notion_proof_db_id is None
