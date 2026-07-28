"""Tests for the verify_*.py catalog builder.

Pure stdlib — does not need the async pytest stack, so it can run standalone:
    python3 -m pytest tests/test_verify_catalog.py
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "ops" / "build_verify_catalog.py"

_spec = importlib.util.spec_from_file_location("build_verify_catalog", MODULE_PATH)
assert _spec and _spec.loader
catalog = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(catalog)


def test_catalog_covers_every_verify_script() -> None:
    scripts = {p.name for p in catalog.SCRIPTS_DIR.glob("verify_*.py")}
    rows = catalog.collect_rows()
    cataloged = {name for name, _purpose in rows}
    assert cataloged == scripts


def test_committed_catalog_is_in_sync() -> None:
    rows = catalog.collect_rows()
    rendered = catalog.render(rows)
    assert catalog.CATALOG_PATH.exists(), f"missing {catalog.CATALOG_PATH}"
    assert catalog.CATALOG_PATH.read_text(encoding="utf-8") == rendered


def test_no_docstring_scripts_are_flagged_not_guessed() -> None:
    rows = catalog.collect_rows()
    for name, purpose in rows:
        if purpose == catalog.NO_DOCSTRING:
            path = catalog.SCRIPTS_DIR / name
            source = path.read_text(encoding="utf-8")
            import ast

            tree = ast.parse(source)
            assert ast.get_docstring(tree) is None
