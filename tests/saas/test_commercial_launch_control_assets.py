from pathlib import Path


def test_commercial_launch_control_assets_exist():
    required = [
        Path("data/commercial/commercial_launch_control_manifest.json"),
        Path("scripts/commercial/generate_commercial_launch_control.py"),
        Path("apps/web/lib/commercial-launch-control-snapshot.ts"),
        Path("apps/web/app/(saas)/app/commercial-launch/page.tsx"),
    ]
    for path in required:
        assert path.exists(), f"missing {path}"
        assert path.read_text(encoding="utf-8").strip(), f"empty {path}"


def test_commercial_launch_control_keeps_guardrails():
    manifest = Path("data/commercial/commercial_launch_control_manifest.json").read_text(encoding="utf-8")
    assert "no fake ROI" in manifest
    assert "no fake testimonials" in manifest
    assert "source_url required" in manifest
    assert "proof pack required" in manifest
