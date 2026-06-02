"""Contract: the Market Production OS layer is internally consistent + doctrine-safe.

Mirrors `scripts/verify_market_production_os.py`. Keeps the docs, schemas, and
synthetic example data in lock-step, and asserts the load-bearing doctrine
invariants (no send without unsubscribe; 250 drafts != 250 sends).
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
VERIFIER = REPO_ROOT / "scripts" / "verify_market_production_os.py"


def _load_verifier():
    spec = importlib.util.spec_from_file_location("verify_market_production_os", VERIFIER)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_market_production_os_verifier_passes() -> None:
    ok, errors, _info = _load_verifier().run_checks()
    assert ok, "Market Production OS verifier failed:\n" + "\n".join(errors)


def test_all_schemas_have_canonical_id() -> None:
    files = list((REPO_ROOT / "schemas").glob("*.schema.json"))
    assert len(files) >= 8, "expected the 8 Market Production OS schemas"
    for path in files:
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["$id"].startswith("https://dealix.sa/schemas/"), path.name
        assert "2020-12" in data["$schema"], path.name
        assert data.get("additionalProperties") is False, path.name


def test_master_index_encodes_draft_not_send_rule() -> None:
    txt = (REPO_ROOT / "docs/market_os/MARKET_PRODUCTION_OS_AR.md").read_text(encoding="utf-8")
    assert "250" in txt
    assert "draft" in txt.lower()
    assert "send" in txt.lower() or "إرسال" in txt


def test_keystone_docs_carry_disclaimer() -> None:
    disclaimer = "Estimated value is not Verified value"
    for rel in (
        "docs/market_os/MARKET_PRODUCTION_OS_AR.md",
        "docs/outreach/EMAIL_DELIVERABILITY_POLICY_AR.md",
        "docs/outreach/UNSUBSCRIBE_POLICY_AR.md",
        "docs/gtm/GTM_CONTROL_ROOM_AR.md",
    ):
        txt = (REPO_ROOT / rel).read_text(encoding="utf-8")
        assert disclaimer in txt, rel


def test_outreach_draft_examples_have_unsubscribe() -> None:
    path = REPO_ROOT / "data/templates/market_os_outreach_draft_example.jsonl"
    rows = [json.loads(ln) for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    assert rows, "expected at least one example draft"
    for rec in rows:
        assert rec.get("unsubscribe_included") is True
        assert rec.get("approval_status") in {
            "pending",
            "approved",
            "rejected",
            "rewrite",
            "nurture",
            "do_not_contact",
        }


def test_sector_keys_match_prospect_enum() -> None:
    import yaml  # PyYAML is a repo dependency

    sectors = yaml.safe_load((REPO_ROOT / "data/sectors/sectors.yaml").read_text(encoding="utf-8"))
    keys = {s["key"] for s in sectors["sectors"]}
    prospect = json.loads((REPO_ROOT / "schemas/prospect.schema.json").read_text(encoding="utf-8"))
    enum = set(prospect["properties"]["sector"]["enum"])
    assert keys == enum, "sectors.yaml keys must match prospect.schema sector enum"
