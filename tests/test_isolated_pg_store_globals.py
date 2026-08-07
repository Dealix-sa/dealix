"""The isolated Postgres store accessor must survive its second call.

``get_isolated_sync_postgres_store`` declared::

    global _worker_thread, _store_singleton

but assigned ``_worker_loop``, ``_worker_engine`` and ``_worker_inner`` in its
reset block. Without the declaration those assignments made the names *local*
for the whole function, which broke it two ways:

1. The guard ``_store_singleton is not None and _worker_loop is not None``
   raised ``UnboundLocalError`` — but only from the **second** call onward,
   because ``and`` short-circuits while ``_store_singleton`` is still None.
   The singleton accessor therefore worked exactly once: green in a smoke
   test, broken on the second request.
2. The reset never reached module state, so restarting the worker left the
   previous loop, engine and store in place.

Reproduced before fixing::

    first call : built
    second call: UnboundLocalError -> cannot access local variable
                 '_worker_loop' where it is not associated with a value

Ruff reports this as F823, and it went unflagged because
``auto_client_acquisition`` was outside the CI lint scope — the same gap that
hid the sentiment bug in ``core``. Both packages are in scope now.

These tests read the function's declarations rather than starting a real
Postgres worker, so they run without a database.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

MODULE = Path(__file__).resolve().parents[1] / (
    "auto_client_acquisition/revenue_memory/isolated_pg_event_store.py"
)

# Names the function both reads and assigns; each must be declared global.
WORKER_GLOBALS = ["_worker_loop", "_worker_engine", "_worker_inner"]


def _function(name: str) -> ast.FunctionDef:
    tree = ast.parse(MODULE.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name == name:
            return node
    raise AssertionError(f"{name} not found in {MODULE.name}")


def _declared_globals(func: ast.AST) -> set[str]:
    return {
        name
        for node in ast.walk(func)
        if isinstance(node, ast.Global)
        for name in node.names
    }


def _assigned_names(func: ast.AST) -> set[str]:
    return {
        target.id
        for node in ast.walk(func)
        if isinstance(node, ast.Assign)
        for target in node.targets
        if isinstance(target, ast.Name)
    }


@pytest.mark.parametrize("name", WORKER_GLOBALS)
def test_worker_state_is_declared_global(name):
    """The regression: assigning without declaring made the name local."""
    func = _function("get_isolated_sync_postgres_store")

    assert name in _declared_globals(func), (
        f"{name} is assigned in get_isolated_sync_postgres_store but not "
        f"declared global — the read above it raises UnboundLocalError on "
        f"the second call, and the reset never reaches module state"
    )


def test_every_name_the_accessor_assigns_is_declared_global():
    """Catches the next one, not just the three known names."""
    func = _function("get_isolated_sync_postgres_store")
    module_level = {
        "_worker_loop",
        "_worker_engine",
        "_worker_inner",
        "_worker_thread",
        "_store_singleton",
    }

    undeclared = (_assigned_names(func) & module_level) - _declared_globals(func)

    assert not undeclared, f"assigned but not declared global: {sorted(undeclared)}"


def test_shutdown_declares_everything_it_resets():
    """The teardown path has the same failure mode if a name is missed."""
    func = _function("shutdown_isolated_postgres_revenue_worker")
    module_level = {
        "_worker_loop",
        "_worker_engine",
        "_worker_inner",
        "_worker_thread",
        "_store_singleton",
    }

    undeclared = (_assigned_names(func) & module_level) - _declared_globals(func)

    assert not undeclared, f"assigned but not declared global: {sorted(undeclared)}"
