"""
Public safety scanner.

Refuses content that looks like it leaks PII, payment details, or
private operational data into the public repo.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

# Email regex: require a letter before "@" and reject pure version-like
# right-hand sides (e.g. "lucide@0.469.0") so we don't false-positive on
# npm/package strings.
EMAIL_RE = re.compile(r"\b[a-zA-Z][a-zA-Z0-9_.+-]*@(?!\d+\.\d)[a-zA-Z][a-zA-Z0-9-]*\.[a-zA-Z][a-zA-Z0-9-.]+\b")
PHONE_RE = re.compile(r"\+?\d[\d\s\-]{7,}\d")
IBAN_SA_RE = re.compile(r"\bSA\d{2}[\dA-Z]{20,22}\b")
CARD_RE = re.compile(r"\b(?:\d[ -]?){13,19}\b")

PRIVATE_KEYWORDS = (
    "BEGIN PRIVATE KEY",
    "BEGIN RSA PRIVATE KEY",
    "BEGIN OPENSSH PRIVATE KEY",
    "AKIA",  # AWS access key prefix
    "AIza",  # Google API key prefix
    "sk_live_",
    "rk_live_",
    "ghp_",
    "github_pat_",
)


@dataclass(frozen=True, slots=True)
class PublicSafetyFinding:
    kind: str
    sample: str


# Allowlisted email domains: example/test fixtures and Dealix's own
# public mailboxes (security@, hello@, contact@, etc.). The full local
# part is permitted as long as the domain is on this list.
_ALLOWED_EMAIL_DOMAINS = (
    "example.com", "example.org", "example.net", "example.sa",
    "yourco.sa", "company.sa", "ai-company.sa", "yourdomain.com",
    "dealix.test", "dealix.me", "dealix.com", "dealix.sa", "dealix.io",
)

# Phone placeholders frequently used in docs.
_ALLOWED_PHONE_PATTERNS = (
    "+966501234567", "+966500000000", "+966512345678", "+966550000000",
    "+966 50 123 4567", "+966 500 000 000", "+966 512 345 678",
)

# Documentation-only secret format markers.
_ALLOWED_SECRET_CONTEXTS = ("sk_live_xxxxx", "sk_live_...", "sk_live_<", "sk_live_REDACTED")


# Well-known service identifiers that *look* like emails but are not PII.
_ALLOWED_EMAIL_LITERALS = ("git@github.com", "noreply@github.com")


def _is_allowlisted_email(addr: str) -> bool:
    if addr.lower() in _ALLOWED_EMAIL_LITERALS:
        return True
    _, _, domain = addr.rpartition("@")
    domain = domain.lower()
    return any(domain == d or domain.endswith("." + d) for d in _ALLOWED_EMAIL_DOMAINS)


def _is_allowlisted_phone(text: str, sample: str) -> bool:
    if sample.strip() in _ALLOWED_PHONE_PATTERNS:
        return True
    digits = re.sub(r"\D", "", sample)
    # Common placeholder pattern: ends with many zeros, or has obvious
    # increment 1234567.
    return digits.endswith("0000000") or digits.endswith("1234567")


def scan(text: str) -> list[PublicSafetyFinding]:
    findings: list[PublicSafetyFinding] = []
    for m in EMAIL_RE.findall(text):
        if not _is_allowlisted_email(m):
            findings.append(PublicSafetyFinding("email", m))
    for m in PHONE_RE.findall(text):
        digits = re.sub(r"\D", "", m)
        if len(digits) >= 9 and not _is_allowlisted_phone(text, m):
            findings.append(PublicSafetyFinding("phone", m))
    for m in IBAN_SA_RE.findall(text):
        findings.append(PublicSafetyFinding("iban_sa", m))
    for m in CARD_RE.findall(text):
        findings.append(PublicSafetyFinding("card_like", m))
    for kw in PRIVATE_KEYWORDS:
        idx = text.find(kw)
        while idx != -1:
            context = text[idx: idx + len(kw) + 20]
            if not any(safe in context for safe in _ALLOWED_SECRET_CONTEXTS):
                findings.append(PublicSafetyFinding("secret_marker", kw))
                break
            idx = text.find(kw, idx + 1)
    return findings


def is_safe(text: str) -> bool:
    return not scan(text)
