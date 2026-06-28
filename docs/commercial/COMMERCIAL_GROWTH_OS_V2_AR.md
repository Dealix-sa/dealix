# Dealix Commercial Growth OS v2

## التعريف

Commercial Growth OS v2 هو نظام تشغيل تجاري ذكي للشركات يربط:

```text
Lead sourcing
→ Source validation
→ ICP scoring
→ Growth cards
→ Reply classification
→ Negotiation drafts
→ Booking options
→ Proposal briefs
→ Follow-up tasks
→ Command Room report
```

## القيمة الحقيقية للعميل

بدل أن تضيع المبيعات بين واتساب والإيميل ولينكدإن وملفات Excel، يعطي Dealix الإدارة وفريق المبيعات قائمة يومية واضحة:

- من نكلم؟
- لماذا؟
- ماذا نرسل؟
- أي قناة مناسبة؟
- ماذا نفعل إذا رد؟
- متى نحجز؟
- ماذا نعرض؟
- ما المتابعة التالية؟

## القنوات

- Email: مسودات ورسائل controlled-live لاحقًا بعد الموافقة.
- WhatsApp: فقط بعد opt-in، ولا يوجد cold WhatsApp.
- LinkedIn: manual-assisted فقط، بدون automated DM.
- Phone: task/manual call فقط.
- Website form / partner referral: مسارات بديلة منخفضة المخاطر.

## الأتمتة

الافتراضي A0_DRAFT_ONLY:

- يولد كروت.
- يصنف ردود.
- يقترح تفاوض.
- يولد booking options.
- يولد proposal briefs.
- يولد follow-up tasks.
- يكتب report.

الإرسال والحجز live مقفل حتى تتحقق الموافقات، opt-in، opt-out، rate limits، وclaim guard.

## التشغيل

```bash
python scripts/commercial/run_commercial_growth_os.py
python scripts/commercial/verify_commercial_growth_os.py
python -m pytest -q tests/test_commercial_growth_os_v2.py
```

## مؤشرات النجاح

- كل حساب له source_url أو يتم حظره من الإرسال.
- كل كرت له owner_decision و next_action.
- كل WhatsApp outbound يتطلب opt-in.
- كل proposal يتطلب approval.
- كل booking option لا يكتب في التقويم افتراضيًا.
- كل follow-up task يبقى draft.
- كل التقرير يظهر في `reports/commercial/growth_os/latest.json`.
