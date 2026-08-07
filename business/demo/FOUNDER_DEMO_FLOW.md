# Founder Demo Flow — Internal Reference

Step-by-step the founder follows during a live demo.

## Before the call
1. Open `/command-center` in tab 1.
2. Open `/revenue-machine` in tab 2.
3. Open `/daily-draft` in tab 3.
4. Open `/proof-vault` in tab 4.
5. Open `/enterprise-readiness` in tab 5.
6. Have `LIVE_WORKFLOW_REVIEW_SCRIPT.md` open on second screen.

## During the call
- Speak the Arabic script if the buyer is Arabic-first, English otherwise.
- After every section, ask: "هل هذا قريب من تحديكم اليوم؟" / "Does this match a real friction you're hitting?"
- If yes, drill into the specific friction; pivot to the workflow review offer.
- If no, pivot to a different OS module.

## After the call
- Score the lead in `business/_data/scored_leads.json` via `scripts/score_leads.py`.
- Generate a follow-up using `scripts/generate_followup_queue.py`.
- Generate a tailored proposal using `scripts/generate_proposal.py`.
- Schedule the workflow review.

## Anti-patterns
- Do not promise outcomes. Promise the diagnostic sprint produces a written artifact.
- Do not improvise pricing. Read from `/pricing`.
- Do not skip the governance pillar even if the buyer doesn't ask — it's the differentiator.
