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

# Scan scope. This began as `api/routers` alone — the HTTP surface, where an
# attacker-supplied ID lands. That was too narrow: a request-supplied id does
# not stop being attacker-controlled when it is handed to a background worker
# or a service layer. Widening it surfaced a live cross-tenant *write* in
# core/memory/embedding_service.py, reached through a job payload rather than
# a URL, which no amount of router coverage would ever have caught.
#
# `db/` is deliberately absent: model definitions and migrations are where the
# tenant columns are declared, not where rows are fetched by id.
DEFAULT_PATHS = (
    "api",
    "core",
    "dealix",
    "company",
    "auto_client_acquisition",
    "autonomous_growth",
    "integrations",
    "platform_core",
)

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
    (
        "api/routers/auth.py",
        "RefreshTokenRecord",
    ): (
        "Self-scoped: keyed on the hash of the presented token plus the user "
        "id from that same verified token. The token is the credential — "
        "holding it is what the query checks."
    ),
    (
        "api/routers/auth.py",
        "RoleRecord",
    ): (
        "Self-scoped: the role id comes from the loaded user's own role_id, "
        "and only the role name is returned."
    ),
    (
        "api/security/auth_deps.py",
        "UserRecord",
    ): (
        "Identity establishment: the user id is the `sub` claim of an "
        "already-verified JWT, not a caller-supplied handle. This query is "
        "how the request's tenant is discovered, so requiring a tenant "
        "predicate on it would be circular — there is no tenant yet."
    ),
    (
        "api/security/auth_deps.py",
        "RoleRecord",
    ): (
        "Self-scoped: the role id comes from the loaded user's own role_id, "
        "and only the role name is returned. Same shape as the entry for "
        "api/routers/auth.py."
    ),
    (
        "core/memory/embedding_service.py",
        "AccountEmbeddingRecord",
    ): (
        "No tenant boundary exists to enforce: account_embeddings.account_id "
        "is unique, so there is exactly one row per account platform-wide, "
        "and the accounts table carries no tenant_id at all. tenant_id here "
        "records who indexed the row, not who owns it. Adding the predicate "
        "would make a second tenant's upsert miss the row and violate the "
        "unique constraint. The gap is in the schema — an embedding table "
        "with tenant_id over a base table without one — and belongs to a "
        "migration, not to this query. Contrast index_conversation in the "
        "same file, where conversation_id is NOT unique and the predicate is "
        "both required and safe."
    ),
    (
        "dealix/billing/service.py",
        "SubscriptionRecord",
    ): (
        "Internal primitive, never reached with a caller-supplied id: every "
        "route in api/routers/billing.py resolves the subscription through "
        "get_active_subscription_for_tenant(tenant_id) first and passes that "
        "record's own id. Re-check this entry if a router ever accepts a "
        "subscription_id from a request."
    ),
    (
        "platform_core/stores.py",
        "RoleRecord",
    ): (
        "Rollback of fixtures the same enterprise-loop run created: the "
        "role_ids are threaded in alongside the tenant_id being rolled back, "
        "not read from a request. Cleanup path, not a handler."
    ),
    (
        "core/queue/tasks.py",
        "BackgroundJobRecord",
    ): (
        "Worker-side status writer: the job id is the one the queue handed "
        "this worker, not an id from a request, and the write only sets "
        "status/output/error/timestamps on that same row. There is no user "
        "identity in a worker context to scope by; the tenant boundary for "
        "jobs is enforced where they are created and read "
        "(api/routers/jobs.py, tests/test_jobs_tenant_isolation.py)."
    ),
    (
        "api/routers/pricing.py",
        "PaymentRecord",
    ): (
        "Provider-keyed idempotency: reached only from the Moyasar webhook "
        "after verify_webhook(), and keyed on the provider's globally unique "
        "payment id. No caller-supplied handle is involved."
    ),
    # Founder-internal tooling. These routers read and write the whole
    # prospecting graph across tenants by design, and are gated at the router
    # by require_admin_key — the platform-admin credential, not a tenant one.
    # A tenant predicate here would be meaningless; the guard is the auth.
    **{
        (f"api/routers/{module}.py", "ContactRecord"): (
            "Cross-tenant by design; gated at the router by require_admin_key "
            "(platform-admin only, verified in "
            "tests/test_founder_tools_admin_gate.py)."
        )
        for module in (
            "automation",
            "data",
            "dominance",
            "drafts",
            "email_send",
            "outreach",
        )
    },
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


def _rel(path: Path) -> str:
    """Repo-relative path, falling back to the absolute one.

    The script accepts arbitrary paths on the command line, so a target
    outside the repository is a supported invocation. ``relative_to`` raises
    for those, which turned an ordinary ad-hoc scan into a traceback.
    """
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


class UnparseableSource(Exception):
    """A file in scope could not be parsed, so it was never actually checked."""


def scan_file(path: Path, models: set[str]) -> list[tuple[int, str]]:
    """Return ``(line, model)`` for each unscoped tenant-owned query.

    Raises:
        UnparseableSource: the file could not be parsed. A file that cannot be
            parsed has not been checked, and a guard that reports PASS over
            files it never read is worse than no guard — so this is raised
            rather than warned about. Four files in ``dealix/`` carry a UTF-8
            BOM and used to land here silently.
    """
    # utf-8-sig, not utf-8: a leading BOM decodes to U+FEFF under plain utf-8
    # and ast.parse rejects it as a non-printable character on line 1.
    try:
        source = path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeDecodeError) as exc:
        raise UnparseableSource(f"{path}: could not read: {exc}") from exc

    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        raise UnparseableSource(f"{path}: could not parse: {exc}") from exc

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

    # `session.get(Model, some_id)` is the same fetch-by-ID with none of the
    # syntax the rule above looks for — no select(), no .where() — so it was
    # invisible to this gate entirely. It cannot carry a tenant predicate, so
    # the check has to follow the call, as api/routers/billing.py:pay_invoice
    # does: `if invoice is None or invoice.tenant_id != tenant_id: 404`.
    #
    # The rule is therefore function-scoped and deliberately loose: any
    # mention of `.tenant_id` anywhere in the enclosing function counts as the
    # guard. A tighter rule would flag correct code, and a gate that cries
    # wolf gets disabled — the same reasoning as the narrowness of the select
    # rule above.
    for node in ast.walk(tree):
        if not (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "get"
            and node.args
        ):
            continue
        first = node.args[0]
        model = first.id if isinstance(first, ast.Name) else None
        if model not in models:
            continue

        function = _enclosing_function(node, parent)
        if function is not None and any(
            isinstance(child, ast.Attribute) and child.attr == "tenant_id"
            for child in ast.walk(function)
        ):
            continue
        violations.add((node.lineno, model))

    return sorted(violations)


def _enclosing_function(
    node: ast.AST, parent: dict[int, ast.AST]
) -> ast.FunctionDef | ast.AsyncFunctionDef | None:
    current: ast.AST | None = node
    while current is not None:
        current = parent.get(id(current))
        if isinstance(current, ast.FunctionDef | ast.AsyncFunctionDef):
            return current
    return None


def load_baseline() -> set[str]:
    """Known, already-tracked violations. Absent file means an empty set."""
    if not BASELINE_PATH.exists():
        return set()
    return {
        line.strip()
        for line in BASELINE_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    }


def collect(
    files: list[Path], models: set[str]
) -> tuple[list[tuple[str, int, str]], list[str]]:
    """Scan ``files``; return ``(findings, unparseable)``.

    Unparseable files are returned rather than swallowed so the caller can fail
    on them. Previously they were printed to stderr and the gate still exited
    0, which meant PASS could be reported over files nobody had read.
    """
    found: list[tuple[str, int, str]] = []
    unparseable: list[str] = []
    for path in files:
        rel = _rel(path)
        try:
            hits = scan_file(path, models)
        except UnparseableSource as exc:
            unparseable.append(str(exc))
            continue
        for line, model in hits:
            if (rel, model) in ALLOWLIST:
                continue
            found.append((rel, line, model))
    return found, unparseable


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
    found, unparseable = collect(files, models)

    # A violation is identified by file and model, not by line number, so
    # unrelated edits that shift lines do not spuriously fail the gate.
    keys = {f"{rel}::{model}" for rel, _line, model in found}

    # Baseline bookkeeping is only meaningful over the full default scope. A
    # partial scan sees none of the other entries and would otherwise call
    # them fixed — regenerating from that would silently drop live findings.
    scanned = {_rel(path) for path in files}
    full_scope = not [a for a in argv[1:] if not a.startswith("--")]

    if "--write-baseline" in argv:
        if not full_scope:
            print(
                "refusing to write the baseline from a partial scan: run with "
                "no path arguments so every tracked entry is re-checked.",
                file=sys.stderr,
            )
            return 1
        if not keys:
            # Nothing left to hold back. A comment-only file would read as
            # though a ratchet were still in place, so remove it instead.
            if BASELINE_PATH.exists():
                BASELINE_PATH.unlink()
                print(f"backlog empty — removed {BASELINE_PATH.name}")
            else:
                print("backlog empty — no baseline needed")
            return 0
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
            f"{rel}:{line}: {model} is fetched by id with no "
            f"{model}.tenant_id check — an ID from another tenant "
            f"would reach this row."
        )

    for message in unparseable:
        print(message, file=sys.stderr)

    print(
        f"TENANT_SCOPED_QUERY_GATE="
        f"{'FAIL' if (new or unparseable) else 'PASS'} "
        f"files={len(files)} new={len(new)} baseline={len(baseline)} "
        f"fixed_since_baseline={len(fixed)} unparseable={len(unparseable)}"
    )
    if unparseable:
        print(
            "A file in scope could not be parsed, so it was not checked. "
            "Reporting PASS over unread files is how a guard goes quietly "
            "blind — fix the file rather than narrowing the scan.",
            file=sys.stderr,
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
    return 1 if (new or unparseable) else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
