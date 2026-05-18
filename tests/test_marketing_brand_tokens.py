"""Smoke tests for marketing brand tokens and GTM asset tree."""

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
MS = REPO_ROOT / "docs" / "marketing-system"
TOKENS_PATH = MS / "brand" / "brand-tokens.yaml"

GTM_MANIFEST = [
    MS / "FOUNDER_GTM_PLAYBOOK.md",
    MS / "brand" / "brand-tokens.yaml",
    MS / "brand" / "BRAND_KIT.md",
    MS / "brand" / "marketing-shared.css",
    MS / "presentations" / "live-deck-b2b-ar.md",
    MS / "presentations" / "leave-behind-b2b-ar.md",
    MS / "presentations" / "appendix-technical-ar.md",
    MS / "presentations" / "RTL_QA_CHECKLIST.md",
    MS / "presentations" / "committee" / "cfo-slide-ar.md",
    MS / "presentations" / "committee" / "it-slide-ar.md",
    MS / "presentations" / "committee" / "revops-slide-ar.md",
    MS / "collateral" / "executive-one-pager-ar.md",
    MS / "collateral" / "executive-one-pager-ar.html",
    MS / "collateral" / "founder-story-ar.md",
    MS / "sales-enablement" / "discovery-script-ar.md",
    MS / "sales-enablement" / "mutual-close-checklist-ar.md",
    MS / "email-sequences" / "post-discovery-ar.md",
    MS / "linkedin" / "post-templates-ar.md",
    MS / "fundraising" / "investor-deck-outline-ar.md",
    MS / "web" / "landing-hero-copy-ar.md",
    MS / "digital-sales-room" / "hub.html",
    MS / "digital-sales-room" / "MAP_TEMPLATE.md",
]


def test_brand_tokens_yaml_loads():
    data = yaml.safe_load(TOKENS_PATH.read_text(encoding="utf-8"))
    assert data["version"]
    assert data["colors"]["deep_green"] == "#0A4D3F"
    assert data["colors"]["gold"] == "#C9A961"


def test_brand_tokens_typography_arabic():
    data = yaml.safe_load(TOKENS_PATH.read_text(encoding="utf-8"))
    assert "IBM Plex Sans Arabic" in data["typography"]["arabic"]["family"]


def test_gtm_manifest_files_exist():
    missing = [p for p in GTM_MANIFEST if not p.is_file()]
    assert not missing, f"missing GTM files: {missing}"


def test_leave_behind_has_twelve_action_titles():
    text = (MS / "presentations" / "leave-behind-b2b-ar.md").read_text(encoding="utf-8")
    numbered = [line for line in text.splitlines() if line.strip() and line.strip()[0].isdigit() and ". " in line[:4]]
    assert len(numbered) >= 12


def test_founder_playbook_references_production_smoke():
    text = (MS / "FOUNDER_GTM_PLAYBOOK.md").read_text(encoding="utf-8")
    assert "verify_railway_production_config" in text
    assert "healthz" in text
