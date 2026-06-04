"""No external-send code exists anywhere in the launch-control surface."""

from __future__ import annotations

from tests._lc_util import REPO_ROOT

from launch_os.compliance import find_external_send

# Implementation surface (excludes verifier/scanner files that *name* the
# forbidden patterns as detection rules).
SURFACE_GLOBS = (
    "launch_os/__init__.py",
    "launch_os/paths.py",
    "launch_os/leads.py",
    "launch_os/drafts.py",
    "launch_os/safety.py",
    "launch_os/readiness.py",
    "launch_os/media_social.py",
    "scripts/commercial_generate_400_drafts.py",
    "scripts/commercial_safety_audit.py",
    "scripts/commercial_launch_readiness.py",
    "scripts/media_social_calendar_generate.py",
)


def test_no_external_send_patterns():
    offenders = {}
    for rel in SURFACE_GLOBS:
        p = REPO_ROOT / rel
        hits = find_external_send(p.read_text(encoding="utf-8"))
        if hits:
            offenders[rel] = hits
    assert offenders == {}, f"external-send patterns found: {offenders}"


def test_drafts_carry_no_recipient():
    from launch_os.drafts import generate_drafts
    for d in generate_drafts(target=400):
        for field in ("email", "phone", "mobile", "whatsapp", "to_address", "recipient_email"):
            assert field not in d
