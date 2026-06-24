from pathlib import Path


def test_gtm_and_product_files_exist():
    required = [
        "business/products/REVENUE_COMMAND_ROOM_OS.md",
        "business/products/COMPANY_BRAIN_OS.md",
        "business/products/CLIENT_DELIVERY_OS.md",
        "gtm/FIRST_30_DAYS_GTM.md",
        "trust/COMMERCIAL_SAFETY_GATES.md",
    ]
    for path in required:
        assert Path(path).exists(), path
