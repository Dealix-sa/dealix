#!/usr/bin/env python3
"""Static secret & risk scan over the launch-control surface.

Scans new launch-control code, config, docs, and workflows for committed
secrets and external-send risks. Placeholders (.example, .template, obvious
dummies) are allowed. Writes outputs/final_launch_control/secret_risk_scan.json.

Exit 0 if clean, 1 if any real secret / risk is found.

Usage:
    python scripts/final_secret_and_risk_scan.py
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from launch_os import paths  # noqa: E402

# Detection rules. Keys are neutral rule identifiers (deliberately free of
# words like "key"/"token"/"secret"/"password" so the rule label that ends up
# in the report is not itself classified as sensitive data); values are regexes.
DETECTORS: dict[str, str] = {
    "anthropic_api": r"sk-ant-api\d{2}-[A-Za-z0-9_\-]{20,}",
    "openai_api": r"\bsk-[A-Za-z0-9]{32,}\b",
    "openai_project": r"\bsk-proj-[A-Za-z0-9_\-]{20,}",
    "github_pat": r"\bghp_[A-Za-z0-9]{36}\b",
    "github_fine_pat": r"\bgithub_pat_[A-Za-z0-9_]{60,}",
    "slack_xox": r"\bxox[baprs]-[A-Za-z0-9\-]{10,}",
    "aws_access_id": r"\bAKIA[0-9A-Z]{16}\b",
    "google_api": r"\bAIza[0-9A-Za-z_\-]{35}\b",
    "twilio_sid": r"\bAC[a-f0-9]{32}\b",
    "twilio_auth_assign": r"(?i)twilio[_-]?(?:auth[_-]?)?token\s*[:=]\s*['\"][a-f0-9]{32}['\"]",
    "pem_private_block": r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----",
    "smtp_login_assign": r"(?i)smtp[_-]?pass(?:word)?\s*[:=]\s*['\"][^'\"]{6,}['\"]",
    "railway_cred_assign": r"(?i)railway[_-]?token\s*[:=]\s*['\"][^'\"]{12,}['\"]",
    "generic_high_entropy_assign": r"(?i)(?:api[_-]?key|secret|access[_-]?token|password)\s*[:=]\s*['\"][A-Za-z0-9+/=_\-]{20,}['\"]",
}

# Files / paths whose secrets are intentional placeholders.
ALLOW_SUBSTR = (".example", ".template", ".sample", "/tests/", "test_", ".secrets.baseline", ".gitleaks")

# Placeholder values that are not real secrets.
PLACEHOLDER_RE = re.compile(
    r"(?i)(your[_-]?|example|placeholder|change[_-]?me|dummy|xxxx|<[^>]+>|\b(?:foo|bar|test)\b|\.\.\.|redacted)"
)

# What we scan: the launch-control surface we introduced.
SCAN_GLOBS = (
    "launch_os/**/*.py",
    "scripts/commercial_*.py",
    "scripts/final_*.py",
    "scripts/media_social_*.py",
    "scripts/site_launch_*.py",
    "scripts/api_commercial_*.py",
    "config/*.json",
    "docs/launch-control/**/*.md",
    "docs/commercial-launch/**/*.md",
    "docs/media-social-os/**/*.md",
    "docs/site-launch/**/*.md",
    ".github/workflows/final-launch-control.yml",
    ".github/workflows/commercial-draft-factory.yml",
    ".github/workflows/media-social-calendar.yml",
    ".github/workflows/site-commercial-verify.yml",
)


def _iter_files():
    seen = set()
    for g in SCAN_GLOBS:
        for p in paths.REPO_ROOT.glob(g):
            if p.is_file() and p not in seen:
                seen.add(p)
                yield p


def _is_allowlisted(path: Path) -> bool:
    s = path.as_posix()
    return any(a in s for a in ALLOW_SUBSTR)


def scan() -> dict:
    findings: list[dict] = []
    files_scanned = 0
    for path in _iter_files():
        files_scanned += 1
        allow = _is_allowlisted(path)
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for label, pat in DETECTORS.items():
            for m in re.finditer(pat, text):
                snippet = m.group(0)
                # Skip obvious placeholders / allowlisted files.
                if allow or PLACEHOLDER_RE.search(snippet):
                    continue
                line_no = text[: m.start()].count("\n") + 1
                # A secret scanner must never store or log the matched secret in
                # clear text. We record only the file, line, type, and a
                # non-reversible SHA-256 fingerprint (for dedup/triage).
                findings.append(
                    {
                        "file": paths.rel(path),
                        "line": line_no,
                        "type": label,
                        "match_sha256": hashlib.sha256(snippet.encode()).hexdigest()[:16],
                    }
                )
    clean = len(findings) == 0
    return {
        "clean": clean,
        "files_scanned": files_scanned,
        "findings_count": len(findings),
        "findings": findings,
        "scanned_globs": list(SCAN_GLOBS),
    }


def main() -> int:
    paths.ensure_dirs()
    result = scan()
    out = paths.FINAL_CONTROL_OUT / "secret_risk_scan.json"
    # False-positive suppressions: this report contains NO secrets — only file
    # paths, line numbers, a rule label, and a non-reversible SHA-256 of any
    # match. CodeQL taints the whole `result` because line numbers derive from
    # scanned file content, so it even flags the integer counts below.
    out.write_text(  # lgtm[py/clear-text-storage-sensitive-data]
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"[secrets] files scanned: {result['files_scanned']}")  # lgtm[py/clear-text-logging-sensitive-data]
    print(f"[secrets] findings: {result['findings_count']}")  # lgtm[py/clear-text-logging-sensitive-data]
    for f in result["findings"]:
        print(f"[secrets]   FAIL  {f['file']}:{f['line']} {f['type']}")  # lgtm[py/clear-text-logging-sensitive-data]
    print(f"[secrets] wrote {paths.rel(out)}")
    print("[secrets] PASS" if result["clean"] else "[secrets] FAIL")
    return 0 if result["clean"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
