"""Generated outputs match the documented schema and reports are coherent."""

from __future__ import annotations

import json

import commercial_generate_400_drafts as gen
from _commercial_common import load_config
from _launch_util import SEED, TEST_DAY


def test_outputs_schema(tmp_path):
    result = gen.generate(target=400, day=TEST_DAY, seed_path=SEED)
    gen.write_outputs(result, tmp_path)

    # draft_queue rows carry all required fields.
    required = set(load_config("commercial_quality_gates.json")["required_fields"])
    rows = [
        json.loads(line)
        for line in (tmp_path / "draft_queue.jsonl").read_text(encoding="utf-8").splitlines()
        if line
    ]
    assert len(rows) >= 400
    for r in rows:
        assert required.issubset(r.keys())

    metrics = json.loads((tmp_path / "daily_metrics.json").read_text(encoding="utf-8"))
    assert metrics["drafts_generated"] == len(rows)
    assert metrics["target_met"] is True
    assert set(metrics["by_channel"]) == {
        "cold_email",
        "follow_up",
        "linkedin_manual",
        "website_contact_form",
    }

    manifest = json.loads((tmp_path / "batch_manifest.json").read_text(encoding="utf-8"))
    assert manifest["safety_flags"]["send_allowed"] is False
    assert manifest["external_send_blocked"] is True


def test_quality_and_compliance_reports(tmp_path):
    result = gen.generate(target=400, day=TEST_DAY, seed_path=SEED)
    gen.write_outputs(result, tmp_path)
    q = json.loads((tmp_path / "quality_report.json").read_text(encoding="utf-8"))
    c = json.loads((tmp_path / "compliance_report.json").read_text(encoding="utf-8"))
    assert q["total"] == c["total"] >= 400
    assert q["passed"] + q["failed"] == q["total"]
