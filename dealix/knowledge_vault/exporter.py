"""Deterministic, local-only export of Dealix knowledge into an Obsidian vault.

The exporter intentionally avoids network calls, plugin downloads, automatic commits,
and live production reads. It mirrors approved repository Markdown and explicitly
selected KnowledgeAccumulator JSON snapshots into a source-cited vault that Claude
Code or another local coding agent can inspect directly.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import unicodedata
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable

DEFAULT_SOURCE_ROOTS = (
    "README.md",
    "AGENTS.md",
    "docs/knowledge",
    "docs/knowledge_base",
    "docs/company",
    "docs/playbooks",
    "docs/commercial",
    "docs/ops",
    "docs/agents",
    "reports/final",
)
DEFAULT_KNOWLEDGE_JSON = "data/knowledge/accumulated_intel.json"
MAX_MARKDOWN_BYTES = 2 * 1024 * 1024
MAX_KNOWLEDGE_JSON_BYTES = 5 * 1024 * 1024
VAULT_MARKER = ".dealix-knowledge-vault.json"
EXCLUDED_PARTS = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    "secrets",
    "private",
}


@dataclass(frozen=True)
class ExportResult:
    """Summary and proof locations for one export run."""

    vault_root: Path
    source_documents: int
    knowledge_entries: int
    company_pages: int
    sector_pages: int
    manifest_path: Path
    proof_log_path: Path


def _slug(value: str, fallback: str = "untitled") -> str:
    normalized = unicodedata.normalize("NFKC", value).strip()
    normalized = re.sub(r"[^\w\- ]+", "", normalized, flags=re.UNICODE)
    normalized = re.sub(r"[\s_]+", "-", normalized).strip("-").lower()
    return normalized or fallback


def _yaml_value(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


def _merge_frontmatter(text: str, metadata: dict[str, Any]) -> str:
    lines = [f"{key}: {_yaml_value(value)}" for key, value in metadata.items()]
    block = "\n".join(lines)
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return f"{text[:end]}\n{block}{text[end:]}"
    return f"---\n{block}\n---\n\n{text}"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _has_excluded_part(path: Path) -> bool:
    return any(part.casefold() in EXCLUDED_PARTS for part in path.parts)


def _is_safe_source(path: Path, repo_root: Path) -> bool:
    try:
        relative = path.resolve().relative_to(repo_root.resolve())
    except ValueError:
        return False
    if _has_excluded_part(relative):
        return False
    if path.suffix.lower() != ".md":
        return False
    try:
        return path.stat().st_size <= MAX_MARKDOWN_BYTES
    except OSError:
        return False


def _discover_markdown(repo_root: Path, source_roots: Iterable[str]) -> list[Path]:
    discovered: set[Path] = set()
    for raw_root in source_roots:
        candidate = (repo_root / raw_root).resolve()
        if not candidate.exists():
            continue
        if candidate.is_file():
            if _is_safe_source(candidate, repo_root):
                discovered.add(candidate)
            continue
        for path in candidate.rglob("*.md"):
            if path.is_file() and _is_safe_source(path, repo_root):
                discovered.add(path.resolve())
    return sorted(discovered, key=lambda path: path.as_posix())


def _wiki_target(relative_markdown_path: Path) -> str:
    return relative_markdown_path.with_suffix("").as_posix()


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def _write_marker(vault_root: Path) -> None:
    marker = {
        "schema_version": 1,
        "owner": "dealix_knowledge_vault_exporter",
        "purpose": "generated_read_only_projection",
    }
    _write_text(
        vault_root / VAULT_MARKER,
        json.dumps(marker, ensure_ascii=False, indent=2),
    )


def _marker_is_owned(vault_root: Path) -> bool:
    marker_path = vault_root / VAULT_MARKER
    if not marker_path.is_file():
        return False
    try:
        marker = json.loads(marker_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return False
    return (
        isinstance(marker, dict)
        and marker.get("schema_version") == 1
        and marker.get("owner") == "dealix_knowledge_vault_exporter"
    )


def _safe_clean(vault_root: Path, repo_root: Path) -> None:
    if vault_root.is_symlink():
        raise ValueError(f"Refusing to clean symlinked vault path: {vault_root}")
    resolved = vault_root.resolve()
    forbidden = {Path("/").resolve(), Path.home().resolve(), repo_root.resolve()}
    if resolved in forbidden or len(resolved.parts) < 3:
        raise ValueError(f"Refusing to clean unsafe vault path: {resolved}")
    if not resolved.exists():
        return
    if not resolved.is_dir() or not _marker_is_owned(resolved):
        raise ValueError(f"Refusing to clean unowned vault path: {resolved}")
    shutil.rmtree(resolved)


def _validate_output_location(
    *,
    repo_root: Path,
    vault_root: Path,
    source_roots: Iterable[str],
) -> None:
    if vault_root == repo_root:
        raise ValueError("Vault output cannot be the repository root")
    for raw_root in source_roots:
        source = (repo_root / raw_root).resolve()
        if source.is_file():
            continue
        if vault_root == source or vault_root.is_relative_to(source):
            raise ValueError(
                f"Vault output cannot be inside a configured source root: {source}"
            )


def _resolve_knowledge_json(
    repo_root: Path,
    knowledge_json: Path | None,
) -> Path | None:
    if knowledge_json is None:
        return None
    candidate = knowledge_json
    if not candidate.is_absolute():
        candidate = repo_root / candidate
    resolved = candidate.resolve()
    try:
        relative = resolved.relative_to(repo_root)
    except ValueError as exc:
        raise ValueError("Knowledge JSON must stay inside the Dealix repository") from exc
    if _has_excluded_part(relative):
        raise ValueError("Knowledge JSON cannot come from a private or excluded path")
    if resolved.suffix.lower() != ".json":
        raise ValueError("Knowledge input must be a JSON file")
    if resolved.exists() and resolved.stat().st_size > MAX_KNOWLEDGE_JSON_BYTES:
        raise ValueError("Knowledge JSON exceeds the bounded export size")
    return resolved


def _render_vault_readme(generated_at: str) -> str:
    return f"""# Dealix Knowledge Vault

Generated at: `{generated_at}`

This vault is a **read-only knowledge projection**, not a second production database.
It mirrors approved Dealix Markdown and, only when explicitly selected, a bounded
KnowledgeAccumulator JSON snapshot.

## Open it

1. Run the exporter from the Dealix repository.
2. Open the output folder as a vault in Obsidian.
3. Open Claude Code in the same folder when you need source-grounded Q&A.
4. Start with [[HOME]] and [[wiki/meta/Export Manifest]].

## Trust rules

- Cite the exact `dealix_source_path` or knowledge `source` for every factual answer.
- Treat generated links and summaries as navigation aids, not independent evidence.
- Do not place secrets, `.env` files, customer credentials, or production dumps here.
- Knowledge JSON is opt-in and is never included by CI or scheduled export by default.
- This exporter performs no network calls, plugin downloads, auto-commits, sends, or deploys.
"""


def _render_claude_instructions() -> str:
    return """# Claude instructions for the Dealix Knowledge Vault

Use this vault as a source-grounded second brain.

1. Read [[HOME]] first.
2. Prefer original mirrored source documents under `wiki/sources/repo/`.
3. For each non-trivial factual claim, cite the exact source path shown in frontmatter.
4. Separate facts, inference, and recommendations explicitly.
5. Never invent customer results, revenue, proof, production state, or completed work.
6. Never expose secrets or request secret-dumping commands.
7. Do not edit the Dealix production repository from this exported vault.
8. Treat KnowledgeAccumulator entries as claims with confidence and source metadata, not as verified truth by default.
"""


def _write_obsidian_config(vault_root: Path) -> None:
    graph = {
        "collapse-filter": False,
        "search": "path:wiki",
        "showTags": True,
        "showAttachments": False,
        "hideUnresolved": True,
        "showOrphans": False,
        "showArrow": True,
        "nodeSizeMultiplier": 1.4,
        "lineSizeMultiplier": 1.1,
        "colorGroups": [
            {"query": "path:wiki/entities", "color": {"a": 1, "rgb": 12945088}},
            {"query": "path:wiki/concepts", "color": {"a": 1, "rgb": 5227007}},
            {"query": "path:wiki/sources", "color": {"a": 1, "rgb": 6986069}},
            {"query": "path:wiki/meta", "color": {"a": 1, "rgb": 5676246}},
        ],
    }
    app = {
        "userIgnoreFilters": [
            ".vault-meta/",
            "manifest.json",
            "proof-log.json",
        ]
    }
    _write_text(vault_root / ".obsidian" / "graph.json", json.dumps(graph, indent=2))
    _write_text(vault_root / ".obsidian" / "app.json", json.dumps(app, indent=2))


def _export_repository_sources(
    repo_root: Path,
    vault_root: Path,
    source_roots: Iterable[str],
    generated_at: str,
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    destination_root = vault_root / "wiki" / "sources" / "repo"
    for source_path in _discover_markdown(repo_root, source_roots):
        relative = source_path.relative_to(repo_root)
        destination = destination_root / relative
        original = source_path.read_text(encoding="utf-8", errors="replace")
        exported = _merge_frontmatter(
            original,
            {
                "dealix_type": "repository_source",
                "dealix_source_path": relative.as_posix(),
                "dealix_exported_at": generated_at,
            },
        )
        _write_text(destination, exported)
        records.append(
            {
                "source_path": relative.as_posix(),
                "vault_path": destination.relative_to(vault_root).as_posix(),
                "sha256": _sha256(destination),
            }
        )
    return records


def _load_knowledge_entries(path: Path | None) -> list[dict[str, Any]]:
    if path is None or not path.exists():
        return []
    raw = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(raw, dict):
        raw = raw.get("entries", [])
    if not isinstance(raw, list):
        raise ValueError("Knowledge JSON must contain a list or an object with an entries list")
    return [entry for entry in raw if isinstance(entry, dict)]


def _bilingual_text(raw: Any) -> str:
    if isinstance(raw, str):
        return raw
    if not isinstance(raw, dict):
        return ""
    en = str(raw.get("en") or "").strip()
    ar = str(raw.get("ar") or "").strip()
    parts = []
    if en:
        parts.append(en)
    if ar and ar != en:
        parts.append(ar)
    return "\n\n".join(parts)


def _export_knowledge_entries(
    entries: list[dict[str, Any]], vault_root: Path, generated_at: str
) -> tuple[list[dict[str, Any]], dict[str, list[str]], dict[str, list[str]]]:
    records: list[dict[str, Any]] = []
    by_company: dict[str, list[str]] = {}
    by_sector: dict[str, list[str]] = {}
    used_slugs: dict[str, str] = {}
    root = vault_root / "wiki" / "sources" / "knowledge"
    for index, entry in enumerate(entries, start=1):
        entry_id = str(entry.get("entry_id") or f"entry-{index}")
        slug = _slug(entry_id)
        prior = used_slugs.get(slug)
        if prior is not None and prior != entry_id:
            raise ValueError(
                f"Knowledge entry identifiers collide after normalization: {prior!r} and {entry_id!r}"
            )
        used_slugs[slug] = entry_id
        title = _bilingual_text(entry.get("title")) or entry_id
        content = _bilingual_text(entry.get("content"))
        company = str(entry.get("company") or "").strip()
        sector = str(entry.get("sector") or "").strip()
        source = str(entry.get("source") or "unknown")
        category = str(entry.get("category") or "unknown")
        tags = entry.get("tags") if isinstance(entry.get("tags"), list) else []
        confidence = entry.get("confidence", 0.5)
        destination = root / f"{slug}.md"
        metadata = {
            "dealix_type": "knowledge_entry",
            "entry_id": entry_id,
            "category": category,
            "source": source,
            "company": company or None,
            "sector": sector or None,
            "tags": tags,
            "confidence": confidence,
            "created_at": entry.get("created_at"),
            "expires_at": entry.get("expires_at"),
            "dealix_exported_at": generated_at,
        }
        body = f"# {title}\n\n{content or '_No content supplied._'}\n\n## Source\n\n`{source}`"
        _write_text(destination, _merge_frontmatter(body, metadata))
        target = _wiki_target(destination.relative_to(vault_root))
        if company:
            by_company.setdefault(company, []).append(target)
        if sector:
            by_sector.setdefault(sector, []).append(target)
        records.append(
            {
                "entry_id": entry_id,
                "vault_path": destination.relative_to(vault_root).as_posix(),
                "source": source,
                "confidence": confidence,
                "sha256": _sha256(destination),
            }
        )
    return records, by_company, by_sector


def _write_map_pages(
    vault_root: Path,
    directory: str,
    page_type: str,
    mapping: dict[str, list[str]],
    generated_at: str,
) -> int:
    count = 0
    used_slugs: dict[str, str] = {}
    for name, targets in sorted(mapping.items(), key=lambda item: item[0].casefold()):
        slug = _slug(name)
        prior = used_slugs.get(slug)
        if prior is not None and prior != name:
            raise ValueError(
                f"{page_type.title()} names collide after normalization: {prior!r} and {name!r}"
            )
        used_slugs[slug] = name
        destination = vault_root / "wiki" / directory / f"{slug}.md"
        links = "\n".join(f"- [[{target}]]" for target in sorted(set(targets)))
        body = f"# {name}\n\n## Linked knowledge\n\n{links or '_No linked knowledge._'}"
        _write_text(
            destination,
            _merge_frontmatter(
                body,
                {
                    "dealix_type": page_type,
                    "name": name,
                    "dealix_exported_at": generated_at,
                },
            ),
        )
        count += 1
    return count


def _write_navigation(
    vault_root: Path,
    source_records: list[dict[str, Any]],
    knowledge_records: list[dict[str, Any]],
    generated_at: str,
) -> None:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for record in source_records:
        root = record["source_path"].split("/", 1)[0]
        grouped.setdefault(root, []).append(record)

    sections = []
    for root, records in sorted(grouped.items()):
        links = []
        for record in records:
            target = _wiki_target(Path(record["vault_path"]))
            links.append(f"- [[{target}|{record['source_path']}]]")
        sections.append(f"## {root}\n\n" + "\n".join(links))

    home = f"""# Dealix Second Brain

Exported at: `{generated_at}`

- Repository sources: **{len(source_records)}**
- Knowledge entries: **{len(knowledge_records)}**

## Start here

- [[wiki/meta/Export Manifest]]
- [[wiki/meta/Proof Index]]
- [[wiki/entities/README|Company index]]
- [[wiki/concepts/README|Sector index]]

{chr(10).join(sections)}
"""
    _write_text(vault_root / "HOME.md", home)

    manifest_lines = ["# Export Manifest", "", f"Generated at: `{generated_at}`", ""]
    for record in source_records:
        target = _wiki_target(Path(record["vault_path"]))
        manifest_lines.append(f"- [[{target}|{record['source_path']}]]")
    _write_text(vault_root / "wiki" / "meta" / "Export Manifest.md", "\n".join(manifest_lines))

    proof_lines = ["# Proof Index", "", "Every exported file is hashed in `proof-log.json`.", ""]
    for record in knowledge_records:
        target = _wiki_target(Path(record["vault_path"]))
        proof_lines.append(
            f"- [[{target}|{record['entry_id']}]] — source: `{record['source']}` — "
            f"confidence: `{record['confidence']}`"
        )
    _write_text(vault_root / "wiki" / "meta" / "Proof Index.md", "\n".join(proof_lines))


def _write_index_page(vault_root: Path, directory: str, title: str) -> None:
    root = vault_root / "wiki" / directory
    pages = sorted(path for path in root.glob("*.md") if path.name != "README.md")
    links = "\n".join(
        f"- [[{_wiki_target(path.relative_to(vault_root))}|{path.stem}]]" for path in pages
    )
    _write_text(root / "README.md", f"# {title}\n\n{links or '_No pages generated._'}")


def export_knowledge_vault(
    *,
    repo_root: Path,
    vault_root: Path,
    source_roots: Iterable[str] = DEFAULT_SOURCE_ROOTS,
    knowledge_json: Path | None = None,
    clean: bool = False,
) -> ExportResult:
    """Export approved Dealix knowledge into an Obsidian-compatible local vault."""

    repo_root = repo_root.resolve()
    if vault_root.is_symlink():
        raise ValueError(f"Vault output cannot be a symlink: {vault_root}")
    vault_root = vault_root.resolve()
    source_roots = tuple(source_roots)
    _validate_output_location(
        repo_root=repo_root,
        vault_root=vault_root,
        source_roots=source_roots,
    )
    selected_knowledge_json = _resolve_knowledge_json(repo_root, knowledge_json)
    if selected_knowledge_json is not None and selected_knowledge_json.is_relative_to(vault_root):
        raise ValueError("Knowledge JSON cannot be read from the generated vault")
    if clean:
        _safe_clean(vault_root, repo_root)
    vault_root.mkdir(parents=True, exist_ok=True)
    _write_marker(vault_root)
    generated_at = datetime.now(UTC).isoformat()

    _write_obsidian_config(vault_root)
    _write_text(vault_root / "README.md", _render_vault_readme(generated_at))
    _write_text(vault_root / "CLAUDE.md", _render_claude_instructions())

    source_records = _export_repository_sources(
        repo_root, vault_root, source_roots, generated_at
    )
    entries = _load_knowledge_entries(selected_knowledge_json)
    knowledge_records, by_company, by_sector = _export_knowledge_entries(
        entries, vault_root, generated_at
    )
    company_pages = _write_map_pages(
        vault_root, "entities", "company", by_company, generated_at
    )
    sector_pages = _write_map_pages(
        vault_root, "concepts", "sector", by_sector, generated_at
    )
    _write_index_page(vault_root, "entities", "Companies")
    _write_index_page(vault_root, "concepts", "Sectors")
    _write_navigation(vault_root, source_records, knowledge_records, generated_at)

    knowledge_json_manifest = (
        selected_knowledge_json.relative_to(repo_root).as_posix()
        if selected_knowledge_json is not None
        else None
    )
    manifest = {
        "schema_version": 1,
        "generated_at": generated_at,
        "repo_root": ".",
        "source_roots": list(source_roots),
        "knowledge_json": knowledge_json_manifest,
        "knowledge_json_opt_in": selected_knowledge_json is not None,
        "counts": {
            "repository_sources": len(source_records),
            "knowledge_entries": len(knowledge_records),
            "company_pages": company_pages,
            "sector_pages": sector_pages,
        },
        "repository_sources": source_records,
        "knowledge_entries": knowledge_records,
    }
    manifest_path = vault_root / "manifest.json"
    _write_text(manifest_path, json.dumps(manifest, ensure_ascii=False, indent=2))

    hashed_files = []
    for path in sorted(vault_root.rglob("*")):
        if path.is_file() and path.name != "proof-log.json":
            hashed_files.append(
                {
                    "path": path.relative_to(vault_root).as_posix(),
                    "sha256": _sha256(path),
                    "bytes": path.stat().st_size,
                }
            )
    proof_log = {
        "schema_version": 1,
        "generated_at": generated_at,
        "action": "dealix_knowledge_vault_export",
        "network_calls": 0,
        "external_actions": 0,
        "knowledge_json_opt_in": selected_knowledge_json is not None,
        "files": hashed_files,
    }
    proof_log_path = vault_root / "proof-log.json"
    _write_text(proof_log_path, json.dumps(proof_log, ensure_ascii=False, indent=2))

    return ExportResult(
        vault_root=vault_root,
        source_documents=len(source_records),
        knowledge_entries=len(knowledge_records),
        company_pages=company_pages,
        sector_pages=sector_pages,
        manifest_path=manifest_path,
        proof_log_path=proof_log_path,
    )
