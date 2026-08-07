# Proposal Template

> **Status:** Default template. The proposal is a document, not a deck.
> **Pricing policy:** see `docs/offers/PRICING_LOGIC_AND_APPROVAL_POLICY_AR.md`.
> **Schema:** `schemas/launch/proposal_pack.schema.json`.

## The structure (12 sections, max 6 pages)

### 1. Client context (½ page)

- Client name.
- Industry + city.
- Decision makers (with roles).
- The discovery call date(s).
- The pain statement (in the client's words).

### 2. Problem (1 page)

- What we heard.
- What we observed in the data (audit findings if applicable).
- The cost of inaction (the 12-month cost of doing nothing).
- The urgency (why now).

### 3. Current leakage (1 page)

- 3–5 specific leaks we found.
- Each leak has: where it is, how often, what it costs, who owns the fix.
- Format: table.

### 4. Proposed system (1 page)

- The offer (which one from the ladder).
- What it includes.
- What it does NOT include.
- The expected outcome (1 sentence).
- The proof metric (how we measure success).

### 5. Scope (½ page)

- Timeline.
- Phases (week-by-week).
- Deliverables.
- Required access.

### 6. Out of scope (¼ page)

- The 3–5 things we explicitly do not do.
- Cold WhatsApp.
- Auto-reply.
- Final pricing commitment.
- Replacement of CRM / ERP.

### 7. Assumptions (¼ page)

- The 3–5 assumptions we are making.
- Each one: "If this is false, we re-scope."

### 8. Responsibilities (½ page)

- What the client does.
- What Dealix does.
- What neither does.

### 9. Success metrics (½ page)

- The proof metric.
- The secondary metrics.
- How we report (weekly, monthly).
- What happens at end of pilot.

### 10. Risks (½ page)

- The 3–5 risks.
- Each one: likelihood, impact, mitigation.
- Format: table.

### 11. Pricing (¼ page, in `pricing_status: draft_only` mode)

- `pricing_status: draft_only` (or `approved_range_required` / `founder_approval_required`).
- If range: the SAR range, with note: "Final price set at founder approval."
- The payment handoff policy (no link, no auto-send, founder-approved handoff).

### 12. Next step (¼ page)

- The action: sign the proposal + consent record + book kickoff.
- The date: specific.
- The person: named.
- The escalation: what if they delay.

## The hard rules

1. **Never put a final price** without founder sign-off.
2. **Never include a payment link** in the proposal.
3. **Never promise specific outcomes** (use proof metrics).
4. **Never include fake case studies** (real ones only, with permission).
5. **Never use banned words** ("guaranteed", "100%", "always", "best", "transformative").
6. **Always carry `evidence_level`** for every claim.
7. **Always carry `risk_level`** for the engagement.
8. **Always include a kill criterion** (what makes the engagement fail).

## The 5 sections to spend the most time on

1. **Problem** — if the buyer doesn't feel the pain, nothing else matters.
2. **Current leakage** — this is the proof. Make it specific.
3. **Proposed system** — the offer, in the buyer's language.
4. **Success metrics** — the proof metric. Without it, the pilot is a hope.
5. **Pricing** — the founder signs this last. Do not send without sign-off.

## The follow-up after the proposal is sent

- Day 1: 1-sentence acknowledgement: "تم الإرسال. متى تقدر تراجعه؟"
- Day 3: ask for the decision date: "متى نقدر نحجز قرار؟"
- Day 7: re-cap the value: "بناءً على المشكلة اللي ناقشناها، هذا اللي راح نحققه."
- Day 14: breakup: "لو ما في رد خلال أسبوع، أحذف العرض من عندك. لو احتجتني بعد 60 يوم، اعمل reply."

## The format

Markdown source → PDF (using `scripts/proposal_pack_dry_run.py`). The script:

- Reads the JSON proposal pack.
- Validates against the schema.
- Renders to Markdown.
- Optionally converts to PDF (requires pandoc — optional).

The PDF is the deliverable. The Markdown is the source for review.

## When to update

- After 5 proposals: if signature rate < 30%, the problem section is weak.
- After 10 proposals: if scope-creep rate > 30%, the scope section is unclear.
- After 20 proposals: if pilot-to-renewal < 30%, the success metric is wrong.
