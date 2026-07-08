# Dealix Launch Conversation & Negotiation Engine

Draft-only, approval-first engine that turns targets into scored opportunities,
matched offers, multi-channel message drafts, objection responses, negotiation
plans, proof packs, an approval queue, follow-ups, and a daily command report.

**Nothing is ever sent. The founder approves every external message.**

---

## Why this exists

Dealix is not a CRM and not a dashboard. It is an AI-native operating system for
Saudi B2B companies that answers, every day:

- Who do we target today, and why?
- What offer fits this client?
- What message fits each channel?
- How do we answer objections and negotiate?
- How do we prove value without inventing results?
- What needs founder approval, and what happens next?

This engine is the conversation + negotiation layer that produces those answers
as reviewable drafts.

---

## Pipeline

```
safety guard → company brain → target scoring → offer matching →
message generation → objection handling → negotiation planning →
proof building → approval queue → follow-up planning → learning loop
```

Every stage is a small stdlib-only module under `dealix/conversation_engine/`.

| Module | Responsibility |
|---|---|
| `safety_guard.py` | Blocks the run if any send/auto/production flag is enabled |
| `company_brain.py` | Loads founder profile, offers, personas, objections, channels, proof rules |
| `target_profile.py` | Scores targets (0–100) from signals + persona overlap → hot/warm/cold |
| `offer_matcher.py` | Picks the best-fit offer(s) from the 6-offer ladder |
| `message_generator.py` | Builds email / WhatsApp / LinkedIn / call drafts |
| `channel_adapter.py` | Channel names, approval rules, CSV flattening |
| `objection_handler.py` | Structured responses from the objection bank |
| `negotiation_planner.py` | Per-target negotiation plan + concession rules |
| `proof_builder.py` | Proof pack + forbidden-claim validation |
| `approval_policy.py` | Turns every external action into a pending approval item |
| `followup_planner.py` | Conservative, permission-based follow-up cadence |
| `learning_loop.py` | Self-improvement suggestions for the next run |
| `engine.py` | Orchestrates the full pipeline into one JSON payload |

---

## How the system chooses a client

`target_profile.score_target` weights buying signals (lost follow-up, leaking
leads, weak follow-up, market entry, enterprise readiness, …) and adds a bonus
when signals overlap the target's persona pains. Score bands:

- `hot` ≥ 70 · `warm` ≥ 45 · `cold` otherwise

`offer_matcher.match_offer` then ranks offers by how many of their `fit_signals`
overlap the target's signals, plus a persona-preference bonus.

## How it generates messages

Each message is **pain-hypothesis-based**, permission-first, has a clear CTA,
uses the canonical founder email, and never claims guaranteed results. General
filler like "we help you with AI" is not produced — every draft is built from
target segment → pain hypothesis → offer match → proof angle → CTA.

## How it negotiates

`negotiation_planner.build_plan` produces a starting position, minimum
commitment (a small pilot), likely objections with responses, and concession
rules that **never drop price first**: reduce scope, start with a pilot, ask for
proof permission, tie payment to a clear deliverable.

## How it proves value

`proof_builder.build_proof_pack` assembles a 10-part proof pack and validates it
against the forbidden-claims list. It measures things like qualified
opportunities, follow-ups created, missed leads detected, time saved — it never
promises revenue or ROI.

## How it avoids spam

- WhatsApp is **warm-only**; cold WhatsApp is forbidden (`cold_send_forbidden`).
- LinkedIn is manual DM after acceptance; no scraping, no automation.
- Every external action lands in the approval queue as `pending_founder_approval`.

## How the founder uses it daily

```bash
python scripts/commercial/run_dealix_launch_conversation_engine.py --mode draft-only --limit 25
python scripts/commercial/verify_dealix_launch_conversation_engine.py
```

Then review `reports/dealix_conversation_negotiation/latest.md` (the daily
command report), approve/revise/reject/hold items in `approval_queue.csv`, and
send approved drafts manually.

## How it becomes SaaS later

The engine is data-driven (`data/dealix_conversation_negotiation/*.json`). Swap
the founder profile, offers, personas, and seed targets per tenant and the same
pipeline runs as a per-client OS behind the MCP Gateway / Tenant Foundation.

---

## Outputs

Generated under `reports/dealix_conversation_negotiation/` (gitignored — never
committed):

- `latest.json` — full payload
- `latest.md` — Daily Launch Command report
- `approval_queue.csv` — every external action, pending founder decision
- `opportunity_graph.csv` — scored opportunities
- `email_drafts.csv` / `whatsapp_drafts.csv` — channel drafts
- `negotiation_playbooks.csv` — per-target negotiation plans
- `proof_pack.md` — proof-of-value packs
- `slack_brief.md` — internal Slack brief draft for the founder (never posted)

## Safety

The engine refuses to run (`BLOCKED_BY_SAFETY_GUARD`) if any of these are
enabled: `EXTERNAL_SEND_ENABLED`, `EMAIL_SEND_ENABLED`, `WHATSAPP_SEND_ENABLED`,
`WHATSAPP_ALLOW_LIVE_SEND`, `SMS_SEND_ENABLED`, `AUTO_WHATSAPP_ENABLED`,
`AUTO_EMAIL_ENABLED`, `AUTO_LINKEDIN_ENABLED`, `AUTO_PAYMENT_CAPTURE_ENABLED`,
`AUTO_MERGE_ENABLED`, `PRODUCTION_MUTATION_ENABLED`, or if `OUTBOUND_MODE` is not
`draft_only`. This aligns with the Dealix Outbound Safety Policy.

The only approved founder email is **sami.assiri11@gmail.com** and it is
hard-enforced in code (`company_brain.CANONICAL_FOUNDER_EMAIL`).
