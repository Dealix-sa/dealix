from pathlib import Path


def test_startup_os_day_assets_exist():
    required = [
        Path("data/commercial/startup_os_operating_config.json"),
        Path("scripts/commercial/run_startup_os_day.py"),
        Path("scripts/commercial/generate_founder_daily_brief.py"),
        Path("scripts/commercial/generate_startup_proof_pack.py"),
        Path("apps/web/lib/founder-daily-brief-snapshot.ts"),
        Path("apps/web/app/(saas)/app/founder-brief/page.tsx"),
    ]
    for path in required:
        assert path.exists(), f"missing {path}"
        assert path.read_text(encoding="utf-8").strip(), f"empty {path}"


def test_startup_os_day_keeps_safe_defaults():
    combined = "\n".join(
        Path(path).read_text(encoding="utf-8")
        for path in [
            "data/commercial/startup_os_operating_config.json",
            "scripts/commercial/generate_founder_daily_brief.py",
            "scripts/commercial/generate_startup_proof_pack.py",
        ]
    )
    assert "no live outbound by default" in combined
    assert "no fake ROI" in combined
    assert "source_url required" in combined
