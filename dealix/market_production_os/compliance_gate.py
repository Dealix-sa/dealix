"""The six-gate compliance check over a single outreach draft.

Gates: Brand Voice · Offer Match · Personalization · Compliance (opt-out,
subject honesty, sender identity, suppression) · plus the optional canonical
governance ``policy_check_draft`` folded in when the heavy stack is importable.
Deliverability and Founder Approval are checked at the account / workflow
layer (see ``deliverability.py`` / ``sending_ramp.py``).

The banned-term lists mirror
``auto_client_acquisition/governance_os/draft_gate.py`` and extend it with
cold-email-specific checks (CAN-SPAM / Google sender guidelines).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable

from dealix.market_production_os.models import OFFERS
from dealix.market_production_os.personalization import personalization_floor_ok

# Mirror of draft_gate.audit_draft_text forbidden terms.
_FORBIDDEN_TERMS: tuple[str, ...] = (
    "scraping",
    "scrape ",
    "purchased list",
    "cold whatsapp",
    "linkedin automation",
    "auto-send",
    "auto send",
    "send automatically without approval",
)
_GUARANTEE_TERMS: tuple[str, ...] = (
    "guaranteed sales",
    "guaranteed results",
    "guaranteed roi",
    "guarantee roi",
    "we guarantee",
    "نضمن لك",
    "نضمن لكم",
    "نضمن النتائج",
    "نضمن لك مبيعات",
    "fake proof",
    "fake testimonial",
)
_HYPE_TERMS: tuple[str, ...] = (
    "10x",
    "supercharge",
    "revolutionary",
    "disrupting",
    "transform your business",
)
# Cold subjects must not impersonate a reply/forward thread.
_MISLEADING_SUBJECT_PREFIXES: tuple[str, ...] = ("re:", "fwd:", "fw:", "رد:", "رد :")
_SPAMMY_SUBJECT: tuple[str, ...] = ("!!!", "$$$", "100% free", "act now", "free!!!")


@dataclass(frozen=True, slots=True)
class ComplianceResult:
    allowed: bool
    failures: tuple[str, ...] = ()
    gates: dict[str, bool] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "allowed": self.allowed,
            "failures": list(self.failures),
            "gates": dict(self.gates),
        }


def _hits(blob: str, terms: Iterable[str]) -> list[str]:
    return [t for t in terms if t in blob]


def _optional_policy_check(text: str) -> bool | None:
    """Fold the canonical governance check when its (heavy) stack imports.

    Returns True/False from ``policy_check_draft`` if available, else None so
    this module stays usable without pydantic / the app stack.
    """
    try:
        from auto_client_acquisition.governance_os import policy_check_draft
    except Exception:
        return None
    try:
        return bool(policy_check_draft(text).allowed)
    except Exception:
        return None


def check_draft(
    draft: dict[str, Any],
    *,
    suppressed_hashes: Iterable[str] = (),
    recipient_email_sha256: str | None = None,
    is_warm: bool = False,
) -> ComplianceResult:
    """Run all gates over a draft dict. Pure + deterministic."""
    failures: list[str] = []
    gates: dict[str, bool] = {}

    subject = str(draft.get("subject") or "")
    body = str(draft.get("body") or "")
    blob = f"{subject}\n{body}".lower()

    # Gate 1 — Brand voice / claims
    voice_ok = True
    for hit in _hits(blob, _GUARANTEE_TERMS):
        failures.append(f"guaranteed_claim:{hit}")
        voice_ok = False
    for hit in _hits(blob, _FORBIDDEN_TERMS):
        failures.append(f"forbidden_term:{hit}")
        voice_ok = False
    for hit in _hits(blob, _HYPE_TERMS):
        failures.append(f"hype:{hit}")
        voice_ok = False
    gates["brand_voice"] = voice_ok

    # Gate 2 — Offer match
    offer = draft.get("offer")
    offer_ok = offer in OFFERS
    if not offer_ok:
        failures.append(f"unknown_offer:{offer}")
    gates["offer_match"] = offer_ok

    # Gate 3 — Personalization floor
    level = str(draft.get("personalization_level", "P0"))
    touch = str(draft.get("touch_type", "first_touch"))
    pers_ok = personalization_floor_ok(level, touch, is_warm=is_warm)
    if not pers_ok:
        failures.append(f"personalization_below_floor:{level}")
    gates["personalization"] = pers_ok

    # Gate 4 — Compliance (opt-out, subject honesty, sender identity, suppression)
    comp_ok = True
    if not draft.get("unsubscribe_included") or draft.get("unsubscribe_method", "none") == "none":
        failures.append("missing_unsubscribe")
        comp_ok = False
    subj_l = subject.strip().lower()
    if any(subj_l.startswith(p) for p in _MISLEADING_SUBJECT_PREFIXES):
        failures.append("misleading_subject_prefix")
        comp_ok = False
    for hit in _hits(subj_l, _SPAMMY_SUBJECT):
        failures.append(f"spammy_subject:{hit}")
        comp_ok = False
    sender = draft.get("sender_identity") or {}
    if not (sender.get("from_name") and sender.get("from_email") and sender.get("physical_address")):
        failures.append("incomplete_sender_identity")
        comp_ok = False
    if recipient_email_sha256 and recipient_email_sha256 in set(suppressed_hashes):
        failures.append("recipient_suppressed")
        comp_ok = False
    gates["compliance"] = comp_ok

    # Optional — canonical governance policy
    policy = _optional_policy_check(f"{subject}\n{body}")
    if policy is False:
        failures.append("governance_policy_blocked")
        gates["governance_policy"] = False
    elif policy is True:
        gates["governance_policy"] = True

    allowed = voice_ok and offer_ok and pers_ok and comp_ok and (policy is not False)
    return ComplianceResult(allowed=allowed, failures=tuple(failures), gates=gates)
