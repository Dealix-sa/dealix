"""PublicSafety scanner catches PII / secret-like patterns."""
from __future__ import annotations

from dealix.trust.public_safety import is_safe, scan


def test_detects_real_email():
    findings = scan("Reach me at sami@bank.com.sa")
    assert any(f.kind == "email" for f in findings)


def test_allows_example_email():
    assert is_safe("Reach me at sami@example.com")


def test_detects_saudi_phone():
    findings = scan("Call +966 555 123 456 for help")
    assert any(f.kind == "phone" for f in findings)


def test_detects_iban():
    findings = scan("Wire to SA0380000000608010167519 today.")
    assert any(f.kind == "iban_sa" for f in findings)


def test_detects_secret_marker():
    findings = scan("AWS key starts with AKIAEXAMPLE12345678")
    assert any(f.kind == "secret_marker" for f in findings)
