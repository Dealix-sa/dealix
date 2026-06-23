"""Test: a client workspace is not ready to build until acceptance criteria are signed."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts" / "delivery"))

from client_blueprint import blueprint_status, SIGNED_MARKERS  # noqa: E402
from create_client_workspace import create_workspace  # noqa: E402

TEST_SLUG = "_test_delivery_ac"


@pytest.fixture()
def workspace():
    path = create_workspace(TEST_SLUG, overwrite=True)
    yield path
    if path.exists():
        shutil.rmtree(path)


def _sign_acceptance_criteria(workspace: Path) -> None:
    ac = workspace / "02_solution" / "acceptance_criteria.md"
    text = ac.read_text(encoding="utf-8")
    # Replace unchecked sign-off boxes with checked ones.
    text = text.replace("- [ ] Sponsor signature:", "- [x] Sponsor signature: Jane Doe")
    text = text.replace("- [ ] Dealix delivery lead signature:", "- [x] Dealix delivery lead signature: Agent")
    ac.write_text(text, encoding="utf-8")


def test_not_ready_when_unsigned(workspace: Path) -> None:
    """A fresh workspace must not be ready to build (acceptance criteria unsigned)."""
    report = blueprint_status(TEST_SLUG)
    assert report["acceptance_criteria_signed"] is False
    assert report["ready_to_build"] is False


def test_ready_when_signed(workspace: Path) -> None:
    """After signing acceptance criteria, the workspace must be ready to build."""
    _sign_acceptance_criteria(workspace)
    report = blueprint_status(TEST_SLUG)
    assert report["acceptance_criteria_signed"] is True
    assert report["ready_to_build"] is True


def test_signed_markers_present_in_template(workspace: Path) -> None:
    """The template acceptance-criteria file must contain the signed markers we look for."""
    ac = workspace / "02_solution" / "acceptance_criteria.md"
    text = ac.read_text(encoding="utf-8")
    # The unchecked form of each marker must be present.
    assert "- [ ] Sponsor signature" in text
    assert "- [ ] Dealix delivery lead signature" in text
    # The SIGNED_MARKERS are the checked equivalents.
    assert all("[x]" in m for m in SIGNED_MARKERS)