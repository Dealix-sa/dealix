"""
DLP — last-line check before any output leaves the Dealix perimeter.
"""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.security.output_sanitizer import sanitize_output


@dataclass
class DLPVerdict:
    safe: bool
    findings: list[str]
    redacted_text: str


_SECRET_TOKENS = (
    "AKIA",         # AWS access key
    "ghp_",         # GitHub PAT
    "xoxb-",        # Slack
    "sk-",          # generic API key prefix
    "supabase_anon",
    "DATABASE_URL=",
)


def scan_for_data_loss(text: str) -> DLPVerdict:
    if not text:
        return DLPVerdict(True, [], "")
    findings: list[str] = []
    for token in _SECRET_TOKENS:
        if token in text:
            findings.append(f"secret_token:{token}")
    s = sanitize_output(text, redact_pii=True)
    findings.extend(s.findings)
    return DLPVerdict(
        safe=s.safe and not any(f.startswith("secret_token") for f in findings),
        findings=findings,
        redacted_text=s.sanitized_text,
    )
