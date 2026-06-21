# DEALIX WEEK 1 QUICK WINS — IMPLEMENTATION GUIDE
**Date:** 2026-06-17 to 2026-06-20  
**Owner:** Founder (Sami Assiri)  
**Status:** READY TO EXECUTE  

This guide provides step-by-step instructions for 11 high-impact documentation + configuration tasks that can be completed in one week with zero code risk.

---

## MONDAY 2026-06-17 (TODAY) — Start Here

### TASK 1: Freeze External Product Names (2 hours)

**Objective:** Create a single source of truth for customer-facing product names. End the 8-name confusion.

**Current problem:**
- Internal docs mention: "WhatsApp Revenue OS," "Review Intelligence OS," "Command Center," "Brand Intelligence OS," "Growth Engine OS," "Customer Experience OS," "AI Agent Workforce OS," "Custom Enterprise Systems"
- Customers see different names in different materials
- Sales team isn't consistent
- This creates confusion + reduces perceived value

**Solution:**
Create `/home/user/dealix/docs/PRODUCT_NAMING_AUTHORITY.md` with:

1. **External (customer-facing) names** — ONLY use these 4 in any customer communication
2. **Internal module map** — Shows which 32+ internal modules map to these 4
3. **Enforcement rule** — "If you're tempted to say 'WhatsApp Revenue OS,' say 'Dealix Radar + AI Team' instead"
4. **Audit checklist** — How to verify all materials use correct names

**Steps to implement:**

1. Open your editor and create `docs/PRODUCT_NAMING_AUTHORITY.md`

2. Fill in this content:
```markdown
# DEALIX PRODUCT NAMING AUTHORITY
**Version:** 1.0  
**Effective:** 2026-06-17 to 2026-09-17 (locked for 90 days)  
**Owner:** Founder  
**Last updated:** 2026-06-17

---

## EXTERNAL NAMES ONLY (Use in All Customer Communication)

| External Name | What It Does | Customer Perception |
|---------------|-------------|-------------------|
| **Dealix Radar** | Market visibility, lead discovery, opportunity scoring | "I can see all my leads + know which are most valuable" |
| **Dealix AI Team** | AI agents for daily operations (sales, growth, operations, support, executive) | "AI makes decisions for me, I approve them" |
| **Dealix Portal** | Customer interface, dashboard, approval workflows, reporting | "One place to see and control everything" |
| **Dealix Proof** | Evidence packs, case studies, ROI tracking, impact measurement | "Proof that this works in SAR, not just claims" |

---

## INTERNAL MODULE MAP (Do Not Use in Customer Communication)

These 32+ modules exist but are HIDDEN from customers. Never say these names to customers:

| Internal Module Name | Maps to External Name | Do Not Mention to Customers |
|----------------------|----------------------|----------------------------|
| leadops_spine | Radar | "leadops_spine" is internal term |
| customer_brain | AI Team | Keep technical names in code only |
| approval_center | Portal | Even if customer asks "what's the approval system?" answer is "Portal," not "approval_center" |
| payment_ops | Portal + Proof | --- |
| proof_ledger | Proof | --- |
| governance_os | Portal | --- |
| [... 26 more internal names] | [... maps] | Never expose in customer docs |

---

## ENFORCEMENT RULE

**If you catch yourself saying any of these to a customer, STOP and use the external name:**

| ❌ Wrong (Internal) | ✅ Right (External) |
|-----------------|------------|
| "We use the WhatsApp Revenue OS" | "Dealix Radar + AI Team + Portal" |
| "The Command Center dashboard" | "Dealix Portal" |
| "Review Intelligence OS" | "Dealix Radar (for reviews) + Proof" |
| "The governance layer" | "Dealix Portal approvals" |
| "Our AI agents run the proof ledger" | "Dealix AI Team generates Dealix Proof" |

---

## CUSTOMER COMMUNICATION CHECKLIST

Before sending any customer-facing material (email, proposal, case study, slide deck), audit it:

- [ ] Search document for: "WhatsApp," "Revenue OS," "Command Center," "Review Intelligence," "Growth Engine," "Enterprise System"
- [ ] Search for internal module names: "leadops," "customer_brain," "governance," "payment_ops"
- [ ] Replace all with external names (Radar, AI Team, Portal, Proof)
- [ ] Read it once: Does it make sense to a non-technical customer?
- [ ] If unclear, rewrite it

---

## EXAMPLE: HOW TO DESCRIBE DEALIX

### ❌ Wrong (confusing, uses 8+ names):
"Dealix includes the WhatsApp Revenue OS for lead management, the Command Center for visibility, the Review Intelligence OS for reputation, the Growth Engine OS for expansion, and the AI Agent Workforce OS for operations."

### ✅ Right (clear, uses 4 names):
"Dealix has four layers: Radar (see all opportunities), AI Team (automate decisions), Portal (control everything), and Proof (measure impact)."

---

## QUESTIONS?

If a customer asks "what is X?", answer using ONLY the 4 external names. Example:

Customer: "Can Dealix manage our WhatsApp leads?"
You: "Yes. Dealix Radar finds your leads. Dealix AI Team routes them. Dealix Portal shows you everything. Dealix Proof measures the impact."

Customer: "Can I see a proof that this works?"
You: "Yes, Dealix Proof gives you evidence packs showing exactly what worked."

---

## NEXT REVIEW

This naming lock expires on 2026-09-17. At that point, the Founder decides:
- Keep these 4 names (likely)
- Or pivot to new names (unlikely unless massive market feedback)

Changing names after we've sold to customers is confusing. So we lock for 90 days minimum.

---

## AUDIT LOG

When completed, log here:
- 2026-06-17: Document created. All sales materials to be audited by 2026-06-20.
```

3. **Save the file** to `docs/PRODUCT_NAMING_AUTHORITY.md`

4. **Audit existing materials:**
   - Search all files in `/sales/` and `/docs/` for: "WhatsApp Revenue OS", "Command Center", "Review Intelligence", "Growth Engine", "Brand Intelligence", "Customer Experience OS", "AI Agent Workforce OS"
   - For each file found, replace with correct external name
   - Example: "WhatsApp Revenue OS" → "Dealix Radar + AI Team"

5. **Update README.md** to reference this doc in the "What is Dealix?" section

**Time:** ~2 hours  
**By Friday?** Yes  
**Risk:** None (documentation only)  
**Impact:** Sales team has clarity. Customers see consistent messaging. Brand identity locks in.

---

### TASK 2: Create 3-Slide Founder Pitch Deck (1.5 hours)

**Objective:** Give Founder a 90-second pitch for warm outreach (instead of 10+ minutes of rambling).

**Current problem:**
- Pitch is scattered across 10+ docs
- Inconsistent messaging
- Takes too long to explain

**Solution:**
Create a 3-slide deck (Google Slides, Keynote, or PowerPoint):

**Slide 1: THE PROBLEM**
```
Headline: "Your Saudi B2B Company Is Losing 30–60% of Revenue"

Why?
- WhatsApp leads slip through cracks (no system)
- No unified view of KPIs (decisions are slow)
- Manual workflows eat time and money
- No proof that AI improvements work

Question: Is this you?
```

**Slide 2: THE SOLUTION**
```
Headline: "Dealix = AI Operating System"

Four layers:
1. Dealix Radar — Find & score leads (Saudi B2B context)
2. Dealix AI Team — Automate decisions (WhatsApp, email, reports)
3. Dealix Portal — Control center with approvals
4. Dealix Proof — Evidence packs showing ROI in Riyal

Timeline: 7 days to deployment (not months)
Margin: 70%+ gross profit for your company
```

**Slide 3: WHY DEALIX**
```
Headline: "Why Not HubSpot, Salesforce, Apollo, or DIY?"

✓ Arabic-first (not English defaults + translation)
✓ PDPL-native (not bolted-on compliance)
✓ Approval-first (humans approve, AI recommends)
✓ Saudi context (ZATCA, local workflows)
✓ Founder-led quality (not agency churn)
✓ Proven (real customers, real proof)

Offer: 499 SAR proof sprint (test before buying)
Diagnostic: 7,500 SAR (3–7 days, full roadmap)
```

**Implementation:**
1. Open Google Slides (or your preferred tool)
2. Create 3 slides with content above
3. Use Dealix brand colors (from DESIGN_SYSTEM.md)
4. Download as PDF and save to `presentations/founder_pitch_deck.pdf`
5. Share link with Warm List (so they see what you're building)

**Time:** ~1.5 hours  
**By Friday?** Yes  
**Risk:** None (presentation only)  
**Impact:** Founder can pitch in 90 seconds. Warm prospects immediately understand. Closing rate increases.

---

### TASK 3: Lock Pricing & Payment Terms (1.5 hours)

**Objective:** Single source of truth for pricing. End "what's the price?" ambiguity.

**Current problem:**
- Pricing scattered across multiple docs (PRICING_AND_OFFER_LADDER_AR.md, DEALIX_BUSINESS_MODEL.md, sales pages)
- Different prices in different places (4,999 SAR vs. different prices in docs)
- No clarity on payment terms
- Sales people invent pricing instead of looking up the truth

**Solution:**
Create `/home/user/dealix/docs/PRICING_AUTHORITY.md`:

```markdown
# DEALIX PRICING & PAYMENT AUTHORITY
**Version:** 1.0  
**Effective:** 2026-06-17 to 2026-08-17 (locked for 60 days)  
**Owner:** Founder  
**Currency:** SAR (Saudi Riyal)  
**Last updated:** 2026-06-17

---

## OFFER LADDER (6 tiers)

### TIER 1: Free AI Diagnostic
- **Price:** 0 SAR
- **Duration:** 30 minutes (1 Zoom or WhatsApp call)
- **Output:** 3 identified revenue leaks + recommended first OS
- **Purpose:** Qualify + build trust + convert to paid
- **Who should buy:** Anyone curious (no commitment)

### TIER 2: Micro Proof Sprint
- **Price:** 499 SAR (fixed)
- **Duration:** 7 days
- **Output:** 1 quick-win OS deployed, documented
- **Payment terms:** 100% upfront (due at invoice)
- **Purpose:** Proof of concept (low-risk entry)
- **Who should buy:** Want to test before committing

### TIER 3: Data Intelligence Pack
- **Price:** 1,500 SAR (fixed)
- **Duration:** 2–3 days
- **Output:** Lead scoring + data asset (CRM enrichment)
- **Payment terms:** 100% upfront
- **Purpose:** Data asset (doesn't expire, repeatable value)
- **Who should buy:** Need customer/lead data fast

### TIER 4: Managed AI Operations
- **Price:** 2,999–4,999 SAR/month (retainer)
- **Duration:** Ongoing (monthly renewal)
- **Output:** Weekly AI operations, reports, monthly review
- **Payment terms:** Monthly in advance (auto-renew)
- **Purpose:** Recurring revenue, sticky customer
- **Who should buy:** Want ongoing value (not one-time project)

**Pricing decision rule for Tier 4:**
- New customer (first month): 2,999 SAR (entry-level)
- If customer is large (>50 people) or high-touch: 3,999 SAR
- If customer wants all 4 OS layers (full suite): 4,999 SAR
- Price increases only after 6 months (avoid surprises)

### TIER 5: Transformation Diagnostic
- **Price:** 7,500 SAR (default) to 25,000 SAR (complex)
- **Duration:** 3–7 days
- **Output:** Full workflow map, leakage map, KPI model, first system recommendation, implementation quote, 14-day pilot plan
- **Payment terms:** 50% upfront (3,750 SAR), 50% on delivery (Day 7)
- **Purpose:** Enterprise entry, creates roadmap for multi-system engagement
- **Who should buy:** Need full business picture before committing
- **Pricing decision rule:**
  - Default: 7,500 SAR
  - If customer has >10 locations or >500 people: 12,500 SAR
  - If customer is in highly regulated industry (finance, healthcare): 15,000 SAR
  - If customer has existing AI/data infrastructure: 25,000 SAR (more complex integration)

### TIER 6: Custom Enterprise System
- **Price:** 25,000 to 100,000+ SAR
- **Duration:** 4–12 weeks
- **Output:** Production AI system integrated into customer's operations
- **Payment terms:** 30% upfront, 40% at Day 7 (proof), 30% at final delivery
- **Purpose:** Largest revenue, reference customer creation
- **Who should buy:** Need custom solution (not productized offering)
- **Pricing decision rule:**
  - Minimum 25,000 SAR (cost of 4+ weeks founder time)
  - 50,000+ SAR if requires integration with 3+ external systems
  - 100,000+ SAR if requires custom AI training on customer data

---

## PAYMENT TERMS (Golden Rule: 50/50 on delivery, monthly in advance for retainers)

| Offer | Payment Timeline | How to Calculate |
|-------|-----------------|------------------|
| Tier 1 (Free) | N/A | Free (lead magnet) |
| Tier 2 (Sprint) | 100% upfront | Invoice Day 1, delivery Day 7 |
| Tier 3 (Data) | 100% upfront | Invoice Day 1, delivery Day 3 |
| Tier 4 (Retainer) | Monthly in advance | Invoice on Day 1 of month, continues auto |
| Tier 5 (Diag) | 50% upfront, 50% on delivery | 50% due Day 1, 50% due Day 7 |
| Tier 6 (Custom) | 30% / 40% / 30% | Day 1 (30%), Day 7 (40%), Day 21 (30%) |

---

## REFUND POLICY

- **Tier 2 (Sprint):** 14-day money-back guarantee (if not satisfied)
- **Tier 3 (Data):** No refund (data delivered Day 1)
- **Tier 4 (Retainer):** No refund (as of Month 1). Can cancel with 30-day notice
- **Tier 5 (Diagnostic):** No refund (diagnostic delivered Day 1–3)
- **Tier 6 (Custom):** Negotiated per contract

---

## CURRENCY & ADJUSTMENTS

- **Official currency:** SAR (Saudi Riyal)
- **GCC adjustment:** If customer is outside Saudi (UAE, Kuwait, etc.), add 5% to price (currency risk)
- **USD reference:** Do NOT quote in USD. If customer asks, convert SAR ÷ 3.75 (approximate), but always invoice in SAR
- **Discounts:** Founder approval only. Max 10% for multi-year commitments or referral partners

---

## INVOICING RULES

- **Invoice format:** DEALIX-[YY][MM]-[SEQ] (example: DEALIX-260617-001 = June 17, 2026, invoice #1)
- **Who can create invoices:** Founder only (approval gate)
- **Payment methods:** Bank transfer (preferred), Moyasar (payment gateway)
- **Payment confirmation:** Founder verifies payment received before delivering
- **No auto-invoicing:** All invoices generated by founder (enforces approval gate)

---

## VALIDATION CHECKLIST

Before quoting any customer:

- [ ] Have you checked this doc?
- [ ] Did you offer the right tier (not a discount tier)?
- [ ] Did you explain payment terms (50/50, upfront, monthly)?
- [ ] Does the customer understand what's included (check PRODUCT_FEATURE_MATRIX.md)?
- [ ] If the customer asked for a discount, did you say "let me check with founder"?
- [ ] If the customer wants custom pricing, did you say "custom work is Tier 6, minimum 25K"?

---

## EXAMPLES

**Customer: "How much for a 7-day sprint?"**
Answer: "499 SAR. You pay 100% upfront when we start (invoice today), and we deliver on Day 7."

**Customer: "Can I do 499 SAR for a Diagnostic?"**
Answer: "No, Diagnostics are 7,500 SAR (3–7 day engagement, full roadmap). Sprints are 499 SAR (7-day, 1 quick win). Which fits your timeline?"

**Customer: "Can you do a 30% discount for annual commitment?"**
Answer: "Let me check with the Founder. Our standard is no discounts, but annual commitments are rare — I'll ask."

**Customer: "We want Tier 4 retainer but your price is 3,999 SAR."**
Answer: "That's correct for your company size. If budget is tight, Tier 2 (499 SAR sprint) proves value first, then we upgrade to Tier 4. Would that work?"

---

## REVISION HISTORY

| Date | Change | Reason |
|------|--------|--------|
| 2026-06-17 | Document created | Lock pricing for Q2 2026 |
| [future] | [future changes] | [reason] |

---

## QUESTIONS?

If you have a pricing question not covered here, email founder. Don't invent pricing.
```

**Implementation:**
1. Create `docs/PRICING_AUTHORITY.md` with content above
2. Link to this doc from: `sales/DEALIX_MASTER_ONE_PAGER_AR.md`, `sales/DEALIX_MASTER_ONE_PAGER_EN.md`, `landing/pricing.html`
3. Audit all existing price quotes to ensure they match this doc
4. Share with sales team + contractors: "From now on, all quotes reference PRICING_AUTHORITY.md"

**Time:** ~1.5 hours  
**By Friday?** Yes  
**Risk:** None (documentation only)  
**Impact:** No more "what's the price?" debates. All quotes consistent. Founder time saved (no email back-and-forths on pricing).

---

### TASK 4: Create Product Feature Matrix (1.5 hours)

**Objective:** Show exactly which OS + features come with each tier.

**Current problem:**
- Customer asks: "Is X included in my plan?"
- Answer varies depending on who responds
- No clear way to answer "what's different between Tier 2 and Tier 4?"

**Solution:**
Create `/home/user/dealix/docs/PRODUCT_FEATURE_MATRIX.md`:

```markdown
# DEALIX PRODUCT FEATURE MATRIX
**Version:** 1.0  
**Updated:** 2026-06-17  
**Owner:** Founder

---

## HOW TO READ THIS

Rows = Features / OS layers  
Columns = Offer tiers (Tier 1–6)  
Symbol meanings:
- ✓ = included (full access)
- ✓ (limited) = included with restrictions
- ✗ = not included

---

## FEATURE MATRIX

|  | Free Diagnostic | Micro Sprint (499 SAR) | Data Pack (1,500 SAR) | Managed Ops (2,999+/mo) | Transform Diag (7,500) | Custom System (25K+) |
|---|---|---|---|---|---|---|
| **DEALIX RADAR** | | | | | | |
| Lead discovery | View-only | ✓ (1 month) | ✓ | ✓ | ✓ | ✓ |
| ICP scoring | Demo | Basic | ✓ | ✓ | ✓ | ✓ |
| Opportunity ranking | ✗ | ✗ | ✓ | ✓ | ✓ | ✓ |
| **DEALIX AI TEAM** | | | | | | |
| Sales Agent | Demo | Limited | Limited | ✓ | ✓ | ✓ |
| Growth Agent | Demo | ✗ | ✗ | ✓ | ✓ | ✓ |
| Support Agent | Demo | ✗ | ✗ | ✓ | ✓ | ✓ |
| Operations Agent | Demo | ✗ | ✗ | ✓ | ✓ | ✓ |
| Executive Agent | Demo | ✗ | ✗ | ✓ | ✓ | ✓ |
| **DEALIX PORTAL** | | | | | | |
| Customer dashboard | Mobile view | Web view | ✓ | ✓ + mobile | ✓ + mobile | Custom |
| Approval workflows | ✗ | 1 gate (limited) | 1 gate | ✓ (all) | ✓ (all) | ✓ (all) |
| WhatsApp integration | ✗ | Draft-only | Draft-only | ✓ (live) | ✓ (live) | ✓ (live) |
| Email integration | ✗ | Draft-only | Draft-only | ✓ (live) | ✓ (live) | ✓ (live) |
| **DEALIX PROOF** | | | | | | |
| Proof pack assembly | N/A | Manual (Day 7) | Manual (Day 3) | Automated (weekly) | Automated (daily) | Automated (daily) |
| ROI calculator | N/A | Simple | ✓ | Dashboard | Dashboard | Dashboard + API |
| Case study export | N/A | Draft | Draft | Ready | Ready | Branded + API |
| **ADDITIONAL** | | | | | | |
| Founder delivery hours | 0.5h | 8h | 4h | 2h/month | 20h | Custom |
| Customer support | Email only | Email | Email | Priority 4h SLA | Priority 2h SLA | Dedicated |
| Integrations | 0 | 0 | 1 (CRM read) | 3–5 | 5–10 | Custom |

---

## TIER POSITIONING

### Why choose each tier?

**Tier 1 (Free Diagnostic):**
- "Just curious about what Dealix does"
- 30 min conversation
- No commitment, no payment

**Tier 2 (Micro Sprint - 499 SAR):**
- "Show me it works with one quick win"
- 7 days, low risk, affordable
- Proof before committing to more

**Tier 3 (Data Pack - 1,500 SAR):**
- "We need lead/customer data fast"
- 2–3 days
- Data doesn't expire (use it forever)

**Tier 4 (Managed Ops - 2,999–4,999 SAR/month):**
- "Run our operations with AI daily"
- Ongoing, sticky relationship
- Highest lifetime value

**Tier 5 (Transformation Diagnostic - 7,500 SAR):**
- "We need a full roadmap before committing"
- 3–7 days
- Outputs implementation plan for 25K+ system

**Tier 6 (Custom System - 25K+):**
- "We need a completely custom solution"
- 4–12 weeks
- Highest value, reference customer

---

## MIGRATION PATHS (How customers move between tiers)

```
Free Diagnostic (satisfied) → Tier 2 Micro Sprint (499 SAR)
Tier 2 (worked!) → Tier 4 Managed Ops (retainer)
Tier 3 (data asset) → Tier 4 (ongoing operations)
Tier 5 Diagnostic (roadmap ready) → Tier 6 Custom System
Tier 4 (growing) → Tier 5 + Tier 6 expansion
```

---

## CUSTOMER SELF-SERVICE

If a customer asks "Is X in my plan?", they can:
1. Search this matrix for their tier
2. Find the row (feature/OS)
3. See if it's ✓ or ✗

---

## COMMON QUESTIONS

**Q: Can I add features from Tier 4 to my Tier 2 sprint?**
A: No, tiers are locked. If Tier 2 proves value, upgrade to Tier 4 (monthly) or Tier 5 (3–7 days). We don't mix tiers mid-engagement.

**Q: What if I want 2 of the 5 AI agents, not all 5?**
A: Tier 4 includes all 5. If you only want 2, you're still paying for 5 (no à la carte pricing). Tier 6 (Custom) can do à la carte if you want custom pricing.

**Q: Can I downgrade from Tier 4 to Tier 2?**
A: No, Tier 2 is one-time (7 days). If Tier 4 doesn't work, you cancel the retainer (30-day notice).

---

## UPDATING THIS MATRIX

When we ship new features:
1. Update this matrix
2. Email customer base: "New feature in Tier 4!" (if applicable)
3. Offer existing customers to upgrade if the feature is valuable

Don't surprise customers. Announce feature additions.
```

**Implementation:**
1. Create `docs/PRODUCT_FEATURE_MATRIX.md` with content above
2. Link from: PRICING_AUTHORITY.md, Product Docs portal (Week 2), sales proposals
3. Use this matrix in every customer call ("Here's what's in your tier")

**Time:** ~1.5 hours  
**By Friday?** Yes  
**Risk:** None (documentation only)  
**Impact:** Customers understand what they're buying. No "this feature isn't in my plan" complaints. Sales clarity.

---

### TASK 5: Extend CS SOP to Year 1 (2 hours)

**Objective:** Add Month 2–12 playbook so Founder knows exactly what to do to prevent churn + drive upsell.

**Current problem:**
- CS SOP ends at Day 14
- After Month 1 retainer invoice, no playbook
- Founder improvises instead of following system
- Churn risk is high (no expansion conversation after Month 1)

**Solution:**
Update `/home/user/dealix/docs/CUSTOMER_SUCCESS_SOP.md` to add:

**Section to add after existing Day 0–14 SOP:**

```markdown
# PHASE 4: MONTH 1 CHECK-IN (New)
## Timeline: Day 14 (decision) → Day 30 (retainer customer's first month)

### If customer chose "Partner" (retainer):

**Week 1 (Days 14–21): Onboarding to Managed Ops**
- [ ] Send welcome email (outline Month 1 schedule)
- [ ] Grant Portal access (full permissions for the customer's team)
- [ ] Schedule first weekly ops review (Friday, 30 min call)
- [ ] Explain what to expect: daily AI decisions, weekly reviews, monthly strategic call

**Week 2–3 (Days 22–35): Daily operations**
- [ ] AI Team runs daily (Sales Agent, Ops Agent, Executive Agent)
- [ ] Founder approves 5–10 decisions/day for this customer
- [ ] Customer sees updates in Portal (live dashboard)
- [ ] Weekly 30-min call Friday: "What's working? What's not?"

**Week 4 (Days 36–42): Month 1 Check-in Call (60 minutes)**
- [ ] Review Month 1 proof events (leads qualified, time saved, revenue opportunities)
- [ ] Show: "Here's what AI recommended, here's what we actually did, here's the impact"
- [ ] Ask: "What's working? What's not? What would unlock 2x value?"
- [ ] Decision point: Continue as-is, expand to another OS, or pause?

---

# PHASE 5: MONTHS 2–3 VALUE REALIZATION (New)
## Timeline: Day 42 → Day 90

**Goal:** Prove the retainer is 10x cheaper than the value it generates.

### Week 5–6: Deepen one OS
- [ ] Based on Month 1 feedback, expand AI scope to unlock more value
- [ ] Example: "Sales Agent worked → now add Growth Agent for content automation"
- [ ] No charge if expanding within retainer; otherwise offer Tier 5 upsell

### Week 7: Executive Sponsor Review (NEW PERSON!)
- [ ] Invite customer CFO/CEO to review proof (30–60 min call with founder)
- [ ] Present: "AI automation saved X hours, unlocked Y revenue"
- [ ] This is the "aha moment" for C-level buy-in (critical for renewal)
- [ ] If strong executive buy-in: propose expansion or Tier 6 custom system

### Week 8: Month 2 Check-in
- [ ] Metrics update (proof events, revenue impact, time saved)
- [ ] Next 3 ideas for value unlock
- [ ] Expansion conversation if Month 1 metrics support it (health score ≥ 8, proof events ≥ 5)

---

# PHASE 6: EXPANSION PHASE (New)
## Timeline: Days 90–180 (Months 3–6)

**Goal:** From 1 OS → 3+ OS (or Tier 5 Transformation Diagnostic upsell).

### Expansion Triggers

You automatically propose expansion if ANY of these are true:

**Trigger 1: Healthy customer (health_score ≥ 8 for 30 days)**
- Recommendation: Tier 5 Transformation Diagnostic (7,500 SAR, full roadmap)
- Why: Healthy customer is ready to go bigger
- Timing: Propose at Month 3

**Trigger 2: High proof velocity (≥3 proof events/week)**
- Recommendation: Add 2 new OS layers to Tier 4 (no price increase)
- Why: Customer is getting value; let them do more
- Timing: Propose immediately (don't wait)

**Trigger 3: Revenue impact >100K SAR in Month 3**
- Recommendation: Tier 6 Custom System (25K–100K SAR, 4–12 weeks)
- Why: If one OS generated 100K, full system could generate 300K+
- Timing: Propose at Month 3 strategic review

### Month 3 Strategic Review (90 minutes, invite CEO + CFO)
- [ ] Present 3 options: (a) expand scope, (b) add new OS, (c) enterprise plan
- [ ] Show financial projection for next 12 months
- [ ] Define success metrics for expansion commitment
- [ ] Decision: Upgrade to Tier 5 or stay with Tier 4?

### Months 4–5: Implement Expansion
- [ ] Deploy new OS / features
- [ ] Weekly reviews to ensure adoption
- [ ] Prepare case study (if agreed)

### Month 6: Annual Review (Early)
- [ ] Customer LTV calculation (12-month projection)
- [ ] Renewal conversation (any changes? Price increase?)
- [ ] Referral ask ("who else needs this?")

---

# PHASE 7: RETENTION PHASE (New)
## Timeline: Days 180–365 (Months 7–12)

**Goal:** Lock in renewal, maximize NPS (target ≥ 8/10).

### Monthly Cadence (pick a day, always same day, e.g. Fridays)

| Month | Founder Conversation | Focus |
|-------|----------------------|-------|
| Month 7 | "How can we improve?" | Gather feedback, iterate |
| Month 8 | "Are you hitting your Year 1 goals?" | Measure impact |
| Month 9 | "What's the new priority for Year 2?" | Plan ahead |
| Month 10 | "Let's plan Year 2 together" | Strategic alignment |
| Month 11 | "Are we aligned on renewal?" | Confirm intent |
| Month 12 | "Renew + expand or pause?" | Renewal conversation |

### Churn Prevention (IF health < 6 at any point)
- [ ] Day 1: Founder reaches out (not a CS person) — "Hey, noticed engagement dropped, everything okay?"
- [ ] Day 3: In-person or video call with customer decision-maker — "What's not working?"
- [ ] Day 7: Root cause diagnosis + corrective plan — "Here's how we'll fix this"
- [ ] Target: Recover to health ≥ 7 within 30 days

### Renewal Negotiation (30 days before renewal date)
- [ ] No surprises. Discuss renewal price 30 days out
- [ ] Options: (a) renew at same price, (b) renew with expansion (+20%), (c) pause (option to restart)
- [ ] Lock renewal 14 days before date (email confirmation)
- [ ] If customer is pausing: ask for feedback (exit survey)

---

# PHASE 8: ANNUAL REVIEW & YEAR 2 PLANNING (New)
## Timeline: Day 365 (Month 12)

### Once per year (2-hour strategic review with decision-maker):
- [ ] Show: Year 1 impact (ROI, time saved, revenue unlocked) — full report
- [ ] Preview: Year 2 opportunities (new OS, deeper integrations)
- [ ] Discuss: Expansion to Tier 6 (custom system)?
- [ ] Measure: NPS score (annual, not monthly)
- [ ] Ask: Referral request ("How many did you refer? Any new leads you know?")

---

# MEASUREMENT GATES (By The Numbers)

**Success is:**

| Phase | Gate | Target |
|-------|------|--------|
| Day 14 | Customer completed sprint (1 OS deployed) | ✓ |
| Day 14 | Customer received proof pack (≥3 proof events) | ✓ |
| Day 30 | Retainer customer activated in Portal (≥3 logins) | ✓ |
| Day 45 | Retainer customer reviewed weekly ops (≥2 reviews) | ✓ |
| Month 1 | Customer NPS ≥ 7 | ✓ |
| Month 3 | Retainer customer generated ≥5 proof events | ✓ |
| Month 3 | Customer health score ≥ 7 | ✓ |
| Month 3 | Customer expanded OR renewed commitment | ✓ |
| Month 6 | Retainer customer MRR impact ≥ 2x retainer price | ✓ |
| Month 6 | Customer provided referral OR case study permission | ✓ |
| Month 6 | Upsell to Tier 5 OR expansion initiated | ✓ |
| Year 1 | Customer renewed retainer (or upgraded to Tier 6) | ✓ |
| Year 1 | Customer NPS ≥ 8 | ✓ |
| Year 1 | Customer provided public case study (if agreed) | ✓ |
| Year 1 | Customer referred 1+ peers | ✓ |

---

# ESCALATION RULES (Handle Immediately)

**Red flags (handle within 24 hours):**
- Customer says "we're not seeing value"
- Customer hasn't logged in for 7+ days
- NPS = 4 or lower (detractor)
- Support ticket without response in 4+ hours
- Customer calls founder directly (usually means CS slipped)

**Action:** Founder calls customer directly. Diagnose + fix.

**Orange flags (handle within 48 hours):**
- Health score < 6 (churn risk)
- Customer feedback is "meh" (NPS 5–7)
- Upsell conversation missed 30-day window
- Retainer payment delayed >3 days

**Action:** Founder sends email + schedules call.

**Green flags (celebrate):**
- Customer NPS ≥ 8 (promoter)
- Customer generates 3+ proof events/week
- Customer referred 1+ leads
- Customer proactively asks for new OS/capability

**Action:** Thank-you email, referral reward, case study request.
```

**Implementation:**
1. Open existing `docs/CUSTOMER_SUCCESS_SOP.md`
2. Add sections above after the Day 0–14 section
3. Save + commit: "docs: extend CS SOP with Month 1–12 playbook"
4. Share with team: "From Month 2 onward, follow this SOP (not improvisation)"

**Time:** ~2 hours  
**By Friday?** Yes  
**Risk:** None (documentation only)  
**Impact:** Founder has clear roadmap for retainer customers. Churn drops. Expansion conversations happen on schedule.

---

Continue with TASK 6–11 tomorrow and the remaining days.

(Due to length constraints, here are the remaining 6 tasks in abbreviated form — same depth, but summarized)

---

## TUESDAY 2026-06-18

### TASK 6: Create Operations Audit Checklist (1.5 hours)
**What:** Document what each daily ritual script does (dealix_micro_day.sh, dealix_revenue_day.sh, etc.) + troubleshooting.

**File:** Create `docs/DAILY_OPERATIONS_CHECKLIST.md`

**Content:**
- What each script does
- Expected output files
- How to troubleshoot if it breaks
- Who owns each script
- When to escalate

**Impact:** New team member runs daily ops without interrupting founder.

---

### TASK 7: Export OpenAPI Spec (1 hour)
**What:** Run API export script and publish docs.

**Command:** `python scripts/export_openapi.py > docs/api/openapi-v1.json`

**Then:** Create `docs/api/index.md` (getting started for partners)

**Impact:** Partners + integrators can build on API.

---

## WEDNESDAY 2026-06-19

### TASK 8: Create Data Dictionary (1.5 hours)
**File:** Create `docs/DATA_DICTIONARY.md`

**Content:**
- Every metric: name, definition, calculation, refresh rate, owner
- Searchable (team can grep for answers)
- Examples: health_score, adoption_rate, mrr, churn_rate

**Impact:** New team member finds answer without asking founder.

---

### TASK 9: Create Role Playbook Template (1.5 hours)
**File:** Create `docs/ROLE_PLAYBOOK_TEMPLATE.md`

**Content:**
- First 90 Days goals (by month)
- Daily/weekly/monthly rituals
- Decision framework
- Escalation rules
- Top 3 mentors
- Success metrics

**Impact:** Future Sales Head, CTO, CS Head get structured onboarding.

---

## THURSDAY 2026-06-20

### TASK 10: Create Landing Page Wireframes (1 hour)
**What:** 5-page website structure (Home, Pricing, Offers, Why Dealix, Contact).

**Tool:** Google Slides or Figma

**Content:**
- Page 1: Hero (problem + Dealix solution)
- Page 2: Pricing (show all 6 tiers)
- Page 3: Offers (Radar, AI Team, Portal, Proof)
- Page 4: Why Dealix (competitive matrix)
- Page 5: Contact (Calendly + email + WhatsApp)

**Impact:** Website can be built Week 2 (Webflow or Next.js).

---

### TASK 11: Define Expansion Gates (1 hour)
**File:** Create `docs/EXPANSION_GATES_2026.md`

**Content:**
- Gate 1: 1K MRR (case studies unlocked)
- Gate 2: 5K MRR (sales setter hire)
- Gate 3: 10K MRR (delivery ops hire)
- Gate 4: 20K MRR (enterprise sales hire)
- Gate 5: 50K MRR (Series A ready)

**Impact:** Founder can answer "should we hire?" by checking doc (not gut feel).

---

## FRIDAY 2026-06-20 — VERIFICATION

**Checklist:**

- [ ] Task 1: PRODUCT_NAMING_AUTHORITY.md created + all sales materials audited
- [ ] Task 2: 3-slide pitch deck shared + tested on 1 warm contact
- [ ] Task 3: PRICING_AUTHORITY.md created + linked from sales materials
- [ ] Task 4: PRODUCT_FEATURE_MATRIX.md created + shared with team
- [ ] Task 5: CS SOP extended to Year 1 + shared with team
- [ ] Task 6: DAILY_OPERATIONS_CHECKLIST.md created
- [ ] Task 7: OpenAPI spec exported + docs published
- [ ] Task 8: DATA_DICTIONARY.md created (searchable)
- [ ] Task 9: ROLE_PLAYBOOK_TEMPLATE.md + filled examples created
- [ ] Task 10: Landing page wireframes created
- [ ] Task 11: EXPANSION_GATES_2026.md created + founder reviewed

**Friday deliverable:**
- 11 new docs + updated materials
- All linked from a central "Week 1 Complete" document
- Ready to send to team + contractors

---

## TOTAL WEEK 1 TIME INVESTMENT

- Founder: ~18 hours (mostly writing, thinking, auditing)
- Engineer: ~2 hours (API export)
- Designer: ~1 hour (pitch deck + wireframes)
- **Total: ~21 hours**

**ROI:** Founder saves 2–3 hours/week going forward (no more "what's the price?" or "is X in my plan?"). In 10 weeks, 20–30 hours saved.

---

**Next Steps:**

1. **Friday EOD:** All 11 tasks complete
2. **Week 2:** Start medium-term initiatives (billing automation, website, CS dashboard)
3. **Week 4:** Measure impact (are sales clearer? Is website driving leads? Did CS improve?)

