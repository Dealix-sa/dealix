# Revenue Sprint — Delivery Playbook

> The exact day-by-day execution plan for every Sprint.
> Deviation = log it in `clients/{client}/delivery_notes.md` (private).

## Day 0 — Kickoff (≤ 2 hr)

- Payment received → confirm in `revenue/cash_collected.csv`
- Send kickoff message + 30-min kickoff call invite
- Open workspace: `clients/{client_name}/` (private repo) using `_template/`
- Founder fills `CLIENT_INTAKE.md` from kickoff call notes

## Day 1 — Scope Lock + Sector Setup (≤ 4 hr)

- Confirm scope matches `OFFER.md` (no scope drift)
- Pull sector playbook from `docs/acquisition/SECTOR_PLAYBOOKS.md`
- Set up scored prospect template (50 rows target)
- Identify enrichment sources (allow-listed only)
- Confirm trust posture (suppression, claim_guard active)

## Days 2–3 — Prospect Sourcing + Scoring (≤ 8 hr)

- Source 80 candidates from allow-listed channels
- Run scoring agent → rank by fit score
- Filter to top 50 (≥ 60 fit score)
- Enrich each: company size, sector role, buyer name + role, trigger signal
- Manual QA spot-check on 5 random rows

## Day 4 — Message Drafts (≤ 4 hr)

- Pull sector message patterns from `SECTOR_PLAYBOOKS.md`
- Draft 3 variants in Arabic + 3 in English (same intent, different framings)
- Add personalization slots for the prospect's trigger signal
- Run `claim_guard.py` on each draft → fix any flags
- Founder reviews + approves

## Day 5 — Objection Responses + Evidence Pack (≤ 4 hr)

- Identify top 3 objections this sector typically raises (from playbook + intake)
- Draft 2 framings each (Arabic + English) — total 12 responses
- Build evidence pack:
  - Sources used (URLs + access dates)
  - Methodology (one page)
  - Exclusions + sanitization notes
  - Sample sanitization examples

## Day 6 — QA + Handoff Prep (≤ 4 hr)

- Run `QA_CHECKLIST.md` end-to-end
- Fix any QA fails
- Assemble handoff PDF + working files
- Schedule 30-min handoff call for Day 7

## Day 7 — Handoff Call + Capture (≤ 2 hr)

- 30-min walkthrough call with client
- Hand over PDF + working files
- Ask for feedback (live, captured)
- Discuss upsell path (Data Pack or Managed Ops) — soft, no pressure
- Fill `CASE_STUDY_CAPTURE.md` for future case study (sanitization required)
- Move pipeline stage to `delivered`

## Total Founder Hours

~28 hours across 7 days → ~4 hr/day average → fits 2 simultaneous Sprints (8 hr/day) if needed.

## Roles

- **Founder:** scope, approvals, QA, handoff call
- **Agents:** scoring, enrichment, draft (per approval matrix)
- **Contractor (if any):** sourcing volume, never approvals

## Approvals Required Within The Sprint

- Outreach drafts: A1 (founder per batch)
- Sample artifacts shared with client: A2 (founder per send)
- Any public claim derived from this sprint: A3 (founder + evidence)
- Sharing this client's data anywhere: A4 (prohibited without explicit consent)

## Risk Flags To Catch Early

- Client wants to expand scope mid-Sprint → "Yes, that's the next rung. Let's complete this and discuss."
- Client wants us to send on their behalf → "Sprint is hand-off. Sending is a Managed Ops feature."
- Client shares restricted data → store in private workspace only, never in public repo
- Founder bandwidth tight → consider declining new Sprint until current finishes

## Done Definition

Sprint is "done" when:
- 5 deliverables shipped
- Evidence pack approved
- Handoff call completed
- Client feedback captured
- Case study draft started (even if not yet shareable)
- Pipeline updated to `delivered`
- Cash recognized in `revenue/cash_collected.csv`

## When Things Go Wrong

- L1 (< 24 hr late): apologize in handoff, no refund
- L2 (> 24 hr late or partial): pro-rated refund per `BILLING_POLICY.md`
- L3 (failed scope or trust incident): full refund + post-mortem + offer pause

Every miss → root cause in `clients/{client}/delivery_misses.md` and aggregated to `learning/`.
