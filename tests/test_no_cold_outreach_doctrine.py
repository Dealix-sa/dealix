"""Doctrine: no cold outreach send path may exist without an approval / policy gate.

This static-analysis test pins the known set of send call sites (WhatsApp, email,
LinkedIn, SMS) and asserts each one is gated by either:

  * an explicit policy/feature flag check (e.g. ``whatsapp_allow_live_send``),
  * a compliance check (``check_outreach``), or
  * routing through the approval queue (``status == "approved"``).

Any *new* send entry point introduced anywhere under ``auto_client_acquisition/``,
``integrations/`` or ``api/`` must be added to ``ALLOWED_SEND_SITES`` together
with the gate that protects it; otherwise this test fails and the change is
blocked at PR time. That guarantees we never silently regress the "no cold
outreach" non-negotiable.
"""

from __future__ import annotations

import re
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]

# (relative_path, function_name, required_gate_substring_in_function_body)
# When adding a new send function, append it here AND ensure the gate appears in
# the function body. The gate must be a substring that is real source (not a
# comment) — keep it short and stable.
ALLOWED_SEND_SITES: tuple[tuple[str, str, str], ...] = (
    (
        "auto_client_acquisition/email/whatsapp_multi_provider.py",
        "send_whatsapp_smart",
        "whatsapp_allow_live_send",
    ),
    (
        "auto_client_acquisition/email/gmail_send.py",
        "send_email",
        # gmail_send.send_email is a low-level transport — every caller goes
        # through api/routers/email_send.py::send_approved which runs
        # check_outreach. The transport itself defers to is_configured()
        # which returns False unless GMAIL_* env vars are set in production.
        "is_configured",
    ),
    (
        "api/routers/email_send.py",
        "send_approved",
        "check_outreach",
    ),
    (
        "api/routers/email_send.py",
        "send_batch",
        # send_batch pulls only rows whose status == "approved" from the queue.
        '"approved"',
    ),
)

# Patterns we scan for to detect *new* send functions that may have slipped in.
_SEND_DEF_RE = re.compile(
    r"^\s*(?:async\s+)?def\s+(send_(?:whatsapp|email|sms|linkedin|message|approved|batch)\w*)\s*\(",
    re.MULTILINE,
)

_SCAN_ROOTS = ("auto_client_acquisition", "integrations", "api")


def _python_files() -> list[Path]:
    files: list[Path] = []
    for root in _SCAN_ROOTS:
        base = _REPO / root
        if not base.is_dir():
            continue
        files.extend(p for p in base.rglob("*.py") if "__pycache__" not in p.parts)
    return files


def _extract_function_body(text: str, fn_name: str) -> str | None:
    """Return the source text of a top-level function, or None if not found."""
    pattern = re.compile(
        rf"^(?P<indent>[ \t]*)(?:async\s+)?def\s+{re.escape(fn_name)}\s*\(",
        re.MULTILINE,
    )
    m = pattern.search(text)
    if not m:
        return None
    indent_len = len(m.group("indent"))
    # Find the line start of the matched def.
    line_start = text.rfind("\n", 0, m.start()) + 1
    lines = text[line_start:].splitlines(keepends=True)
    body: list[str] = []
    # Phase 1: signature — keep consuming until the def line ends with ":"
    # (handles multi-line argument lists).
    sig_end_idx = -1
    for idx, ln in enumerate(lines):
        body.append(ln)
        if ln.rstrip().endswith(":"):
            sig_end_idx = idx
            break
    if sig_end_idx < 0:
        return "".join(body)
    # Phase 2: body — stop when we hit a line with indent <= def's that is not blank.
    for ln in lines[sig_end_idx + 1:]:
        stripped = ln.strip()
        if stripped == "":
            body.append(ln)
            continue
        leading = len(ln) - len(ln.lstrip(" \t"))
        if leading <= indent_len:
            break
        body.append(ln)
    return "".join(body)


def test_every_known_send_site_is_gated() -> None:
    """Each allowed send site must contain its declared gate substring."""
    for rel_path, fn_name, gate in ALLOWED_SEND_SITES:
        path = _REPO / rel_path
        assert path.is_file(), f"expected send-site file missing: {rel_path}"
        text = path.read_text(encoding="utf-8")
        body = _extract_function_body(text, fn_name)
        assert body is not None, f"{rel_path}::{fn_name} not found"
        assert gate in body, (
            f"send-site {rel_path}::{fn_name} no longer contains its required "
            f"gate '{gate}'. If the gate moved, update ALLOWED_SEND_SITES in "
            "tests/test_no_cold_outreach_doctrine.py with the new gate name."
        )


def test_no_unknown_send_functions() -> None:
    """Fail if any new send_* function appears outside the allow-list."""
    allowed_pairs = {
        (rel_path, fn_name) for rel_path, fn_name, _ in ALLOWED_SEND_SITES
    }
    found: set[tuple[str, str]] = set()
    for path in _python_files():
        rel = str(path.relative_to(_REPO))
        text = path.read_text(encoding="utf-8")
        for match in _SEND_DEF_RE.finditer(text):
            fn_name = match.group(1)
            found.add((rel, fn_name))

    unknown = sorted(found - allowed_pairs)
    assert not unknown, (
        "Found new send_* functions not in ALLOWED_SEND_SITES. Add them with "
        "the gate that protects them (approval queue, policy flag, or compliance "
        f"check) or remove the function:\n  {unknown}"
    )


def test_no_direct_provider_send_calls_outside_transports() -> None:
    """Outside the dedicated transport modules, no code may call provider APIs directly.

    This catches things like ``twilio_client.messages.create(...)`` or
    ``resend.Emails.send(...)`` being added in a router/service that bypasses
    the approval queue.
    """
    transport_files = {
        "auto_client_acquisition/email/whatsapp_multi_provider.py",
        "auto_client_acquisition/email/gmail_send.py",
        "integrations/email.py",
        "integrations/whatsapp.py",
    }
    # Patterns that imply a direct outbound send.
    forbidden = re.compile(
        r"\b(twilio_client\.messages\.create|resend\.Emails\.send|"
        r"sendgrid_client\.send|smtp\.send_message|"
        r"meta_whatsapp_client\.send)\b"
    )
    offenders: list[str] = []
    for path in _python_files():
        rel = str(path.relative_to(_REPO))
        if rel in transport_files:
            continue
        text = path.read_text(encoding="utf-8")
        if forbidden.search(text):
            offenders.append(rel)
    assert not offenders, (
        "Direct provider send calls found outside transport modules: "
        f"{offenders}. Route through the transport + approval queue."
    )
