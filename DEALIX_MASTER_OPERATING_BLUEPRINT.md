# Dealix Master Operating Blueprint

## Purpose
The single source of truth that integrates every operating system at Dealix into one coherent map. If a document or script claims to be authoritative and isn't referenced here, it is not authoritative.

## The 10 Operating Systems
1. **Security, Reliability, Supply Chain OS** — `docs/security/SECURITY_RELIABILITY_SUPPLY_CHAIN_OS.md`
2. **Company Data Architecture** — `docs/data/COMPANY_DATA_ARCHITECTURE.md`
3. **Executive Control Plane** — `docs/control_plane/EXECUTIVE_CONTROL_PLANE.md`
4. **Revenue Operations Playbook** — `docs/revenue/REVENUE_OPERATIONS_PLAYBOOK.md`
5. **Delivery & Client Success OS** — `docs/client_success/DELIVERY_CLIENT_SUCCESS_OS.md`
6. **Finance, Pricing, Capital OS** — `docs/finance/FINANCE_PRICING_CAPITAL_OS.md`
7. **Trust, Compliance, AI Risk OS** — `docs/trust/TRUST_COMPLIANCE_AI_RISK_OS.md`
8. **Brand, Proof, Content OS** — `docs/content/BRAND_PROOF_CONTENT_OS.md`
9. **Productization & Engineering OS** — `docs/product/PRODUCTIZATION_ENGINEERING_OS.md`
10. **People, Delegation, Partner OS** — `docs/people/PEOPLE_DELEGATION_PARTNER_OS.md`

## The 11 non-negotiables
1. Founder-led sales motion. No cold automated outreach.
2. Public/private boundary respected at all times.
3. No PII or customer data in the public repo.
4. Dual logging: every revenue action lands in the action log AND the capital asset ledger.
5. Trust approval required for any external claim.
6. No backwards-compatibility hacks: change the code, don't shim it.
7. No overclaim in content or proposals.
8. Sprint verifiers must pass before commit.
9. Bad revenue is filtered out before it reaches pipeline.
10. AI risk register reviewed weekly until first paying customer.
11. Restore drill quarterly; access review monthly.

## Operating cadence
- **Daily** (15 min): `make mission-control`, `make ceo-action-queue`, top one action.
- **Weekly** (60 min): `make ceo-weekly`, `make weekly-close`, `make business-score`, `make assurance`.
- **Monthly**: access review, restore drill window, pricing review.

## The 5-rung productized ladder
1. **Free Diagnostic** — under 30 min, produces a one-page snapshot.
2. **499 SAR Sprint** — 7-day Revenue Intelligence Sprint.
3. **1,500 SAR Data Pack** — sector data pack with proof attachments.
4. **2,999–4,999 SAR/mo Managed Ops** — recurring revenue ops retainer.
5. **5K–25K SAR Custom AI** — bespoke build, gated by SaaS readiness.

## Decision authorities
- **Founder**: pricing, hiring, public claims, anything > 5,000 SAR/mo recurring spend, anything that ships externally.
- **Delivery sub-agent**: per-customer sprint execution, no external messages.
- **Sales sub-agent**: lead qualification, proposal drafts, never sends external messages.
- **Engineer sub-agent**: code, tests, migrations.
- **Content sub-agent**: bilingual docs, SOPs, proposal templates.

## Reference maps
- **Integration map**: `DEALIX_INTEGRATION_MAP.md`
- **Final repo tree**: `DEALIX_FINAL_REPO_TREE.md`
- **System completion matrix**: `DEALIX_SYSTEM_COMPLETION_MATRIX.md`
- **Execution roadmap**: `DEALIX_EXECUTION_ROADMAP_FINAL.md`
- **Definition of done**: `DEALIX_DEFINITION_OF_DONE.md`
- **Implementation sprint pack**: `DEALIX_IMPLEMENTATION_SPRINT_PACK.md`

## Verification
- `python scripts/verify_master_operating_blueprint.py`
- `python scripts/verify_implementation_sprint_pack.py`
- `make implementation-check`
