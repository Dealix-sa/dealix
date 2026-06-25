from pathlib import Path


def test_startup_command_center_assets_exist():
    required = [
        Path("data/commercial/startup_os_product_matrix.json"),
        Path("scripts/commercial/generate_startup_command_center.py"),
        Path("apps/web/lib/startup-command-snapshot.ts"),
        Path("apps/web/app/(saas)/app/startup-command/page.tsx"),
    ]
    for path in required:
        assert path.exists(), f"missing {path}"
        assert path.read_text(encoding="utf-8").strip(), f"empty {path}"


def test_startup_command_center_preserves_safe_mode():
    matrix = Path("data/commercial/startup_os_product_matrix.json").read_text(encoding="utf-8")
    assert "draft_only" in matrix
    assert "WHATSAPP_ALLOW_LIVE_SEND" in matrix
    assert "false" in matrix
