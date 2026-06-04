"""Seed leads validation accepts the example file and rejects malformed leads."""

from __future__ import annotations

from _commercial_common import write_jsonl
from _launch_util import SEED
from commercial_seed_leads_validate import validate


def test_example_seed_is_valid():
    assert validate(SEED) == []


def test_missing_field_is_flagged(tmp_path):
    bad = tmp_path / "bad.jsonl"
    write_jsonl(bad, [{"lead_id": "L1", "company_name": "X"}])  # missing most fields
    errors = validate(bad)
    assert errors
    assert any("missing field" in e for e in errors)


def test_unknown_vertical_is_flagged(tmp_path):
    bad = tmp_path / "bad.jsonl"
    write_jsonl(
        bad,
        [
            {
                "lead_id": "L1",
                "company_name": "X",
                "vertical": "spaceships",
                "country": "Saudi Arabia",
                "city": "Riyadh",
                "buyer_title": "CEO",
                "stage": "new",
                "source": "test",
                "opt_in_status": "unknown",
            }
        ],
    )
    assert any("unknown vertical" in e for e in validate(bad))
