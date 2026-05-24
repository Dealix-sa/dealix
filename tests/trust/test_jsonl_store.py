"""Tests for dealix.trust._jsonl_store.JsonlStore."""

from __future__ import annotations

from pathlib import Path

import pytest

from dealix.trust._jsonl_store import JsonlStore


def test_append_and_load(tmp_path: Path) -> None:
    store = JsonlStore(tmp_path / "approvals.jsonl")
    store.append({"id": "a", "n": 1})
    store.append({"id": "b", "n": 2})
    loaded = store.load_list()
    assert loaded == [{"id": "a", "n": 1}, {"id": "b", "n": 2}]


def test_replace_all_is_atomic(tmp_path: Path) -> None:
    store = JsonlStore(tmp_path / "evidence.jsonl")
    store.append({"id": "old"})
    store.replace_all([{"id": "x"}, {"id": "y"}])
    loaded = store.load_list()
    assert loaded == [{"id": "x"}, {"id": "y"}]
    # Confirm no leftover .tmp temp files survived in the directory.
    leftovers = [p for p in tmp_path.iterdir() if p.suffix == ".tmp"]
    assert leftovers == []


def test_load_when_file_missing_yields_nothing(tmp_path: Path) -> None:
    store = JsonlStore(tmp_path / "does-not-exist.jsonl")
    assert store.exists() is False
    assert store.load_list() == []


def test_recover_from_partial_line(tmp_path: Path) -> None:
    path = tmp_path / "partial.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        handle.write('{"id": "ok"}\n')
        # Truncated / corrupt second line — must be skipped, not crash.
        handle.write('{"id": "broken", "x":\n')
        handle.write('{"id": "ok2"}\n')
    store = JsonlStore(path)
    loaded = store.load_list()
    assert loaded == [{"id": "ok"}, {"id": "ok2"}]


def test_ensure_parent_creates_nested(tmp_path: Path) -> None:
    nested = tmp_path / "deep" / "deeper" / "store.jsonl"
    store = JsonlStore(nested)
    assert store.ensure_parent() is True
    assert nested.parent.exists()
