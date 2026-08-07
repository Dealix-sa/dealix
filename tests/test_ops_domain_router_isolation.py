"""Ops domain aggregation must isolate one degraded optional subrouter."""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from fastapi import APIRouter

from api.routers.domains import ops


def test_one_import_failure_does_not_drop_other_ops_routers(monkeypatch) -> None:
    monkeypatch.delenv("DEALIX_STRICT_OPTIONAL_ROUTERS", raising=False)
    expected: list[APIRouter] = []

    def _fake_import(module_path: str) -> SimpleNamespace:
        if module_path.endswith("ops_knowledge"):
            raise OSError("simulated read-only filesystem")
        router = APIRouter()
        expected.append(router)
        return SimpleNamespace(router=router)

    monkeypatch.setattr(ops.importlib, "import_module", _fake_import)

    assert ops.get_routers() == expected
    assert len(expected) == len(ops._ROUTER_MODULES) - 1


def test_strict_mode_still_fails_fast(monkeypatch) -> None:
    monkeypatch.setenv("DEALIX_STRICT_OPTIONAL_ROUTERS", "1")

    def _fail_import(module_path: str) -> SimpleNamespace:
        raise OSError(f"simulated failure for {module_path}")

    monkeypatch.setattr(ops.importlib, "import_module", _fail_import)

    with pytest.raises(RuntimeError, match="Optional Ops subrouter failed to import"):
        ops.get_routers()
