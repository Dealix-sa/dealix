from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_full_repo_matrix_uses_safe_defaults_and_testsprite() -> None:
    script = read("scripts/ops/run_full_repo_test_matrix.sh")

    assert "EXTERNAL_SEND_ENABLED=\"${EXTERNAL_SEND_ENABLED:-false}\"" in script
    assert "WHATSAPP_ALLOW_LIVE_SEND=\"${WHATSAPP_ALLOW_LIVE_SEND:-false}\"" in script
    assert "OUTBOUND_MODE=\"${OUTBOUND_MODE:-draft_only}\"" in script
    assert "testsprite-env-check" in script
    assert "testsprite-mcp-smoke" in script


def test_full_repo_matrix_keeps_legacy_pytest_diagnostic_not_blocking() -> None:
    script = read("scripts/ops/run_full_repo_test_matrix.sh")

    assert "pytest-launch-critical-suite" in script
    assert "pytest-full-suite-diagnostic" in script
    assert "run_step \"pytest-full-suite-diagnostic\" optional" in script


def test_makefile_exposes_operator_commands() -> None:
    makefile = read("Makefile")

    assert "full-repo-test:" in makefile
    assert "security-smoke-ci:" in makefile
    assert "bash scripts/ops/run_full_repo_test_matrix.sh" in makefile


def test_dev_dependencies_include_pytest_timeout() -> None:
    pyproject = read("pyproject.toml")

    assert "pytest-timeout" in pyproject


def test_launch_safety_verifiers_exist() -> None:
    assert (ROOT / "scripts/verify_no_auto_external_send.py").is_file()
    assert (ROOT / "scripts/verify_company_launch_ready.py").is_file()
    assert (ROOT / "scripts/ops/security_smoke_ci.py").is_file()
