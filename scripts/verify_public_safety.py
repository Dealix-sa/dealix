import re
from pathlib import Path

SKIP_FILES = {
    "scripts/verify_public_safety.py",
    "DEALIX_ARCHITECTURE_MAP.md",
    "DEALIX_EXECUTION_LEDGER.md",
    "docs/trust/PUBLIC_REPO_SAFETY.md",
}

SKIP_DIR_PREFIXES = (
    ".git/",
    "node_modules/",
    ".venv/",
    "venv/",
    "dist/",
    "build/",
    "__pycache__/",
    "tests/",
)

BLOCKED_PATH_PARTS = [
    "real_leads",
    "private_pipeline_data",
    "outreach_queue_real",
    "payment_receipts_real",
    "client_call_notes",
    "customer_bank_details",
    "customer_secrets",
]

REAL_SECRET_PATTERNS = [
    re.compile(r"sk_live_[A-Za-z0-9]{20,}"),
    re.compile(r"sk-[A-Za-z0-9]{30,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"AIza[0-9A-Za-z_\-]{30,}"),
    re.compile(r"ghp_[A-Za-z0-9]{30,}"),
    re.compile(r"gho_[A-Za-z0-9]{30,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{40,}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{20,}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |ENCRYPTED )?PRIVATE KEY-----"),
    re.compile(r"eyJ[A-Za-z0-9_-]{30,}\.[A-Za-z0-9_-]{30,}\.[A-Za-z0-9_-]{20,}"),
]

TEXT_EXTENSIONS = {".md", ".txt", ".csv", ".json", ".yaml", ".yml", ".py", ".ts", ".tsx", ".js", ".html", ".env"}

violations = []

for path in Path(".").rglob("*"):
    if path.is_dir():
        continue
    rel = path.as_posix()
    if any(rel.startswith(prefix) or f"/{prefix}" in rel for prefix in SKIP_DIR_PREFIXES):
        continue
    if rel in SKIP_FILES:
        continue

    lower_path = rel.lower()
    for blocked in BLOCKED_PATH_PARTS:
        if blocked in lower_path:
            violations.append(f"Blocked path pattern: {rel}")

    if path.suffix.lower() not in TEXT_EXTENSIONS:
        continue
    try:
        text = path.read_text(errors="ignore")
    except Exception:
        continue
    for pattern in REAL_SECRET_PATTERNS:
        match = pattern.search(text)
        if match:
            violations.append(f"Potential real secret in {rel}: pattern '{pattern.pattern}'")

if violations:
    print("Public safety violations:")
    for violation in violations:
        print(f"- {violation}")
    raise SystemExit(1)
print("PASS: no obvious public safety violations found.")
