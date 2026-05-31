"""
quality_gate.py — Dealix Growth OS
Scores outreach drafts on 8 criteria (total 100 points).

Scoring:
  company_personalization: 20
  clear_pain:              20
  single_offer:            15
  simple_cta:              10
  channel_language:        10
  no_exaggeration:         10
  compliance_optout:       10
  brevity_clarity:          5
  TOTAL:                   100

Decisions:
  90-100 → ready (auto_send eligible)
  82-89  → founder_review
  70-81  → rewrite
  <70    → reject
"""

import re
from pathlib import Path
from typing import Optional

try:
    import yaml
    _HAS_YAML = True
except ImportError:
    _HAS_YAML = False

_BASE = Path(__file__).parent
_SCORING_CONFIG = _BASE / "config" / "scoring.yml"

_FORBIDDEN_PHRASES = [
    "guaranteed roi", "guaranteed results", "guarantee", "100% automated",
    "ai replaces", "no human needed", "proven to double", "we guarantee",
    "risk-free investment", "unlimited leads", "100% accurate",
    "ضمان", "مضمون", "أتمتة كاملة",
]

_OPT_OUT_PATTERNS = [
    r"unsubscribe", r"opt.?out", r"remove me", r"إلغاء الاشتراك",
    r"إيقاف", r"لإلغاء", r"to stop",
]

_CTA_PATTERNS = [
    r"\d{1,2}.?min", r"call", r"schedule", r"reply", r"book",
    r"مكالمة", r"حجز", r"رد", r"تواصل",
]

_PAIN_INDICATORS = [
    r"losing", r"costs", r"slow", r"manual", r"chaos", r"inefficien",
    r"leak", r"gap", r"problem", r"challenge", r"تخسر", r"يدوي",
    r"بطيء", r"فجوة", r"تحدي",
]

_WORD_LIMITS = {
    "email": 150,
    "whatsapp": 80,
    "linkedin": 200,
    "instagram": 100,
    "messenger": 100,
    "x": 60,
    "telegram": 150,
    "website_forms": 200,
    "calls": 50,
}


class DraftQualityGate:
    """
    Scores and makes a decision on an outreach draft.

    Expected draft dict fields:
        text (str): the draft body text
        subject (str, optional): email subject line
        channel (str): email | whatsapp | linkedin | etc.
        language (str): en | ar
        company_name (str, optional): for personalization check
        sector (str, optional): for pain relevance check
    """

    def __init__(self, config: Optional[dict] = None):
        if config:
            self.weights = config
        elif _HAS_YAML and _SCORING_CONFIG.exists():
            with open(_SCORING_CONFIG, "r", encoding="utf-8") as f:
                raw = yaml.safe_load(f) or {}
            self.weights = raw.get("scoring", {}).get("draft_quality_weights", {})
        else:
            self.weights = {
                "company_personalization": 20,
                "clear_pain": 20,
                "single_offer": 15,
                "simple_cta": 10,
                "channel_language": 10,
                "no_exaggeration": 10,
                "compliance_optout": 10,
                "brevity_clarity": 5,
            }

    def score_draft(self, draft: dict) -> dict:
        """
        Score a draft against 8 quality criteria.

        Returns:
            {
                total_score: int,
                breakdown: {criterion: {score, max, reason}},
                decision: str,
                governance_decision: str,
            }
        """
        text = draft.get("text", "")
        subject = draft.get("subject", "")
        channel = draft.get("channel", "email").lower()
        language = draft.get("language", "en").lower()
        company_name = draft.get("company_name", "")
        full_text = f"{subject} {text}".lower().strip()

        breakdown = {}
        total = 0

        # 1. Company personalization (20 pts)
        w = self.weights.get("company_personalization", 20)
        score_1 = 0
        reason_1 = "No company-specific reference found"
        if company_name and company_name.lower() in full_text:
            score_1 = w
            reason_1 = f"Company name '{company_name}' found in draft"
        elif any(re.search(p, full_text, re.IGNORECASE) for p in [
            r"\byour\b", r"\byou\b", r"شركتكم", r"مؤسستكم", r"لديكم",
        ]):
            score_1 = int(w * 0.7)
            reason_1 = "Generic 'your company' reference — good but not specific"
        breakdown["company_personalization"] = {
            "score": score_1, "max": w, "reason": reason_1
        }
        total += score_1

        # 2. Clear pain (20 pts)
        w = self.weights.get("clear_pain", 20)
        pain_hits = sum(
            1 for p in _PAIN_INDICATORS
            if re.search(p, full_text, re.IGNORECASE)
        )
        if pain_hits >= 2:
            score_2 = w
            reason_2 = f"Clear pain articulated ({pain_hits} pain indicators)"
        elif pain_hits == 1:
            score_2 = int(w * 0.6)
            reason_2 = "One pain indicator — strengthen specificity"
        else:
            score_2 = 0
            reason_2 = "No pain indicators found — draft too feature-focused"
        breakdown["clear_pain"] = {"score": score_2, "max": w, "reason": reason_2}
        total += score_2

        # 3. Single offer (15 pts)
        w = self.weights.get("single_offer", 15)
        offer_keywords = [
            "sprint", "diagnostic", "pack", "managed", "custom",
            "سبرينت", "تشخيص", "حزمة", "إدارة",
        ]
        offer_count = sum(
            1 for kw in offer_keywords
            if re.search(rf"\b{kw}\b", full_text, re.IGNORECASE)
        )
        if offer_count <= 1:
            score_3 = w
            reason_3 = "Single clear offer"
        elif offer_count == 2:
            score_3 = int(w * 0.5)
            reason_3 = "Two offers mentioned — consider focusing on one"
        else:
            score_3 = 0
            reason_3 = f"Multiple offers ({offer_count}) — confusing CTA"
        breakdown["single_offer"] = {"score": score_3, "max": w, "reason": reason_3}
        total += score_3

        # 4. Simple CTA (10 pts)
        w = self.weights.get("simple_cta", 10)
        cta_hits = sum(
            1 for p in _CTA_PATTERNS
            if re.search(p, full_text, re.IGNORECASE)
        )
        if cta_hits >= 1:
            score_4 = w
            reason_4 = "Clear CTA found"
        else:
            score_4 = 0
            reason_4 = "No clear CTA — add a specific next step"
        breakdown["simple_cta"] = {"score": score_4, "max": w, "reason": reason_4}
        total += score_4

        # 5. Channel language match (10 pts)
        w = self.weights.get("channel_language", 10)
        score_5 = w
        reason_5 = "Language matches channel norms"
        ar_chars = len(re.findall(r'[؀-ۿ]', text))
        en_chars = len(re.findall(r'[a-zA-Z]', text))
        detected_lang = "ar" if ar_chars > en_chars else "en"
        if detected_lang != language:
            score_5 = int(w * 0.5)
            reason_5 = f"Detected language ({detected_lang}) does not match declared ({language})"
        if channel == "linkedin" and language == "ar":
            score_5 = int(w * 0.8)
            reason_5 = "LinkedIn Arabic — acceptable but English preferred for some segments"
        breakdown["channel_language"] = {
            "score": score_5, "max": w, "reason": reason_5
        }
        total += score_5

        # 6. No exaggeration (10 pts)
        w = self.weights.get("no_exaggeration", 10)
        forbidden_hits = [
            phrase for phrase in _FORBIDDEN_PHRASES
            if phrase in full_text
        ]
        if not forbidden_hits:
            score_6 = w
            reason_6 = "No forbidden/exaggerated claims found"
        else:
            score_6 = 0
            reason_6 = f"Forbidden phrases found: {forbidden_hits[:3]}"
        breakdown["no_exaggeration"] = {
            "score": score_6, "max": w, "reason": reason_6
        }
        total += score_6

        # 7. Compliance opt-out (10 pts)
        w = self.weights.get("compliance_optout", 10)
        optout_found = any(
            re.search(p, full_text, re.IGNORECASE)
            for p in _OPT_OUT_PATTERNS
        )
        if optout_found:
            score_7 = w
            reason_7 = "Opt-out mechanism present"
        elif channel in ("instagram", "messenger", "telegram"):
            score_7 = w
            reason_7 = "Inbound channel — opt-out in platform settings is sufficient"
        else:
            score_7 = 0
            reason_7 = "No opt-out found — required for email, WhatsApp"
        breakdown["compliance_optout"] = {
            "score": score_7, "max": w, "reason": reason_7
        }
        total += score_7

        # 8. Brevity / clarity (5 pts)
        w = self.weights.get("brevity_clarity", 5)
        word_count = len(text.split())
        limit = _WORD_LIMITS.get(channel, 150)
        if word_count <= limit:
            score_8 = w
            reason_8 = f"Within word limit ({word_count}/{limit} words)"
        elif word_count <= limit * 1.3:
            score_8 = int(w * 0.5)
            reason_8 = f"Slightly over limit ({word_count}/{limit} words)"
        else:
            score_8 = 0
            reason_8 = f"Over word limit ({word_count}/{limit} words) — trim significantly"
        breakdown["brevity_clarity"] = {
            "score": score_8, "max": w, "reason": reason_8
        }
        total += score_8

        decision = self.make_decision(total)

        return {
            "total_score": total,
            "breakdown": breakdown,
            "decision": decision,
            "governance_decision": f"draft_quality_{decision}_{total}_pts",
        }

    def make_decision(self, score: int) -> str:
        """
        Map score to decision:
          90-100 → ready
          82-89  → founder_review
          70-81  → rewrite
          <70    → reject
        """
        if score >= 90:
            return "ready"
        elif score >= 82:
            return "founder_review"
        elif score >= 70:
            return "rewrite"
        else:
            return "reject"
