from __future__ import annotations

import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_defusedxml_is_declared_in_vercel_runtime_dependencies() -> None:
    """Vercel installs FastAPI dependencies from pyproject.toml."""
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    dependencies = [item.lower() for item in project["project"]["dependencies"]]
    assert any(item.startswith("defusedxml") for item in dependencies)


def test_defusedxml_dependency_contract_matches_requirements_file() -> None:
    """Keep local/CI and Vercel dependency manifests aligned."""
    requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8").lower().splitlines()
    assert any(line.strip().startswith("defusedxml") for line in requirements)


def test_pytest_plugins_are_development_dependencies_only() -> None:
    runtime = (ROOT / "requirements.txt").read_text(encoding="utf-8").lower().splitlines()
    development = (
        (ROOT / "requirements-dev.txt").read_text(encoding="utf-8").lower().splitlines()
    )

    assert not any(line.strip().startswith("pytest") for line in runtime)
    assert any(line.strip().startswith("pytest-timeout") for line in development)
    assert any(line.strip().startswith("pytest-xdist") for line in development)
