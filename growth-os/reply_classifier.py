"""
reply_classifier.py — Dealix Growth OS
Classifies inbound replies and determines next action.

Classification categories:
  interested, details_requested, wrong_person, pricing_requested,
  security_concern, not_now, not_interested, unsubscribe, bounce

Non-negotiable: unsubscribe replies trigger immediate suppression.
"""

import re


CLASSIFICATIONS = [
    "interested",
    "details_requested",
    "wrong_person",
    "pricing_requested",
    "security_concern",
    "not_now",
    "not_interested",
    "unsubscribe",
    "bounce",
]

# Keyword patterns per classification — order matters (first match wins for ties)
_PATTERNS = {
    "bounce": {
        "en": [
            r"delivery failed", r"undeliverable", r"mail delivery failure",
            r"does not exist", r"no such user", r"mailbox full",
            r"address rejected", r"550", r"551", r"552", r"553", r"554",
        ],
        "ar": [],
    },
    "unsubscribe": {
        "en": [
            r"\bunsubscribe\b", r"\bremove me\b", r"\bstop\b", r"\bopt.?out\b",
            r"not interested", r"please remove", r"take me off",
            r"don.t contact", r"do not contact", r"no thanks",
        ],
        "ar": [
            r"إلغاء الاشتراك", r"إيقاف", r"توقف", r"أوقف", r"لا أريد",
            r"إزالة", r"حذف", r"لا شكراً", r"لا تتصل",
        ],
    },
    "security_concern": {
        "en": [
            r"\bsecurity\b", r"\bgdpr\b", r"\bpdpl\b", r"\bprivacy\b",
            r"\bdata protection\b", r"\bcompliance\b", r"\baudit\b",
            r"\biso\b", r"\bcertif", r"\bsoc 2\b",
        ],
        "ar": [
            r"أمان", r"أمن البيانات", r"حماية البيانات", r"الخصوصية",
            r"امتثال", r"تدقيق",
        ],
    },
    "pricing_requested": {
        "en": [
            r"\bprice\b", r"\bpricing\b", r"\bcost\b", r"\bhow much\b",
            r"\brate\b", r"\bfee\b", r"\bquote\b", r"\bbudget\b",
        ],
        "ar": [
            r"السعر", r"التكلفة", r"كم يكلف", r"سعر", r"تسعير",
            r"الميزانية", r"عرض سعر",
        ],
    },
    "wrong_person": {
        "en": [
            r"wrong person", r"not the right", r"not in charge",
            r"please contact", r"you should reach", r"forward to",
            r"not my area", r"not my department",
        ],
        "ar": [
            r"ليس الشخص المناسب", r"تواصل مع", r"أحل إلى",
            r"ليس من اختصاصي", r"ليس قسمي",
        ],
    },
    "not_now": {
        "en": [
            r"not right now", r"maybe later", r"not at the moment",
            r"busy right now", r"not this quarter", r"next year",
            r"check back", r"reach out later", r"not a priority",
        ],
        "ar": [
            r"ليس الآن", r"ربما لاحقاً", r"بعد فترة", r"مشغول",
            r"غير أولوية", r"تواصل لاحقاً",
        ],
    },
    "details_requested": {
        "en": [
            r"tell me more", r"more details", r"how does it work",
            r"can you explain", r"what does", r"what is", r"share",
            r"send me", r"overview", r"brochure", r"information",
        ],
        "ar": [
            r"أخبرني أكثر", r"مزيد من التفاصيل", r"كيف يعمل",
            r"اشرح لي", r"ما هو", r"أرسل لي", r"معلومات",
        ],
    },
    "interested": {
        "en": [
            r"\byes\b", r"\binterested\b", r"\blet.s talk\b", r"\bschedule\b",
            r"\bcall\b", r"\bmeeting\b", r"\bbook\b", r"\bwhen can\b",
            r"sounds good", r"great idea", r"love to", r"would like to",
        ],
        "ar": [
            r"نعم", r"مهتم", r"تحدث", r"نتحدث", r"موعد",
            r"فكرة جيدة", r"يبدو جيداً", r"نعم أريد",
        ],
    },
    "not_interested": {
        "en": [
            r"not interested", r"no thank", r"don.t need",
            r"already have", r"not looking", r"not a fit",
        ],
        "ar": [
            r"غير مهتم", r"لا شكراً", r"لا نحتاج", r"لدينا بالفعل",
        ],
    },
}


class ReplyClassifier:
    """
    Classifies inbound reply text into one of the standard categories
    and returns the recommended next action.
    """

    def classify(self, text: str, language: str = "en") -> dict:
        """
        Classify a reply message.

        Args:
            text: raw reply text
            language: "en" or "ar" — guides which pattern set to prioritize

        Returns:
            {classification, confidence, matched_keywords, language, governance_decision}
        """
        if not text or not text.strip():
            return {
                "classification": "bounce",
                "confidence": 0.5,
                "matched_keywords": [],
                "language": language,
                "governance_decision": "empty_reply_classified_as_bounce",
            }

        text_lower = text.lower().strip()
        scores: dict[str, int] = {c: 0 for c in CLASSIFICATIONS}
        matched_keywords: list[str] = []

        for classification, lang_patterns in _PATTERNS.items():
            patterns = lang_patterns.get(language, []) + lang_patterns.get("en", [])
            for pattern in patterns:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    scores[classification] += 1
                    matched_keywords.append(pattern)

        # Find the classification with highest score
        best = max(scores, key=lambda k: scores[k])
        best_score = scores[best]

        if best_score == 0:
            # No pattern matched — classify as details_requested (safest default)
            best = "details_requested"
            confidence = 0.3
        elif best_score == 1:
            confidence = 0.6
        elif best_score <= 3:
            confidence = 0.8
        else:
            confidence = 0.95

        return {
            "classification": best,
            "confidence": round(confidence, 2),
            "matched_keywords": list(set(matched_keywords))[:5],
            "language": language,
            "governance_decision": f"reply_classified_{best}",
        }

    def get_next_action(self, classification: dict) -> dict:
        """
        Given a classification result, return the recommended next action.

        Returns:
            {action, draft_reply, crm_update, urgency, governance_decision}
        """
        c = classification.get("classification", "details_requested")

        action_map = {
            "interested": {
                "action": "book_discovery_call",
                "draft_reply": (
                    "Thank you for your interest! I would love to schedule a brief 15-minute call "
                    "to understand your situation better. What time works for you this week? / "
                    "شكراً لاهتمامك! أودّ جدولة مكالمة سريعة لمدة 15 دقيقة. متى يناسبك هذا الأسبوع؟"
                ),
                "crm_update": {
                    "stage": "discovery_call_requested",
                    "lead_tier": "A",
                    "next_touch": "within_24h",
                },
                "urgency": "high",
            },
            "details_requested": {
                "action": "send_diagnostic_overview",
                "draft_reply": (
                    "Great to hear from you. I will send over a 2-page overview of how the diagnostic works "
                    "along with a sample output so you can see exactly what you would receive. / "
                    "سعيد بردك. سأرسل لك ملخصاً من صفحتين يشرح كيف يعمل التشخيص مع نموذج لمخرجاته."
                ),
                "crm_update": {
                    "stage": "nurturing",
                    "lead_tier": "B",
                    "next_touch": "within_48h",
                },
                "urgency": "medium",
            },
            "pricing_requested": {
                "action": "send_pricing_and_book_call",
                "draft_reply": (
                    "Happy to share the pricing details. Our entry point is a free 48-hour diagnostic "
                    "with no commitment. The paid sprint starts at 499 SAR. "
                    "Would a 15-minute call be easier to walk through the options? / "
                    "يسعدني مشاركة تفاصيل الأسعار. البداية تشخيص مجاني 48 ساعة بدون التزام. "
                    "السبرينت المدفوع يبدأ من 499 ريال. هل مكالمة 15 دقيقة أسهل لاستعراض الخيارات؟"
                ),
                "crm_update": {
                    "stage": "pricing_shared",
                    "lead_tier": "B",
                    "next_touch": "within_24h",
                },
                "urgency": "high",
            },
            "security_concern": {
                "action": "escalate_to_founder",
                "draft_reply": (
                    "Absolutely — security and compliance are core to what we do. "
                    "Our founder would like to speak with you directly to address your requirements. "
                    "Can we schedule a call? / "
                    "بالتأكيد — الأمن والامتثال في صميم عملنا. "
                    "مؤسسنا يودّ التحدث معك مباشرة لمعالجة متطلباتك. هل يمكننا جدولة مكالمة؟"
                ),
                "crm_update": {
                    "stage": "founder_escalation_required",
                    "lead_tier": "A",
                    "next_touch": "founder_within_24h",
                },
                "urgency": "high",
            },
            "wrong_person": {
                "action": "ask_for_referral",
                "draft_reply": (
                    "Thank you for letting me know. Could you point me to the right person at your organization? / "
                    "شكراً لإعلامي. هل يمكنك توجيهي إلى الشخص المناسب في مؤسستكم؟"
                ),
                "crm_update": {
                    "stage": "referral_requested",
                    "lead_tier": "C",
                    "next_touch": "within_72h",
                },
                "urgency": "low",
            },
            "not_now": {
                "action": "mark_future_follow_up",
                "draft_reply": (
                    "Completely understood. I will check back in 60 days — "
                    "no pressure in the meantime. / "
                    "مفهوم تماماً. سأتواصل معك خلال 60 يوماً — لا ضغط في هذه الأثناء."
                ),
                "crm_update": {
                    "stage": "future_follow_up",
                    "lead_tier": "C",
                    "next_touch": "60_days",
                },
                "urgency": "low",
            },
            "not_interested": {
                "action": "close_respectfully",
                "draft_reply": (
                    "Understood — I appreciate you letting me know. "
                    "I will not follow up further. Wishing you the best. / "
                    "مفهوم — أقدر لك وضوحك. لن أتواصل مجدداً. مع تمنياتي بالتوفيق."
                ),
                "crm_update": {
                    "stage": "closed_not_interested",
                    "lead_tier": "D",
                    "next_touch": "never",
                },
                "urgency": "low",
            },
            "unsubscribe": {
                "action": "add_to_suppression_immediately",
                "draft_reply": (
                    "You have been removed from our list — no further messages will be sent. / "
                    "تمت إزالتك من قائمتنا — لن يتم إرسال أي رسائل أخرى."
                ),
                "crm_update": {
                    "stage": "unsubscribed",
                    "lead_tier": "D",
                    "next_touch": "never",
                    "suppression_required": True,
                },
                "urgency": "critical",
            },
            "bounce": {
                "action": "mark_invalid_email",
                "draft_reply": None,
                "crm_update": {
                    "stage": "bounced",
                    "lead_tier": "D",
                    "next_touch": "never",
                    "suppression_required": True,
                },
                "urgency": "medium",
            },
        }

        result = action_map.get(
            c,
            {
                "action": "escalate_to_founder",
                "draft_reply": None,
                "crm_update": {"stage": "unknown", "lead_tier": "C"},
                "urgency": "medium",
            },
        )
        result["governance_decision"] = f"next_action_{result['action']}_for_{c}"
        return result
