#!/usr/bin/env python3
"""Unified founder Close Packet generator.

Turns a single warm prospect into one bilingual, send-ready markdown packet
by orchestrating the existing close-flow functions. No new business logic is
invented here: qualification, diagnostic, proposal, and outreach style are all
reused from their canonical modules.

Reused entry points:
- auto_client_acquisition.sales_os.qualification.qualify
- scripts.dealix_ai_ops_diagnostic.build_diagnostic + render_markdown
- auto_client_acquisition.sales_os.proposal_renderer.render_proposal + ProposalContext
- warm-list bilingual message style (mirrored, not imported, to keep this offline)
- auto_client_acquisition.connectors.tech_detect.detect_stack (optional, --domain only)

Doctrine constraints honored:
- Outreach is a DRAFT only. The founder sends manually. Nothing is auto-sent.
- No invented KPIs or metrics; no guaranteed-outcome language.
- Every outreach draft passes through governance_os.policy_check_draft. If the
  draft or the requested channel is blocked, the channel is refused and no
  message is emitted.
- A reject or refer-out qualification produces no proposal and no outreach.

The core (build_close_packet) is a pure function over a dict so it can be
tested without subprocess and without network access.

Usage:
    python scripts/dealix_close_packet_generator.py \
        --company "Demo Saudi Realty" --sector real_estate \
        --decision-maker "Ahmad Al-Zaini" --role CEO --city Riyadh \
        --channel whatsapp --relationship warm \
        --out data/activation_pack/close_packet_DEMO.md
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from auto_client_acquisition.governance_os import policy_check_draft
from auto_client_acquisition.sales_os.proposal_renderer import (
    ProposalContext,
    render_proposal,
)
from auto_client_acquisition.sales_os.qualification import qualify
from scripts.dealix_ai_ops_diagnostic import build_diagnostic, render_markdown

# Qualification flags consumed by qualify(); each has a warm-lead default.
_QUALIFY_FLAGS: tuple[str, ...] = (
    "pain_clear",
    "owner_present",
    "data_available",
    "accepts_governance",
    "has_budget",
    "wants_safe_methods",
    "proof_path_visible",
    "retainer_path_visible",
)

# Warm-lead defaults: a warm referral with budget and a visible proof path.
# retainer_path_visible stays False so a default warm lead scores 90 (ACCEPT)
# without over-claiming a confirmed retainer path.
_WARM_DEFAULTS: dict[str, bool] = {
    "pain_clear": True,
    "owner_present": True,
    "data_available": True,
    "accepts_governance": True,
    "has_budget": True,
    "wants_safe_methods": True,
    "proof_path_visible": True,
    "retainer_path_visible": False,
}

_VALID_CHANNELS: tuple[str, ...] = ("linkedin", "whatsapp", "email")
_VALID_RELATIONSHIPS: tuple[str, ...] = ("warm", "cold", "referral")

# Offer catalogue keyed by qualification decision. Reject / refer_out have no
# offer on purpose (no proposal is produced for them).
_OFFER_BY_DECISION: dict[str, dict[str, Any]] = {
    "accept": {
        "title_en": "7-Day Revenue Intelligence Sprint",
        "title_ar": "Sprint ذكاء الإيراد — 7 أيام",
        "motion": "revenue_intelligence_sprint",
        "price_sar": 499,
        "delivery_days": 7,
        "proof_score_target": 80,
        "exclusions": ProposalContext.__dataclass_fields__["exclusions"].default,
    },
    "reframe": {
        "title_en": "Scoped Discovery (Data-to-Revenue)",
        "title_ar": "Discovery محدود النطاق (من البيانات إلى الإيراد)",
        "motion": "scoped_discovery",
        "price_sar": 249,
        "delivery_days": 5,
        "proof_score_target": 70,
        "exclusions": ProposalContext.__dataclass_fields__["exclusions"].default,
    },
    "diagnostic_only": {
        "title_en": "Capability Diagnostic (Diagnostic-Only)",
        "title_ar": "تشخيص القدرة التشغيلية (تشخيص فقط)",
        "motion": "capability_diagnostic",
        "price_sar": 0,
        "delivery_days": 1,
        "proof_score_target": 60,
        "exclusions": ProposalContext.__dataclass_fields__["exclusions"].default,
    },
}

_DISCLAIMER_LINES: tuple[str, ...] = (
    "Estimated value is not Verified value / "
    "القيمة التقديرية ليست قيمة مُتحقَّقة",
    "Estimated outcomes are not guaranteed outcomes / "
    "النتائج التقديرية ليست نتائج مضمونة",
)

# Per-channel CTA options (founder picks exactly one before sending).
_CTA_OPTIONS: tuple[str, ...] = (
    "Risk Score",
    "Sample Proof",
    "10-min demo",
)


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _slug(value: str) -> str:
    keep = [c.lower() if c.isalnum() else "_" for c in (value or "").strip()]
    slug = "".join(keep).strip("_")
    while "__" in slug:
        slug = slug.replace("__", "_")
    return slug or "prospect"


def _resolve_flags(prospect: dict[str, Any]) -> dict[str, bool]:
    """Resolve the 8 qualification flags from the prospect dict.

    A `signals` mapping (if present) or top-level booleans override the
    relationship-derived defaults. Cold relationships start from a weaker
    posture so they do not silently qualify as ACCEPT.
    """
    relationship = str(prospect.get("relationship") or "warm").lower()
    signals = prospect.get("signals")

    if isinstance(signals, dict):
        # A signals dict is authoritative: it is a complete allowlist. Any flag
        # not present is treated as False. This matches the CLI --signals
        # shortcut and keeps the verdict predictable for callers and tests.
        base = {flag: bool(signals.get(flag, False)) for flag in _QUALIFY_FLAGS}
    else:
        base = dict(_WARM_DEFAULTS)
        if relationship == "cold":
            # Cold contacts have not shown pain/budget/data yet — keep them
            # diagnostic-grade until the founder confirms otherwise.
            base.update(
                {
                    "pain_clear": False,
                    "data_available": False,
                    "has_budget": False,
                    "proof_path_visible": True,
                }
            )

    # Explicit top-level booleans (rare) win over both forms above.
    for flag in _QUALIFY_FLAGS:
        if flag in prospect:
            base[flag] = bool(prospect[flag])
    return base


def _render_outreach_messages(
    *,
    name: str,
    company: str,
    role: str,
    sector: str,
    channel: str,
    cta: str,
    warm_intro_notes: str,
) -> tuple[str, str]:
    """Build channel-length-tuned bilingual outreach drafts.

    Mirrors the warm-list bilingual style. Contains no metrics, no guarantees,
    and no cold-channel language. WhatsApp is shortest, email longest.
    """
    intro_ar = (
        f" ({warm_intro_notes})" if warm_intro_notes else ""
    )
    intro_en = (
        f" ({warm_intro_notes})" if warm_intro_notes else ""
    )
    cta_line_ar = {
        "Risk Score": "أقدر أرسل لك Risk Score مبدئي بدون أي التزام",
        "Sample Proof": "أقدر أشاركك عينة Proof Pack من نفس القطاع",
        "10-min demo": "نقدر نسوي مكالمة 10 دقائق أشرح لك الطريقة",
    }.get(cta, "أقدر أرسل لك Risk Score مبدئي بدون أي التزام")
    cta_line_en = {
        "Risk Score": "I can send you a starter Risk Score with no commitment",
        "Sample Proof": "I can share a sample Proof Pack from your sector",
        "10-min demo": "we can do a 10-minute call so I walk you through it",
    }.get(cta, "I can send you a starter Risk Score with no commitment")

    # Governance posture is stated positively. Forbidden techniques are never
    # named in outreach copy so the draft passes policy_check_draft cleanly and
    # the prospect never sees those terms.
    if channel == "whatsapp":
        ar = (
            f"السلام عليكم {name},\n"
            f"معك سامي من Dealix. أعمل مع شركات {sector} على ذكاء الإيراد "
            f"بحوكمة واضحة: كل خطوة بموافقتك، ومن مصادر موثّقة، وبدون وعود.{intro_ar}\n"
            f"بالنظر لدورك في {company} كـ{role}، {cta_line_ar}. مناسب؟"
        )
        en = (
            f"Hi {name},\n"
            f"Sami from Dealix. I work with {sector} companies on revenue "
            f"intelligence under explicit governance: approval-first, "
            f"source-verified, and no promises.{intro_en}\n"
            f"Given your role at {company} as {role}, {cta_line_en}. Open to it?"
        )
        return ar, en

    if channel == "linkedin":
        ar = (
            f"السلام عليكم {name},\n\n"
            f"معك سامي من Dealix. أبني خدمة ذكاء إيراد لشركات {sector} "
            f"السعودية — بيانات نظيفة، فرص مرتبة، Proof Pack — كلها محكومة "
            f"بحوكمة AI: كل خطوة بموافقتك، ومن مصادر موثّقة، وبدون وعود.{intro_ar}\n\n"
            f"بالنظر لدورك في {company} كـ{role}، {cta_line_ar}.\n\n"
            f"شكرًا — سامي."
        )
        en = (
            f"Hi {name},\n\n"
            f"Sami from Dealix. I'm building revenue intelligence for Saudi "
            f"{sector} companies — clean data, ranked opportunities, a Proof "
            f"Pack — all under explicit AI governance: approval-first, "
            f"source-verified, and no promises.{intro_en}\n\n"
            f"Given your role at {company} as {role}, {cta_line_en}.\n\n"
            f"Thanks — Sami."
        )
        return ar, en

    # email (longest)
    ar = (
        f"السلام عليكم {name},\n\n"
        f"معك سامي من Dealix. نساعد شركات {sector} السعودية على تحويل "
        f"بياناتها التشغيلية إلى فرص إيراد مرتبة، مع Proof Pack موثّق لكل "
        f"مخرج. كل شيء محكوم بحوكمة AI: كل خطوة بموافقتك، ومن مصادر موثّقة، "
        f"وبدون أرقام مخترعة، وبدون وعود.{intro_ar}\n\n"
        f"بالنظر لدورك في {company} كـ{role} وقطاع {sector}، أعتقد فيه "
        f"قيمة واضحة نقدر نثبتها قبل أي التزام:\n"
        f"  • تشخيص مبدئي للقدرة التشغيلية\n"
        f"  • Sprint مدفوع 499 ريال (7 أيام، Proof Pack، نطاق محدد)\n\n"
        f"{cta_line_ar}.\n\n"
        f"شكرًا — سامي."
    )
    en = (
        f"Hi {name},\n\n"
        f"Sami from Dealix. We help Saudi {sector} companies turn their "
        f"operating data into ranked revenue opportunities, with a documented "
        f"Proof Pack for every output. Everything runs under explicit AI "
        f"governance: approval-first, source-verified, no invented numbers, "
        f"and no promises.{intro_en}\n\n"
        f"Given your role at {company} as {role} in {sector}, I believe there "
        f"is clear value we can prove before any commitment:\n"
        f"  • a starter operating-capability diagnostic\n"
        f"  • a 499 SAR paid Sprint (7 days, Proof Pack, defined scope)\n\n"
        f"{cta_line_en}.\n\n"
        f"Thanks — Sami."
    )
    return ar, en


def _build_proposal_section(
    *,
    decision: str,
    company: str,
    handle: str,
    sector: str,
    city: str,
    engagement_id: str,
) -> dict[str, Any]:
    """Render the matched proposal for a non-rejected decision.

    Returns a dict with the motion, price, and rendered markdown, or a
    no-proposal marker for reject / refer_out.
    """
    offer = _OFFER_BY_DECISION.get(decision)
    if offer is None:
        return {
            "produced": False,
            "motion": None,
            "price_sar": None,
            "reason": "no_proposal_for_decision",
            "markdown": "",
        }

    context = ProposalContext(
        customer_name=company,
        customer_handle=handle,
        sector=sector,
        city=city,
        engagement_id=engagement_id,
        price_sar=int(offer["price_sar"]),
        delivery_days=int(offer["delivery_days"]),
        proof_score_target=int(offer["proof_score_target"]),
        exclusions=offer["exclusions"],
        proposal_date=datetime.now(UTC).strftime("%Y-%m-%d"),
    )
    markdown = render_proposal(context)
    return {
        "produced": True,
        "motion": offer["motion"],
        "title_en": offer["title_en"],
        "title_ar": offer["title_ar"],
        "price_sar": int(offer["price_sar"]),
        "markdown": markdown,
    }


def _stack_section(detected_stack: dict[str, Any] | None) -> dict[str, Any]:
    """Normalize an optional detect_stack result into a small summary."""
    if not isinstance(detected_stack, dict):
        return {"available": False, "tools": [], "signals": [], "note": "no_domain_provided"}

    tools_raw = detected_stack.get("tools") or []
    signals_raw = detected_stack.get("signals") or []
    tools: list[str] = []
    for t in tools_raw:
        if isinstance(t, dict):
            name = str(t.get("name") or "").strip()
            if name:
                tools.append(name)
        elif isinstance(t, str):
            tools.append(t)
    signals: list[str] = []
    for s in signals_raw:
        if isinstance(s, dict):
            name = str(s.get("name") or "").strip()
            if name:
                signals.append(name)
        elif isinstance(s, str):
            signals.append(s)
    return {
        "available": bool(tools or signals),
        "domain": str(detected_stack.get("domain") or ""),
        "status": str(detected_stack.get("status") or ""),
        "tools": tools[:12],
        "signals": signals[:12],
        "note": "" if (tools or signals) else "no_stack_detected",
    }


def build_close_packet(
    prospect: dict[str, Any],
    *,
    detected_stack: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Assemble the full close packet for one prospect.

    Pure function: no I/O, no network. Pass `detected_stack` (the dict form of
    a TechStackResult) only when a domain was enriched upstream; otherwise the
    diagnostic degrades gracefully.

    Returns a machine-readable dict; the rendered bilingual markdown is under
    the `markdown` key. `build_close_packet_markdown` returns just the string.
    """
    company = str(prospect.get("company") or "").strip()
    if not company:
        raise ValueError("company_required")
    sector = str(prospect.get("sector") or "").strip()
    if not sector:
        raise ValueError("sector_required")

    city = str(prospect.get("city") or "Riyadh").strip() or "Riyadh"
    decision_maker = str(prospect.get("decision_maker") or "").strip()
    role = str(prospect.get("role") or "").strip()
    channel = str(prospect.get("channel") or "whatsapp").strip().lower()
    if channel not in _VALID_CHANNELS:
        raise ValueError(f"invalid_channel:{channel}")
    relationship = str(prospect.get("relationship") or "warm").strip().lower()
    if relationship not in _VALID_RELATIONSHIPS:
        raise ValueError(f"invalid_relationship:{relationship}")
    warm_intro_notes = str(prospect.get("warm_intro_notes") or "").strip()
    raw_request_text = str(prospect.get("raw_request_text") or "").strip()
    generated_at = str(prospect.get("generated_at") or _now_iso())

    flags = _resolve_flags(prospect)

    qualification = qualify(
        raw_request_text=raw_request_text,
        sector=sector,
        city=city,
        **flags,
    )
    decision = qualification.decision
    doctrine_violations = list(qualification.doctrine_violations)

    # ── Channel safety: relationship + doctrine + governance pre-check ──
    channel_refused = False
    channel_refusal_reasons: list[str] = []
    safe_channel_alternative = "founder-initiated warm introduction (manual)"

    if doctrine_violations:
        channel_refused = True
        channel_refusal_reasons.append("doctrine_violation")
    if relationship == "cold":
        # Cold-channel outreach is never automated; the packet refuses to draft
        # an outreach message for a cold basis and routes to a warm path.
        channel_refused = True
        channel_refusal_reasons.append("cold_relationship_basis")

    # ── Diagnostic (reused, bilingual) ──
    diagnostic = build_diagnostic(
        company=company,
        sector=sector,
        region=city,
        problem=raw_request_text,
        language="both",
    )
    diagnostic_markdown = render_markdown(diagnostic)
    stack = _stack_section(detected_stack)

    # ── Proposal (matched to decision) ──
    handle = "@" + _slug(company)
    engagement_id = f"CP-{_slug(company)[:24]}"
    proposal = _build_proposal_section(
        decision=decision,
        company=company,
        handle=handle,
        sector=sector,
        city=city,
        engagement_id=engagement_id,
    )

    # ── Outreach draft (only if safe + a proposal/engagement exists) ──
    outreach: dict[str, Any] = {
        "produced": False,
        "channel": channel,
        "reason": "",
        "policy_issues": [],
        "ar": "",
        "en": "",
    }
    cta = _CTA_OPTIONS[0]
    engageable = decision in _OFFER_BY_DECISION
    if not engageable:
        outreach["reason"] = "no_outreach_for_reject_or_refer_out"
    elif channel_refused:
        outreach["reason"] = "channel_refused:" + ",".join(channel_refusal_reasons)
    else:
        name = decision_maker or "—"
        ar_msg, en_msg = _render_outreach_messages(
            name=name,
            company=company,
            role=role or "—",
            sector=sector,
            channel=channel,
            cta=cta,
            warm_intro_notes=warm_intro_notes,
        )
        # Governance pre-check: the canonical guard used by the doctrine tests.
        check = policy_check_draft(ar_msg + "\n" + en_msg)
        if not check.allowed:
            outreach["reason"] = "policy_blocked"
            outreach["policy_issues"] = list(check.issues)
            channel_refused = True
            channel_refusal_reasons.append("policy_blocked")
        else:
            outreach.update({"produced": True, "ar": ar_msg, "en": en_msg, "cta": cta})

    machine = {
        "company": company,
        "sector": sector,
        "city": city,
        "decision_maker": decision_maker,
        "role": role,
        "channel": channel,
        "relationship": relationship,
        "generated_at": generated_at,
        "qualification": qualification.to_dict(),
        "decision": decision,
        "doctrine_violations": doctrine_violations,
        "channel_refused": channel_refused,
        "channel_refusal_reasons": channel_refusal_reasons,
        "safe_channel_alternative": safe_channel_alternative,
        "diagnostic": diagnostic,
        "detected_stack": stack,
        "proposal": proposal,
        "outreach": outreach,
        "cta_options": list(_CTA_OPTIONS),
        "disclaimer": list(_DISCLAIMER_LINES),
    }
    machine["markdown"] = _render_packet_markdown(
        machine,
        diagnostic_markdown=diagnostic_markdown,
    )
    return machine


def build_close_packet_markdown(
    prospect: dict[str, Any],
    *,
    detected_stack: dict[str, Any] | None = None,
) -> str:
    """Convenience wrapper returning only the rendered bilingual markdown."""
    return build_close_packet(prospect, detected_stack=detected_stack)["markdown"]


def _decision_badge(decision: str) -> str:
    return {
        "accept": "ACCEPT",
        "reframe": "REFRAME",
        "diagnostic_only": "DIAGNOSTIC_ONLY",
        "reject": "REJECT",
        "refer_out": "REFER_OUT",
    }.get(decision, decision.upper())


def _render_packet_markdown(machine: dict[str, Any], *, diagnostic_markdown: str) -> str:
    q = machine["qualification"]
    decision = machine["decision"]
    lines: list[str] = []

    # 1. Header
    lines.append(f"# Close Packet — {machine['company']}")
    lines.append("")
    lines.append(
        f"**Sector:** {machine['sector']} · **City:** {machine['city']} · "
        f"**Channel:** {machine['channel']} · **Relationship:** {machine['relationship']}"
    )
    dm = machine["decision_maker"] or "—"
    role = machine["role"] or "—"
    lines.append(f"**Decision maker:** {dm} ({role})")
    lines.append(f"**Generated at:** {machine['generated_at']}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # 2. Qualification verdict
    lines.append("## 1. Qualification verdict / حكم التأهيل")
    lines.append("")
    lines.append(f"- **Decision / القرار:** `{_decision_badge(decision)}`")
    lines.append(f"- **Score / الدرجة:** {q['score']} / 100")
    lines.append(f"- **Recommended offer / العرض المقترح:** `{q['recommended_offer']}`")
    if q.get("reasons"):
        lines.append(f"- **Reasons / الأسباب:** {', '.join(q['reasons'])}")
    lines.append("")
    if machine["doctrine_violations"]:
        lines.append(
            "> **DOCTRINE VIOLATION / خرق العقيدة:** "
            + ", ".join(machine["doctrine_violations"])
        )
        lines.append(">")
        lines.append(
            "> The requested approach violates a non-negotiable. The offending "
            "channel is REFUSED. Safe alternative: "
            f"**{machine['safe_channel_alternative']}**."
        )
        lines.append(
            "> النهج المطلوب يخالف مبدأ غير قابل للتفاوض. القناة المخالفة "
            "مرفوضة. البديل الآمن: مقدّمة دافئة يبدؤها المؤسس يدويًا."
        )
        lines.append("")

    # 3. Free diagnostic (reused)
    lines.append("## 2. Free diagnostic / التشخيص المجاني")
    lines.append("")
    stack = machine["detected_stack"]
    if stack.get("available"):
        lines.append(
            "**Detected stack / المكدّس المكتشف "
            f"({stack.get('domain', '')}):** "
            + ", ".join(stack.get("tools") or []) or "—"
        )
        if stack.get("signals"):
            lines.append(
                "**Signals / الإشارات:** " + ", ".join(stack["signals"])
            )
        lines.append("")
    else:
        note = stack.get("note") or "no_domain_provided"
        lines.append(f"_Stack enrichment: {note} (insufficient_data — graceful degrade)._")
        lines.append("")
    lines.append(diagnostic_markdown)
    lines.append("")
    lines.append("---")
    lines.append("")

    # 4. Matched proposal
    lines.append("## 3. Matched proposal / العرض المطابق")
    lines.append("")
    proposal = machine["proposal"]
    if proposal["produced"]:
        lines.append(
            f"**Motion:** `{proposal['motion']}` · "
            f"**Price:** {proposal['price_sar']} SAR · "
            f"matched to decision `{_decision_badge(decision)}`."
        )
        lines.append("")
        lines.append(proposal["markdown"])
    else:
        lines.append(
            "**No proposal produced.** Decision "
            f"`{_decision_badge(decision)}` does not qualify for an offer."
        )
        lines.append("")
        lines.append(
            "Recommended next step: **refer out** politely. Do not pitch. "
            "لا يوجد عرض — يُفضّل الإحالة (refer-out) بأدب دون أي عرض."
        )
    lines.append("")
    lines.append("---")
    lines.append("")

    # 5. Channel-optimized outreach DRAFT
    lines.append("## 4. Outreach DRAFT — founder sends manually; never auto-sent")
    lines.append("## (مسوّدة تواصل — يرسلها المؤسس يدويًا؛ لا تُرسَل تلقائيًا)")
    lines.append("")
    outreach = machine["outreach"]
    if outreach["produced"]:
        lines.append(
            f"**Channel:** {outreach['channel']} · **Suggested CTA:** "
            f"{outreach.get('cta', _CTA_OPTIONS[0])} "
            "(pick exactly one before sending)."
        )
        lines.append("")
        lines.append("### Arabic (primary) / عربي (أساسي)")
        lines.append("```")
        lines.append(outreach["ar"])
        lines.append("```")
        lines.append("")
        lines.append("### English (secondary)")
        lines.append("```")
        lines.append(outreach["en"])
        lines.append("```")
    else:
        reason = outreach.get("reason") or "not_produced"
        lines.append(f"**No outreach draft produced.** Reason: `{reason}`.")
        if outreach.get("policy_issues"):
            lines.append(
                "Policy issues: " + ", ".join(outreach["policy_issues"]) + "."
            )
        lines.append("")
        if reason.startswith("channel_refused") or reason == "policy_blocked":
            lines.append(
                "Offending channel REFUSED. Use the safe alternative: "
                f"**{machine['safe_channel_alternative']}**."
            )
            lines.append(
                "القناة المخالفة مرفوضة. استخدم البديل الآمن: "
                "مقدّمة دافئة يبدؤها المؤسس يدويًا."
            )
        else:
            lines.append(
                "Reject / refer-out decisions get no outreach. Decline politely. "
                "قرارات الرفض/الإحالة بلا تواصل — اعتذر بأدب."
            )
    lines.append("")
    lines.append("---")
    lines.append("")

    # 6. Founder pre-send checklist
    lines.append("## 5. Founder pre-send checklist / قائمة ما قبل الإرسال")
    lines.append("")
    lines.append("- [ ] Source / relationship basis logged (warm / referral only)")
    lines.append("- [ ] No doctrine violation flagged above")
    lines.append("- [ ] Exactly one CTA chosen (Risk Score | Sample Proof | 10-min demo)")
    lines.append("- [ ] No invented metric, no guaranteed-outcome wording")
    lines.append("- [ ] Reviewed by founder before any manual send")
    lines.append("")
    lines.append("- [ ] أساس العلاقة مسجّل (دافئ / إحالة فقط)")
    lines.append("- [ ] لا خرق عقيدة أعلاه")
    lines.append("- [ ] CTA واحد فقط (Risk Score | Sample Proof | 10-min demo)")
    lines.append("- [ ] لا أرقام مخترعة ولا وعود بنتائج")
    lines.append("- [ ] مراجعة المؤسس قبل أي إرسال يدوي")
    lines.append("")
    lines.append("---")
    lines.append("")

    # 7. Footer disclaimer
    lines.append("## Disclaimer / إخلاء مسؤولية")
    for d in machine["disclaimer"]:
        lines.append(f"- _{d}_")
    lines.append("")
    return "\n".join(lines)


def _enrich_domain(domain: str) -> dict[str, Any] | None:
    """Run the async tech detector for a domain. Degrade gracefully on failure.

    Network-bound; called only from the CLI when --domain is supplied. The core
    builder never calls this so tests stay offline.
    """
    import asyncio

    try:
        from auto_client_acquisition.connectors.tech_detect import detect_stack
    except Exception:
        return None
    try:
        result = asyncio.run(detect_stack(domain, timeout=10.0))
    except Exception:
        return None
    try:
        return result.to_dict()
    except Exception:
        return None


def _build_prospect_from_args(args: argparse.Namespace) -> dict[str, Any]:
    prospect: dict[str, Any] = {
        "company": args.company,
        "sector": args.sector,
        "decision_maker": args.decision_maker or "",
        "role": args.role or "",
        "city": args.city,
        "channel": args.channel,
        "relationship": args.relationship,
        "warm_intro_notes": args.warm_intro_notes or "",
        "raw_request_text": args.raw_request_text or "",
    }
    # Resolve the 8 qualification flags: explicit --flag/--no-flag wins; else
    # the --signals shortcut; else relationship-derived defaults in the core.
    signals: dict[str, bool] = {}
    if args.signals:
        requested = {s.strip().lower() for s in args.signals.split(",") if s.strip()}
        unknown = requested - set(_QUALIFY_FLAGS)
        if unknown:
            raise SystemExit(
                "unknown --signals flags: " + ", ".join(sorted(unknown))
            )
        for flag in _QUALIFY_FLAGS:
            signals[flag] = flag in requested
    for flag in _QUALIFY_FLAGS:
        val = getattr(args, flag, None)
        if val is not None:
            signals[flag] = bool(val)
    if signals:
        prospect["signals"] = signals
    return prospect


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate one bilingual, send-ready founder Close Packet."
    )
    parser.add_argument("--company", required=True)
    parser.add_argument("--sector", required=True)
    parser.add_argument("--decision-maker", dest="decision_maker", default="")
    parser.add_argument("--role", default="")
    parser.add_argument("--city", default="Riyadh")
    parser.add_argument("--channel", choices=list(_VALID_CHANNELS), default="whatsapp")
    parser.add_argument(
        "--relationship", choices=list(_VALID_RELATIONSHIPS), default="warm"
    )
    parser.add_argument("--warm-intro-notes", dest="warm_intro_notes", default="")
    parser.add_argument(
        "--domain", default="", help="Optional domain for tech-stack enrichment."
    )
    parser.add_argument(
        "--raw-request-text",
        dest="raw_request_text",
        default="",
        help="Free-text prospect request (scanned for doctrine violations).",
    )
    parser.add_argument(
        "--signals",
        default="",
        help=(
            "Comma-separated qualification flags to set true "
            "(e.g. pain_clear,owner_present,data_available). Any not listed "
            "are treated as false. Overridden by explicit --flag options."
        ),
    )
    # Explicit per-flag toggles (override --signals and defaults).
    for flag in _QUALIFY_FLAGS:
        dest = flag
        cli = flag.replace("_", "-")
        parser.add_argument(
            f"--{cli}",
            dest=dest,
            action="store_true",
            default=None,
        )
        parser.add_argument(
            f"--no-{cli}",
            dest=dest,
            action="store_false",
            default=None,
        )
    parser.add_argument(
        "--out",
        default="",
        help="Output markdown path (default data/outreach/close_packet_<company>.md).",
    )
    parser.add_argument(
        "--json",
        dest="json_out",
        default="",
        help="Optional path for the machine-readable JSON packet.",
    )
    args = parser.parse_args(argv)

    prospect = _build_prospect_from_args(args)

    detected_stack: dict[str, Any] | None = None
    if args.domain.strip():
        detected_stack = _enrich_domain(args.domain.strip())

    packet = build_close_packet(prospect, detected_stack=detected_stack)

    out_path = (
        Path(args.out)
        if args.out
        else REPO_ROOT / "data" / "outreach" / f"close_packet_{_slug(args.company)}.md"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(packet["markdown"], encoding="utf-8")

    if args.json_out:
        json_path = Path(args.json_out)
        json_path.parent.mkdir(parents=True, exist_ok=True)
        machine = {k: v for k, v in packet.items() if k != "markdown"}
        json_path.write_text(
            json.dumps(machine, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    print(f"OK: wrote close packet to {out_path}")
    print(f"  decision: {packet['decision']} (score {packet['qualification']['score']}/100)")
    print(f"  proposal: {'yes' if packet['proposal']['produced'] else 'none'}")
    print(f"  outreach: {'draft' if packet['outreach']['produced'] else 'refused/none'}")
    if packet["doctrine_violations"]:
        print(f"  doctrine_violations: {', '.join(packet['doctrine_violations'])}")
    if args.json_out:
        print(f"  json: {args.json_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
