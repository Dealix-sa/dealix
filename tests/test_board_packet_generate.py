"""V10 — board_packet_generate writes a packet with all mandatory sections."""

from __future__ import annotations

import importlib.util
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
_SCRIPT = REPO / "scripts" / "board_packet_generate.py"


def _load():
    spec = importlib.util.spec_from_file_location("board_packet_generate", _SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_main_writes_packet(tmp_path: Path) -> None:
    mod = _load()
    rc = mod.main(["--month", "2026-01", "--out-root", str(tmp_path)])
    assert rc == 0
    out = tmp_path / "2026-01" / "BOARD_PACKET.md"
    assert out.is_file()


def test_packet_has_mandatory_sections() -> None:
    mod = _load()
    text = mod.build_packet("2026-01")
    for section in (
        "Executive Summary",
        "Revenue Activity",
        "Pipeline Quality",
        "Delivery Status",
        "Product Progress",
        "Risks",
        "Cash Assumptions",
        "Hiring Triggers",
        "Decisions Required",
        "Evidence Links",
        "No Fake Traction",
    ):
        assert section in text, f"missing board section: {section}"
