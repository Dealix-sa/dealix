"""V10 — ceo_cockpit_generate composes a single-screen cockpit (no external send)."""

from __future__ import annotations

import importlib.util
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
_SCRIPT = REPO / "scripts" / "ceo_cockpit_generate.py"


def _load():
    spec = importlib.util.spec_from_file_location("ceo_cockpit_generate", _SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_script_exists() -> None:
    assert _SCRIPT.is_file()


def test_main_writes_cockpit(tmp_path: Path) -> None:
    mod = _load()
    out = tmp_path / "CEO_COCKPIT.md"
    rc = mod.main(["--out", str(out)])
    assert rc == 0
    text = out.read_text(encoding="utf-8")
    assert "CEO Cockpit" in text


def test_cockpit_has_required_sections() -> None:
    mod = _load()
    text = mod.build_cockpit("2026-01-01 00:00 UTC")
    for section in (
        "Decision Queue",
        "Risk Queue",
        "Opportunity Queue",
        "Next Actions",
        "Finance Assumptions",
        "NO-GO",
    ):
        assert section in text, f"missing cockpit section: {section}"


def test_cockpit_states_no_external_send() -> None:
    mod = _load()
    text = mod.build_cockpit("2026-01-01 00:00 UTC")
    assert "لا يرسل خارجيًا" in text
    assert "ممنوع" in text
