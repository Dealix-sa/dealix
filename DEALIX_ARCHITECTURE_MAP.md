# Dealix Architecture Map

> Owner: Founder. Verify: `scripts/verify_architecture.py`.

How the Master Tree composes into a working system.

```
[ Founder ]
    |
    v
[ docs/founder/ ]  ---->  daily brief, decision queue, weekly review
    |
    v
[ control_plane/ ] -----> company_state -> ceo_brief -> decision_engine
    |                                                       |
    |                                                       v
    |                                              [ approval_router ]
    |                                                       |
    |                                                       v
    |                                              [ action_router ]
    v
[ operating_intelligence/ ] -> priority, bottlenecks, opportunities,
                               weekly + monthly synthesis
    |
    v
[ dealix/agents/ ] -> founder_brief, lead_finder, scoring, message,
                      proposal, delivery_report, qa, trust_guard,
                      content, finance_watch, client_success, learning
    |
    v
[ dealix/workflows/ ] -> daily_ceo_brief, daily_lead_discovery,
                         lead_scoring_batch, founder_outreach_queue,
                         sample_pack_generation, proposal_generation,
                         payment_verification, delivery_report_generation,
                         case_study_generation, weekly_ceo_review,
                         monthly_strategy_review
    |
    v
[ dealix/trust/ ]  + [ dealix/registers/ ] enforce: approval_matrix,
                     autonomy_policy, claim_guard, suppression,
                     data_retention, evidence_pack, public_safety,
                     audit, incident_response, policy_engine
    |
    v
[ api/ + db/ + integrations/ ] - public surfaces and external systems
    |
    v
[ landing/ + apps/web/ ] - public proof, demand capture
```

## Boundaries

- **Public repo:** code, docs, trust, CI, verification, demos, evals,
  landing, apps/web, control-plane scaffolding.
- **Private repo:** real customer data, leads, payments, decisions,
  approvals, prompts with sensitive content, contractor notes, capital
  plans.

The boundary is enforced by `scripts/verify_public_safety.py` and
`scripts/verify_private_boundary.py`.

## Required Checks for `main`

- `ci` (the workflow at `.github/workflows/ci.yml`)
- `dealix-control` (`dealix-control.yml`)
- `dealix-full-ops` (`dealix-full-ops.yml`)
- `dealix-company-os` (`dealix-company-os.yml`)
- `security` (`security.yml`)
- `scorecard` (`scorecard.yml`)
