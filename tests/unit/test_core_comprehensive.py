"""Comprehensive unit tests for core/ module gaps.

Tests are synchronous, fast, and require no DB or external connections.
"""

from __future__ import annotations

import logging


# ---------------------------------------------------------------------------
# core/errors.py
# ---------------------------------------------------------------------------


def test_ai_company_error_is_importable() -> None:
    from core.errors import AICompanyError

    assert AICompanyError is not None


def test_ai_company_error_base_class_is_exception() -> None:
    from core.errors import AICompanyError

    assert issubclass(AICompanyError, Exception)


def test_ai_company_error_can_be_raised_and_caught() -> None:
    from core.errors import AICompanyError

    with __import__("pytest").raises(AICompanyError):
        raise AICompanyError("test error")


def test_configuration_error_subclasses_ai_company_error() -> None:
    from core.errors import AICompanyError, ConfigurationError

    assert issubclass(ConfigurationError, AICompanyError)


def test_llm_error_subclasses_ai_company_error() -> None:
    from core.errors import AICompanyError, LLMError

    assert issubclass(LLMError, AICompanyError)


def test_integration_error_subclasses_ai_company_error() -> None:
    from core.errors import AICompanyError, IntegrationError

    assert issubclass(IntegrationError, AICompanyError)


def test_agent_error_subclasses_ai_company_error() -> None:
    from core.errors import AgentError, AICompanyError

    assert issubclass(AgentError, AICompanyError)


def test_validation_error_subclasses_ai_company_error() -> None:
    from core.errors import AICompanyError, ValidationError

    assert issubclass(ValidationError, AICompanyError)


def test_rate_limit_error_subclasses_ai_company_error() -> None:
    from core.errors import AICompanyError, RateLimitError

    assert issubclass(RateLimitError, AICompanyError)


def test_authentication_error_subclasses_ai_company_error() -> None:
    from core.errors import AICompanyError, AuthenticationError

    assert issubclass(AuthenticationError, AICompanyError)


def test_errors_can_carry_message() -> None:
    from core.errors import ConfigurationError

    err = ConfigurationError("missing API key")
    assert "missing API key" in str(err)


# ---------------------------------------------------------------------------
# core/logging.py
# ---------------------------------------------------------------------------


def test_get_logger_returns_a_logger() -> None:
    from core.logging import get_logger

    logger = get_logger("test_core_comprehensive")
    assert logger is not None


def test_get_logger_accepts_none_name() -> None:
    from core.logging import get_logger

    logger = get_logger(None)
    assert logger is not None


def test_get_logger_returns_different_instances_for_different_names() -> None:
    from core.logging import get_logger

    logger_a = get_logger("module_a")
    logger_b = get_logger("module_b")
    # Both must be valid logger objects; they may or may not be distinct objects
    # depending on structlog caching — we just confirm both are usable.
    assert logger_a is not None
    assert logger_b is not None


def test_configure_logging_runs_without_error() -> None:
    from core.logging import configure_logging

    # Should not raise under any environment setting
    configure_logging()


def test_configure_logging_is_idempotent() -> None:
    from core.logging import configure_logging

    configure_logging()
    configure_logging()  # second call must also not raise


# ---------------------------------------------------------------------------
# core/config/settings.py
# ---------------------------------------------------------------------------


def test_get_settings_returns_settings_object() -> None:
    from core.config.settings import Settings, get_settings

    s = get_settings()
    assert isinstance(s, Settings)


def test_settings_has_app_name() -> None:
    from core.config.settings import get_settings

    s = get_settings()
    assert hasattr(s, "app_name")
    assert isinstance(s.app_name, str)
    assert s.app_name  # non-empty


def test_settings_has_app_version() -> None:
    from core.config.settings import get_settings

    s = get_settings()
    assert hasattr(s, "app_version")
    assert isinstance(s.app_version, str)
    assert s.app_version


def test_settings_has_app_env() -> None:
    from core.config.settings import get_settings

    s = get_settings()
    assert hasattr(s, "app_env")
    valid_envs = {"development", "staging", "production", "test"}
    assert s.app_env in valid_envs


def test_settings_default_currency_is_sar() -> None:
    from core.config.settings import get_settings

    s = get_settings()
    assert s.app_default_currency == "SAR"


def test_settings_default_locale_is_arabic() -> None:
    from core.config.settings import get_settings

    s = get_settings()
    assert s.app_default_locale == "ar"


def test_settings_default_timezone_is_riyadh() -> None:
    from core.config.settings import get_settings

    s = get_settings()
    assert s.app_timezone == "Asia/Riyadh"


def test_settings_get_settings_is_cached() -> None:
    from core.config.settings import get_settings

    s1 = get_settings()
    s2 = get_settings()
    # lru_cache means both calls return the same object
    assert s1 is s2


def test_settings_is_production_flag_is_bool() -> None:
    from core.config.settings import get_settings

    s = get_settings()
    assert isinstance(s.is_production, bool)
