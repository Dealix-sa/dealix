from pathlib import Path


def test_commercial_pack_files_exist():
    required = [
        "docs/ops/COMMERCIAL_READINESS_CONTROL_CENTER_AR.md",
        "business/products/COMMERCIAL_PRODUCT_CATALOG.md",
        "sales/COMMERCIAL_FOUNDATION_PACK_AR.md",
        "scripts/commercial/commercial_readiness_check.py",
        "scripts/commercial/generate_commercial_go_live_pack.py",
    ]
    for item in required:
        assert Path(item).exists()
