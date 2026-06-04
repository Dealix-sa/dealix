"""Media/social verifier passes: docs + config + calendar + no auto-post code."""

from __future__ import annotations

from tests._lc_util import REPO_ROOT, load_script


def test_media_social_verify_passes():
    mod = load_script("media_social_verify")
    result = mod.run()
    failed = [c for c in result["checks"] if c["critical"] and not c["passed"]]
    assert result["pass"] is True, f"critical failures: {failed}"


def test_no_auto_post_code_flag():
    mod = load_script("media_social_verify")
    result = mod.run()
    names = {c["name"]: c for c in result["checks"]}
    assert names["no_auto_post_code"]["passed"] is True
