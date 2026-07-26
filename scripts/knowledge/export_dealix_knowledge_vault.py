#!/usr/bin/env python3
"""Export Dealix knowledge into an Obsidian-compatible source-cited vault."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Direct execution sets sys.path[0] to scripts/knowledge rather than the
# repository root. Bootstrap the checkout root so the documented one-command
# invocation works without requiring PYTHONPATH or an editable install.
REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from dealix.knowledge_vault.exporter import (
    DEFAULT_KNOWLEDGE_JSON,
    DEFAULT_SOURCE_ROOTS,
    export_knowledge_vault,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Build a local-only Obsidian vault from approved Dealix Markdown. "
            "A bounded KnowledgeAccumulator JSON snapshot is included only when "
            "--knowledge-json is supplied explicitly."
        )
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
        help="Dealix repository root (default: current directory)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("artifacts/dealix-knowledge-vault"),
        help="Vault output directory",
    )
    parser.add_argument(
        "--source-root",
        action="append",
        dest="source_roots",
        help="Approved Markdown file/directory relative to repo root; repeatable",
    )
    parser.add_argument(
        "--knowledge-json",
        type=Path,
        help=(
            "Opt-in KnowledgeAccumulator JSON snapshot inside the repository; "
            f"for example {DEFAULT_KNOWLEDGE_JSON}. Omit for repository-only export."
        ),
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help=(
            "Replace only an output directory previously marked as owned by the "
            "Dealix knowledge-vault exporter"
        ),
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    repo_root = args.repo_root.resolve()
    output = args.output
    if not output.is_absolute():
        output = repo_root / output
    knowledge_json = args.knowledge_json
    if knowledge_json is not None and not knowledge_json.is_absolute():
        knowledge_json = repo_root / knowledge_json

    result = export_knowledge_vault(
        repo_root=repo_root,
        vault_root=output,
        source_roots=tuple(args.source_roots or DEFAULT_SOURCE_ROOTS),
        knowledge_json=knowledge_json,
        clean=args.clean,
    )
    summary = {
        "status": "ok",
        "vault_root": result.vault_root.as_posix(),
        "source_documents": result.source_documents,
        "knowledge_entries": result.knowledge_entries,
        "company_pages": result.company_pages,
        "sector_pages": result.sector_pages,
        "knowledge_json_opt_in": knowledge_json is not None,
        "manifest": result.manifest_path.as_posix(),
        "proof_log": result.proof_log_path.as_posix(),
        "network_calls": 0,
        "external_actions": 0,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
