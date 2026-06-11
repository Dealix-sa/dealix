# Dealix V10-V20 Execution Plan

## Phase ordering

| Phase | Title | Output gate |
| --- | --- | --- |
| V10 | Enterprise release baseline + demo pack + master runner | `dealix_v10_run_all.sh` green, web build green |
| V11 | CRM admin UI + operator UI + review queue + API routes | new pages render, API contracts respond JSON |
| V12 | Quote-to-cash + deal desk + contract templates + payment stubs | quote/deal/invoice scripts run end-to-end |
| V13 | Client portal + delivery workspace + proof rhythm | demo workspace + proof report generated |
| V14 | AI router v2 + prompts + knowledge base + evals | router default deterministic, evals pass |
| V15 | Market intelligence + competitive + pricing power | three briefs generated |
| V16 | Trust center + audit log + approval matrix + security hardening | security_review + audit report pass |
| V17 | Industry landing pages + SEO/content factory + campaigns + partners | campaign + content + partner packs generated |
| V18 | Platformization + module registry + API contract + tenant stubs | module catalog + tenant report generated |
| V19 | Deployment runbook + observability + backup + CI finalization | release guard + ci readiness pass |
| V20 | Launch kit + post-launch OS + final verifier + PR | `dealix_v20_run_all.sh` green, PR opened |

## Universal per-phase contract

1. Add the deliverables for that phase only.
2. Run the phase's master script if it has one, plus `pre_push_guard.py`.
3. `cd apps/web && npm run typecheck && npm run build` if new pages were added.
4. Commit with message `checkpoint: Dealix V<phase> <title>`.
5. Push `feature/dealix-v10-v20-enterprise-commercial-os` to origin.
6. Update `reports/execution/DEALIX_V10_V20_EXECUTION_LOG.md` with `date` + `git log --oneline -5`.

## Safety invariants enforced at every phase

- No secrets committed (`check_no_secrets.py`).
- No auto-send connectors. All outreach drafts queue for human approval.
- Demo data labeled demo at source.
- No fake testimonials, no fake metrics on public-facing pages.
- Payment provider integrations are stubs only; no real charges.
- Production WhatsApp/email require official API + credentials + terms review and remain disabled by default.
- Legal/compliance templates are operational scaffolds, not legal advice.
