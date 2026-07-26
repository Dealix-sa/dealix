from __future__ import annotations

import json
from pathlib import Path

import pytest

from dealix.knowledge_vault.exporter import export_knowledge_vault


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_export_builds_source_cited_obsidian_vault(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    vault = tmp_path / "vault"
    _write(repo / "README.md", "# Dealix\n\nCanonical overview.")
    _write(
        repo / "docs" / "knowledge" / "graph.md",
        "---\nstatus: canonical\n---\n\n# Knowledge Graph\n\nSector to proof.",
    )
    _write(repo / "docs" / "secrets" / "leak.md", "# Must not export")
    _write(
        repo / "data" / "knowledge" / "accumulated_intel.json",
        json.dumps(
            [
                {
                    "entry_id": "knl-001",
                    "category": "deal_insight",
                    "title": {"en": "Clinic follow-up", "ar": "متابعة العيادة"},
                    "content": {
                        "en": "Follow-up speed is a measurable hypothesis.",
                        "ar": "سرعة المتابعة فرضية قابلة للقياس.",
                    },
                    "source": "meeting-note-001",
                    "sector": "Healthcare",
                    "company": "Example Clinic",
                    "tags": ["follow-up"],
                    "confidence": 0.7,
                    "created_at": "2026-07-26T00:00:00+00:00",
                    "expires_at": None,
                }
            ],
            ensure_ascii=False,
        ),
    )

    result = export_knowledge_vault(
        repo_root=repo,
        vault_root=vault,
        source_roots=("README.md", "docs"),
        clean=True,
    )

    assert result.source_documents == 2
    assert result.knowledge_entries == 1
    assert result.company_pages == 1
    assert result.sector_pages == 1
    assert (vault / ".obsidian" / "graph.json").exists()
    assert (vault / "HOME.md").exists()
    assert (vault / "CLAUDE.md").exists()
    assert (vault / "wiki" / "entities" / "example-clinic.md").exists()
    assert (vault / "wiki" / "concepts" / "healthcare.md").exists()
    assert not (vault / "wiki" / "sources" / "repo" / "docs" / "secrets" / "leak.md").exists()

    mirrored = (
        vault / "wiki" / "sources" / "repo" / "docs" / "knowledge" / "graph.md"
    ).read_text(encoding="utf-8")
    assert "status: canonical" in mirrored
    assert 'dealix_source_path: "docs/knowledge/graph.md"' in mirrored

    manifest = json.loads(result.manifest_path.read_text(encoding="utf-8"))
    assert manifest["counts"]["repository_sources"] == 2
    assert manifest["counts"]["knowledge_entries"] == 1

    proof = json.loads(result.proof_log_path.read_text(encoding="utf-8"))
    assert proof["network_calls"] == 0
    assert proof["external_actions"] == 0
    assert any(item["path"] == "HOME.md" for item in proof["files"])


def test_clean_refuses_repository_root(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()

    with pytest.raises(ValueError, match="Refusing to clean unsafe vault path"):
        export_knowledge_vault(
            repo_root=repo,
            vault_root=repo,
            source_roots=(),
            clean=True,
        )
