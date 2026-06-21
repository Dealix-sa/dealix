from __future__ import annotations


def _clean(value: str | None, fallback: str = "") -> str:
    value = (value or "").strip()
    return value or fallback


def render_email(row: dict[str, str]) -> str:
    company = _clean(row.get("company"), "الشركة")
    sector = _clean(row.get("sector"), "قطاعكم")
    city = _clean(row.get("city"), "السعودية")
    pain = _clean(row.get("pain"), "تشتت المتابعة اليومية")
    offer = _clean(row.get("offer"), "Revenue Command Room Sprint")

    subject = f"{company} — فكرة عملية لتحويل {pain} إلى نظام تشغيل يومي"

    return f"""To: {row.get("email", "")}
Subject: {subject}

السلام عليكم،

أنا سامي من Dealix.

لاحظنا أن شركات {sector} في {city} غالبًا تواجه تحدي: {pain}.

اقتراحنا ليس أداة إضافية. نبني لكم {offer}:
- غرفة قيادة يومية للفرص والمتابعات
- ترتيب واضح للأولويات
- متابعة مؤسسية عبر Email/WhatsApp بعد الموافقة
- لوحة SLA للإدارة
- تقرير يومي مختصر: ماذا حدث؟ ماذا نرسل؟ ماذا نغلق؟

نبدأ بـ Pilot صغير 7–14 يوم على ألم واحد فقط، بدون تغيير أنظمتكم الحالية.

إذا مناسب، أرسل لكم صفحة واحدة مخصصة لـ {company} توضح:
1. أين تضيع الفرص
2. كيف نغلق فجوة المتابعة
3. شكل النظام المقترح قبل التنفيذ

هل يناسبكم موعد قصير هذا الأسبوع؟

تحياتي،
سامي — Dealix

لإيقاف التواصل، أرسل "إيقاف" وسنزيلك من القائمة فورًا.
"""


def render_whatsapp_text(row: dict[str, str]) -> str:
    company = _clean(row.get("company"), "الشركة")
    pain = _clean(row.get("pain"), "تشتت المتابعة")
    offer = _clean(row.get("offer"), "Revenue Command Room Sprint")

    return f"""السلام عليكم، أنا سامي من Dealix.

عندي فكرة مختصرة لـ {company} بخصوص: {pain}.

نبني لكم {offer}: غرفة قيادة يومية للفرص والمتابعات والتقارير، بدون تغيير أنظمتكم الحالية.

اختر أحد الخيارات:
1) أرسل التصور
2) احجز مكالمة 20 دقيقة
3) ليس الآن
4) إيقاف
"""


def render_whatsapp_buttons_payload(row: dict[str, str]) -> dict:
    company = _clean(row.get("company"), "الشركة")
    pain = _clean(row.get("pain"), "تشتت المتابعة")

    return {
        "type": "interactive",
        "interactive": {
            "type": "button",
            "header": {"type": "text", "text": "Dealix Revenue Command Room"},
            "body": {
                "text": (
                    f"السلام عليكم، فكرة مختصرة لـ {company} بخصوص {pain}. "
                    "نبني غرفة قيادة للفرص والمتابعات والتقارير اليومية."
                )
            },
            "footer": {"text": "Dealix — approval-first outreach"},
            "action": {
                "buttons": [
                    {"type": "reply", "reply": {"id": "send_brief", "title": "أرسل التصور"}},
                    {"type": "reply", "reply": {"id": "book_call", "title": "احجز مكالمة"}},
                    {"type": "reply", "reply": {"id": "stop", "title": "إيقاف"}},
                ]
            },
        },
    }


def render_company_brief(row: dict[str, str]) -> str:
    company = _clean(row.get("company"), "الشركة")
    sector = _clean(row.get("sector"), "القطاع")
    pain = _clean(row.get("pain"), "تشتت المتابعة")
    offer = _clean(row.get("offer"), "Revenue Command Room Sprint")

    return f"""# Dealix One-Page Brief — {company}

## الشركة

- الاسم: {company}
- القطاع: {sector}
- الموقع: {row.get("website", "")}
- المدينة: {row.get("city", "")}

## الألم التشغيلي المفترض

{pain}

## العرض المقترح

{offer}

## ماذا نبني في أول 7–14 يوم؟

1. Command Room للفرص والمتابعات.
2. قائمة أولويات يومية.
3. Drafts للرسائل والمتابعات.
4. SLA Dashboard مبسط.
5. تقرير يومي للإدارة.
6. Proof Pack قبل/بعد.

## الضمان التشغيلي

- لا إرسال خارجي بدون موافقة.
- لا WhatsApp بدون opt-in.
- لا وعود ROI مزيفة.
- كل رسالة لها سجل ومصدر وسبب.

## الخطوة التالية

مكالمة تشخيص 20 دقيقة لتحديد الألم الأول الذي يستحق Pilot.
"""
