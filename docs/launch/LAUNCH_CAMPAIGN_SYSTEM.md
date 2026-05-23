# Launch Campaign System — Dealix

## الدور — Role

نظام بناء وتنفيذ الحملات السوقية كحلقة قابلة للقياس — وليس "نشاطات".

A campaign factory: every market motion is structured, time-boxed, owned, measured, and either scaled, fixed, or killed.

## بنية الحملة — Campaign structure

كل حملة تُعرَّف بـ:

```yaml
id: campaign_<slug>
sector: erp_crm | cybersecurity | logistics | ...
hypothesis: "نعتقد أن CFO شركات ERP يدفعون 1500 ريال مقابل Data Pack"
offer: data_pack_diagnostic
proof_required: [sample_diagnostic, payment_capture_ready]
trust_class: low | medium | high
distribution_channels: [warm_intro, founder_inbox, linkedin_dm_approved]
duration_days: 14
success_criteria:
  cash_collected_sar: 1500
  meetings_booked: 3
  approved_proposals: 2
kill_criteria:
  weeks_without_response: 2
  rejected_proposals: 3
owner: founder
status: draft | approved | active | paused | killed | scaled
```

## دورة الحملة — Campaign loop

1. **Hypothesize** — كتابة الفرضية من learning memory.
2. **Approve** — Trust gate + Founder approval (لا حملة بدون اعتماد).
3. **Equip** — إنتاج الأصول من Sample Factory + Proposal Factory.
4. **Distribute** — صياغة الرسائل في `distribution/queues.json` بانتظار إرسال يدوي.
5. **Capture** — كل رد يدخل `conversation_log` + يُربط بالحملة.
6. **Measure** — Scorecard أسبوعي.
7. **Decide** — Kill / Fix / Scale.

## الحدود الصارمة — Hard rules

- لا حملة active بدون `Trust class` معتمدة.
- لا إرسال آلي — كل رسالة منتظرة موافقة يدوية.
- لا حملة بدون `kill_criteria` معرّفة مسبقًا.
- لا تشغيل حملتين متوازيتين على نفس الـ ICP بدون فرق هدف واضح.
- لا استخدام بيانات scraped — kein cold WhatsApp / LinkedIn automation.

## المصدر الواحد للحقيقة — Source of truth

- ملف الحملة: `<private_ops>/launch/campaigns/<campaign_id>.yaml`
- الحملة الفعالة: `<private_ops>/launch/active_campaign.yaml` (symlink أو نسخة لحالة `active` فقط).

## الملكية — Ownership

- Owner: Founder.
- Approver: Trust gate + Founder.
- Reviewer: Sales lead.
