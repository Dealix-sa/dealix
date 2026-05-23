"""Block public-facing claims that violate Dealix trust boundaries.

Scans source and docs for risky absolute claims ("guaranteed", "100% accurate",
"always", "never fails") that imply unbounded promises. Allows them only inside
explicitly listed paths (negation files, tests, doctrine references).
"""

from pathlib import Path

SCAN_DIRS = ["dealix", "ops_runtime", "execution_engine", "dealix_cli", "docs/agents"]

RISKY_PHRASES = [
    "guaranteed result",
    "100% accurate",
    "always works",
    "never fails",
    "fully autonomous decision",
]

ALLOWLIST_SUBSTRINGS = [
    "tests/",
    "verify_trust_boundary_terms",
    "doctrine",
    "negation",
]


def is_allowlisted(path: Path) -> bool:
    s = str(path).replace("\\", "/")
    return any(token in s for token in ALLOWLIST_SUBSTRINGS)


failures: list[str] = []

for folder in SCAN_DIRS:
    base = Path(folder)
    if not base.exists():
        continue
    for file in base.rglob("*"):
        if not file.is_file():
            continue
        if file.suffix not in {".py", ".md", ".yml", ".yaml", ".txt"}:
            continue
        if is_allowlisted(file):
            continue
        text = file.read_text(encoding="utf-8", errors="ignore").lower()
        for phrase in RISKY_PHRASES:
            if phrase in text:
                failures.append(f"{file} contains trust-boundary phrase: {phrase}")

if failures:
    print("Trust boundary terms check failed:")
    for f in failures:
        print("-", f)
    raise SystemExit(1)

print("PASS: no trust-boundary violations found.")
