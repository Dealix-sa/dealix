"""Master verifier passes against a fresh, committed launch surface."""

from __future__ import annotations

from tests._lc_util import load_script, ensure_run


def test_master_verification_passes():
    ensure_run()
    mod = load_script("final_launch_control_verify")
    result = mod.run()
    failed = [c for c in result["checks"] if c["critical"] and not c["passed"]]
    assert result["pass"] is True, f"critical failures: {failed}"


def test_master_verification_writes_artifacts():
    ensure_run()
    mod = load_script("final_launch_control_verify")
    assert mod.main() == 0
    from launch_os import paths
    assert (paths.FINAL_CONTROL_OUT / "final_verification.json").exists()
    assert (paths.FINAL_CONTROL_OUT / "final_verification.md").exists()
