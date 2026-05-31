# Commercial strategy snapshot — 2026-05-28

## Focus
- stage: pilot_execution
- primary_offer_id: revenue_proof_sprint_499
- rationale: بايلوتات جاهزة للقالب — ركّز على Sprint 499 + PILOT_EXECUTION_RUNBOOK

## Offers
- free_mini_diagnostic: 0.0 SAR — اكتمال النموذج خلال 24 ساعة + جواز قرار أولي
- revenue_proof_sprint_499: 499.0 SAR — ≥10 فرص مؤهلة + Proof Pack خلال 7 أيام
- data_to_revenue_pack_1500: 1500.0 SAR — ≥20 فرصة معتمدة + تقرير مخاطر بيانات
- growth_ops_monthly_2999: 2999.0 SAR — موجز أسبوعي + تحسين معدل رد على المسودات
- support_os_addon_1500: 1500.0 SAR — SLA أول رد + تصنيف تذاكر
- executive_command_center_7500: 7500.0 SAR — موجز يومي + board pack شهري
- agency_partner_os: 0.0 SAR — إحالة مدفوعة واحدة على الأقل / ربع

## Weekly motions
- sun: راجع لقطة Business NOW + KPIs التجارية المعلّقة
- mon: حدّث قائمة دافئة (~30) — مسودات فقط
- tue: POST /api/v1/leads لاختبار مسار intake
- wed: anti-waste قبل أي رسالة خارجية
- thu: راجع موافقات اليوم — لا إرسال بدون جواز
- fri: Proof / تقرير أسبوعي للعميل النشط
- sat: شغّل run_business_now.sh + حدّث cache

## Guardrails
- لا واتساب بارد ولا LinkedIn تلقائي
- لا إرسال خارجي بدون موافقة صريحة
- شغّل anti-waste قبل أي حملة أو رسالة خارجية
- لا upsell بدون Proof Pack أو دليل L3+
- لا أرقام CRM في الأتمتة — عبّئ kpi_founder_commercial_import.yaml يدوياً
