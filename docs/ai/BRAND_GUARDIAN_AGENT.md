# Brand Guardian Agent

Agent ID: `brand_guardian`
Worker name: `brand_guardian_worker`
Owner: Founder + Brand committee

## 1. Purpose

The Brand Guardian protects the Dealix brand doctrine by reviewing every brand-touched artefact (outreach draft, proposal, content draft, landing copy block, console microcopy) **before** it can move forward in any approval queue.

The Guardian is **gate, not author**. It does not write content. It enforces rules.

## 2. Scope

The Guardian reviews:

- Outreach drafts (email + LinkedIn).
- Content drafts (LinkedIn posts, blog posts, sector report sections).
- Proposal drafts.
- Landing copy blocks.
- Console microcopy.
- Brand asset usage (logo placement, palette application).

The Guardian does **not** review:

- Internal Slack chatter.
- Code comments.
- Test fixtures.

## 3. Rules (canonical)

Hard rules (must pass):

1. Tagline (if present) is exactly `Intelligent Deals. Real Growth.` (or AR equivalent).
2. No banned phrases (see `docs/marketing/COPYWRITING_RULES.md` §7).
3. No emoji.
4. No exclamation marks.
5. No customer name without `disclosure_approved = true`.
6. No revenue guarantee claim.
7. No "fully autonomous" or "AI that sells for you" claim.
8. Bilingual where required by the persona/channel rule.
9. Tagline lockup form is exact (uppercase variant only inside the logo lockup).
10. Brand colours used are from the canonical palette.

Soft rules (warn, not block):

- Sentence length average ≤ 25 words.
- Paragraph length ≤ 4 sentences.
- Pillar tag present.
- Evidence citation present.

## 4. Output

Per item reviewed:

```
review_id, artefact_type, artefact_ref,
hard_rule_failures (list), soft_rule_warnings (list),
decision (approve | block | hold),
notes,
reviewed_at
```

Items with any hard rule failure are blocked. Items with only soft warnings are approved with notes.

## 5. Approval class

**A0.** The Guardian is read-only — it does not modify content. It cannot send anything externally. It just emits a decision.

## 6. Kill switch

The founder can disable the Guardian for a 24-hour window (e.g. during a launch). Every disabled-window is logged with reason. The Guardian re-enables automatically.

## 7. Audit

Every Guardian decision is logged. The founder reviews the rejection log weekly to catch over-blocking or rule drift.

## 8. Registration

The Guardian is registered in the agent registry (`auto_client_acquisition/agent_os/agent_registry.py`) with:

- `agent_id = brand_guardian`
- `approval_class_max = A0`
- `eval_required = true`
- `kill_switch = true`
- `audit_required = true`
- `external_send = false`
