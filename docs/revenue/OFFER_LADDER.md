# Dealix Offer Ladder

The five rungs the company sells. Every conversation, proposal, and contract maps to exactly one rung. The ladder is the single source of truth for what Dealix offers.

## Purpose
Lock the company on a small, ordered set of offers so the founder, the AI, and the customer share the same vocabulary. Each rung has clear inputs, deliverables, price, and the qualification criteria that determine which rung a customer fits.

## Owner
Sami (Founder).

## Review Cadence
Monthly, on the first Friday.

## Inputs
- Pipeline data on what customers asked for and paid for.
- Refusal reasons from lost deals.
- Delivery cost data per offer.
- Competitive positioning notes.

## Outputs
- The five rungs below.
- The qualification rule that maps a customer to a rung.
- The pricing range per rung.
- The proposal template per rung.

## Rules
- A proposal that does not match a rung is rejected by the AI and escalated to the founder.
- Pricing below the floor is allowed only with founder approval, logged in the approval log.
- No new offer enters the ladder until it has produced two paid deliveries.
- An offer that fails to produce paid revenue for two quarters drops off the ladder.

## Metrics
- Number of deals per rung per quarter.
- Average deal size per rung.
- Win rate per rung.
- Time from lead to paid per rung.

## Evidence
- Pipeline tracker tagged by rung.
- Proposal files in `sales/proposal_notes/` tagged by rung.
- Cash collected ledger tagged by rung.

## The Five Rungs

### 1. Signal Sample — free
- **For:** Cold prospects who have not yet engaged.
- **What they get:** A one-page customised data signal sample for their company or sector.
- **Cost to deliver:** ~2 hours of founder + AI.
- **Qualification:** Real company, real email, real interest. No mass-sample requests.
- **Goal:** Get a reply, learn what they actually want, move to Revenue Sprint.

### 2. Revenue Sprint — 499 SAR
- **For:** Prospects who replied to the Signal Sample and want a deeper look.
- **What they get:** A seven-day diagnostic and revenue-intelligence report on their pipeline, scored against the Dealix data model.
- **Cost to deliver:** ~1 day founder + AI.
- **Qualification:** Confirmed company, confirmed buyer, paid up front.
- **Goal:** Prove the value of the data, sell a Data Pack or Managed Ops.

### 3. Data Pack — 1,500 SAR
- **For:** Customers who completed a Revenue Sprint and need ongoing data.
- **What they get:** A productised, sector-specific data pack with quarterly refresh.
- **Cost to deliver:** ~3 days quarterly.
- **Qualification:** Paying customer of the Revenue Sprint.
- **Goal:** Establish ongoing revenue, prove retention.

### 4. Managed Ops — 2,999–4,999 SAR / month
- **For:** Customers who need Dealix to run a piece of their revenue operation.
- **What they get:** A monthly retainer where Dealix runs an outbound, intelligence, or ops loop on their behalf.
- **Cost to deliver:** ~3 days/month founder + AI.
- **Qualification:** Paid two months of Data Pack, or one Revenue Sprint plus founder review.
- **Goal:** Build the MRR base, prove the operating model.

### 5. Dealix OS / Custom AI — 5,000–25,000 SAR / month
- **For:** Customers who want a piece of Dealix Company OS embedded in their business.
- **What they get:** A custom AI operating layer, agent workflows, or data infrastructure built and managed by Dealix.
- **Cost to deliver:** ~10 days delivery + 3 days/month maintenance.
- **Qualification:** Paying Managed Ops customer for 3+ months, or strategic enterprise referral.
- **Goal:** Build long-term enterprise revenue.

## Qualification Rule

A lead enters the ladder at the lowest rung that matches their declared intent and capacity. Movement up the ladder requires evidence at the current rung (payment, satisfaction signal, or explicit request for the next rung).

## Last Reviewed
2026-05-23
