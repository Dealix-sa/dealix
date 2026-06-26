from pathlib import Path


def test_trust_control_assets_exist():
    required = [
        Path("data/commercial/trust_control_manifest.json"),
        Path("scripts/commercial/generate_trust_control.py"),
        Path("apps/web/lib/trust-control-snapshot.ts"),
        Path("apps/web/app/(saas)/app/trust-control/page.tsx"),
    ]
    for path in required:
        assert path.exists(), f"missing {path}"
        assert path.read_text(encoding="utf-8").strip(), f"empty {path}"


def test_trust_control_blocks_bad_claims():
    manifest = Path("data/commercial/trust_control_manifest.json").read_text(encoding="utf-8")
    assert "guaranteed ROI" in manifest
    assert "fake testimonial" in manifest
    assert "no fake ROI" in manifest
    assert "proof pack" in manifest
