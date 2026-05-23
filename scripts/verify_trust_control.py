"""Verify the Trust Control system is in place."""

from pathlib import Path

required = [
    "docs/trust/TRUST_CONTROL_SYSTEM.md",
    "docs/trust/APPROVAL_MATRIX.md",
    "docs/trust/AUTONOMY_POLICY.md",
    "docs/trust/NO_OVERCLAIM_POLICY.md",
    "docs/trust/SAFE_LANGUAGE_LIBRARY.md",
    "docs/trust/PUBLIC_PRIVATE_BOUNDARY.md",
]

failures = []

for file in required:
    path = Path(file)
    if not path.exists():
        failures.append(f"Missing: {file}")
    elif path.stat().st_size < 150:
        failures.append(f"Too short: {file}")

text = Path("docs/trust/TRUST_CONTROL_SYSTEM.md").read_text(encoding="utf-8", errors="ignore")
for term in ["A3", "A2", "guaranteed revenue", "sensitive data", "public repo"]:
    if term not in text:
        failures.append(f"TRUST_CONTROL_SYSTEM missing: {term}")

if failures:
    print("Trust control verification failed:")
    for f in failures:
        print("-", f)
    raise SystemExit(1)

print("PASS: trust control system is ready.")
