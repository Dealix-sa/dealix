from pathlib import Path

SCAN_DIRS = ["dealix", "ops_runtime", "execution_engine", "control_plane", "operating_intelligence"]

RISKY_TERMS = [
    "send_email(",
    "send_dm(",
    "post_to_linkedin(",
    "publish(",
    "charge_customer(",
    "refund(",
    "export_client_data(",
]

ALLOWLIST = [
    "docs/",
    "tests/",
]

failures = []

for folder in SCAN_DIRS:
    base = Path(folder)
    if not base.exists():
        continue

    for file in base.rglob("*.py"):
        text = file.read_text(encoding="utf-8", errors="ignore")
        for term in RISKY_TERMS:
            if term in text:
                failures.append(f"{file} contains risky autonomous action: {term}")

if failures:
    print("Autonomous external action check failed:")
    for f in failures:
        print("-", f)
    raise SystemExit(1)

print("PASS: no autonomous external action patterns found.")
