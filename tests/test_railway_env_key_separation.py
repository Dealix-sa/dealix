"""Regression coverage for generated Railway credential separation."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def _load_script(name: str):
    path = ROOT / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _parse_env(path: Path) -> dict[str, str]:
    return {
        key: value
        for line in path.read_text(encoding="utf-8").splitlines()
        if line and not line.startswith("#") and "=" in line
        for key, value in [line.split("=", 1)]
    }


def test_sync_keeps_service_and_admin_credentials_independent(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    sync = _load_script("sync_railway_generated_env")
    api_env = tmp_path / ".env.railway.generated"
    frontend_env = tmp_path / ".env.railway.frontend.generated"
    api_env.write_text(
        "API_KEYS=service-key\nADMIN_API_KEYS=admin-key\n",
        encoding="utf-8",
    )
    frontend_env.write_text(
        "NEXT_PUBLIC_DEALIX_ADMIN_API_KEY=admin-key\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(sync, "API_ENV", api_env)
    monkeypatch.setattr(sync, "FE_ENV", frontend_env)
    monkeypatch.setattr(sys, "argv", ["sync_railway_generated_env.py"])

    assert sync.main() == 0

    api = _parse_env(api_env)
    frontend = _parse_env(frontend_env)
    assert api["DEALIX_API_KEY"] == "service-key"
    assert api["DEALIX_ADMIN_API_KEY"] == "admin-key"
    assert api["DEALIX_API_KEY"] != api["DEALIX_ADMIN_API_KEY"]
    assert "NEXT_PUBLIC_DEALIX_ADMIN_API_KEY" not in frontend
    assert frontend["DEALIX_ADMIN_API_KEY"] == "admin-key"
    assert frontend["DEALIX_API_KEY"] == "service-key"


def test_closure_sources_never_derive_service_key_from_admin(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    apply_env = _load_script("apply_founder_closure_env")
    source = tmp_path / ".env.founder.closure.local"
    source.write_text("ADMIN_API_KEYS=admin-only\n", encoding="utf-8")
    monkeypatch.setattr(apply_env, "SOURCE_FILES", (source,))

    sources = apply_env._collect_sources()
    service = (
        sources.get("DEALIX_API_KEY")
        or sources.get("API_KEYS", "").split(",")[0].strip()
    )

    assert service == ""


def test_sync_rejects_legacy_admin_derived_service_alias(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    sync = _load_script("sync_railway_generated_env")
    api_env = tmp_path / ".env.railway.generated"
    frontend_env = tmp_path / ".env.railway.frontend.generated"
    api_env.write_text(
        "ADMIN_API_KEYS=shared-old-key\n"
        "DEALIX_ADMIN_API_KEY=shared-old-key\n"
        "DEALIX_API_KEY=shared-old-key\n",
        encoding="utf-8",
    )
    frontend_env.write_text(
        "DEALIX_ADMIN_API_KEY=shared-old-key\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(sync, "API_ENV", api_env)
    monkeypatch.setattr(sync, "FE_ENV", frontend_env)
    monkeypatch.setattr(sys, "argv", ["sync_railway_generated_env.py"])

    assert sync.main() == 1

    api = _parse_env(api_env)
    assert "API_KEYS" not in api
    assert "DEALIX_API_KEY" not in api


def test_sync_rejects_overlap_in_any_rotated_key(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    sync = _load_script("sync_railway_generated_env")
    api_env = tmp_path / ".env.railway.generated"
    frontend_env = tmp_path / ".env.railway.frontend.generated"
    api_env.write_text(
        "API_KEYS=service-key,shared-key\n"
        "ADMIN_API_KEYS=admin-key,shared-key\n",
        encoding="utf-8",
    )
    frontend_env.write_text("DEALIX_ADMIN_API_KEY=admin-key\n", encoding="utf-8")
    monkeypatch.setattr(sync, "API_ENV", api_env)
    monkeypatch.setattr(sync, "FE_ENV", frontend_env)
    monkeypatch.setattr(sys, "argv", ["sync_railway_generated_env.py"])

    assert sync.main() == 1


def test_closure_preserves_full_rotated_key_lists(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    apply_env = _load_script("apply_founder_closure_env")
    source = tmp_path / ".env.founder.closure.local"
    source.write_text(
        "API_KEYS=service-one,service-two\n"
        "ADMIN_API_KEYS=admin-one,admin-two\n",
        encoding="utf-8",
    )
    target_api = tmp_path / ".env.railway.generated"
    target_fe = tmp_path / ".env.railway.frontend.generated"
    monkeypatch.setattr(apply_env, "SOURCE_FILES", (source,))
    monkeypatch.setattr(apply_env, "TARGET_API", target_api)
    monkeypatch.setattr(apply_env, "TARGET_FE", target_fe)

    sources = apply_env._collect_sources()
    api_updates = {key: sources[key] for key in ("API_KEYS", "ADMIN_API_KEYS")}
    apply_env._write_merged(target_api, api_updates)

    parsed = _parse_env(target_api)
    assert parsed["API_KEYS"] == "service-one,service-two"
    assert parsed["ADMIN_API_KEYS"] == "admin-one,admin-two"


def test_validator_rejects_credential_overlap_and_missing_frontend_key(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    validate = _load_script("validate_railway_generated_env")
    api_env = tmp_path / ".env.railway.generated"
    frontend_env = tmp_path / ".env.railway.frontend.generated"
    api_env.write_text(
        "\n".join(
            f"{key}=value-{key}"
            for key in validate.REQUIRED_API
        )
        + "\nCALENDLY_WEBHOOK_SECRET=cal-secret\n"
        + "API_KEYS=service-key,shared-key\n"
        + "DEALIX_API_KEY=service-key\n"
        + "ADMIN_API_KEYS=admin-key,shared-key\n",
        encoding="utf-8",
    )
    frontend_env.write_text(
        "\n".join(
            f"{key}=value-{key}"
            for key in validate.REQUIRED_FE
            if key != "DEALIX_API_KEY"
        )
        + "\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(validate, "ROOT", tmp_path)
    monkeypatch.setattr(sys, "argv", ["validate_railway_generated_env.py", "--from-railway-env"])

    assert validate.main() == 1


def test_validator_rejects_stale_service_alias_after_rotation() -> None:
    validate = _load_script("validate_railway_generated_env")
    api = {
        "API_KEYS": "service-new,service-next",
        "ADMIN_API_KEYS": "admin-new,admin-next",
        "DEALIX_API_KEY": "service-old",
        "DEALIX_ADMIN_API_KEY": "admin-new",
    }
    frontend = {
        "DEALIX_API_KEY": "service-old",
        "DEALIX_ADMIN_API_KEY": "admin-new",
    }

    issues = validate._alias_membership_issues(api, frontend)

    assert "api: DEALIX_API_KEY is not in API_KEYS" in issues
    assert "frontend: DEALIX_API_KEY is not in API_KEYS" in issues


def test_ops_proxy_forwards_both_server_side_credentials() -> None:
    proxy = (
        ROOT
        / "frontend"
        / "src"
        / "app"
        / "api"
        / "dealix-proxy"
        / "[...path]"
        / "route.ts"
    ).read_text(encoding="utf-8")

    assert 'process.env.DEALIX_API_KEY || ""' in proxy
    assert '"X-API-Key": SERVICE_KEY' in proxy
    assert '"X-Admin-API-Key": ADMIN_KEY' in proxy


def test_validator_rejects_a_missing_backend_admin_alias() -> None:
    """An absent alias must fail, not skip the check.

    Backend admin guards read DEALIX_ADMIN_API_KEY directly and return
    early when it is empty (api/routers/weekly_reports.py:_require_admin,
    customer_health_scoring.py, commercial.py). An environment that omits
    the alias therefore has no admin boundary on those routers at all, so
    reporting OK for it would be fail-open validation.
    """
    validate = _load_script("validate_railway_generated_env")
    api = {
        "API_KEYS": "service-key",
        "ADMIN_API_KEYS": "admin-key",
        "DEALIX_API_KEY": "service-key",
        # DEALIX_ADMIN_API_KEY deliberately absent
    }
    frontend = {
        "DEALIX_API_KEY": "service-key",
        "DEALIX_ADMIN_API_KEY": "admin-key",
    }

    issues = validate._alias_membership_issues(api, frontend)

    assert "api: DEALIX_ADMIN_API_KEY is missing" in issues


def test_validator_requires_the_backend_admin_alias_to_be_present() -> None:
    """The alias must also be a declared requirement of the backend file."""
    validate = _load_script("validate_railway_generated_env")
    assert "DEALIX_ADMIN_API_KEY" in validate.REQUIRED_API


def test_validator_rejects_a_missing_service_alias() -> None:
    validate = _load_script("validate_railway_generated_env")
    api = {
        "API_KEYS": "service-key",
        "ADMIN_API_KEYS": "admin-key",
        "DEALIX_ADMIN_API_KEY": "admin-key",
    }
    frontend = {
        "DEALIX_API_KEY": "service-key",
        "DEALIX_ADMIN_API_KEY": "admin-key",
    }

    issues = validate._alias_membership_issues(api, frontend)

    assert "api: DEALIX_API_KEY is missing" in issues
