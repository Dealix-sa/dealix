# Dealix Company OS Scorecard

The single page that tells the founder, in 30 seconds, whether the company is operating or just existing. Updated every Friday after the Weekly Intelligence Review.

## Purpose
Show the live operational state of every system in Dealix Company OS — what is ready, what needs fixing, what is failing — with the evidence that supports each score and the verifier that proves it. Used as the entry point for the Weekly CEO Review.

## Owner
Sami (Founder).

## Review Cadence
Weekly, every Friday before 18:00 Riyadh time. Re-scored monthly against doctrine.

## Inputs
- Output of every `verify_*.py` script.
- The pipeline tracker (private ops).
- The approval log (private ops).
- The weekly intelligence review.
- The friction log.

## Outputs
- The scorecard table below.
- The single "Next Action" per system, owned by the founder.
- The list of systems that moved up or down this week.

## Rules
- Every system has exactly one score (0–100).
- Every score has at least one piece of evidence linked.
- Every score has a verifier that proves it.
- A system without evidence cannot exceed 60.
- A system without a verifier cannot exceed 70.
- Only paid customer evidence justifies a score above 90.

## Metrics
- Average score across all systems.
- Count of systems at PASS (>=85).
- Count of systems at FIX (<70).
- Week-over-week delta.

## Evidence
- This file, with the date in the table footer.
- Linked verifier outputs in `scripts/`.
- Linked private ops files for revenue, delivery, trust.

## Scorecard

| System | Score | Status | Evidence | Verification | Next Action |
|---|---:|---|---|---|---|
| Founder OS | 60 | FIX | docs/founder/* | verify_document_quality.py | Run daily brief for 5 days |
| Strategy OS | 65 | FIX | docs/strategy/* | verify_document_quality.py | Lock offer ladder |
| Revenue OS | 55 | FIX | docs/revenue/OFFER_LADDER.md | verify_company_os_deep.py | Add 25 leads, send 25 DMs |
| Acquisition OS | 50 | FIX | docs/acquisition/* | verify_document_quality.py | First 25 outreach attempts |
| Sales OS | 60 | FIX | docs/sales/* | verify_document_quality.py | Send 1 proposal |
| Delivery OS | 65 | FIX | docs/delivery/* | verify_company_os_deep.py | Prepare 3 samples |
| Trust OS | 70 | READY INTERNAL | docs/trust/* | verify_company_os_deep.py | Log first 10 approvals |
| Finance OS | 50 | FIX | docs/finance/* | verify_document_quality.py | Set up MRR tracker |
| Client Success OS | 50 | FIX | docs/client_success/* | verify_document_quality.py | Define handover ritual |
| Product OS | 60 | FIX | docs/product/* | verify_document_quality.py | Lock v1 surface |
| Content OS | 55 | FIX | docs/content/* | verify_document_quality.py | Publish 1 sector report |
| Learning OS | 55 | FIX | docs/learning/WEEKLY_INTELLIGENCE_REVIEW.md | verify_company_os_deep.py | Write first review |
| People OS | 50 | FIX | docs/people/* | verify_document_quality.py | Define founder role |
| Agents OS | 55 | FIX | docs/agents/* | verify_document_quality.py | Lock 3 agent contracts |
| AI Management OS | 60 | FIX | docs/ai_management/* | verify_document_quality.py | Define autonomy ladder |
| Control Plane OS | 60 | FIX | docs/control_plane/* | verify_document_quality.py | Wire daily brief |
| Ops OS | 65 | FIX | docs/ops/* | verify_document_quality.py | Lock 7 daily rituals |

## Status legend
- **PASS** (≥85): system is operating with paid customer evidence.
- **READY INTERNAL** (70–84): system is operating internally, no paid evidence yet.
- **FIX** (<70): system is not yet operational. Highest-priority systems take precedence.

## Last Updated
2026-05-23

## Last Reviewed
2026-05-23
