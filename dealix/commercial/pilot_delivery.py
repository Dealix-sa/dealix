"""
Pilot Delivery Kit — 7-day 499 SAR Sprint (S1) Workflow.
طقم تسليم البرنامج التجريبي — برنامج 7 أيام بـ 499 ريال (S1).

Manages the structured 7-day pilot delivery:
  Day 1: Intake call + Pain map
  Day 2: Current state audit + data request
  Day 3-5: Draft messages (2/day, approval-gated)
  Day 6: Proof event documentation
  Day 7: Week-1 report + upsell conversation

Constitutional: All message drafts are approval-gated (NO_LIVE_SEND).
Payment must be confirmed before delivery starts (NO_LIVE_CHARGE).
"""

from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from typing import Any

log = logging.getLogger(__name__)


@dataclass
class PilotContext:
    pilot_id: str
    account_id: str
    company_name: str
    contact_name: str
    sector: str
    pain_points: str
    amount_sar: float = 499.0
    payment_ref: str = ""  # Moyasar invoice ID or bank transfer ref
    payment_confirmed: bool = False
    started_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    current_day: int = 1


@dataclass
class DayTask:
    day: int
    title_ar: str
    title_en: str
    tasks_ar: list[str]
    tasks_en: list[str]
    deliverable_ar: str
    deliverable_en: str
    requires_approval: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "day": self.day,
            "title_ar": self.title_ar,
            "title_en": self.title_en,
            "tasks_ar": self.tasks_ar,
            "tasks_en": self.tasks_en,
            "deliverable_ar": self.deliverable_ar,
            "deliverable_en": self.deliverable_en,
            "requires_approval": self.requires_approval,
        }


@dataclass
class PilotPlan:
    pilot_id: str
    account_id: str
    company_name: str
    days: list[DayTask]
    payment_confirmed: bool
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict[str, Any]:
        return {
            "pilot_id": self.pilot_id,
            "account_id": self.account_id,
            "company_name": self.company_name,
            "days": [d.to_dict() for d in self.days],
            "payment_confirmed": self.payment_confirmed,
            "created_at": self.created_at.isoformat(),
        }

    def to_markdown_ar(self) -> str:
        lines = [
            f"# خطة برنامج التجربة — {self.company_name}",
            f"**رقم البرنامج:** {self.pilot_id}",
            f"**تاريخ البدء:** {self.created_at.strftime('%Y-%m-%d')}",
            f"**السعر:** 499 ريال سعودي",
            "",
            "---",
            "",
        ]
        for day in self.days:
            lines += [
                f"## اليوم {day.day}: {day.title_ar}",
                "",
                "**المهام:**",
            ]
            for task in day.tasks_ar:
                lines.append(f"- {task}")
            lines += [
                "",
                f"**المُخرج:** {day.deliverable_ar}",
                "",
            ]
            if day.requires_approval:
                lines.append("⚠️ **يتطلب موافقة الفاوندر قبل الإرسال**\n")
        return "\n".join(lines)


# ── 7-day canonical plan ──────────────────────────────────────────

def build_pilot_plan(ctx: PilotContext) -> PilotPlan:
    """
    Build the canonical 7-day pilot plan for a specific company.
    Constitutional: payment must be confirmed before this is used operationally.
    """
    days: list[DayTask] = [
        DayTask(
            day=1,
            title_ar="مكالمة الاستقبال وخريطة الألم",
            title_en="Intake Call & Pain Mapping",
            tasks_ar=[
                f"مكالمة مع {ctx.contact_name} (30-45 دقيقة)",
                "رسم خريطة عملية استقبال العملاء المحتملين الحالية",
                "تحديد أبطأ 3 نقاط في العملية",
                "التحقق من القنوات المستخدمة (واتساب / إيميل / لينكد إن)",
                "تسجيل خريطة الألم في ملف التشخيص",
            ],
            tasks_en=[
                f"Call with {ctx.contact_name} (30-45 min)",
                "Map current lead intake process",
                "Identify the 3 slowest points in the process",
                "Verify channels in use (WhatsApp / Email / LinkedIn)",
                "Record pain map in diagnostic file",
            ],
            deliverable_ar="خريطة ألم موثّقة تُظهر الفجوات الرئيسية",
            deliverable_en="Documented pain map showing key gaps",
        ),
        DayTask(
            day=2,
            title_ar="تدقيق الوضع الراهن وطلب البيانات",
            title_en="Current State Audit & Data Request",
            tasks_ar=[
                f"مراجعة أدوات {ctx.company_name} الحالية (CRM / Excel / واتساب)",
                "حساب متوسط وقت الرد الحالي",
                "تحديد حجم العملاء المحتملين شهرياً",
                "طلب آخر 20 عميل محتمل كعينة (مجهولة الهوية)",
                "رسم مخطط العملية الحالية",
            ],
            tasks_en=[
                f"Review {ctx.company_name}'s current tools (CRM / Excel / WhatsApp)",
                "Calculate current average response time",
                "Identify monthly lead volume",
                "Request last 20 leads as sample (anonymized)",
                "Draw current process flowchart",
            ],
            deliverable_ar="تقرير تدقيق موجز مع إحصائيات الوضع الراهن",
            deliverable_en="Brief audit report with current state statistics",
        ),
        DayTask(
            day=3,
            title_ar="إعداد أول دفعة رسائل ذكية (موافقة مطلوبة)",
            title_en="First Smart Message Batch (Approval Required)",
            tasks_ar=[
                "تحليل عينة العملاء المحتملين من اليوم 2",
                "إعداد 2 مسودات رسائل مخصصة (واتساب/إيميل)",
                "عرض المسودات على الفاوندر للمراجعة والموافقة",
                "تعديل الرسائل بناءً على ملاحظات الفاوندر",
            ],
            tasks_en=[
                "Analyze lead sample from Day 2",
                "Prepare 2 personalized message drafts (WhatsApp/email)",
                "Present drafts to founder for review and approval",
                "Revise messages based on founder feedback",
            ],
            deliverable_ar="2 رسائل مخصصة جاهزة للإرسال بعد الموافقة",
            deliverable_en="2 personalized messages ready to send after approval",
            requires_approval=True,
        ),
        DayTask(
            day=4,
            title_ar="إعداد ثاني دفعة رسائل (موافقة مطلوبة)",
            title_en="Second Smart Message Batch (Approval Required)",
            tasks_ar=[
                "متابعة نتائج الرسائل من اليوم 3 (ردود / عدم رد)",
                "إعداد 2 مسودات رسائل متابعة مخصصة",
                "عرض المسودات للموافقة",
                "توثيق أي رد إيجابي كحدث إثبات",
            ],
            tasks_en=[
                "Track Day 3 message results (replies / no reply)",
                "Prepare 2 personalized follow-up drafts",
                "Present drafts for approval",
                "Document any positive reply as proof event",
            ],
            deliverable_ar="2 رسائل متابعة مخصصة + تقرير نتائج اليوم 3",
            deliverable_en="2 follow-up messages + Day 3 results report",
            requires_approval=True,
        ),
        DayTask(
            day=5,
            title_ar="إعداد ثالث دفعة رسائل + بناء القاعدة",
            title_en="Third Message Batch + Foundation Building",
            tasks_ar=[
                "إعداد 2 مسودات رسائل إضافية للشريحة التالية",
                "بناء قاعدة استجابات جاهزة (5 ردود نموذجية)",
                "عرض المسودات للموافقة",
                "إعداد قالب تقرير الأسبوع الأول",
            ],
            tasks_en=[
                "Prepare 2 additional drafts for next segment",
                "Build ready-response library (5 template responses)",
                "Present drafts for approval",
                "Prepare week-1 report template",
            ],
            deliverable_ar="2 رسائل إضافية + مكتبة ردود جاهزة (5 قوالب)",
            deliverable_en="2 additional messages + ready-response library (5 templates)",
            requires_approval=True,
        ),
        DayTask(
            day=6,
            title_ar="توثيق حدث الإثبات",
            title_en="Proof Event Documentation",
            tasks_ar=[
                "جمع كل نتائج الأسبوع (ردود، اجتماعات محجوزة، صفقات)",
                "توثيق أقوى نتيجة كحدث إثبات رسمي",
                "حساب: وقت الرد قبل وبعد / نسبة الردود",
                "إعداد ملخص الإثبات للعميل",
                "طلب شهادة العميل (اختياري، موافقته مطلوبة)",
            ],
            tasks_en=[
                "Collect all week results (replies, meetings booked, deals)",
                "Document strongest result as formal proof event",
                "Calculate: response time before/after / reply rate",
                "Prepare proof summary for client",
                "Request client testimonial (optional, requires consent)",
            ],
            deliverable_ar="حدث إثبات رسمي موثّق مع أرقام قابلة للقياس",
            deliverable_en="Formal documented proof event with measurable numbers",
        ),
        DayTask(
            day=7,
            title_ar="تقرير الأسبوع الأول ومحادثة التطوير",
            title_en="Week-1 Report & Expansion Conversation",
            tasks_ar=[
                "إعداد تقرير الأسبوع الأول الكامل",
                "عرض التقرير على العميل (مكالمة 30 دقيقة)",
                "عرض خيار الاستمرار (Managed Ops 2,999 ريال/شهر)",
                "توثيق قرار العميل في نظام التشغيل",
                "إرسال طقم الإثبات الكامل للعميل",
            ],
            tasks_en=[
                "Prepare complete week-1 report",
                "Present report to client (30-min call)",
                "Offer continuation option (Managed Ops 2,999 SAR/mo)",
                "Document client decision in operating system",
                "Send complete proof pack to client",
            ],
            deliverable_ar="تقرير أسبوع كامل + حدث إثبات + عرض للاستمرار",
            deliverable_en="Complete week report + proof event + continuation offer",
        ),
    ]

    return PilotPlan(
        pilot_id=ctx.pilot_id,
        account_id=ctx.account_id,
        company_name=ctx.company_name,
        days=days,
        payment_confirmed=ctx.payment_confirmed,
    )


def get_day_brief(plan: PilotPlan, day: int) -> dict[str, Any]:
    """Get today's tasks and deliverables for the founder."""
    if day < 1 or day > 7:
        raise ValueError(f"Day must be 1-7, got {day}")
    day_task = plan.days[day - 1]
    deadline = plan.created_at + timedelta(days=day - 1)
    return {
        "pilot_id": plan.pilot_id,
        "company": plan.company_name,
        "day": day,
        "deadline": deadline.strftime("%Y-%m-%d"),
        "title_ar": day_task.title_ar,
        "title_en": day_task.title_en,
        "tasks_ar": day_task.tasks_ar,
        "tasks_en": day_task.tasks_en,
        "deliverable_ar": day_task.deliverable_ar,
        "deliverable_en": day_task.deliverable_en,
        "requires_approval": day_task.requires_approval,
        "constitutional_note": "جميع الرسائل تتطلب موافقة الفاوندر قبل الإرسال" if day_task.requires_approval else None,
    }


def save_pilot(plan: PilotPlan) -> None:
    """Persist pilot plan to local file ledger."""
    try:
        pilots_dir = os.path.join(
            os.path.dirname(__file__), "..", "..", "data", "pilots"
        )
        os.makedirs(pilots_dir, exist_ok=True)
        path = os.path.join(pilots_dir, f"{plan.pilot_id}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(plan.to_dict(), f, ensure_ascii=False, indent=2)
        log.info("Pilot plan saved: %s", path)
    except Exception as exc:
        log.warning("Could not save pilot plan: %s", exc)
