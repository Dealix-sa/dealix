"""Output schema: draft records and run artifacts have the expected shape."""

from __future__ import annotations

import json


from launch_os.drafts import generate_drafts, write_run

REQUIRED_KEYS = {
    "draft_id", "created_at", "lead_id", "company", "vertical", "city",
    "channel", "offer", "subject_en", "subject_ar", "body_en", "body_ar",
    "priority_score", "icp_score", "send_allowed", "external_send_blocked",
    "no_auto_send", "requires_founder_approval", "status", "compliance",
}


def test_draft_record_schema():
    for d in generate_drafts(target=400):
        assert REQUIRED_KEYS.issubset(d.keys())
        assert isinstance(d["send_allowed"], bool)
        assert isinstance(d["priority_score"], int)
        assert isinstance(d["compliance"], dict)


def test_jsonl_round_trip(tmp_path):
    drafts = generate_drafts(target=400)
    out = tmp_path / "c"
    summary = write_run(drafts, out, out / "latest")
    lines = (summary["run_dir"] / "draft_queue.jsonl").read_text(encoding="utf-8").splitlines()
    assert len([ln for ln in lines if ln.strip()]) == len(drafts)
    parsed = [json.loads(ln) for ln in lines if ln.strip()]
    assert all(REQUIRED_KEYS.issubset(p.keys()) for p in parsed)


def test_daily_metrics_schema(tmp_path):
    from launch_os.readiness import daily_metrics
    m = daily_metrics(generate_drafts(target=400))
    for k in ("generated_at", "total_drafts", "drafts_sent", "by_vertical", "by_offer"):
        assert k in m
