from pathlib import Path

REQUIRED_SECTIONS = [
    "## Purpose",
    "## Owner",
    "## Review Cadence",
    "## Inputs",
    "## Outputs",
    "## Rules",
    "## Metrics",
    "## Evidence",
]

DOC_FOLDERS = [
    "docs/founder",
    "docs/strategy",
    "docs/revenue",
    "docs/acquisition",
    "docs/sales",
    "docs/delivery",
    "docs/trust",
    "docs/finance",
    "docs/client_success",
    "docs/product",
    "docs/content",
    "docs/learning",
    "docs/people",
    "docs/agents",
    "docs/ai_management",
    "docs/control_plane",
    "docs/ops",
]

# Master Content Pack v1 enforces the standard on files registered in the
# allowlist below. Legacy docs that have not been migrated to the standard
# can be added incrementally as they are updated. This keeps the verifier
# strict on what it owns and silent on what it does not yet own.
ALLOWLIST_FILE = Path("docs/.doc_standard_allowlist.txt")

failures = []

if ALLOWLIST_FILE.exists():
    allowlisted = {
        line.strip()
        for line in ALLOWLIST_FILE.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    }
else:
    allowlisted = None  # None means "check everything" (legacy behaviour).

def check_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8", errors="ignore")

    if path.stat().st_size < 120:
        failures.append(f"Too short: {path}")
        return

    missing_sections = [section for section in REQUIRED_SECTIONS if section not in text]

    if missing_sections:
        failures.append(f"{path} missing sections: {', '.join(missing_sections)}")

for folder in DOC_FOLDERS:
    base = Path(folder)
    if not base.exists():
        failures.append(f"Missing folder: {folder}")
        continue

    for path in base.rglob("*.md"):
        rel = str(path).replace("\\", "/")
        if allowlisted is not None and rel not in allowlisted:
            continue
        check_file(path)

if failures:
    print("Document quality failures:")
    for failure in failures:
        print(f"- {failure}")
    raise SystemExit(1)

print("PASS: all registered operating documents meet Dealix document standard.")
