"""Layer 3 — Content generation under draft_gate + claim_safety.

Produces bilingual short drafts. Refuses guaranteed-outcome language. Strips
PII before returning. Output is DRAFT_ONLY unless caller has an approval id.
"""
from __future__ import annotations

import re
from typing import Any

from auto_client_acquisition.ai_layers.schemas import LayerContext, LayerResult

# Conservative claim-safety patterns mirrored from governance_os.claim_safety.
_AR_GUARANTEE = re.compile(r"نضمن|ضمان\s*(?:نتائج|نتيجة|مبيعات|أرباح)")
_EN_GUARANTEE = re.compile(
    r"\bguaranteed?\s+(?:sales?|revenue|results?|roi|leads?|deals?)\b",
    re.IGNORECASE,
)
# Light PII redaction; the canonical detector lives in data_os.pii_classifier.
_EMAIL = re.compile(r"[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}")
_PHONE = re.compile(r"\+?\d[\d\s\-\(\)]{6,}\d")


def _redact(text: str) -> tuple[str, bool]:
    redacted = _EMAIL.sub("[REDACTED_EMAIL]", text)
    redacted = _PHONE.sub("[REDACTED_PHONE]", redacted)
    return redacted, redacted != text


def _has_unsafe_claim(text: str) -> bool:
    return bool(_AR_GUARANTEE.search(text) or _EN_GUARANTEE.search(text))


def _make_draft(
    *,
    topic: str,
    audience: str,
    cta: str,
    locale: str,
) -> str:
    if locale == "ar":
        return (
            f"مرحباً — بخصوص {topic} للقطاع {audience}: نقترح تشخيصاً مجانياً "
            f"يُغطي مصادر البيانات، فُرَص الإيرادات، وفجوات الامتثال. "
            f"{cta}"
        )
    return (
        f"Hello — regarding {topic} for the {audience} sector: we propose a "
        f"free diagnostic covering data sources, revenue opportunities, and "
        f"compliance gaps. {cta}"
    )


def run(ctx: LayerContext) -> LayerResult:
    """Generate a bilingual draft.

    Expected payload keys: topic (str), audience (str), cta (str), locales
    (list[str] subset of {'ar','en'}).
    """
    topic = str(ctx.payload.get("topic", "Revenue Intelligence Sprint"))
    audience = str(ctx.payload.get("audience", "B2B"))
    cta = str(ctx.payload.get("cta", "Reply to schedule the diagnostic."))
    locales = ctx.payload.get("locales", ["ar", "en"]) or ["ar", "en"]

    drafts: dict[str, str] = {}
    notes: list[str] = []
    redacted_any = False
    blocked = False

    for loc in locales:
        loc_key = "ar" if loc == "ar" else "en"
        text = _make_draft(topic=topic, audience=audience, cta=cta, locale=loc_key)
        if _has_unsafe_claim(text) or _has_unsafe_claim(topic) or _has_unsafe_claim(cta):
            blocked = True
            notes.append(f"unsafe_claim_blocked:{loc_key}")
            continue
        red, was_redacted = _redact(text)
        if was_redacted:
            redacted_any = True
        drafts[loc_key] = red

    if blocked and not drafts:
        return LayerResult(
            layer="content_generation",
            customer_id=ctx.customer_id,
            ok=False,
            governance_decision="REDACT",
            output={"reason": "unsafe_claim", "topic": topic},
            notes=tuple(notes),
        )

    decision = "REQUIRE_APPROVAL" if ctx.external_action_requested else "DRAFT_ONLY"
    if redacted_any:
        notes.append("pii_redacted")

    # Always end with the bilingual disclaimer per doctrine.
    disclaimer = (
        "Estimated value is not Verified value / "
        "القيمة التقديرية ليست قيمة مُتحقَّقة"
    )

    return LayerResult(
        layer="content_generation",
        customer_id=ctx.customer_id,
        ok=True,
        governance_decision=decision,
        output={
            "drafts": drafts,
            "disclaimer": disclaimer,
            "external_action_requested": ctx.external_action_requested,
        },
        notes=tuple(notes),
        capital_asset_candidates=("draft_template",) if not blocked else (),
    )
