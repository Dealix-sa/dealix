# CEO Operating Context — Dealix

**Owner**: Sami Assiri  
**Date**: 2026-06-10  
**Status**: Active

---

## What Dealix Is

Dealix is a **Saudi-first AI Business Transformation company**. We do not sell
software licenses. We sell operating systems — structured AI-powered workflows
that replace manual, broken, or missing business processes inside Saudi companies.

Our clients are: clinics, retail chains, professional services firms, SMEs, and
mid-market companies in Saudi Arabia that are losing revenue due to operational
inefficiency.

Our moat: we combine Arabic-first AI, PDPL compliance, ZATCA awareness, and
deep understanding of how Saudi businesses actually operate.

---

## Primary Offer: Transformation Diagnostic Sprint

| Field | Value |
|-------|-------|
| Price | 7,500 – 25,000 SAR |
| Duration | 3–7 days |
| Delivery format | Remote + Zoom review |
| Output | Workflow map, Leakage map, KPI model, First system recommendation, Implementation quote, 14-day pilot plan |
| Positioning | "نكتشف أين يتسرب إيرادك، وكيف يتوقف" |

This is the entry point to every enterprise engagement. The sprint creates:
- Credibility with the client
- A paid proof of capability
- A natural upsell to Managed Ops or Custom System

---

## Current Confirmed State (as of Wave 1)

- `main` includes Company OS, Founder OS, Micro Master OS, website transformation pages, production health scripts.
- `scripts/dealix_micro_day.sh` works and generates CEO report, approval queue, CRM update, daily offer, and lead research.
- Production API health passing.
- PR #706 merged (transformation OS).

---

## Daily Operating Rhythm

### Morning (CEO)
1. Run `./scripts/dealix_micro_day.sh`
2. Review `company/reports/MICRO_MASTER_CEO_REPORT.md`
3. Review `company/outbox/approval_queue.md` — approve or reject each item manually
4. Act on top 3 revenue actions

### Weekly (Revenue)
1. Review CRM pipeline in `company/crm/`
2. Check lead research in `company/lead_research/`
3. Update proposal statuses
4. Decide on new outreach batch

### Monthly (Strategic)
1. Review KPI model
2. Assess Wave progress
3. Decide next product/service additions

---

## Sales Motion

We are founder-led sales. Sami handles all external communications directly.
No automated sending. No bots that message clients.

**Outreach channels:**
- Personal WhatsApp (warm intros only)
- LinkedIn DM (connection-based)
- Email (warm list)
- Referrals from existing clients

**Qualification criteria:**
- Saudi-based company
- 10+ employees OR 500K+ SAR annual revenue
- Clear operational problem (not just "we want AI")
- Decision maker reachable

---

## Revenue Targets

| Period | Target |
|--------|--------|
| Month 1 | First paid sprint (7,500 SAR min) |
| Month 3 | 3 active sprint clients |
| Month 6 | 2 Managed Ops retainers + 1 Custom System |
| Year 1 | 500,000+ SAR revenue |

---

## Operating Accounts (Saudi)

Primary sectors with diagnostic sprint potential:
- Medical clinics & healthcare groups
- Legal offices & professional services
- Retail chains
- Real estate agencies
- Education & training centers
- Logistics & delivery companies

---

## Claude Code Session Rules

When starting a new Claude Code session in this repo:

1. Read `CLAUDE.md` first.
2. Read this file.
3. Run `git status --short` to see current state.
4. Do NOT start running scripts without reading what they do.
5. State which Wave you are executing.
6. Stop after creating PR — do not proceed to next Wave.

---

## Escalation Gates

These require founder decision before proceeding:

| Situation | Action |
|-----------|--------|
| Proposal ready to send | Founder reviews and sends manually |
| Invoice to issue | Founder issues via Zoho/Wave manually |
| PR ready to merge | Founder reviews and merges |
| New service price change | Founder approves |
| New API key needed | Founder rotates via Railway dashboard |
| Client data to store | Founder confirms PDPL classification |
