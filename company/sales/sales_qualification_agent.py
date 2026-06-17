#!/usr/bin/env python3
"""AI Sales Qualification Agent — BANT scoring and objection handling."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
RUNTIME_DIR = ROOT / "company" / "runtime"
RUNTIME_DIR.mkdir(parents=True, exist_ok=True)


# BANT Qualification Framework (20 points max)
BANT_INDICATORS = {
    "budget": {
        "label": "Budget Authority",
        "max_points": 5,
        "indicators": {
            "strong": {"text": "Has discretionary budget approved", "points": 5},
            "medium": {"text": "Budget available but needs approval", "points": 3},
            "weak": {"text": "No budget identified", "points": 0},
        }
    },
    "authority": {
        "label": "Decision Authority",
        "max_points": 5,
        "indicators": {
            "strong": {"text": "Founder/CEO/CTO (solo decision maker)", "points": 5},
            "medium": {"text": "Department head (can influence)", "points": 3},
            "weak": {"text": "Individual contributor (no signature power)", "points": 0},
        }
    },
    "need": {
        "label": "Real Problem/Pain",
        "max_points": 5,
        "indicators": {
            "strong": {"text": "Major pain (10M+ SAR annual impact)", "points": 5},
            "medium": {"text": "Moderate pain (1-10M SAR impact)", "points": 3},
            "weak": {"text": "Nice-to-have, not critical", "points": 0},
        }
    },
    "timeline": {
        "label": "Decision Timeline",
        "max_points": 5,
        "indicators": {
            "strong": {"text": "This month", "points": 5},
            "medium": {"text": "Q3 2026", "points": 3},
            "weak": {"text": "Q4+ or indefinite", "points": 0},
        }
    },
}


# Common objections and responses (Khaliji Arabic + English)
OBJECTION_BANK = {
    "price_sensitivity": {
        "objection_ar": "499 ريال كتير شوي",
        "objection_en": "499 SAR is too expensive",
        "response_ar": """أحس فيك. لكن شف: كل عميل تفقده = 10K-50K SAR ضائع
499 ريال = رجل واحد متابع في الـ WhatsApp يوميا
بيفرق بين عميل يرجع وعميل ضايع
جرب 14 يوم، شوف الفرق بنفسك""",
        "response_en": "I understand. But here's the thing: each lost client = 10K-50K SAR wasted. 499 SAR = one person who chases every lead daily. Test 14 days, see the difference yourself.",
    },
    "not_urgent": {
        "objection_ar": "ما عندنا الوقت حاليا",
        "objection_en": "We don't have time right now",
        "response_ar": """مفهوم. لكن هذا بالضبط السبب:
لو عندك فريق 5 أشخاص وكلهم مشغولين، النظام يوفر لهم 5 ساعات يومية
دولك 40 ساعة أسبوع = شخص كامل مجاني
متى نبدأ?""",
        "response_en": "I get it. But that's exactly why: if your team of 5 is stretched, the system frees up 5 hours daily per person. That's 40 hours per week = 1 full person for free. When do we start?",
    },
    "already_using_tool": {
        "objection_ar": "عندنا Salesforce / HubSpot بالفعل",
        "objection_en": "We already use Salesforce / HubSpot",
        "response_ar": """تمام، Salesforce قوي للـ Enterprise. لكن:
- Salesforce ما يرد على العملاء تلقائي
- Salesforce ما يتابع الفرص بـ WhatsApp
- Salesforce ما مصمم لشركات السعودية
ديليكس = WhatsApp OS. نحنا نركز على اللي Salesforce ما بيسويه""",
        "response_en": "Salesforce is great for Enterprise. But: it doesn't auto-respond to clients, doesn't chase opportunities via WhatsApp, and isn't built for Saudi companies. Dealix = WhatsApp OS. We do what Salesforce can't.",
    },
    "needs_boss_approval": {
        "objection_ar": "أنا بأسأل الـ CEO",
        "objection_en": "I need to ask my CEO",
        "response_ar": """كويس. خليني أتكلم معه; ساعته أسهل عشان يشوف الفائدة مباشرة
معنا 30 دقيقة لـ diagnostic بس
متى يكون وقت الـ CEO؟""",
        "response_en": "Perfect. Let me talk to them directly; it's easier when they see the benefit firsthand. We just need 30 minutes for a diagnostic. When's best for the CEO?",
    },
    "wants_more_info": {
        "objection_ar": "خليني أتفكر شوي",
        "objection_en": "Let me think about it",
        "response_ar": """أحس بك. الحقيقة أفضل طريقة للتفكير = التجربة
نرسل لك فيديو 3 دقايق; شوفه وقول لي شنو رأيك
ولو عندك أسئلة، نرد ثاني 24 ساعة
تمام?""",
        "response_en": "Absolutely. The best way to decide = to try. We'll send you a 3-min video; watch it and tell me what you think. Any questions, we reply within 24 hours. Sound good?",
    },
}


def generate_bant_assessment(diagnostic_notes: str) -> dict[str, Any]:
    """Generate BANT score from diagnostic call notes.

    This is a template; in production, this would use Claude to analyze notes.
    For now, return a scoring template.
    """
    return {
        "timestamp": datetime.now().isoformat(),
        "diagnostic_notes_summary": diagnostic_notes[:100] + "..." if len(diagnostic_notes) > 100 else diagnostic_notes,
        "bant_scores": {
            "budget": {
                "score": 3,  # Default: medium
                "indicator": "Budget available but needs approval",
                "evidence": "Company mentioned FY budget cycle in Q2"
            },
            "authority": {
                "score": 5,
                "indicator": "Founder/CEO (solo decision maker)",
                "evidence": "Called the owner directly"
            },
            "need": {
                "score": 5,
                "indicator": "Major pain (10M+ SAR impact)",
                "evidence": "20% lead loss = 500K+ annual impact"
            },
            "timeline": {
                "score": 5,
                "indicator": "This month",
                "evidence": "Ready to start pilot week of June 24"
            },
        },
        "total_bant_score": 18,  # Out of 20
        "qualification_level": "MOVE FAST",  # 16-20 = MOVE FAST; 12-15 = FOLLOW UP; 8-11 = FLAG; 0-7 = END
        "recommendation": "Close pilot this week. High probability.",
    }


def generate_objection_response(objection_type: str, company_name: str = "company") -> dict[str, str]:
    """Generate AI-drafted objection response for founder to review.

    Returns: Draft response ready for founder approval before sending.
    """
    obj = OBJECTION_BANK.get(objection_type, OBJECTION_BANK.get("wants_more_info"))

    return {
        "id": f"objection_{objection_type}_{datetime.now().timestamp()}",
        "type": "objection_response",
        "objection_arabic": obj["objection_ar"],
        "objection_english": obj["objection_en"],
        "draft_response_ar": obj["response_ar"],
        "draft_response_en": obj["response_en"],
        "context": f"Response to {company_name}",
        "timestamp": datetime.now().isoformat(),
        "requires_approval": True,
        "approval_status": "pending",
    }


def generate_followup_reminder(
    prospect_name: str,
    company_name: str,
    last_contact: str,
    days_since: int
) -> dict[str, str]:
    """Generate AI-drafted follow-up reminder for founder approval."""
    followup_type = "day_3" if days_since <= 3 else "day_7" if days_since <= 7 else "day_14"

    followup_messages = {
        "day_3": {
            "ar": f"""السلام عليكم {prospect_name} 👋

يوم 3 من التجربة; كيف الحال?
عندك فيه 2-3 دقايق لتفقد أول عميل ادخلناه في النظام?

أي أسئلة أو مشاكل?
""",
            "en": f"Day 3 check-in: How's it going? Any quick feedback on the system?"
        },
        "day_7": {
            "ar": f"""السلام عليكم {prospect_name} 👋

يوم 7: يمكن شفت فرق في المتابعة?
الفريق استطاع يتابع أكتر عملاء بنفس الوقت?

شنو أحس?
""",
            "en": f"Day 7 check-in: Are you seeing the difference in follow-up? Any early wins?"
        },
        "day_14": {
            "ar": f"""السلام عليكم {prospect_name} 👋

انتهينا من الـ 14 يوم!
شنو رأيك؟ ودك تستمر بـ 3,999 ريال شهري؟

نرسل لك العقد اليوم ولو قولت نعم
""",
            "en": f"14 days complete! Ready to upgrade to monthly? Send contract today."
        }
    }

    msg = followup_messages[followup_type]

    return {
        "id": f"followup_{prospect_name}_{datetime.now().timestamp()}",
        "type": "followup_reminder",
        "prospect_name": prospect_name,
        "company_name": company_name,
        "followup_stage": followup_type,
        "days_since_last_contact": days_since,
        "draft_message_ar": msg["ar"],
        "draft_message_en": msg["en"],
        "channel": "whatsapp",
        "scheduled_for": datetime.now().isoformat(),
        "requires_approval": True,
        "approval_status": "pending",
    }


def save_approval_queue(items: list[dict[str, Any]]) -> Path:
    """Save approval queue as JSON (for frontend /decisions.html to display)."""
    queue_path = RUNTIME_DIR / "approval_queue.json"

    with open(queue_path, 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

    return queue_path


def main() -> int:
    """Generate sample qualification items for founder approval."""
    print("🤖 Sales Qualification Agent")
    print("=" * 50)

    approval_queue = []

    # Sample 1: BANT Assessment
    bant = generate_bant_assessment("Owner has 20% lead loss, ready to start immediately")
    approval_queue.append({
        "type": "bant_assessment",
        "content": bant,
        "requires_approval": False,  # BANT is auto-logged; founder just reviews
    })
    print("✅ Generated BANT assessment")

    # Sample 2: Objection Response
    obj_response = generate_objection_response("price_sensitivity", "محمد - عقارات الحمد")
    approval_queue.append(obj_response)
    print("✅ Generated objection response draft")

    # Sample 3: Follow-up Reminder
    followup = generate_followup_reminder("محمد", "عقارات الحمد", "2026-06-17", 3)
    approval_queue.append(followup)
    print("✅ Generated follow-up reminder")

    # Save approval queue
    queue_path = save_approval_queue(approval_queue)
    print(f"\n💾 Approval queue saved: {queue_path}")
    print(f"Items awaiting approval: {len([i for i in approval_queue if i.get('requires_approval')])}")

    return 0


if __name__ == '__main__':
    exit(main())
