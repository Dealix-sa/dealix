# Evidence Pack — Sample — حقيبة الأدلة (عيّنة)

> **Sample — illustrative.** This is what Dealix delivers as proof for one customer engagement. Every engagement closes with an Evidence Pack. The format here is the standard; values are sanitized placeholders.
>
> **عيّنة توضيحية.** هذا ما يسلّمه ديلكس كدليل لكل ارتباط عميل. كل ارتباط يُختم بحقيبة أدلة. التنسيق هنا هو المعيار، والقيم محجوزات مُعقَّمة.

---

## 0. Cover — الغلاف

- **Engagement:** Revenue Hunter Pilot — Customer A (شركة عميل أ)
- **Engagement ID:** ENG-2026-0042
- **Period:** 2026-04-01 → 2026-05-22
- **Dealix lead:** [Name redacted]
- **Customer executive sponsor:** [Name redacted, role: Commercial Director]
- **Document version:** 1.0
- **Date issued:** 2026-05-25

---

## 1. Scope Memo — مذكرة النطاق

**Objective.** Identify and verify ten qualified opportunities for [Customer A] in the regional industrial services segment, governed by Dealix policies and tied to the customer's CRM.

**In scope.** Inbound discovery against public sources, opportunity drafting in CRM (Reviewer-approved writes), Evidence Pack v1 production.

**Out of scope.** External outreach of any kind. Cold email, cold WhatsApp, LinkedIn automation, scraping. Pricing negotiations.

**Success criteria.** Ten opportunities entered into CRM, each with a written rationale, source citation, and an evidenced revenue range; Evidence Pack delivered within 10 business days of pilot close.

---

## 2. Agent Registry Snapshot — لقطة سجل الوكلاء

Agents active during the engagement:
- `revenue_hunter` — owner: Commercial Lead, approval class: Reviewer.
- `trust_agent` — owner: Risk & Compliance, approval class: Reviewer.
- `proposal_drafter` — owner: Sales Ops, approval class: Reviewer.
- `evidence_pack_assembler` — owner: Risk & Compliance, approval class: Auto.

Full registry: see `AGENT_REGISTRY_SAMPLE.md`.

---

## 3. Tool Permission Snapshot — لقطة مصفوفة الصلاحيات

Effective matrix as of 2026-05-22. No deltas since the engagement opening snapshot. See `TOOL_PERMISSION_MATRIX_SAMPLE.md` for the full matrix.

Key restrictions during this engagement:
- `email_send` forbidden for all agents.
- `payments_write` forbidden for all agents.
- `code_exec` not invoked during the engagement.

---

## 4. Policy Version — نسخة السياسة

- AI Use Policy: v2.3, adopted 2026-03-10 by [Customer A].
- Data Boundaries: KSA residency, classes Public/Internal/Customer-Tenant in scope.
- No deviations during the engagement.

---

## 5. Approvals Log — سجل الموافقات

| Timestamp | Actor | Action | Target | Approval Class | Approver | Reference |
|---|---|---|---|---|---|---|
| 2026-04-03 10:14 | `revenue_hunter` | crm_write (lead creation) | CRM/leads | Reviewer | Commercial Lead | APR-00121 |
| 2026-04-08 14:02 | `proposal_drafter` | file_export (draft proposal) | Internal storage | Reviewer | Sales Ops | APR-00134 |
| 2026-04-15 09:30 | `trust_agent` | payments_read | Billing/ledger (read) | Reviewer | Risk Officer | APR-00141 |
| 2026-04-20 16:45 | `revenue_hunter` | mcp_external_search | Public sources | Allowed (logged) | n/a | APR-00149 |
| 2026-05-12 11:00 | `proposal_drafter` | contract_draft | Internal draft | Founder | Founder office | APR-00188 |

Total privileged actions in window: 314. Reviewer-approved: 47. Founder-approved: 3. Auto (logged): 264. Denied at policy check: 6 (all `email_send` attempts during a misconfigured template — addressed in incident IR-00007 below).

---

## 6. Outcome Graph Excerpt — مقطع من رسم النتائج

The outcome graph traces each agent action to a downstream business outcome. Excerpt for the period:

- Opportunities drafted: 14.
- Opportunities accepted into CRM by Commercial Lead: 11.
- Opportunities scored as Evidenced (vs Estimated): 10.
- Opportunities advanced to Stage 3 (proposal sent by named human): 7.
- Contracts signed in window: 2 (attributed to opportunities OPP-2026-0317, OPP-2026-0322).
- Retainers activated in window: 1 (RET-2026-0044).

Full graph delivered as a structured JSON file `outcome_graph_ENG-2026-0042.json` (not embedded in this sample).

---

## 7. Verified Revenue Attribution Table — جدول إسناد الإيراد المُتحقَّق

| Outcome ID | Type | Customer (anon) | Source-of-Truth System | Verified Value (SAR) | Attribution |
|---|---|---|---|---|---|
| OPP-2026-0317 → CON-2026-0091 | Contract | Customer B-7 | CRM + Billing | 240,000 | `revenue_hunter` (discovery), Commercial Lead (close) |
| OPP-2026-0322 → CON-2026-0094 | Contract | Customer B-12 | CRM + Billing | 165,000 | `revenue_hunter` (discovery), Sales Ops (proposal), Commercial Lead (close) |
| RET-2026-0044 | Retainer | Customer A (expansion) | Billing | 28,000 / month | Engagement-level (governed expansion) |

Values reconciled against the customer's billing system on 2026-05-22.

---

## 8. Incidents — الحوادث

| Incident ID | Severity | Date | Description | Resolution |
|---|---|---|---|---|
| IR-00007 | S2 | 2026-04-11 | Misconfigured proposal template attempted to invoke `email_send`; policy check denied all 6 attempts. | Template patched; agent reviewed; no data exposure. Closed 2026-04-12. |

Total open incidents at engagement close: 0.

---

## 9. Founder Sign-off — اعتماد المؤسس

```
I confirm that this Evidence Pack reflects the governed activity of the engagement
ENG-2026-0042 for the period 2026-04-01 → 2026-05-22. All deviations are recorded.
All sensitive actions were routed through their declared approval class.

Approved: Sami (Founder, Dealix)
Date: 2026-05-25
Approval reference: APR-00201
```

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.*

Related: `/home/user/dealix/docs/trust/AGENT_REGISTRY_SAMPLE.md` · `/home/user/dealix/docs/trust/TOOL_PERMISSION_MATRIX_SAMPLE.md` · `/home/user/dealix/docs/trust/INCIDENT_RESPONSE_SAMPLE.md`
