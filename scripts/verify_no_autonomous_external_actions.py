"""Guardrail check: no scripts in the kit may take autonomous external actions.

This is a static text scan, not a runtime sandbox. It catches the obvious cases —
direct HTTP posts, Slack/WhatsApp/Twilio/Email sends, SMTP, scraping, GitHub PR
creation outside the kit's own scripts — in any file under the Revenue Sprint
Kit surface.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

SCAN_PATHS = [
    REPO_ROOT / "docs/offers/revenue_sprint",
    REPO_ROOT / "docs/delivery/revenue_sprint",
    REPO_ROOT / "docs/trust/NO_OVERCLAIM_POLICY.md",
    REPO_ROOT / "scripts/verify_revenue_sprint_kit.py",
    REPO_ROOT / "scripts/dealix_revenue_sprint_kit.py",
    REPO_ROOT / "private_ops",
]

ALLOWED_SUFFIXES = {".md", ".py"}

# Each pattern is a tuple of (regex, human label). Patterns intentionally err on
# the side of catching false positives — anyone hitting one of these in kit
# code should refactor or explicitly document why it is safe.
BANNED_PATTERNS: list[tuple[str, str]] = [
    (r"\brequests\.(get|post|put|patch|delete)\s*\(", "requests.* HTTP call"),
    (r"\bhttpx\.(get|post|put|patch|delete)\s*\(", "httpx.* HTTP call"),
    (r"\burllib\.request\.urlopen\s*\(", "urllib.request.urlopen"),
    (r"\bsmtplib\.SMTP", "smtplib SMTP send"),
    (r"\btwilio\b", "twilio client"),
    (r"\bslack_sdk\b", "slack_sdk client"),
    (r"\bWebClient\s*\(", "Slack WebClient"),
    (r"\bsend_message\s*\(", "send_message(...)"),
    (r"\bcreate_pull_request\s*\(", "create_pull_request(...)"),
    (r"\bopen_browser\s*\(", "open_browser(...)"),
    (r"\bwebbrowser\.open", "webbrowser.open"),
    (r"\bsubprocess\.(run|Popen|call)\s*\(\s*\[?\s*['\"]curl", "curl via subprocess"),
    (r"\bos\.system\s*\(\s*['\"]curl", "curl via os.system"),
]


def iter_files() -> list[Path]:
    files: list[Path] = []
    for entry in SCAN_PATHS:
        if not entry.exists():
            continue
        if entry.is_file():
            if entry.suffix in ALLOWED_SUFFIXES:
                files.append(entry)
            continue
        for path in entry.rglob("*"):
            if path.is_file() and path.suffix in ALLOWED_SUFFIXES:
                files.append(path)
    return files


def main() -> int:
    failures: list[str] = []
    self_path = Path(__file__).resolve()

    for path in iter_files():
        if path.resolve() == self_path:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError as exc:
            failures.append(f"{path}: unreadable ({exc})")
            continue
        for pattern, label in BANNED_PATTERNS:
            if re.search(pattern, text):
                relative = path.relative_to(REPO_ROOT)
                failures.append(f"{relative}: contains {label}")

    if failures:
        print("Autonomous external action guard failed:")
        for failure in failures:
            print("-", failure)
        return 1

    print("PASS: no autonomous external actions detected in Revenue Sprint Kit.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
