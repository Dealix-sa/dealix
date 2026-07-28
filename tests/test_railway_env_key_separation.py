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
