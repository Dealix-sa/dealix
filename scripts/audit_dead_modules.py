#!/usr/bin/env python3
"""Static import-graph analyzer for the Dealix repo.

Walks ``auto_client_acquisition/`` and ``api/`` and builds the internal
import graph via ``ast``. Classifies every module as one of:

* **ALIVE** — reachable (transitively) from ``api/main.py`` or any
  script under ``scripts/``.
* **TEST_ONLY** — reachable only from a file under ``tests/``.
* **DEAD** — no internal reference at all.
* **ORPHAN_ROUTER** — file declares a FastAPI ``APIRouter`` but
  ``api/main.py`` never includes it.

Emits ``docs/audit/dead_modules_2026-05-22.md`` with four tables and a
one-line excerpt of each module's first top-level symbol so the founder
can scan and recognize what each was meant to be.

Pure stdlib. No network. No execution of scanned code.
"""
from __future__ import annotations

import ast
import sys
from collections import defaultdict, deque
from collections.abc import Iterable
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCAN_DIRS = ["auto_client_acquisition", "api"]
ROOT_DIRS = ["scripts", "tests"]
ROOT_FILE = REPO_ROOT / "api" / "main.py"
OUT_PATH = REPO_ROOT / "docs" / "audit" / "dead_modules_2026-05-22.md"


def file_to_module(path: Path) -> str:
    rel = path.relative_to(REPO_ROOT)
    parts = list(rel.with_suffix("").parts)
    if parts and parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts)


def module_to_file(mod: str, mod_to_file: dict[str, Path]) -> Path | None:
    parts = mod.split(".")
    for i in range(len(parts), 0, -1):
        candidate = ".".join(parts[:i])
        if candidate in mod_to_file:
            return mod_to_file[candidate]
    return None


def collect_imports(file: Path) -> set[str]:
    try:
        tree = ast.parse(file.read_text(encoding="utf-8"), filename=str(file))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return set()
    out: set[str] = set()
    file_module = file_to_module(file)
    if file.name == "__init__.py":
        pkg_parts = file_module.split(".")
    else:
        pkg_parts = file_module.split(".")[:-1]
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                out.add(n.name)
        elif isinstance(node, ast.ImportFrom):
            if node.level and node.level > 0:
                base_parts = pkg_parts[: len(pkg_parts) - (node.level - 1)]
                if node.module:
                    base_parts = base_parts + node.module.split(".")
                base = ".".join(base_parts)
                if base:
                    out.add(base)
                for n in node.names:
                    if base:
                        out.add(f"{base}.{n.name}")
            elif node.module:
                out.add(node.module)
                for n in node.names:
                    out.add(f"{node.module}.{n.name}")
    return {m for m in out if m}


def walk_py(root: Path) -> Iterable[Path]:
    if not root.exists():
        return
    for p in root.rglob("*.py"):
        if "__pycache__" in p.parts:
            continue
        yield p


def first_top_symbol(file: Path) -> str:
    try:
        tree = ast.parse(file.read_text(encoding="utf-8"))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return ""
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            kw = "async def" if isinstance(node, ast.AsyncFunctionDef) else "def"
            args = ", ".join(a.arg for a in node.args.args)
            return f"{kw} {node.name}({args})"
        if isinstance(node, ast.ClassDef):
            return f"class {node.name}"
    return ""


def bfs(roots: Iterable[Path], edges: dict[Path, set[Path]]) -> set[Path]:
    seen: set[Path] = set()
    queue: deque[Path] = deque(roots)
    while queue:
        cur = queue.popleft()
        if cur in seen:
            continue
        seen.add(cur)
        for nxt in edges.get(cur, ()):
            if nxt not in seen:
                queue.append(nxt)
    return seen


def find_apirouter_files(scanned: list[Path]) -> set[Path]:
    out: set[Path] = set()
    for file in scanned:
        try:
            text = file.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if "APIRouter(" in text:
            out.add(file)
    return out


def main() -> int:
    scanned: list[Path] = []
    for d in SCAN_DIRS:
        scanned.extend(walk_py(REPO_ROOT / d))
    scanned.sort()

    mod_to_file: dict[str, Path] = {file_to_module(f): f for f in scanned}

    edges: dict[Path, set[Path]] = defaultdict(set)
    for f in scanned:
        for mod in collect_imports(f):
            target = module_to_file(mod, mod_to_file)
            if target and target != f:
                edges[f].add(target)

    prod_roots: set[Path] = set()
    if ROOT_FILE.exists():
        prod_roots.add(ROOT_FILE)

    scripts_dir = REPO_ROOT / "scripts"
    for sf in walk_py(scripts_dir):
        for mod in collect_imports(sf):
            target = module_to_file(mod, mod_to_file)
            if target:
                prod_roots.add(target)

    test_roots: set[Path] = set()
    for tf in walk_py(REPO_ROOT / "tests"):
        for mod in collect_imports(tf):
            target = module_to_file(mod, mod_to_file)
            if target:
                test_roots.add(target)

    alive = bfs(prod_roots, edges) & set(scanned)
    test_reach = bfs(test_roots, edges) & set(scanned)

    # An __init__.py is implicitly executed by Python when any module
    # inside its package is imported, so a package init for an otherwise-
    # alive package is not really "dead". Mark all such inits as ALIVE.
    alive_dirs = {f.parent for f in alive}
    for f in list(set(scanned) - alive):
        if f.name == "__init__.py" and f.parent in alive_dirs:
            alive.add(f)

    dead = set(scanned) - alive - test_reach
    test_only = test_reach - alive

    apirouter_files = find_apirouter_files(scanned)
    # ORPHAN = declares an APIRouter but no production code path can reach it
    # (i.e. not in the ALIVE set, even transitively through domain bundlers).
    orphan_routers = sorted(apirouter_files - alive)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    lines.append("# Dead-module inventory — 2026-05-22")
    lines.append("")
    lines.append(
        f"Scanned: {', '.join(f'`{d}/`' for d in SCAN_DIRS)} against roots "
        f"`api/main.py` + `scripts/` + `tests/`."
    )
    lines.append("Generated by `scripts/audit_dead_modules.py` (pure-stdlib `ast` analyzer).")
    lines.append("")
    lines.append(f"- **ALIVE**: {len(alive)} modules (reachable from `api/main.py` or any script)")
    lines.append(f"- **TEST_ONLY**: {len(test_only)} modules (used only by `tests/`)")
    lines.append(f"- **DEAD**: {len(dead)} modules (no internal reference)")
    lines.append(f"- **ORPHAN_ROUTER**: {len(orphan_routers)} files declare `APIRouter()` but `api/main.py` never imports them")
    lines.append("")

    def emit(title: str, files: list[Path]) -> None:
        lines.append(f"## {title} ({len(files)})")
        lines.append("")
        if not files:
            lines.append("_None._")
            lines.append("")
            return
        lines.append("| Path | Top symbol |")
        lines.append("|------|------------|")
        for f in files:
            rel = f.relative_to(REPO_ROOT)
            sym = first_top_symbol(f).replace("|", "\\|")
            lines.append(f"| `{rel}` | `{sym}` |")
        lines.append("")

    emit("ORPHAN_ROUTER — declares `APIRouter` but never imported by `api/main.py`", orphan_routers)
    emit("DEAD — zero internal references", sorted(dead))
    emit("TEST_ONLY — used only by `tests/`", sorted(test_only))
    emit("ALIVE — reachable from `api/main.py` or any script", sorted(alive))

    OUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT_PATH.relative_to(REPO_ROOT)}")
    print(
        f"alive={len(alive)} test_only={len(test_only)} dead={len(dead)} "
        f"orphan_routers={len(orphan_routers)}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
