# Founder-only routes

| Route | Purpose | Production gating |
| --- | --- | --- |
| `/crm` | Pipeline view | IdP + RBAC role=founder |
| `/operator` | Daily ops console | IdP + RBAC role=founder |
| `/review-queue` | Draft approvals | IdP + RBAC role=founder |
| `/outreach-lab` | Draft creation | IdP + RBAC role=founder |
| `/followups` | Follow-up queue | IdP + RBAC role=founder |
| `/command-center` | Operating dashboard | IdP + RBAC role=founder |
| `/war-room` | Live ops | IdP + RBAC role=founder |
| `/pipeline` | Revenue forecast | IdP + RBAC role=founder |
| `/kpi-finance` | Finance view | IdP + RBAC role=founder+finance |
| `/deals` | Deal desk | IdP + RBAC role=founder+commercial |
| `/proof-vault` | Proof items | IdP + RBAC role=founder+delivery |
| `/launch` | Launch console | IdP + RBAC role=founder |

Public routes (no gating): `/`, `/ar`, `/brand`, `/offers`, `/pricing`, `/cases`, `/enterprise-readiness`, `/trust-center`, `/safety`, `/book`, `/resources`.
