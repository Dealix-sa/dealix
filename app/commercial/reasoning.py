"""The Commercial Brain — the reasoning core of the living system.

The brain *thinks*: it analyses an account or conversation, decides the next
best action across any commercial motion, picks an honest persuasion angle,
plans guardrailed negotiation, and drafts the next reply — always with a
rationale trace.

Two implementations:

* :class:`HeuristicBrain` — deterministic, explainable, dependency-free. This
  is the default and what the test-suite exercises. It is genuinely
  decision-making (state + signals → action), not a static template.
* :class:`LLMBrain` — optional. When ``COMMERCIAL_LLM_ENABLED=true`` and a
  provider key is configured, it asks a real model for phrasing/strategy and
  **always** falls back to the heuristic brain on any error. It never bypasses
  the safety gates or the claim guard.

Use :func:`get_brain` to obtain the active brain.
"""

from __future__ import annotations

import os
from typing import Any, Mapping, Protocol, runtime_checkable

from app.commercial import persuasion
from app.commercial.engagement_schemas import ActionRecommendation, PersuasionStrategy
from app.commercial.safety import contains_blocked_claim

# Reply intent → (next_stage, recommended_action, priority, risk).
_INTENT_PLAN: dict[str, tuple[str, str, int, str]] = {
    "interested": ("booking", "propose_booking", 1, "low"),
    "meeting_request": ("booking", "propose_booking", 1, "low"),
    "send_details": ("value", "send_details_pack", 2, "low"),
    "partnership_interest": ("value", "advance_partnership", 2, "low"),
    "price_objection": ("negotiation", "handle_objection", 2, "medium"),
    "not_now": ("nurture", "schedule_checkin", 3, "low"),
    "support_question": ("qualifying", "answer_question", 2, "low"),
    "referral": ("qualifying", "capture_referral", 3, "low"),
    "contract_request": ("closing", "escalate_to_founder", 1, "high"),
    "no_interest": ("lost", "close_lost", 4, "medium"),
    "unsubscribe": ("opted_out", "honour_optout", 1, "high"),
    "wrong_person": ("qualifying", "ask_right_contact", 3, "low"),
    "unknown": ("qualifying", "human_review", 3, "low"),
}


@runtime_checkable
class CommercialBrain(Protocol):
    source: str

    def recommend_action(self, context: Mapping[str, Any]) -> ActionRecommendation: ...
    def persuasion_for(self, motion: str) -> PersuasionStrategy: ...
    def draft_reply(self, context: Mapping[str, Any]) -> dict[str, str]: ...


# ── Heuristic (default) brain ───────────────────────────────────────────────────


class HeuristicBrain:
    """Deterministic, explainable decision engine."""

    source = "heuristic"

    def recommend_action(self, context: Mapping[str, Any]) -> ActionRecommendation:
        account_id = str(context.get("account_id", ""))
        ref_id = str(context.get("conversation_id", account_id))
        motion = str(context.get("motion", "sales_prospecting"))
        channel = str(context.get("channel", "email"))
        stage = str(context.get("stage", "opener"))
        intent = str(context.get("last_intent", "") or "")
        icp_score = float(context.get("icp_score", 0.0) or 0.0)
        opted_out = bool(context.get("opted_out", False))
        rationale: list[str] = []

        # Hard stops first.
        if opted_out or intent == "unsubscribe":
            return ActionRecommendation(
                ref_id=ref_id, account_id=account_id,
                recommended_action="honour_optout", motion=motion, channel=channel,
                rationale=["Contact opted out — stop all outreach immediately."],
                confidence=1.0, priority=1, next_stage="opted_out",
                risk_level="high", requires_approval=False, source=self.source,
            )

        # Reply-driven branch.
        if intent and intent in _INTENT_PLAN:
            next_stage, action, priority, risk = _INTENT_PLAN[intent]
            rationale.append(f"Inbound intent '{intent}' → {action}.")
            if intent == "contract_request":
                rationale.append("Legal/contract is A3-restricted: escalate, never accept.")
            angle = persuasion.strategy_for(motion).angle
            confidence = 0.9 if risk == "low" else 0.7
            return ActionRecommendation(
                ref_id=ref_id, account_id=account_id, recommended_action=action,
                motion=motion, channel=channel, rationale=rationale,
                confidence=confidence, priority=priority, persuasion_angle=angle,
                next_stage=next_stage, risk_level=risk,
                requires_approval=(intent != "unsubscribe"), source=self.source,
            )

        # No inbound yet → opener, prioritised by ICP fit.
        if stage in ("opener", ""):
            if icp_score >= 70:
                priority, conf = 1, 0.85
                rationale.append(f"High ICP fit ({icp_score:.0f}) — prioritise opener.")
            elif icp_score >= 50:
                priority, conf = 2, 0.7
                rationale.append(f"Medium ICP fit ({icp_score:.0f}).")
            else:
                priority, conf = 4, 0.5
                rationale.append(f"Low ICP fit ({icp_score:.0f}) — deprioritise.")
            angle = persuasion.strategy_for(motion).angle
            rationale.append(f"Persuasion angle: {angle}.")
            return ActionRecommendation(
                ref_id=ref_id, account_id=account_id, recommended_action="send_opener",
                motion=motion, channel=channel, rationale=rationale, confidence=conf,
                priority=priority, persuasion_angle=angle, next_stage="qualifying",
                risk_level="low", requires_approval=True, source=self.source,
            )

        # Mid-conversation with no fresh inbound → gentle follow-up.
        rationale.append(f"No new inbound at stage '{stage}' → prepare a follow-up.")
        return ActionRecommendation(
            ref_id=ref_id, account_id=account_id, recommended_action="follow_up",
            motion=motion, channel=channel, rationale=rationale, confidence=0.6,
            priority=3, persuasion_angle=persuasion.strategy_for(motion).angle,
            next_stage=stage, risk_level="low", requires_approval=True, source=self.source,
        )

    def persuasion_for(self, motion: str) -> PersuasionStrategy:
        return persuasion.strategy_for(motion)

    def draft_reply(self, context: Mapping[str, Any]) -> dict[str, str]:
        """Produce bilingual draft text for the recommended action.

        Pure phrasing — honest, no claims. The conversation engine adds buttons.
        """
        action = str(context.get("recommended_action", "send_opener"))
        motion = str(context.get("motion", "sales_prospecting"))
        company = str(context.get("company_name", "")) or "there"
        pain = str(context.get("pain_hypothesis", "")) or "your commercial follow-up"
        strat = persuasion.strategy_for(motion)
        objection = str(context.get("objection_type", "")) or str(context.get("last_intent", ""))

        ar, en = _draft_text(action, company, pain, strat, objection)

        # Backstop: never emit a blocked claim.
        if contains_blocked_claim(ar):
            ar = f"مرحباً {company}، يسعدنا ترتيب مكالمة قصيرة لمناقشة {pain} دون أي التزام."
        if contains_blocked_claim(en):
            en = f"Hi {company}, happy to set up a short, no-obligation call about {pain}."
        return {"ar": ar, "en": en}


def _draft_text(
    action: str, company: str, pain: str, strat: PersuasionStrategy, objection: str
) -> tuple[str, str]:
    point = strat.message_points[0] if strat.message_points else ""
    cta = strat.cta
    if action == "send_opener":
        return (
            f"مرحباً {company}، {('' )}لاحظنا فرصة لتحسين {pain}. {point} {cta}",
            f"Hi {company}, we spotted an opportunity around {pain}. {point} {cta}",
        )
    if action == "handle_objection":
        reframe = persuasion.reframe_objection(objection or "price_objection")
        return (
            f"أتفهّم تماماً. بدل الالتزام الكبير، نقترح بداية أصغر تناسب وضعكم "
            f"الحالي حول {pain}. ({reframe})",
            f"Totally understand. Instead of a big commitment, we can start smaller "
            f"around {pain} to fit where you are now.",
        )
    if action in ("propose_booking",):
        return (
            f"ممتاز! أقترح ٣ مواعيد قصيرة لمكالمة حول {pain}. أي وقت يناسبك؟",
            f"Great — I'll propose 3 short slots for a call about {pain}. Which suits you?",
        )
    if action == "send_details_pack":
        return (
            f"بكل سرور، سأجهّز ملخصاً واضحاً (النطاق، المخرجات، نطاق سعري) حول {pain}.",
            f"Happy to — I'll prepare a clear brief (scope, deliverables, pricing range) "
            f"about {pain}.",
        )
    if action == "escalate_to_founder":
        return (
            "شكراً لاهتمامك بالعقد. سأحوّل الأمر للمؤسس لمراجعة الشروط والتسعير، "
            "فهذه قرارات لا نلتزم بها آلياً.",
            "Thanks for moving toward a contract. I'll route terms and pricing to our "
            "founder — those aren't committed automatically.",
        )
    if action == "schedule_checkin":
        return (
            f"تمام، نحترم التوقيت. هل نعاود التواصل بعد فترة بخصوص {pain}؟",
            f"Understood — we respect the timing. Shall we check back later about {pain}?",
        )
    if action == "honour_optout":
        return (
            "تم إيقاف التواصل فوراً، ولن تصلك رسائل أخرى. شكراً لك.",
            "Done — we've stopped outreach immediately. You won't receive further messages.",
        )
    # follow_up / default
    return (
        f"مرحباً {company}، أتابع معك بخصوص {pain}. {cta}",
        f"Hi {company}, following up about {pain}. {cta}",
    )


# ── Optional LLM brain (safe, lazy, falls back) ─────────────────────────────────


class LLMBrain:
    """Wraps a real model for phrasing/strategy, with a heuristic fallback.

    The LLM is only ever used for *phrasing and angle selection*. All routing,
    safety, claim-guarding and approval still flow through the deterministic
    code paths. Any failure (no key, import error, timeout) silently falls back
    to the heuristic brain, so behaviour is always defined.
    """

    source = "llm"

    def __init__(self, fallback: HeuristicBrain | None = None) -> None:
        self._fallback = fallback or HeuristicBrain()

    def recommend_action(self, context: Mapping[str, Any]) -> ActionRecommendation:
        # Action *selection* stays deterministic (auditable). The LLM influences
        # phrasing in draft_reply, not the safety-relevant routing.
        rec = self._fallback.recommend_action(context)
        rec.source = "llm+heuristic"
        return rec

    def persuasion_for(self, motion: str) -> PersuasionStrategy:
        return self._fallback.persuasion_for(motion)

    def draft_reply(self, context: Mapping[str, Any]) -> dict[str, str]:
        try:
            text = self._llm_draft(context)
            if text and not contains_blocked_claim(text.get("ar")) and not contains_blocked_claim(
                text.get("en")
            ):
                return text
        except Exception:
            pass
        return self._fallback.draft_reply(context)

    def _llm_draft(self, context: Mapping[str, Any]) -> dict[str, str] | None:
        import asyncio

        from core.llm.base import Message  # lazy import; optional dependency
        from core.llm.router import get_router

        router = get_router()
        client = None
        for provider in ("anthropic", "openai", "gemini", "glm"):
            try:
                client = router.get_client(provider)  # type: ignore[arg-type]
            except Exception:
                client = None
            if client:
                break
        if client is None:
            return None

        system = (
            "You are a Saudi B2B commercial assistant. Write a short, honest, "
            "bilingual (Arabic then English) message for the given action. "
            "NEVER promise guaranteed results/ROI, never state a final price or "
            "discount, never invent proof. Keep it warm, concise, opt-out-friendly."
        )
        prompt = (
            f"Action: {context.get('recommended_action')}\n"
            f"Motion: {context.get('motion')}\n"
            f"Company: {context.get('company_name')}\n"
            f"Pain: {context.get('pain_hypothesis')}\n"
            f"Persuasion angle: {context.get('persuasion_angle')}\n"
            "Return two short paragraphs: first Arabic, then English."
        )
        resp = asyncio.run(
            client.chat([Message(role="user", content=prompt)], system=system, max_tokens=400)
        )
        content = (resp.content or "").strip()
        if not content:
            return None
        # Split heuristically into AR / EN halves.
        parts = content.split("\n\n", 1)
        ar = parts[0].strip()
        en = parts[1].strip() if len(parts) > 1 else parts[0].strip()
        return {"ar": ar, "en": en}


def get_brain(env: Mapping[str, str] | None = None) -> CommercialBrain:
    """Return the active brain. Heuristic unless LLM is explicitly enabled."""
    e = env if env is not None else os.environ
    if str(e.get("COMMERCIAL_LLM_ENABLED", "")).strip().lower() == "true":
        return LLMBrain()
    return HeuristicBrain()
