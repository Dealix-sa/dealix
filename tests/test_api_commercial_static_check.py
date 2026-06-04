"""API static check: launch-control routers have no external-send patterns."""

from __future__ import annotations

from tests._lc_util import REPO_ROOT, load_script


def test_api_static_check_passes():
    mod = load_script("api_commercial_static_check")
    result = mod.run()
    failed = [c for c in result["checks"] if c["critical"] and not c["passed"]]
    assert result["pass"] is True, f"critical failures: {failed}"


def test_launch_control_routers_no_send():
    mod = load_script("api_commercial_static_check")
    result = mod.run()
    names = {c["name"]: c for c in result["checks"]}
    if "launch_control_routers_no_send" in names:
        assert names["launch_control_routers_no_send"]["passed"] is True
