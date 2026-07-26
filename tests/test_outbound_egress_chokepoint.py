"""Proof that ``EXTERNAL_SEND_ENABLED=false`` actually prevents sending.

This is the test the repository was missing. Dealix documents a kill switch as
its first non-negotiable, but the live send path referenced none of the flags:
``api/routers/email_send.py``, ``auto_client_acquisition/email/gmail_send.py``
and ``integrations/email.py`` contained no mention of ``EXTERNAL_SEND_ENABLED``,
``EMAIL_SEND_ENABLED`` or ``OUTBOUND_MODE``. Approval status was the only
control. ``app/outbound/policy_gate.py`` implemented the rules correctly and had
no live importer at all.

Three layers here, because each catches a different way the guarantee can rot:

1. **Policy** — the flag matrix. Only one combination permits sending.
2. **Structural** — every module that talks to a send provider must route
   through the guard, enforced against a frozen allowlist so a newly added
   egress point fails until someone decides about it.
3. **Runtime** — the network transports are replaced with objects that raise on
   use. If anything reaches the wire while outbound is disabled, these fail.

Layer 3 is the one that cannot be satisfied by accident.
"""

from __future__ import annotations

import ast
import itertools
from pathlib import Path

import pytest

from app.outbound.egress import (
    CHANNEL_FLAGS,
    EgressBlocked,
    assert_egress_permitted,
    egress_permitted,
)

REPO_ROOT = Path(__file__).resolve().parents[1]

ALL_ON = {
    "EXTERNAL_SEND_ENABLED": "true",
    "OUTBOUND_MODE": "controlled_live",
    "EMAIL_SEND_ENABLED": "true",
    "WHATSAPP_SEND_ENABLED": "true",
    "WHATSAPP_ALLOW_LIVE_SEND": "true",
    "SMS_SEND_ENABLED": "true",
}

#: Modules that legitimately contain a provider egress call. Every function in
#: them that reaches the network must carry @guarded_egress. Adding a module
#: here is a deliberate act that shows up in review.
KNOWN_EGRESS_MODULES = {
    "auto_client_acquisition/email/gmail_send.py",
    "auto_client_acquisition/email/whatsapp_multi_provider.py",
    "company/automation/whatsapp_automation.py",
    "integrations/email.py",
    "integrations/whatsapp.py",
}

#: Functions inside those modules that must NOT be guarded, with the reason.
#: Drafts are the safe path — they have to keep working while outbound is off,
#: which is the entire point of draft_only mode.
INTENTIONALLY_UNGUARDED = {
    "create_draft": "drafts are the safe path and must work while outbound is disabled",
}

#: Every messaging-provider endpoint present in this repository.
#:
#: The first version of this list held five entries and missed three real
#: senders, because it was written from the providers I happened to be looking
#: at rather than from the repository. graph.instagram.com in particular was
#: missed because the sibling constant said graph.facebook.com — one character
#: class apart, and the structural scan silently covered nothing in that file.
#: It also meant whatsapp_multi_provider's green-api/ultramsg/fonnte senders
#: were guarded by luck rather than verified.
#:
#: Derived by grepping the tree for provider hostnames, not from memory:
#:   grep -rhoE "https://[a-z0-9.-]*(twilio|unifonic|resend|...)" --include=*.py
PROVIDER_MARKERS = (
    "api.fonnte.com",
    "api.green-api.com",
    "api.resend.com",
    "api.sendgrid.com",
    "api.twilio.com",
    "api.ultramsg.com",
    "api.unifonic.com",
    "gmail.googleapis.com",
    "graph.facebook.com",
    "graph.instagram.com",
    "smtplib.SMTP",
)

#: Modules that send messages but are deliberately outside the commercial kill
#: switch, each with the reason. This is a narrow, argued list — not a place to
#: park anything inconvenient.
MESSAGING_EXEMPT_MODULES = {
    "api/security/mfa.py": (
        "MFA one-time codes are transactional security messages, sent to the "
        "user's own verified device in direct response to their own login "
        "attempt. EXTERNAL_SEND_ENABLED / SMS_SEND_ENABLED govern commercial "
        "outbound; gating MFA on them would lock every user out of their "
        "account the moment outbound is disabled — an outage we would be "
        "inflicting on ourselves, not a safety win. Exempt by decision, and "
        "recorded here so it stays a decision."
    ),
}

#: Modules that mention a provider endpoint without calling it. Each needs a
#: reason, so "it's fine" is never assumed — a wrong entry here is how a real
#: egress point would slip through.
NON_EGRESS_REFERENCES = {
    "api/security/ssrf_guard.py": "blocklists these hosts rather than calling them",
    "api/routers/prospect.py": (
        "returns the endpoint as human-readable instruction text in a webhook "
        "response; makes no request itself"
    ),
}


# ── Layer 1: the flag matrix ────────────────────────────────────────────────


def test_default_environment_blocks_every_channel():
    """With nothing set, no channel may send."""
    for channel in CHANNEL_FLAGS:
        permitted, reason = egress_permitted(channel, env={})
        assert not permitted, f"{channel} permitted with empty env"
        assert reason == "external_send_disabled"


@pytest.mark.parametrize("channel", sorted(CHANNEL_FLAGS))
def test_only_the_full_combination_permits_sending(channel):
    permitted, reason = egress_permitted(channel, env=ALL_ON)
    assert permitted, f"{channel} blocked with everything enabled: {reason}"


@pytest.mark.parametrize(
    "flag", ["EXTERNAL_SEND_ENABLED", "OUTBOUND_MODE", "EMAIL_SEND_ENABLED"]
)
def test_turning_off_any_single_flag_blocks_email(flag):
    """Each flag is independently sufficient to stop a send."""
    env = dict(ALL_ON)
    env[flag] = "false" if flag != "OUTBOUND_MODE" else "draft_only"

    permitted, _ = egress_permitted("email", env=env)

    assert not permitted, f"email still permitted with {flag} disabled"


def test_whatsapp_needs_both_of_its_flags():
    """WHATSAPP_ALLOW_LIVE_SEND is a second, independent brake."""
    for off in ("WHATSAPP_SEND_ENABLED", "WHATSAPP_ALLOW_LIVE_SEND"):
        env = dict(ALL_ON)
        env[off] = "false"
        permitted, _ = egress_permitted("whatsapp", env=env)
        assert not permitted, f"whatsapp permitted with {off}=false"


def test_unknown_channel_is_refused():
    """A new channel opts in explicitly; it never inherits permission."""
    permitted, reason = egress_permitted("telegram", env=ALL_ON)

    assert not permitted
    assert "unknown_channel" in reason


def test_draft_only_is_the_default_when_mode_is_unset():
    env = {k: v for k, v in ALL_ON.items() if k != "OUTBOUND_MODE"}

    permitted, reason = egress_permitted("email", env=env)

    assert not permitted
    assert "mode_not_controlled_live" in reason


def test_full_flag_matrix_permits_exactly_one_combination():
    """Exhaustive over the three email-relevant switches."""
    permitted_combos = []
    for external, mode, email_flag in itertools.product(
        ["true", "false"], ["controlled_live", "draft_only"], ["true", "false"]
    ):
        env = {
            "EXTERNAL_SEND_ENABLED": external,
            "OUTBOUND_MODE": mode,
            "EMAIL_SEND_ENABLED": email_flag,
        }
        if egress_permitted("email", env=env)[0]:
            permitted_combos.append(env)

    assert permitted_combos == [
        {
            "EXTERNAL_SEND_ENABLED": "true",
            "OUTBOUND_MODE": "controlled_live",
            "EMAIL_SEND_ENABLED": "true",
        }
    ], permitted_combos


def test_guard_fails_closed_when_evaluation_raises(monkeypatch):
    """A broken guard must block, never wave the send through."""

    def boom(*_args, **_kwargs):
        raise ValueError("simulated guard failure")

    monkeypatch.setattr("app.outbound.egress.egress_permitted", boom)

    with pytest.raises(EgressBlocked) as excinfo:
        assert_egress_permitted("email")

    assert excinfo.value.reason == "guard_error"


# ── Layer 2: structural — no unguarded egress point may exist ───────────────


def _guarded_function_names(tree: ast.AST) -> set[str]:
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for decorator in node.decorator_list:
            func = decorator.func if isinstance(decorator, ast.Call) else decorator
            name = getattr(func, "id", None) or getattr(func, "attr", None)
            if name == "guarded_egress":
                names.add(node.name)
    return names


def _functions_containing_markers(source: str, tree: ast.AST) -> set[str]:
    """Functions whose body mentions a provider endpoint."""
    hits: set[str] = set()
    lines = source.splitlines()
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        body = "\n".join(lines[node.lineno - 1 : (node.end_lineno or node.lineno)])
        if any(marker in body for marker in PROVIDER_MARKERS):
            hits.add(node.name)
    return hits


@pytest.mark.parametrize("rel_path", sorted(KNOWN_EGRESS_MODULES))
def test_every_provider_call_is_guarded(rel_path):
    path = REPO_ROOT / rel_path
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, rel_path)

    guarded = _guarded_function_names(tree)
    needs_guard = _functions_containing_markers(source, tree)
    unguarded = {
        name
        for name in needs_guard - guarded
        if name not in INTENTIONALLY_UNGUARDED
    }

    assert not unguarded, (
        f"{rel_path} has unguarded provider calls: {sorted(unguarded)}. "
        "Decorate them with @guarded_egress, or record them in "
        "INTENTIONALLY_UNGUARDED with a reason."
    )


def test_no_unknown_module_reaches_a_provider():
    """A new egress point must be declared before it can ship."""
    offenders: set[str] = set()
    for path in REPO_ROOT.rglob("*.py"):
        rel = path.relative_to(REPO_ROOT).as_posix()
        if rel.startswith(("tests/", "scripts/", ".venv")) or "/.venv" in rel:
            continue
        if (
            rel in KNOWN_EGRESS_MODULES
            or rel in NON_EGRESS_REFERENCES
            or rel in MESSAGING_EXEMPT_MODULES
        ):
            continue
        try:
            source = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if any(marker in source for marker in PROVIDER_MARKERS):
            offenders.add(rel)

    assert not offenders, (
        "New modules reference a send provider directly: "
        f"{sorted(offenders)}. Route them through @guarded_egress and add them "
        "to KNOWN_EGRESS_MODULES."
    )


def test_draft_creation_is_deliberately_unguarded():
    """Pin the exemption so removing it is a visible decision."""
    source = (REPO_ROOT / "auto_client_acquisition/email/gmail_send.py").read_text()
    tree = ast.parse(source)

    assert "create_draft" not in _guarded_function_names(tree), (
        "create_draft became guarded — drafts must keep working while "
        "outbound is disabled, otherwise draft_only mode produces nothing."
    )
    assert "send_email" in _guarded_function_names(tree)


# ── Layer 3: runtime — nothing reaches the wire ─────────────────────────────


@pytest.fixture
def transports_that_explode(monkeypatch):
    """Record every attempt to reach the network, then fail loudly.

    Recording matters as much as raising. ``gmail_send._refresh_access_token``
    wraps its POST in a bare ``except Exception``, so an exception-only probe is
    swallowed and the call looks like it never happened. The recorder cannot be
    hidden that way: the list is appended to before anything is raised.

    Yields the list of attempts, so a test can assert on it directly.
    """
    attempts: list[str] = []

    async def recording_post(*_args, **_kwargs):
        attempts.append("httpx.post")
        raise AssertionError("egress attempted: httpx POST reached the network")

    class RecordingSMTP:
        def __init__(self, *_args, **_kwargs):
            attempts.append("smtplib.SMTP")
            raise AssertionError("egress attempted: smtplib.SMTP was constructed")

    def recording_requests_post(*_args, **_kwargs):
        attempts.append("requests.post")
        raise AssertionError("egress attempted: requests.post reached the network")

    monkeypatch.setattr("httpx.AsyncClient.post", recording_post)
    monkeypatch.setattr("smtplib.SMTP", RecordingSMTP)
    # requests is a third transport. Patching only httpx and smtplib meant a
    # sender using requests could reach the network with every test green.
    monkeypatch.setattr("requests.post", recording_requests_post)
    return attempts


@pytest.fixture
def outbound_disabled(monkeypatch):
    for key in (
        "EXTERNAL_SEND_ENABLED",
        "EMAIL_SEND_ENABLED",
        "WHATSAPP_SEND_ENABLED",
        "WHATSAPP_ALLOW_LIVE_SEND",
        "SMS_SEND_ENABLED",
    ):
        monkeypatch.setenv(key, "false")
    monkeypatch.setenv("OUTBOUND_MODE", "draft_only")


@pytest.mark.asyncio
async def test_gmail_send_never_reaches_the_network_when_disabled(
    outbound_disabled, transports_that_explode, monkeypatch
):
    """The headline case: fully configured Gmail, approved content, still blocked."""
    monkeypatch.setenv("GMAIL_CLIENT_ID", "placeholder-client-id")
    monkeypatch.setenv("GMAIL_CLIENT_SECRET", "placeholder-client-secret")
    monkeypatch.setenv("GMAIL_REFRESH_TOKEN", "placeholder-refresh-token")
    monkeypatch.setenv("GMAIL_SENDER_EMAIL", "founder@example.com")

    from auto_client_acquisition.email.gmail_send import send_email

    result = await send_email(
        to_email="buyer@example.com",
        subject="Approved subject",
        body_plain="Approved body with an unsubscribe link.",
    )

    assert result.status == "blocked_policy"

    assert transports_that_explode == [], (
        "Something reached the network while outbound was disabled: "
        f"{transports_that_explode}"
    )


@pytest.mark.asyncio
async def test_email_client_providers_never_reach_the_network_when_disabled(
    outbound_disabled, transports_that_explode
):
    from integrations.email import EmailClient

    client = EmailClient()
    for provider_method in ("_send_resend", "_send_sendgrid", "_send_smtp"):
        result = await getattr(client, provider_method)(
            "buyer@example.com", "subject", "text", None, None
        )
        assert result.success is False, provider_method

    assert transports_that_explode == [], (
        f"Provider reached the network while disabled: {transports_that_explode}"
    )


@pytest.mark.asyncio
async def test_whatsapp_never_reaches_the_network_when_disabled(
    outbound_disabled, transports_that_explode
):
    from auto_client_acquisition.email.whatsapp_multi_provider import (
        _send_via_meta_cloud,
    )

    assert await _send_via_meta_cloud(None, "+966500000000", "hello") is None

    assert transports_that_explode == []


# ── Positive control ────────────────────────────────────────────────────────
#
# Every test above would still pass if the guard simply blocked everything
# unconditionally — which would be a broken product, not a safe one. These
# prove the guard is a gate and not a wall: with outbound deliberately enabled
# the call proceeds past the guard and reaches the transport, where the
# exploding fixture catches it. AssertionError therefore means "the guard
# allowed it through", which is the expected outcome here.


@pytest.fixture
def outbound_fully_enabled(monkeypatch):
    for key, value in ALL_ON.items():
        monkeypatch.setenv(key, value)


@pytest.mark.asyncio
async def test_gmail_send_proceeds_when_outbound_is_enabled(
    outbound_fully_enabled, transports_that_explode, monkeypatch
):
    monkeypatch.setenv("GMAIL_CLIENT_ID", "placeholder-client-id")
    monkeypatch.setenv("GMAIL_CLIENT_SECRET", "placeholder-client-secret")
    monkeypatch.setenv("GMAIL_REFRESH_TOKEN", "placeholder-refresh-token")
    monkeypatch.setenv("GMAIL_SENDER_EMAIL", "founder@example.com")

    from auto_client_acquisition.email.gmail_send import send_email

    # Returns rather than raises: the OAuth refresh swallows transport errors.
    await send_email(
        to_email="buyer@example.com",
        subject="Approved subject",
        body_plain="Approved body.",
    )

    assert transports_that_explode, (
        "Nothing reached the transport with outbound fully enabled — "
        "the guard is blocking unconditionally, which would make the "
        "blocked-path tests above meaningless."
    )


@pytest.mark.asyncio
async def test_smtp_proceeds_when_outbound_is_enabled(
    outbound_fully_enabled, transports_that_explode, monkeypatch
):
    from integrations.email import EmailClient

    client = EmailClient()
    # _send_smtp early-returns unless BOTH host and user are configured.
    monkeypatch.setattr(client.settings, "smtp_host", "smtp.example.com", raising=False)
    monkeypatch.setattr(client.settings, "smtp_user", "placeholder-user", raising=False)
    monkeypatch.setattr(client.settings, "smtp_port", 587, raising=False)

    # Returns rather than raises: _send_smtp catches broadly around the send.
    await client._send_smtp("buyer@example.com", "subject", "text", None, None)

    assert "smtplib.SMTP" in transports_that_explode, (
        "SMTP was never constructed with outbound fully enabled — the guard "
        "is blocking unconditionally."
    )


def test_draft_path_is_unaffected_by_the_kill_switch(monkeypatch):
    """draft_only must still produce drafts — the guard must not touch them."""
    from auto_client_acquisition.email import gmail_send

    assert not hasattr(gmail_send.create_draft, "__egress_channel__"), (
        "create_draft is guarded; draft_only mode would produce nothing."
    )
    assert getattr(gmail_send.send_email, "__egress_channel__", None) == "email"


# ── Regression: the three senders the first version of this file missed ─────


def test_every_messaging_provider_in_the_repo_is_a_known_marker():
    """The marker list must come from the tree, not from memory.

    The first version listed five hosts and missed three live senders. This
    re-derives the set from source so a newly integrated provider fails here
    instead of quietly bypassing the kill switch.
    """
    import re

    pattern = re.compile(
        r"https://([a-z0-9.-]*(?:twilio|unifonic|resend|sendgrid|mailgun|postmark"
        r"|graph\.facebook|graph\.instagram|green-api|ultramsg|fonnte"
        r"|gmail\.googleapis)[a-z0-9.-]*)"
    )
    found: set[str] = set()
    for directory in ("api", "app", "auto_client_acquisition", "dealix", "integrations", "company", "core"):
        for path in (REPO_ROOT / directory).rglob("*.py"):
            found.update(pattern.findall(path.read_text(encoding="utf-8", errors="ignore")))

    unlisted = {host for host in found if host not in PROVIDER_MARKERS}

    assert not unlisted, (
        f"Messaging providers not in PROVIDER_MARKERS: {sorted(unlisted)}. "
        "Add them and confirm every sender using them carries @guarded_egress."
    )


def test_mfa_exemption_is_recorded_with_a_reason():
    """The exemption must be a decision on the record, not an oversight."""
    assert "api/security/mfa.py" in MESSAGING_EXEMPT_MODULES
    assert len(MESSAGING_EXEMPT_MODULES["api/security/mfa.py"]) > 100, (
        "an exemption from the outbound kill switch needs an argued reason"
    )


@pytest.mark.asyncio
async def test_whatsapp_automation_is_blocked_when_outbound_is_disabled(
    outbound_disabled, transports_that_explode, monkeypatch
):
    """company/automation reaches the network via requests, not httpx.

    This sender was missed entirely by the first version: its host was not in
    PROVIDER_MARKERS and its transport was not patched, so it could have sent
    while every test passed.
    """
    monkeypatch.setenv("WHATSAPP_API_KEY", "placeholder-key")
    monkeypatch.setenv("WHATSAPP_BUSINESS_ACCOUNT_ID", "placeholder-account")
    monkeypatch.setenv("WHATSAPP_PHONE_NUMBER_ID", "placeholder-phone")

    from company.automation.whatsapp_automation import WhatsAppAutomation

    result = WhatsAppAutomation().send_message(
        recipient_phone="+966500000000", message_ar="مرحبا"
    )

    assert result["status"] == "blocked_policy"
    assert transports_that_explode == [], (
        f"reached the network while outbound was disabled: {transports_that_explode}"
    )


def test_whatsapp_automation_proceeds_when_outbound_is_enabled(
    outbound_fully_enabled, transports_that_explode, monkeypatch
):
    """Positive control — the guard must be a gate, not a wall."""
    monkeypatch.setenv("WHATSAPP_API_KEY", "placeholder-key")
    monkeypatch.setenv("WHATSAPP_BUSINESS_ACCOUNT_ID", "placeholder-account")
    monkeypatch.setenv("WHATSAPP_PHONE_NUMBER_ID", "placeholder-phone")

    from company.automation.whatsapp_automation import WhatsAppAutomation

    # Unlike the gmail and smtp senders, this one does not swallow transport
    # errors, so the recorder's AssertionError propagates.
    with pytest.raises(AssertionError, match="egress attempted"):
        WhatsAppAutomation().send_message(
            recipient_phone="+966500000000", message_ar="مرحبا"
        )

    assert "requests.post" in transports_that_explode, (
        "requests.post was never reached with outbound fully enabled — the "
        "guard is blocking unconditionally."
    )
