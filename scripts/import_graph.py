#!/usr/bin/env python3
"""Which top-level packages are actually imported, and by what.

Before a package can be quarantined or deleted, "nothing imports this" has to
be evidence rather than an impression. ``grep`` is not sufficient evidence: it
misses ``importlib.import_module("pkg")`` and ``__import__("pkg")``, and it
produces false hits inside strings, comments and unrelated substrings.

This tool parses each file's AST instead, and additionally resolves dynamic
imports whose argument is a string literal.

    python3 scripts/import_graph.py --summary
    python3 scripts/import_graph.py --importers autonomous_growth
    python3 scripts/import_graph.py --orphans

Exit codes: ``--importers`` exits 1 when a package has zero importers, so it
can be used directly as a deletion precondition in a checklist.
"""

from __future__ import annotations

import argparse
import ast
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.lib.repo_scan import iter_candidate_files

# Mirrors the security gates' exclusions: generated, vendored and cache trees
# are not evidence of anything.
SKIP_DIR_NAMES = {
    ".git",
    ".mypy_cache",
    ".next",
    ".nox",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "_attic",
    "build",
    "dist",
    "htmlcov",
    "node_modules",
    "venv",
}
SKIP_PATH_PREFIXES = ("reports/runtime",)

DYNAMIC_IMPORT_CALLS = {"import_module", "__import__"}


def top_level_packages() -> set[str]:
    """Directories and modules that constitute this repo's own namespace."""
    packages: set[str] = set()
    for entry in ROOT.iterdir():
        if entry.name.startswith((".", "_")):
            continue
        if not entry.is_dir():
            continue
        if (entry / "__init__.py").is_file():
            packages.add(entry.name)
        elif next(entry.rglob("*.py"), None) is not None:
            # Namespace-style dirs (no __init__.py) are still importable when
            # the repo root is on sys.path, which is how scripts run. Recurse,
            # because some dirs hold Python only in a nested scripts/ folder
            # and would otherwise look empty and escape the orphan check.
            packages.add(entry.name)
    return packages


def _imported_roots(tree: ast.AST) -> set[str]:
    """Every top-level module name this AST references as an import."""
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                roots.add(alias.name.split(".", 1)[0])
        elif isinstance(node, ast.ImportFrom):
            # level > 0 is a relative import — stays inside its own package.
            if node.level == 0 and node.module:
                roots.add(node.module.split(".", 1)[0])
        elif isinstance(node, ast.Call):
            func = node.func
            name = (
                func.attr
                if isinstance(func, ast.Attribute)
                else func.id
                if isinstance(func, ast.Name)
                else None
            )
            if name in DYNAMIC_IMPORT_CALLS and node.args:
                first = node.args[0]
                if isinstance(first, ast.Constant) and isinstance(first.value, str):
                    roots.add(first.value.split(".", 1)[0])
    return roots


def build_graph() -> dict[str, set[str]]:
    """Map ``package -> {repo-relative importer paths}``."""
    packages = top_level_packages()
    graph: dict[str, set[str]] = defaultdict(set)
    for package in packages:
        graph[package] = set()

    for path in iter_candidate_files(ROOT, SKIP_DIR_NAMES, SKIP_PATH_PREFIXES):
        if path.suffix != ".py":
            continue
        rel = path.relative_to(ROOT).as_posix()
        try:
            tree = ast.parse(path.read_text(encoding="utf-8", errors="ignore"), rel)
        except SyntaxError:
            continue

        owner = rel.split("/", 1)[0]
        for root in _imported_roots(tree):
            if root in packages and root != owner:
                graph[root].add(rel)
    return graph


def _partition(importers: set[str]) -> tuple[set[str], set[str]]:
    """Split importers into (production, tests-and-scripts)."""
    peripheral = {p for p in importers if p.startswith(("tests/", "scripts/"))}
    return importers - peripheral, peripheral


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--summary", action="store_true", help="Importer count per package.")
    group.add_argument("--importers", metavar="PKG", help="List importers of PKG.")
    group.add_argument(
        "--orphans",
        action="store_true",
        help="Packages with zero importers outside tests/ and scripts/.",
    )
    args = parser.parse_args()

    graph = build_graph()

    if args.importers:
        package = args.importers
        if package not in graph:
            print(f"Unknown top-level package: {package}")
            return 2
        production, peripheral = _partition(graph[package])
        print(f"{package}: {len(production)} production, {len(peripheral)} tests/scripts")
        for item in sorted(production):
            print(f"  {item}")
        for item in sorted(peripheral):
            print(f"  [peripheral] {item}")
        return 0 if graph[package] else 1

    if args.orphans:
        orphans = []
        for package, importers in sorted(graph.items()):
            production, peripheral = _partition(importers)
            if not production:
                orphans.append((package, len(peripheral)))
        print(f"IMPORT_GRAPH_ORPHANS={len(orphans)}")
        for package, peripheral_count in orphans:
            note = f" ({peripheral_count} tests/scripts only)" if peripheral_count else ""
            print(f"  {package}{note}")
        return 0

    print(f"{'package':32} {'prod':>6} {'periph':>7}")
    for package, importers in sorted(graph.items(), key=lambda kv: -len(kv[1])):
        production, peripheral = _partition(importers)
        print(f"{package:32} {len(production):6} {len(peripheral):7}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
