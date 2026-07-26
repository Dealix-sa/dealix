"""Scope regression guard for the required ``security-smoke`` CI gate.

The gate must fail on Dealix-authored files that contain credential-shaped
strings, and must NOT fail on vendored third-party code or gitignored runtime
output. Two scope defects previously broke that contract:

  1. Virtualenvs were excluded by name only (``.venv``/``venv``), so a venv
     created under any other name (``.venv-audit``, ``venv312``) was scanned
     and matched credential shapes inside installed dependencies.
  2. The ``reports/runtime`` exclusion never fired: it was stored as a nested
     path in a set matched against single path components, and the prefix
     branch that would have caught it had no applicable entries.

Both produced false failures in a required gate. A safety gate that goes red
for non-reasons invites being weakened, so the scope is pinned by tests here.

Credential-shaped fixtures are built by concatenation so neither this gate nor
gitleaks sees a literal prefix in this source file.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCANNER_PATH = REPO_ROOT / "scripts" / "ops" / "security_smoke_ci.py"

# AWS access-key shape, assembled at runtime.
FAKE_AWS_KEY = "AKIA" + "QRSTUVWX23456789"


@pytest.fixture(scope="module")
def scanner():
    spec = importlib.util.spec_from_file_location("security_smoke_ci", SCANNER_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_detects_secret_in_repo_authored_file(scanner, tmp_path):
    """Baseline: detection still works — this must fail for the right reason."""
    _write(tmp_path / "core" / "config.py", f'AWS_KEY = "{FAKE_AWS_KEY}"\n')

    failures, _ = scanner.scan(tmp_path)

    assert any("core/config.py" in item for item in failures), failures


def test_virtualenv_is_pruned_regardless_of_directory_name(scanner, tmp_path):
    """A venv named anything other than .venv/venv must still be excluded."""
    venv = tmp_path / ".venv-audit"
    _write(venv / "pyvenv.cfg", "home = /usr/local/bin\n")
    _write(
        venv / "lib" / "python3.11" / "site-packages" / "vendor.py",
        f'SAMPLE = "{FAKE_AWS_KEY}"\n',
    )

    failures, warnings = scanner.scan(tmp_path)

    assert failures == []
    assert warnings == []


def test_site_packages_is_pruned_without_venv_marker(scanner, tmp_path):
    """Vendored dependency trees are excluded even with no pyvenv.cfg."""
    _write(
        tmp_path / "lib" / "site-packages" / "vendor.py",
        f'SAMPLE = "{FAKE_AWS_KEY}"\n',
    )

    failures, _ = scanner.scan(tmp_path)

    assert failures == []


def test_reports_runtime_prefix_is_pruned(scanner, tmp_path):
    """Gitignored runtime output must not fail the gate."""
    _write(tmp_path / "reports" / "runtime" / "daily.md", f"token: {FAKE_AWS_KEY}\n")

    failures, _ = scanner.scan(tmp_path)

    assert failures == []


def test_reports_outside_runtime_are_still_scanned(scanner, tmp_path):
    """The prefix exclusion must not swallow the rest of reports/."""
    _write(tmp_path / "reports" / "committed.md", f"token: {FAKE_AWS_KEY}\n")

    failures, _ = scanner.scan(tmp_path)

    assert any("reports/committed.md" in item for item in failures), failures


def test_runtime_prefix_does_not_hide_sibling_directory(scanner, tmp_path):
    """Path-prefix matching must not prune similarly named sibling paths."""
    _write(
        tmp_path / "reports" / "runtime-old" / "committed.md",
        f"token: {FAKE_AWS_KEY}\n",
    )

    failures, _ = scanner.scan(tmp_path)

    assert any("reports/runtime-old/committed.md" in item for item in failures), failures


def test_local_env_file_is_still_rejected(scanner, tmp_path):
    """Committed local env files remain a hard failure."""
    _write(tmp_path / ".env", "APP_SECRET_KEY=whatever\n")

    failures, _ = scanner.scan(tmp_path)

    assert any(".env" in item for item in failures), failures


def test_env_example_files_remain_allowed(scanner, tmp_path):
    """Template env files are documentation, not leaked credentials."""
    _write(tmp_path / ".env.example", "APP_SECRET_KEY=replace-me\n")

    failures, _ = scanner.scan(tmp_path)

    assert failures == []


def test_repo_scan_passes_on_current_tree(scanner):
    """The real repository must be clean under the corrected scope."""
    failures, _ = scanner.scan(REPO_ROOT)

    assert failures == [], failures


# --- scripts/security_smoke.py: the same scope, via the shared mechanism ---


@pytest.fixture(scope="module")
def standalone_gate():
    spec = importlib.util.spec_from_file_location(
        "security_smoke", REPO_ROOT / "scripts" / "security_smoke.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_standalone_gate_prunes_virtualenvs(standalone_gate, tmp_path):
    venv = tmp_path / "venv312"
    _write(venv / "pyvenv.cfg", "home = /usr/local/bin\n")
    _write(venv / "lib" / "site-packages" / "vendor.py", f'K = "{FAKE_AWS_KEY}"\n')

    assert standalone_gate.iter_text_files(tmp_path) == []


def test_standalone_gate_prunes_reports_runtime(standalone_gate, tmp_path):
    _write(tmp_path / "reports" / "runtime" / "daily.md", f"token: {FAKE_AWS_KEY}\n")

    assert standalone_gate.iter_text_files(tmp_path) == []


def test_standalone_gate_scans_runtime_prefix_sibling(standalone_gate, tmp_path):
    _write(
        tmp_path / "reports" / "runtime-old" / "committed.md",
        f"token: {FAKE_AWS_KEY}\n",
    )

    scanned = {p.relative_to(tmp_path).as_posix() for p in standalone_gate.iter_text_files(tmp_path)}

    assert "reports/runtime-old/committed.md" in scanned


def test_standalone_gate_still_scans_github_workflows(standalone_gate, tmp_path):
    """This gate deliberately covers .github/, unlike the CI gate.

    Consolidating the two exclusion sets would have silently dropped workflow
    files from the scan, so the difference is pinned here.
    """
    _write(tmp_path / ".github" / "workflows" / "deploy.yml", "key: value\n")

    scanned = {p.name for p in standalone_gate.iter_text_files(tmp_path)}

    assert "deploy.yml" in scanned


def test_shared_walk_prunes_egg_info_and_pycache():
    from scripts.lib.repo_scan import VENDORED_DIR_NAMES, is_pruned_dir

    assert "site-packages" in VENDORED_DIR_NAMES
    assert is_pruned_dir(Path("/x/pkg.egg-info"), "pkg.egg-info", set())
    assert is_pruned_dir(Path("/x/__pycache__"), "__pycache__", set())
    assert not is_pruned_dir(Path("/x/core"), "core", set())
    assert not is_pruned_dir(
        Path("/x/reports/runtime-old"),
        "reports/runtime-old",
        set(),
        ("reports/runtime",),
    )
