from __future__ import annotations

import json
from pathlib import Path

import pytest

from dealix.knowledge_vault.exporter import VAULT_MARKER, export_knowledge_vault


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _knowledge_payload() -> list[dict[str, object]]:
    return [
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
    ]


def test_export_builds_source_cited_obsidian_vault(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    vault = tmp_path / "vault"
    knowledge_json = repo / "data" / "knowledge" / "accumulated_intel.json"
    _write(repo / "README.md", "# Dealix\n\nCanonical overview.")
    _write(
        repo / "docs" / "knowledge" / "graph.md",
        "---\nstatus: canonical\n---\n\n# Knowledge Graph\n\nSector to proof.",
    )
    _write(repo / "docs" / "secrets" / "leak.md", "# Must not export")
    _write(
        knowledge_json,
        json.dumps(_knowledge_payload(), ensure_ascii=False),
    )

    result = export_knowledge_vault(
        repo_root=repo,
        vault_root=vault,
        source_roots=("README.md", "docs"),
        knowledge_json=knowledge_json,
        clean=True,
    )

    assert result.source_documents == 2
    assert result.knowledge_entries == 1
    assert result.company_pages == 1
    assert result.sector_pages == 1
    assert (vault / VAULT_MARKER).exists()
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
    assert manifest["repo_root"] == "."
    assert manifest["knowledge_json"] == "data/knowledge/accumulated_intel.json"
    assert manifest["knowledge_json_opt_in"] is True
    assert manifest["counts"]["repository_sources"] == 2
    assert manifest["counts"]["knowledge_entries"] == 1

    proof = json.loads(result.proof_log_path.read_text(encoding="utf-8"))
    assert proof["network_calls"] == 0
    assert proof["external_actions"] == 0
    assert proof["knowledge_json_opt_in"] is True
    assert any(item["path"] == "HOME.md" for item in proof["files"])


def test_default_export_does_not_include_knowledge_json(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    vault = tmp_path / "vault"
    _write(repo / "README.md", "# Dealix")
    _write(
        repo / "data" / "knowledge" / "accumulated_intel.json",
        json.dumps(_knowledge_payload(), ensure_ascii=False),
    )

    result = export_knowledge_vault(
        repo_root=repo,
        vault_root=vault,
        source_roots=("README.md",),
        clean=True,
    )

    manifest = json.loads(result.manifest_path.read_text(encoding="utf-8"))
    assert result.knowledge_entries == 0
    assert manifest["knowledge_json"] is None
    assert manifest["knowledge_json_opt_in"] is False


def test_clean_refuses_repository_root(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()

    with pytest.raises(ValueError, match="Vault output cannot be the repository root"):
        export_knowledge_vault(
            repo_root=repo,
            vault_root=repo,
            source_roots=(),
            clean=True,
        )


def test_clean_refuses_unowned_existing_directory(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    vault = tmp_path / "unowned"
    repo.mkdir()
    _write(vault / "keep.txt", "must survive")

    with pytest.raises(ValueError, match="Refusing to clean unowned vault path"):
        export_knowledge_vault(
            repo_root=repo,
            vault_root=vault,
            source_roots=(),
            clean=True,
        )

    assert (vault / "keep.txt").read_text(encoding="utf-8") == "must survive"


def test_clean_replaces_only_owned_generated_vault(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    vault = tmp_path / "vault"
    _write(repo / "README.md", "# Dealix")
    export_knowledge_vault(
        repo_root=repo,
        vault_root=vault,
        source_roots=("README.md",),
    )
    _write(vault / "stale.txt", "remove me")

    export_knowledge_vault(
        repo_root=repo,
        vault_root=vault,
        source_roots=("README.md",),
        clean=True,
    )

    assert not (vault / "stale.txt").exists()
    assert (vault / VAULT_MARKER).exists()


def test_knowledge_json_must_stay_inside_repository(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    outside = tmp_path / "outside.json"
    repo.mkdir()
    _write(outside, "[]")

    with pytest.raises(ValueError, match="must stay inside"):
        export_knowledge_vault(
            repo_root=repo,
            vault_root=tmp_path / "vault",
            source_roots=(),
            knowledge_json=outside,
        )


def test_output_cannot_be_nested_under_source_root(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    docs = repo / "docs"
    docs.mkdir(parents=True)

    with pytest.raises(ValueError, match="inside a configured source root"):
        export_knowledge_vault(
            repo_root=repo,
            vault_root=docs / "generated-vault",
            source_roots=("docs",),
        )


def test_normalized_entry_id_collision_fails_closed(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    knowledge_json = repo / "data" / "knowledge" / "entries.json"
    payload = _knowledge_payload()
    payload.append({**payload[0], "entry_id": "knl_001"})
    _write(knowledge_json, json.dumps(payload, ensure_ascii=False))

    with pytest.raises(ValueError, match="collide after normalization"):
        export_knowledge_vault(
            repo_root=repo,
            vault_root=tmp_path / "vault",
            source_roots=(),
            knowledge_json=knowledge_json,
        )
