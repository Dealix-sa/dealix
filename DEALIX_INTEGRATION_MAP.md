# Dealix Integration Map

How the 10 operating systems wire into one machine.

## Signal flow

```
[ICP filter] -> [Lead sourcing] -> [Qualification score] -> [Outbound cadence]
   |                                                          |
   v                                                          v
[Sample ops] -> [Proposal] -> [Payment path] -> [Delivery] -> [QA] -> [Handoff]
                                                  |              |
                                                  v              v
                                          [Client health] -> [Retention/Retainer]
                                                  |              |
                                                  v              v
                                          [Evidence ledger] -> [Capital asset register]
                                                  |              |
                                                  v              v
                                          [Business score] -> [Control tower brief]
                                                                |
                                                                v
                                          [CEO mission control / action queue]
```

## OS-to-OS dependencies
| Upstream OS | Downstream OS | What flows |
|---|---|---|
| Security, Reliability, Supply Chain | All | Boundary + secret hygiene |
| Company Data Architecture | All | Schemas + private ops contracts |
| Executive Control Plane | Founder | Mission control, action queue, score |
| Revenue Ops | Delivery + CS | Qualified opportunities, proposal, paid contract |
| Delivery + CS | Finance + Content | Paid revenue, proof artifacts |
| Finance + Trust | All | Pricing, approvals, claim governance |
| Brand, Proof, Content | Revenue Ops | Proof library, claim-safe outreach copy |
| Productization + Engineering | Delivery + CS | Repeatable workflows -> templates -> SaaS gate |
| People + Partners | All | Delegation ladder, contractor access, referrals |

## Data flow boundaries
- **Public repo**: docs, scripts, schemas, templates.
- **Private ops** (`dealix-ops-private/`): CSVs, client folders, drafts, evidence.
- **Generated artifacts**: written into private ops by scripts; never committed to the public repo.

## Verifier-to-sprint mapping
| Sprint | Verifier(s) |
|---|---|
| 0 | `verify_security_reliability_os.py`, `verify_public_safety_v2.py`, `verify_data_boundary.py` |
| 1 | `verify_master_operating_blueprint.py` |
| 2 | `verify_company_data_architecture.py` |
| 3 | (covered by Makefile `mission-control`/`assurance` targets) |
| 4 | `verify_revenue_operations_playbook.py` |
| 5 | `verify_delivery_client_success_os.py` |
| 6 | `verify_finance_pricing_os.py`, `verify_trust_ai_risk_os.py` |
| 7 | `verify_brand_proof_content_os.py` |
| 8 | `verify_productization_engineering_os.py`, `verify_people_partner_os.py` |
| ALL | `verify_implementation_sprint_pack.py` |

## Single command
```
make implementation-check
```
Runs the integrated verifier chain in one shot.
