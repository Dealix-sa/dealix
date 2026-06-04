"""Site static check passes (or cleanly skips if apps/web absent)."""

from __future__ import annotations

from tests._lc_util import load_script


def test_site_static_check_passes():
    mod = load_script("site_launch_static_check")
    result = mod.run()
    failed = [c for c in result["checks"] if c["critical"] and not c["passed"]]
    assert result["pass"] is True, f"critical failures: {failed}"


def test_no_forbidden_claims_on_site():
    mod = load_script("site_launch_static_check")
    result = mod.run()
    names = {c["name"]: c for c in result["checks"]}
    if "no_forbidden_claims" in names:
        assert names["no_forbidden_claims"]["passed"] is True
