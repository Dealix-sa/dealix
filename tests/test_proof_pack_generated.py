"""Test: the proof pack can be generated from a client workspace."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts" / "delivery"))

from client_proof import PROOF_FILES, proof_pack
from create_client_workspace import create_workspace

TEST_SLUG = "_test_delivery_proof"


@pytest.fixture()
def workspace():
    path = create_workspace(TEST_SLUG, overwrite=True)
    yield path
    if path.exists():
        shutil.rmtree(path)


def test_proof_pack_generated(workspace: Path) -> None:
    """proof_pack() must write clients/<slug>/proof_pack.md and include every proof file."""
    pack = proof_pack(TEST_SLUG)
    assert pack.exists()
    text = pack.read_text(encoding="utf-8")
    assert "Proof Pack" in text
    for name in PROOF_FILES:
        assert name in text, f"proof pack missing section: {name}"


def test_proof_pack_reports_missing_files(workspace: Path) -> None:
    """If a proof file is removed, the generated pack must list it as missing."""
    missing = workspace / "05_proof" / "open_risks.md"
    missing.unlink()
    pack = proof_pack(TEST_SLUG)
    text = pack.read_text(encoding="utf-8")
    assert "Missing proof files" in text
    assert "open_risks.md" in text


def test_proof_pack_doctrine_header(workspace: Path) -> None:
    """The proof pack must carry the delivery doctrine header."""
    pack = proof_pack(TEST_SLUG)
    text = pack.read_text(encoding="utf-8")
    assert "Map -> Design -> Build -> Operate -> Scale" in text
