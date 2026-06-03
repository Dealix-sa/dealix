# Approval Queue — قائمة الموافقة

The founder's daily decision surface over produced drafts. Nothing is sent from
here — approval only marks drafts eligible for a staged
[sending batch](../../docs/outreach/SENDING_RAMP_PLAN_AR.md).

**Source:** the drafts store, ranked. Regenerate:
`python -m dealix.market_production_os.control_room --produce --print`.

## Today — اليوم

| # | draft_id | company | sector | touch | offer | P-level | gate | decision |
|---|---|---|---|---|---|---|---|---|
| 1 | … | … | … | first_touch | revenue_diagnostic | P2 | pass | ☐ approve ☐ edit ☐ reject |

## Founder decisions — قرارات المؤسس

`Approve` · `Reject` · `Rewrite` · `Shorten` · `Make more formal` ·
`Change offer` · `Move to nurture` · `Do not contact`.

## Daily targets — أهداف اليوم

- Review the **top 50** drafts; flag the **riskiest 10**.
- Approve **30–50** that are ≥ P1 and pass every gate.
- Stage an approved batch **within today's ramp cap** only.

Drafts that fail the [compliance gate](../../docs/outreach/COLD_EMAIL_COMPLIANCE_AR.md)
never appear as approvable.

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
