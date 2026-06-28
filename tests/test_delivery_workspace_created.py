"""Test: creating a client workspace from the _template directory produces all phases."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts" / "delivery"))

from create_client_workspace import PHASES, create_workspace, template_complete

CLIENTS_DIR = REPO_ROOT / "clients"
TEST_SLUG = "_test_delivery_demo"


@pytest.fixture()
def workspace():
    """Create and tear down a throwaway client workspace."""
    path = create_workspace(TEST_SLUG, client_name="Test Delivery Demo", overwrite=True)
    yield path
    if path.exists():
        shutil.rmtree(path)


def test_template_is_complete() -> None:
    """The _template directory must contain every phase file before any workspace can be created."""
    assert template_complete(), "clients/_template is missing expected phase files"


def test_workspace_has_all_phases(workspace: Path) -> None:
    """Every required phase subdirectory must exist in the created workspace."""
    for phase in PHASES:
        assert (workspace / phase).is_dir(), f"missing phase directory: {phase}"


def test_workspace_has_all_phase_files(workspace: Path) -> None:
    """Every file declared in PHASES must be present in the created workspace."""
    for phase, files in PHASES.items():
        for name in files:
            assert (workspace / phase / name).is_file(), f"missing {phase}/{name}"


def test_workspace_readme_written(workspace: Path) -> None:
    """The workspace manifest README must be written by the creator."""
    readme = workspace / "README.md"
    assert readme.exists()
    assert "Map -> Design -> Build -> Operate -> Scale" in readme.read_text(encoding="utf-8")


def test_create_workspace_refuses_duplicate(workspace: Path) -> None:
    """Creating a workspace that already exists must raise without --overwrite."""
    with pytest.raises(FileExistsError):
        create_workspace(TEST_SLUG)
