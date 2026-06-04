"""Seed-lead validation passes for the example file and catches bad records."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts" / "lib"))

import commercial_seed_leads_validate as slv  # noqa: E402

EXAMPLE = ROOT / "data" / "commercial_seed_leads.example.jsonl"


def test_example_seed_leads_valid():
    r = slv.validate(EXAMPLE)
    assert r["passed"] is True
    assert r["count"] >= 10


def test_invalid_vertical_caught(tmp_path):
    p = tmp_path / "bad.jsonl"
    p.write_text(json.dumps({
        "lead_id": "X", "company_name": "Y", "vertical": "not_real",
        "country": "SA", "stage": "raw_lead", "created_at": "2026-01-01T00:00:00Z",
    }) + "\n", encoding="utf-8")
    r = slv.validate(p)
    assert r["passed"] is False
    assert any("unknown vertical" in e for e in r["errors"])
