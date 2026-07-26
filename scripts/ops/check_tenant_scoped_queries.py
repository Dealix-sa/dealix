#!/usr/bin/env python3
"""Fail when a tenant-owned record is queried by ID without a tenant filter.

This is the defect class behind the PDPL, ZATCA and background-jobs
cross-tenant findings: a handler selects a record whose table has a
``tenant_id`` column, filters only on the object's own ID, and returns it.
Every object ID then becomes a cross-tenant handle, because an ID guessed
or leaked from anywhere reaches the row it names regardless of who owns it.

The rule this enforces:

    If a statement selects a model that has a ``tenant_id`` column and
    filters it by an ID, the same statement must also constrain
    ``<Model>.tenant_id``.

Analysis is AST-based, so it is not fooled by formatting or line breaks.
It is deliberately narrow — it flags the exact shape that caused real
leaks and stays quiet elsewhere, because a guard that cries wolf gets
disabled.

The repository carries a backlog of pre-existing violations, tracked in
issue #974. Fixing them all at once would be an unreviewable change, so
this runs as a ratchet: everything already known is recorded in
``tenant_scoped_queries_baseline.txt`` and the gate fails only on queries
that are *new*. The baseline is allowed to shrink and never to grow.

Usage:
    python3 scripts/ops/check_tenant_scoped_queries.py [paths...]
    python3 scripts/ops/check_tenant_scoped_queries.py --write-baseline

Exit codes:
    0  no new violations
    1  at least one new unscoped query
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

# Default scan scope: the HTTP surface, where an attacker-supplied ID lands.
DEFAULT_PATHS = ("api/routers",)

BASELINE_PATH = Path(__file__).with_name("tenant_scoped_queries_baseline.txt")

# Reviewed exceptions. Each entry must say why the query is safe without a
# tenant predicate — an unexplained entry here is how a guard rots.
ALLOWLIST: dict[tuple[str, str], str] = {
    (
        "api/routers/auth.py",
        "UserRecord",
    ): (
        "Self-scoped: the user id comes from an already-verified refresh "
        "token, so the lookup can only reach the token's own user."
    ),
}


def tenant_owned_models() -> set[str]:
    """Names of mapped classes whose table carries a ``tenant_id`` column."""
    from db.models import Base

    return {
        mapper.class_.__name__
        for mapper in Base.registry.mappers
        if "tenant_id" in mapper.class_.__table__.columns
    }


def _names_used(node: ast.AST) -> set[str]:
    """``{"ContactRecord.tenant_id", ...}`` for every attribute access below."""
    out: set[str] = set()
    for child in ast.walk(node):
        if isinstance(child, ast.Attribute) and isinstance(child.value, ast.Name):
            out.add(f"{child.value.id}.{child.attr}")
    return out


def _is_select(call: ast.Call) -> bool:
    func = call.func
    name = func.id if isinstance(func, ast.Name) else getattr(func, "attr", "")
    return name == "select"


def _selected_models(node: ast.AST, models: set[str]) -> set[str]:
    """Tenant-owned models passed to a ``select(...)`` call below ``node``."""
    out: set[str] = set()
    for child in ast.walk(node):
        if not isinstance(child, ast.Call):
            continue
        func = child.func
        name = func.id if isinstance(func, ast.Name) else getattr(func, "attr", "")
        if name != "select":
            continue
        for arg in child.args:
            if isinstance(arg, ast.Name) and arg.id in models:
                out.add(arg.id)
            elif isinstance(arg, ast.Attribute) and isinstance(arg.value, ast.Name):
                if arg.value.id in models:
                    out.add(arg.value.id)
    return out


def scan_file(path: Path, models: set[str]) -> list[tuple[int, str]]:
    """Return ``(line, model)`` for each unscoped tenant-owned query."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except SyntaxError as exc:  # pragma: no cover - surfaced to the operator
        print(f"{path}: could not parse: {exc}", file=sys.stderr)
        return []

    parent: dict[int, ast.AST] = {}
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            parent[id(child)] = node

    def innermost_statement(node: ast.AST) -> ast.stmt | None:
        """The nearest enclosing statement — the scope holding the filters."""
        current: ast.AST | None = node
        while current is not None and not isinstance(current, ast.stmt):
            current = parent.get(id(current))
        return current if isinstance(current, ast.stmt) else None

    # Judge each select() once, in the statement that directly owns it. A
    # query nested in a `with`/`try` must not be re-judged for every wrapper
    # around it, and a whole function body must never be treated as one
    # scope — that would let one filtered query mask an unfiltered neighbour.
    violations: set[tuple[int, str]] = set()
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call) and _is_select(node)):
            continue
        selected = _selected_models(node, models)
        if not selected:
            continue
        statement = innermost_statement(node)
        if statement is None:
            continue

        attributes = _names_used(statement)
        for model in selected:
            filters_by_id = any(
                attr.startswith(f"{model}.") and attr.endswith("id")
                for attr in attributes
            )
            if not filters_by_id:
                continue
            if f"{model}.tenant_id" in attributes:
                continue
            violations.add((statement.lineno, model))

    return sorted(violations)


def load_baseline() -> set[str]:
    """Known, already-tracked violations. Absent file means an empty set."""
    if not BASELINE_PATH.exists():
        return set()
    return {
        line.strip()
        for line in BASELINE_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    }


def collect(files: list[Path], models: set[str]) -> list[tuple[str, int, str]]:
    found: list[tuple[str, int, str]] = []
    for path in files:
        rel = path.relative_to(REPO_ROOT).as_posix()
        for line, model in scan_file(path, models):
            if (rel, model) in ALLOWLIST:
                continue
            found.append((rel, line, model))
    return found


def _resolve_files(argv: list[str]) -> list[Path]:
    args = [a for a in argv[1:] if not a.startswith("--")]
    targets = [Path(a) for a in args] or [REPO_ROOT / p for p in DEFAULT_PATHS]
    files: list[Path] = []
    for target in targets:
        target = target if target.is_absolute() else REPO_ROOT / target
        files.extend(sorted(target.rglob("*.py")) if target.is_dir() else [target])
    return files


def main(argv: list[str]) -> int:
    sys.path.insert(0, str(REPO_ROOT))
    models = tenant_owned_models()
    files = _resolve_files(argv)
    found = collect(files, models)

    # A violation is identified by file and model, not by line number, so
    # unrelated edits that shift lines do not spuriously fail the gate.
    keys = {f"{rel}::{model}" for rel, _line, model in found}

    # Baseline bookkeeping is only meaningful over the full default scope. A
    # partial scan sees none of the other entries and would otherwise call
    # them fixed — regenerating from that would silently drop live findings.
    scanned = {path.relative_to(REPO_ROOT).as_posix() for path in files}
    full_scope = not [a for a in argv[1:] if not a.startswith("--")]

    if "--write-baseline" in argv:
        if not full_scope:
            print(
                "refusing to write the baseline from a partial scan: run with "
                "no path arguments so every tracked entry is re-checked.",
                file=sys.stderr,
            )
            return 1
        BASELINE_PATH.write_text(
            "# Pre-existing unscoped tenant queries — see issue #974.\n"
            "# This list may shrink. It must never grow: a new entry means a\n"
            "# fresh cross-tenant hole. Regenerate only when removing fixed\n"
            "# entries, never to silence a new one.\n"
            + "".join(f"{k}\n" for k in sorted(keys)),
            encoding="utf-8",
        )
        print(f"baseline written: {len(keys)} entries -> {BASELINE_PATH.name}")
        return 0

    baseline = load_baseline()
    new = sorted(keys - baseline)
    # Only an entry whose file this run actually scanned can be called fixed.
    fixed = sorted(
        entry
        for entry in baseline - keys
        if entry.split("::", 1)[0] in scanned
    )

    for rel, line, model in sorted(found):
        if f"{rel}::{model}" not in new:
            continue
        print(
            f"{rel}:{line}: select({model}) is filtered by id with no "
            f"{model}.tenant_id predicate — an ID from another tenant "
            f"would reach this row."
        )

    print(
        f"TENANT_SCOPED_QUERY_GATE={'FAIL' if new else 'PASS'} "
        f"files={len(files)} new={len(new)} baseline={len(baseline)} "
        f"fixed_since_baseline={len(fixed)}"
    )
    if fixed:
        print(
            "Fixed since the baseline was written — remove from the baseline "
            "with --write-baseline: " + ", ".join(fixed)
        )
    if new:
        print(
            "\nResolve by taking the tenant from the authenticated user via "
            "api/security/tenant_scope.py:resolve_tenant_for_user and adding "
            "it to the query, so a row outside the tenant is simply not "
            "found. If the query is genuinely safe, add it to ALLOWLIST in "
            "this script with the reason. Do NOT regenerate the baseline to "
            "silence it.",
            file=sys.stderr,
        )
    return 1 if new else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
