"""V10 — institutional_scale_verify returns PASS and writes its verification JSON."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
_SCRIPT = REPO / "scripts" / "institutional_scale_verify.py"


def _load():
    spec = importlib.util.spec_from_file_location("institutional_scale_verify", _SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_script_exists() -> None:
    assert _SCRIPT.is_file()


def test_verify_passes_and_writes_json() -> None:
    mod = _load()
    rc = mod.main([])
    assert rc == 0, "expected PASS (exit 0)"
    from v10_specs import SPECS

    out = REPO / SPECS[mod.KEY]["json"]
    assert out.is_file()
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["verdict"] == "PASS"
    assert payload["forbidden_hits"] == []
