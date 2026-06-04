"""Guardrail tests: the Commercial Launch OS must never send anything externally.

These tests are deliberately strict. If any of them fail, the system is no
longer review-only and must NOT be shipped.
"""

from __future__ import annotations

import json
from pathlib import Path

from dealix.commercial_launch.engine import (
    ROOT,
    generate_drafts,
    load_config,
)
from dealix.commercial_launch.safety import scan_files

COMMERCIAL_SOURCES = list((ROOT / "dealix" / "commercial_launch").glob("*.py")) + list(
    (ROOT / "scripts").glob("commercial_generate_400_drafts.py")
) + list((ROOT / "scripts").glob("commercial_founder_review_report.py")) + list(
    (ROOT / "scripts").glob("commercial_safety_audit.py")
) + list((ROOT / "scripts").glob("commercial_launch_readiness.py")) + list(
    (ROOT / "scripts").glob("commercial_seed_leads_validate.py")
)


def test_no_active_send_imports_in_sources() -> None:
    report = scan_files(ROOT)
    assert report.passed, [f.__dict__ for f in report.findings]


def test_no_actual_network_send_calls() -> None:
    # No commercial-launch source may import a real mail/automation client.
    bad_imports = [
        "import " + "smtp" + "lib",
        "from " + "smtp" + "lib",
        "import " + "send" + "grid",
        "import " + "sele" + "nium",
        "from " + "play" + "wright",
    ]
    for src in COMMERCIAL_SOURCES:
        text = src.read_text(encoding="utf-8")
        for bad in bad_imports:
            assert bad not in text, f"{src.name} contains forbidden import: {bad}"


def test_generated_drafts_all_blocked() -> None:
    result = generate_drafts(target=400, seed=21, run_date="2026-01-01")
    for d in result.accepted:
        assert d["send_allowed"] is False
        assert d["external_send_blocked"] is True
        assert d["requires_founder_approval"] is True


def test_config_declares_send_blocked() -> None:
    cfg = load_config()
    gp = cfg["channels"]["global_policy"]
    assert gp["external_send"] == "BLOCKED"
    assert gp["auto_send"] == "BLOCKED"
    assert cfg["launch"]["safety"]["external_send_blocked"] is True
    assert cfg["launch"]["safety"]["auto_send_blocked"] is True


def test_whatsapp_is_never_cold_outreach() -> None:
    cfg = load_config()
    wa = next(c for c in cfg["channels"]["channels"] if c["id"] == "whatsapp")
    assert wa["cold_outreach"] == "FORBIDDEN"
    assert wa["status_on_draft"] == "manual_review_only"


def test_linkedin_forbids_automation() -> None:
    cfg = load_config()
    li = next(c for c in cfg["channels"]["channels"] if c["id"] == "linkedin_manual")
    for forbidden in ("browser_automation", "scraping", "auto_connect", "auto_message", "bots"):
        assert forbidden in li["forbidden"]


def test_workflow_has_no_secrets() -> None:
    wf = ROOT / ".github" / "workflows" / "commercial-draft-factory.yml"
    if wf.exists():
        text = wf.read_text(encoding="utf-8")
        assert "secrets." not in text, "workflow must not reference any secrets"
