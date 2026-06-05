"""V10 — enterprise_sales_room_generate writes 7 draft documents, no fake certs."""

from __future__ import annotations

import importlib.util
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
_SCRIPT = REPO / "scripts" / "enterprise_sales_room_generate.py"


def _load():
    spec = importlib.util.spec_from_file_location("enterprise_sales_room_generate", _SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_slugify() -> None:
    mod = _load()
    assert mod.slugify("Acme Trading Co.") == "acme-trading-co"


def test_main_writes_seven_drafts(tmp_path: Path) -> None:
    mod = _load()
    rc = mod.main(["--company", "Acme Co", "--date", "2026-01-01", "--out-root", str(tmp_path)])
    assert rc == 0
    out_dir = tmp_path / "2026-01-01" / "acme-co"
    files = sorted(p.name for p in out_dir.glob("*.md"))
    assert files == sorted(
        [
            "stakeholder_map.md",
            "business_case.md",
            "executive_proposal.md",
            "security_legal_pack.md",
            "procurement_pack.md",
            "pilot_governance.md",
            "close_plan.md",
        ]
    )


def test_no_fake_security_certs() -> None:
    mod = _load()
    pack = mod.build_pack("Acme Co")
    sec = pack["security_legal_pack.md"].lower()
    # Must not affirmatively claim certifications that do not exist.
    assert "iso 27001 certified" not in sec
    assert "soc 2 certified" not in sec
    assert "DRAFT" in pack["security_legal_pack.md"]
