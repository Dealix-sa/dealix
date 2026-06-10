# Dealix Price Book — English (v2.0)

> **Internal reference for the founder and sales.** Sharing any price with a
> customer requires founder approval (human gate — `os/01_CLAUDE.md`). All prices
> are **ex-VAT**; 15% VAT is added per ZATCA rules and shown on the invoice.

**Source of truth:** [`os/config/pricing.yml`](../os/config/pricing.yml) ·
[`os/config/packages.yml`](../os/config/packages.yml) ·
[`os/config/usage_meters.yml`](../os/config/usage_meters.yml).
Change prices there first, then render quotes with
`python scripts/generate_quote.py`.

---

## Commercial principle

Dealix is **not sold as "an AI service"** or as a one-off build. The correct model is:

> **Setup fee + monthly subscription + usage/expansion + performance where possible.**

| Lever | Purpose |
| --- | --- |
| Setup fee | Covers time, analysis, integration, customization, delivery |
| Monthly subscription | Recurring revenue (MRR) |
| Usage / capacity add-ons | Revenue grows with the customer's usage |
| Premium support | Turns support from cost into profit |
| Expansion modules | Same customer buys more instead of constant net-new hunting |

---

## 1) Entry offers (fast close, not margin maximization)

| Offer | Price | Duration | Goal |
| --- | --: | --: | --- |
| AI Workflow Audit | 9,500 | 5 days | Surface chaos, opportunity map, prep the Pilot |
| Regulated / Legal Audit | 15,000 | 7 days | Sensitive sectors: legal/health/finance/large entities |
| AI Revenue Leak Audit | 12,000 | 5 days | Find lost opportunities in sales & follow-up |
| Executive AI Readiness Pack | 18,000 | 10 days | CEO report + roadmap + prioritized use cases |

- **Rule:** never sell an Audit below **5,000**. Start at **9,500** as the standard.
- **Upgrade:** 50% of the Audit value credited if they move to a Pilot within 14 days.

## 2) Paid pilots (ROI proof, not a free trial)

| Offer | Price | Duration | When to sell |
| --- | --: | --: | --- |
| Pilot Lite — No API | 30,000 | 21–30 days | Hesitant client or data not ready |
| **Pilot Pro — With API** | **60,000** | 30 days | Clear system/CRM/Excel/API *(recommended)* |
| Multi-System Pilot | 100,000 | 45 days | Multiple departments or workflows |
| Regulated Pilot | 75,000–120,000 | 45 days | Legal/health/sensitive with human approvals |

**Every Pilot ships:** a working dashboard/workflow + before/after report + an upgrade offer to Production with a monthly subscription.

## 3) Production contracts (Setup + Monthly)

| Product | Setup | Build time | Monthly after delivery |
| --- | --: | --: | --: |
| Maintenance Intelligence OS | 150,000–250,000 | 60 days | 12,000–25,000 |
| Legal Knowledge OS | 180,000–300,000 | 75–90 days | 15,000–35,000 |
| GCC International AI OS | 100,000–220,000 | 30–60 days | 12,000–30,000 |
| Consulting Delivery OS | 120,000–200,000 | 60–75 days | 10,000–25,000 |
| Project Controls AI OS | 180,000–300,000 | 75–90 days | 15,000–35,000 |
| Property Operations OS | 120,000–220,000 | 60–75 days | 10,000–25,000 |
| Healthcare Admin OS | 200,000–350,000 | 90 days | 20,000–45,000 |
| Dealix Command Center | 300,000–500,000 | 90–120 days | 25,000–60,000 |

- **Rule:** any Production under **150,000** hurts Dealix positioning.
- A client who refuses a monthly subscription after delivery is a **cash project only**, not a recurring asset.

---

## 4) Monthly packages — the semi-passive revenue engine

| Package | Monthly | Best for |
| --- | --: | --- |
| Monitor | 8,000 | Small client after a Pilot (retention) |
| **Managed OS** | **15,000** | One running system *(primary target)* |
| Growth + Ops OS | 25,000 | Operationally dependent on Dealix |
| Command Center | 45,000 | Executive team or multiple departments |
| Enterprise Sovereign OS | 60,000+ | Large/sensitive (isolation, governance, SLA) |

> **Best model:** anchor on **15,000** as the target average. Don't make 8,000 the default.

## 5) Usage pricing (package gives an allowance; overage is billed)

| Meter | Unit | Price |
| --- | --- | --: |
| Maintenance tickets | per 1,000 | 1,500–3,000 |
| Legal documents | per 1,000 docs/pages | 2,500–6,000 |
| Leads / dossiers | per 1,000 | 1,500–4,000 |
| Qualified WhatsApp messages | per 1,000 | 800–2,500 |
| Proposals | per 100 | 2,000–5,000 |
| Extra department (Command Center) | per department | 8,000–20,000 / mo |
| Custom weekly executive report | per report | 2,000–7,000 / mo |

> **Example:** Managed OS = 15,000/mo including 3,000 operations. Each extra 1,000 = 2,500. **No discount on overage.**

---

## 6) Payment terms

**Projects (50/30/20):** 50% on signing · 30% after MVP/Pilot · 20% on launch.

**Subscriptions:** 6-month minimum (12 preferred) · monthly in advance · 10% annual discount · early cancel = 2 months penalty · out-of-scope support 500–800/hour.

**Allowed discounts only:** 10% annual prepay · 15% for the first 3 customers in exchange for a case study · **no discount on overage.**

## 7) Margin protection (checked before sending)

| Item | Floor |
| --- | --: |
| Gross margin (projects) | 55% |
| Gross margin (subscriptions) | 65% |
| Net margin target | 25%+ |
| Pilot discount | ≤ 20% |
| Minimum retainer | 8,000 |
| Minimum Production | 150,000 |
| Minimum consulting hour | 500 |

> Before any quote: `python scripts/calculate_margin.py --price <P> --cost <C> --type project|subscription`.

## 8) The final ladder

1. **Entry:** AI Workflow Audit — 9,500
2. **Pilot:** Pilot Pro — 60,000
3. **Production:** from 150,000
4. **Monthly:** Managed OS — 15,000 (primary target)
5. **Premium:** Command Center — 300,000 setup + 45,000/mo

**One-line pitch:**
> "We don't sell a chatbot. Dealix builds a practical operating system for the company:
> it captures the daily breakdowns in follow-up, reporting, maintenance, proposals, and
> approvals, then turns them into measurable workflows. We start with a paid audit, then a
> Pilot, then a production system with a monthly subscription for continuous improvement."

---

## Governance notes

- High-touch invoices are issued **manually** via contract + ZATCA invoice (not Moyasar auto-charge).
- This track is independent of the low-ticket productized ladder (499/1,500/2,999/7,500) in
  `auto_client_acquisition/service_catalog/registry.py` that powers checkout.
- Prices are **estimates** until a quote is signed; language is a **commitment**, not a **guarantee**.
