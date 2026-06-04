"""The draft factory produces >=400 review-only drafts with hard guard flags."""

from __future__ import annotations

from tests._lc_util import REPO_ROOT  # noqa: F401  (ensures repo root on sys.path)

from launch_os.drafts import generate_drafts, write_run, OFFERS
from launch_os import paths


def test_generates_at_least_400():
    drafts = generate_drafts(target=400)
    assert len(drafts) >= 400


def test_every_draft_is_review_only():
    drafts = generate_drafts(target=400)
    for d in drafts:
        assert d["send_allowed"] is False
        assert d["external_send_blocked"] is True
        assert d["no_auto_send"] is True
        assert d["requires_founder_approval"] is True
        assert d["status"] == "queued_for_review"
        assert d["channel"] == "founder_review_queue"


def test_offers_within_ladder():
    valid = {o["key"] for o in OFFERS}
    for d in generate_drafts(target=400):
        assert d["offer"] in valid


def test_write_run_creates_artifacts(tmp_path):
    drafts = generate_drafts(target=400)
    out = tmp_path / "commercial_launch"
    latest = out / "latest"
    summary = write_run(drafts, out, latest)
    assert summary["count"] >= 400
    for name in ("draft_queue.jsonl", "founder_review.md", "top_50_priority.md"):
        assert (summary["run_dir"] / name).exists()
        assert (latest / name).exists()


def test_cli_main_passes(tmp_path, monkeypatch):
    script = __import__("importlib").import_module  # noqa
    from tests._lc_util import load_script
    mod = load_script("commercial_generate_400_drafts")
    assert mod.main(["--target", "400"]) == 0
    assert paths.latest_dir().joinpath("draft_queue.jsonl").exists()
