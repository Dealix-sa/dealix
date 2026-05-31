# Sovereignty Model

Every request flowing through Hermes is classified on the S0–S5 scale.

| Level | Name | Examples |
| --- | --- | --- |
| S0 | PUBLIC | GEO pages, public docs, marketing assets |
| S1 | INTERNAL | Drafts, scoring, ICP analysis |
| S2 | SAMI_APPROVAL | Pricing, contracts, brand claims, campaign launches |
| S3 | CUSTOMER_SENSITIVE | Customer deliverables, customer exports, retainer activation |
| S4 | ENTERPRISE_CRITICAL | Public API surfaces, marketplace listings, partner SLAs |
| S5 | SOVEREIGN_LOCKED | Sovereign memory / strategy — never executes |

The sovereignty gate enforces these levels at runtime. Sami is the
only sovereign actor by default; partners and customers can never act
on S3+ without an explicit approval ticket.
