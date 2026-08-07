#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "company" / "daily"
OUT.mkdir(parents=True, exist_ok=True)

offers = {
    0: ("WhatsApp Revenue OS", "الفرص تضيع في واتساب والمتابعة", "عيادات، عقار، مراكز تدريب"),
    1: ("Review Intelligence OS", "التقييمات والشكاوى لا تتحول إلى قرارات", "مطاعم، عيادات، خدمات محلية"),
    2: ("AI Business Command Center", "الإدارة لا ترى الحقيقة اليومية", "شركات متعددة الفروع، وكالات، B2B"),
    3: ("Brand Intelligence OS", "الهوية والرسائل والعروض غير موحدة", "وكالات، عيادات، مطاعم، خدمات"),
    4: ("Transformation Diagnostic Sprint", "ابدأ بتشخيص مدفوع قبل بناء كامل", "كل القطاعات"),
    5: ("Growth Engine OS", "لا يوجد outbound/follow-up/proposal cadence", "تدريب، B2B، وكالات"),
    6: ("Customer Experience OS", "رحلة العميل متفرقة من أول تواصل إلى retention", "عيادات، مطاعم، B2C"),
}

today = dt.date.today()
name, pain, targets = offers[today.weekday()]
path = OUT / f"{today.isoformat()}_daily_offer.md"

path.write_text(f"""# Dealix Daily Offer

Date: {today.isoformat()}

## Offer
{name}

## Pain Angle
{pain}

## Target Segments
{targets}

## WhatsApp Draft
السلام عليكم، أنا سامي من Dealix.

اليوم أركز على فكرة مهمة: {pain}.

نحن نبني للشركات نظام {name} بحيث يتحول التشغيل اليومي إلى workflow واضح، متابعة، تقارير، وقرارات.

إذا مناسب، أرسل لك مثال مختصر كيف ممكن يطبق على شركتكم؟

## Founder Action
- Send 20 reviewed messages.
- Book 2 discovery calls.
- Push paid diagnostic if prospect is qualified.
""", encoding="utf-8")

print(path)
