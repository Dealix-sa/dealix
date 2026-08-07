# FOUNDER ONLY ACTIONS

## Cannot Be Automated (Require Human Judgment or Legal Authority)

### Legal & Compliance
| # | Action | Why Founder-Only | Urgency | Evidence Needed |
|---|--------|-----------------|---------|----------------|
| F1 | **Legal review of DPA** (`docs/DPA_DEALIX_FULL.md`) | Requires qualified Saudi legal counsel to validate PDPL compliance | Before first paid customer | Lawyer sign-off |
| F2 | **Legal review of Terms of Service** | Must be reviewed by Saudi lawyer for enforceability | Before public launch | Lawyer sign-off |
| F3 | **ZATCA registration for e-invoicing** | Government registration required; cannot be automated | Before first invoice | Registration certificate |
| F4 | **Moyasar live account activation** | Financial KYC + bank account linking | Before first payment | Live Moyasar dashboard |
| F5 | **Commercial registration (SAGIA/MISA)** | Government process | For enterprise sales | CR certificate |

### Business Operations
| # | Action | Why Founder-Only | Urgency | Evidence Needed |
|---|--------|-----------------|---------|----------------|
| F6 | **First paid pilot customer** | Requires personal relationship + negotiation | Day 1-3 | Signed agreement + payment |
| F7 | **Warm intro sending** (LinkedIn/WhatsApp/Email) | Personal network; no automated cold outreach | Daily | Conversation screenshots |
| F8 | **Pricing approval in SAR** | Founder sets final price bands | Before proposals | Approved pricing sheet |
| F9 | **Backup restore drill** | Must verify DR actually works | Week 1 | Recovery time log |
| F10 | **14-day uptime proof** | Requires production environment running | Week 2 | Uptime monitoring dashboard |
| F11 | **Domain/DNS ownership verification** | `dealix.me` registrar access | Before go-live | WHOIS verification |
| F12 | **HubSpot production connection** | Live CRM with real customer data | First customer | HubSpot sync log |

### Technical Decisions
| # | Action | Why Founder-Only | Urgency | Evidence Needed |
|---|--------|-----------------|---------|----------------|
| F13 | **Decide: keep `apps/web/` or deprecate** | Product decision on frontend strategy | Before Phase 1 fix | Decision documented |
| F14 | **Approve CI workflow reduction** | 60 workflows → ~15 may remove founder favorites | Before CI stabilization | Approved workflow list |
| F15 | **LLM provider priority order** | Cost/quality tradeoff per provider | Before scaling | Provider cost analysis |

## What Kimi CAN Do (In Scope)
- ✅ Fix `frontend/` vs `apps/web/` consolidation (code level)
- ✅ Stabilize CI workflows (mark optional vs required)
- ✅ Create ENVIRONMENT_CONTRACT.md
- ✅ Run all verification commands and document results
- ✅ Fix broken imports, syntax errors
- ✅ Document which workflows are safe to disable
- ✅ Create canonical doc index with duplication map
- ✅ Run `make env-check`, `make security-smoke`, `make api-contract-check`
- ✅ Verify Python compileall passes
- ✅ Verify frontend builds
- ✅ Create PR with all changes
