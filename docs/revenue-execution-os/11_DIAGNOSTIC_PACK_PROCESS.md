# Diagnostic Pack Process — عملية حزمة التشخيص

## الغرض (AR)
يصف هذا المستند `scripts/diagnostic_pack_generate.py` والمخرجات التي يُنتجها. الحزمة تحوّل نتائج مكالمة الاكتشاف إلى مجموعة وثائق جاهزة للمراجعة تُسرّع بيع التشخيص وتسليمه. السكربت **يولّد مسودات محلية فقط** للمراجعة، ولا يرسل شيئًا.

## Purpose (EN)
This document describes `scripts/diagnostic_pack_generate.py` and its outputs. The pack turns discovery findings into a review-ready document set that accelerates selling and delivering the diagnostic. The script **only generates local drafts** for review and sends nothing.

## المخرجات / Output Pack

| الملف / File | المحتوى / Content |
|---|---|
| diagnostic_brief.md | ملخص التشخيص: السياق، الأهداف، النطاق / Diagnostic summary: context, goals, scope |
| workflow_map.md | خريطة سير العمل الحالي ونقاط الاحتكاك / Current workflow map and friction points |
| risk_map.md | خريطة المخاطر التشغيلية والأولويات / Operational risk map and priorities |
| pilot_recommendation.md | توصية التجربة المقترحة ومعايير نجاحها / Recommended pilot and success criteria |
| proposal_seed.md | بذرة عرض قابلة للتعديل من المؤسس / An editable proposal seed for the founder |
| handover_checklist.md | قائمة تسليم لضمان اكتمال المخرجات / Handover checklist to ensure completeness |

## سير العملية / Process Flow
1. **الإدخال** / Input: ملاحظات مكالمة الاكتشاف والسياق المجموع.
2. **التوليد** / Generate: تشغيل `scripts/diagnostic_pack_generate.py` لإنتاج الحزمة محليًا.
3. **مراجعة المؤسس** / Founder review: تحرير كل ملف يدويًا والتأكد من الدقة.
4. **العرض** / Present: استخدام `proposal_seed.md` كأساس لعرض يدوي معتمد.
5. **التسليم** / Deliver: عند البيع، استخدام `handover_checklist.md` للتسليم.

## ضوابط الجودة / Quality Controls
- لا أرقام مخترعة أو نتائج عملاء آخرين / No invented numbers or other clients' results.
- لا ضمانات عائد في `proposal_seed.md` / No ROI guarantees in the proposal seed.
- توصية التجربة تربط النجاح بمخرجات قابلة للتحكم / Pilot recommendation ties success to controllable outputs.

## السلامة / Safety
- السكربت يكتب ملفات محلية فقط؛ لا إرسال، لا كشط، لا تعبئة نماذج.
- كل عرض أو تواصل لاحق يدوي ومعتمد من المؤسس.

The script writes local files only; no sending, scraping, or form submission. Any subsequent offer or contact is manual and founder-approved.
