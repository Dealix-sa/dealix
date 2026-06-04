# Event Taxonomy — تصنيف الأحداث والمقاييس

Every metric in the Dealix commercial funnel: its definition, its capture method (`auto` from system or `manual` founder entry), and its schema. No sample values are real; all numbers below are placeholders.

كل مقياس في قمع ديليكس التجاري: تعريفه، وطريقة التقاطه (تلقائي من النظام أو يدوي من المؤسس)، ومخططه. كل الأرقام أدناه أمثلة لا قيم حقيقية.

## Metric catalog — فهرس المقاييس

| Metric | Definition | Capture | Stage |
|---|---|---|---|
| website_visitors | Unique visitors to the site | auto (analytics) | Awareness |
| cta_clicks | Clicks on a primary call-to-action | auto | Interest |
| audit_requests | Submitted audit/diagnostic intake forms | auto | Intent |
| leads_created | Qualified leads entered in CRM | manual | Lead |
| drafts_generated | Outreach/reply drafts produced by the system | auto (run ledger) | Draft |
| founder_review_count | Drafts reviewed by the founder | manual | Review |
| manual_sends | Messages the founder sent manually after approval | manual | Send |
| replies | Responses received from prospects | manual | Response |
| positive_replies | Replies indicating interest | manual | Response |
| booked_diagnostics | Diagnostic calls/engagements scheduled | manual | Diagnostic |
| paid_diagnostics | Diagnostics paid for (Audit tier) | manual | Diagnostic |
| pilots_proposed | Pilot proposals sent | manual | Pilot |
| pilots_sold | Pilots signed | manual | Pilot |
| retainer_starts | Retainers started | manual | Retainer |
| pipeline_sar | Open opportunity value in SAR | manual | Revenue |
| realized_revenue_sar | Invoiced/collected revenue in SAR | manual | Revenue |
| safety_violations | Unsafe drafts caught before send | auto (governance log) | Safety |
| compliance_rejections | Drafts rejected on policy/claim safety | auto (governance log) | Safety |

## Schema — المخطط

```json
{
  "event_id": "string",
  "metric": "website_visitors | cta_clicks | audit_requests | leads_created | drafts_generated | founder_review_count | manual_sends | replies | positive_replies | booked_diagnostics | paid_diagnostics | pilots_proposed | pilots_sold | retainer_starts | pipeline_sar | realized_revenue_sar | safety_violations | compliance_rejections",
  "value": 0,
  "currency": "SAR",
  "capture": "auto | manual",
  "period_start": "YYYY-MM-DD",
  "period_end": "YYYY-MM-DD",
  "entered_by": "founder@dealix.sa | system",
  "source_ref": "ledger_id | analytics_id | manual_note",
  "note": "string"
}
```

Notes:

- `value` is `0` here as a placeholder. Real values are entered manually or exported; never invented.
- `currency` applies only to `pipeline_sar` and `realized_revenue_sar`; omit or set null otherwise.
- `capture=manual` metrics require `entered_by` and a `source_ref` or `note` for auditability.

## Definitions that need discipline — تعريفات تحتاج انضباطًا

- **positive_replies** counts genuine interest, not polite acknowledgement. Tighten the rule and keep it stable so trends are comparable.
- **pipeline_sar** is open opportunity value, clearly separated from `realized_revenue_sar`. Never blend the two.
- **safety_violations** and **compliance_rejections** are counted even when zero — "0 this period" is a real, reportable value.

## Related — مراجع

- Run ledger: [../06_llm_gateway/AI_RUN_LEDGER.md](../06_llm_gateway/AI_RUN_LEDGER.md)
- Governance log: [../05_governance_os/RUNTIME_GOVERNANCE.md](../05_governance_os/RUNTIME_GOVERNANCE.md)
- Value ledger: [../08_value_os/VALUE_LEDGER.md](../08_value_os/VALUE_LEDGER.md)

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
