from __future__ import annotations

import os
import stat
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _assert_valid_yaml(path: Path) -> str:
    text = _read(path)
    assert yaml.safe_load(text) is not None
    return text


def test_founder_commercial_daily_uses_portable_python_launcher() -> None:
    text = _assert_valid_yaml(WORKFLOWS / "founder_commercial_daily.yml")
    assert "py -3" not in text
    assert "python scripts/run_dealix_unified_founder_day.py --quick" in text


def test_production_trust_installs_async_pytest_plugin() -> None:
    text = _assert_valid_yaml(WORKFLOWS / "production_api_trust_smoke.yml")
    assert "pytest-asyncio" in text
    assert "python -m pytest" in text


def test_weekly_verify_installs_import_contract_dependencies() -> None:
    text = _assert_valid_yaml(WORKFLOWS / "founder_weekly_verify.yml")
    for dependency in (
        "pytest-asyncio",
        "pydantic",
        "pydantic-settings",
        "fastapi",
        "httpx",
    ):
        assert dependency in text
    assert "python -m pytest" in text


def test_commercial_expansion_installs_yaml_before_execution() -> None:
    text = _assert_valid_yaml(WORKFLOWS / "commercial-expand-weekly.yml")
    install = text.index("python -m pip install pyyaml")
    execute = text.index("python scripts/expand_commercial_ops_all.py")
    assert install < execute


def test_autonomous_weekly_uses_supported_quick_contract() -> None:
    workflow = _assert_valid_yaml(WORKFLOWS / "founder_autonomous_ops_weekly.yml")
    runner = _read(ROOT / "scripts" / "run_dealix_full_autonomous_ops.py")
    assert "--skip-founder-day" not in workflow
    assert "--quick" in workflow
    assert 'p.add_argument("--quick"' in runner


def test_windows_wrapper_does_not_forward_unsupported_flags() -> None:
    text = _read(ROOT / "scripts" / "run_dealix_full_autonomous_ops.ps1")
    assert '$argsList += "--skip-expand"' not in text
    assert '$argsList += "--skip-founder-day"' not in text
    assert '$argsList += "--skip-gates"' not in text
    assert '$argsList += "--quick"' in text


def test_pilot_brief_script_keeps_executable_contract() -> None:
    path = ROOT / "scripts" / "dealix_pilot_brief.py"
    mode = path.stat().st_mode
    assert os.access(path, os.X_OK)
    assert mode & stat.S_IXUSR
