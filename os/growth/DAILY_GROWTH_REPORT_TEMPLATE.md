# Dealix Daily Growth Report
# تقرير النمو اليومي — Dealix

**Date / التاريخ:** {{today_date}}
**Generated at:** {{generated_at}}
**No live sends | لا إرسال حي:** All drafts require founder approval before sending.

---

## Top 25 Opportunities / أفضل 25 فرصة

| Rank | Company | Sector | Score | Best Offer | Best Channel | Action |
|------|---------|--------|-------|------------|--------------|--------|
| 1 | {{company_1}} | {{sector_1}} | {{score_1}} | {{offer_1}} | {{channel_1}} | {{action_1}} |
| 2 | {{company_2}} | {{sector_2}} | {{score_2}} | {{offer_2}} | {{channel_2}} | {{action_2}} |
| 3 | {{company_3}} | {{sector_3}} | {{score_3}} | {{offer_3}} | {{channel_3}} | {{action_3}} |
| 4 | {{company_4}} | {{sector_4}} | {{score_4}} | {{offer_4}} | {{channel_4}} | {{action_4}} |
| 5 | {{company_5}} | {{sector_5}} | {{score_5}} | {{offer_5}} | {{channel_5}} | {{action_5}} |
| 6-25 | ... | ... | ... | ... | ... | ... |

---

## Top 10 Drafts Ready for Review / أفضل 10 مسودات جاهزة

| Draft ID | Company | Channel | Offer | Persuasion Score | Risk | Action Needed |
|----------|---------|---------|-------|-----------------|------|---------------|
| {{draft_1_id}} | {{draft_1_company}} | {{draft_1_channel}} | {{draft_1_offer}} | {{draft_1_score}} | {{draft_1_risk}} | Approve / Reject |
| {{draft_2_id}} | {{draft_2_company}} | {{draft_2_channel}} | {{draft_2_offer}} | {{draft_2_score}} | {{draft_2_risk}} | Approve / Reject |
| ... | ... | ... | ... | ... | ... | ... |

**To approve:** `python -m dealix.os_runtime approval-check --draft-id <ID>`

---

## Replies Requiring Response / ردود تحتاج رد

{{#each pending_replies}}
- **{{company}}** — replied via {{channel}} at {{reply_time}}
  - Summary: {{reply_summary}}
  - Recommended next action: {{recommended_action}}
{{/each}}

*{{if no_pending_replies}}No pending replies today.{{/if}}*

---

## Channel Health / صحة القنوات

| Channel | Daily Limit | Used Today | % Used | Status |
|---------|------------|-----------|--------|--------|
| Email | 50 | {{email_used}} | {{email_pct}}% | {{email_status}} |
| WhatsApp (opt-in) | 20 | {{wa_used}} | {{wa_pct}}% | {{wa_status}} |
| LinkedIn (manual) | 20 | {{li_used}} | {{li_pct}}% | {{li_status}} |
| Phone Calls | 10 | {{calls_used}} | {{calls_pct}}% | {{calls_status}} |

Status legend: GREEN = <60% | YELLOW = 60-80% | RED = >80%

---

## Anti-Ban Status / حالة مكافحة الحظر

{{#if any_warnings}}
**WARNINGS ACTIVE:**
{{#each warnings}}
- Channel: {{channel}} — {{warning_message}} ({{current_count}}/{{limit}})
{{/each}}
{{else}}
All channels within safe limits. No warnings.
{{/if}}

{{#if circuit_breaker_active}}
**CIRCUIT BREAKER ACTIVE — ALL OUTBOUND HALTED**
Reason: {{circuit_breaker_reason}}
Requires founder approval to resume.
{{/if}}

---

## Revenue Forecast / توقعات الإيرادات

| Metric | Value (SAR) | Notes |
|--------|------------|-------|
| Pipeline (top 25 opportunities) | {{pipeline_total_sar}} | Estimated, not verified |
| Expected conversion (5%) | {{pipeline_5pct_sar}} | Rough estimate |
| Retainer target (month) | {{retainer_target_sar}} | Based on active clients |
| Current MRR | {{current_mrr_sar}} | Verified paid only |

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة*

---

## Today's 3 Priority Actions / أولويات اليوم الثلاث

1. **{{action_1_title}}**
   - What: {{action_1_what}}
   - Command: `{{action_1_command}}`
   - Expected outcome: {{action_1_outcome}}

2. **{{action_2_title}}**
   - What: {{action_2_what}}
   - Command: `{{action_2_command}}`
   - Expected outcome: {{action_2_outcome}}

3. **{{action_3_title}}**
   - What: {{action_3_what}}
   - Command: `{{action_3_command}}`
   - Expected outcome: {{action_3_outcome}}

---

## Doctrine Reminders / تذكيرات المبادئ

- No draft is sent without explicit founder approval.
- No cold WhatsApp automation — opted-in contacts only.
- No LinkedIn automation — founder sends manually only.
- No guaranteed revenue claims to prospects.
- All estimates labeled as estimated, not verified.

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة*
