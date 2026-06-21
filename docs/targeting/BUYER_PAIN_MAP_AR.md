# Buyer Pain Map

> **Status:** Default. Update after the first 5 discovery calls.
> **Companion:** `DECISION_MAKER_PERSONAS_AR.md` · `ICP_SCORING_SYSTEM_AR.md`.

## The 5 daily pains (the ones we sell against)

### 1. Lost follow-ups

- **Symptom:** "We had a great call. Then nothing."
- **Surface:** WhatsApp threads with no reply for 2+ weeks; CRM stages stuck on "Contacted".
- **Cost to the buyer:** lost deals, lost renewals, lost referrals.
- **What Dealix does:** read-only classifier; daily digest of "no movement in 3 / 7 / 14 days".
- **Evidence level:** L2 (we can name the count; we don't promise a fix yet).

### 2. WhatsApp overload

- **Symptom:** "I have 14 unread WhatsApp tabs."
- **Surface:** multiple group chats, multiple 1:1 threads, mixed personal + business.
- **Cost to the buyer:** founder time, response delays, missed signals.
- **What Dealix does:** routing rules, tag taxonomy, daily digest.
- **Evidence level:** L2.

### 3. Reporting black hole

- **Symptom:** "I have no idea what the team did this week."
- **Surface:** no shared dashboard; founder pings each sales rep.
- **Cost to the buyer:** founder time, no pattern detection.
- **What Dealix does:** Command Center (offer 3) with daily digest.
- **Evidence level:** L2.

### 4. Pricing chaos

- **Symptom:** "Every proposal is a new negotiation."
- **Surface:** proposals without scopes; discounts without approval; pricing in chat.
- **Cost to the buyer:** margin erosion, founder-as-bottleneck.
- **What Dealix does:** Proposal & Proof Pack OS (offer 4) with approval queue.
- **Evidence level:** L3 (we have the policy, not yet the proof at scale).

### 5. Onboarding new clients / projects

- **Symptom:** "Every new client feels like starting over."
- **Surface:** no onboarding template; handoff is verbal.
- **Cost to the buyer:** inconsistent delivery, founder rescue missions.
- **What Dealix does:** Client Onboarding Playbook (delivery doc) + AI OS for SMB (offer 5).
- **Evidence level:** L3.

## The pains we explicitly do NOT lead with

| Pain | Why we don't lead with it |
| --- | --- |
| "We have no CRM." | Most have something. The pain is not the tool; it's the discipline. |
| "We need AI." | Buyers don't buy AI; they buy outcomes. AI is the means. |
| "We need to digitize." | Boring, defensive. We sell visibility + decisions, not digitization. |
| "We're losing to bigger agencies." | Often true, but they want to fix the symptom, not the cause. |
| "We need more leads." | Top-of-funnel is a different problem. We solve mid-funnel. |

## How the pain map drives the audit

The audit (`REVENUE_LEAK_AUDIT_OFFER_AR.md`) looks for evidence of these 5 pains in the client's data. The deliverable is 10 specific findings, tagged with which pain they map to.

If a finding does not map to a known pain, it goes in "Other observations" and is not part of the 10.

## How the pain map drives the objection handling

When a prospect says:

- **"We're fine, we have a VA"** → the pain is "WhatsApp overload" + "reporting black hole". Pivot to the gap the VA cannot close.
- **"Our CRM works"** → the pain is "pricing chaos" + "lost follow-ups". Pivot to "the CRM is a tool; the missing layer is decisions."
- **"We don't have time for this"** → the pain is "founder time" + "reporting black hole". Pivot to "the audit takes 5 days, not 5 weeks."

See `OBJECTION_HANDLING_BIBLE_AR.md` for the full list.

## How the pain map drives the content

The 10 content pillars in `FOUNDER_AUTHORITY_CONTENT_SYSTEM_AR.md` are derived from the 5 pains. Each pillar leads with a pain, names it, and points to the next step (the audit or the WhatsApp OS).

## How the pain map evolves

Every 10 discovery calls:

- Add a new pain if the buyer mentioned it 3+ times.
- Drop a pain if the buyer never mentioned it (it may be industry, not universal).
- Re-rank the 5 by frequency.
- Update the audit to look for the new top 3.
