# Ultimate Trust Plane

The Trust Plane is the collection of files + endpoints that, together,
ensure no AI agent in Dealix can act outside founder control.

| Concern | Where it lives |
|---|---|
| Policy classes + rules | `policies/dealix_control_policy.yaml` |
| Runtime evaluation | `api/internal/policy_adapter.py` |
| Approval queue (drafts) | `<private_ops>/approvals/approval_queue.csv` |
| Decision log (audit) | `<private_ops>/trust/approval_decisions.csv` |
| Trust flags | `<private_ops>/trust/trust_flags.csv` |
| Incidents | `<private_ops>/trust/incidents.csv` |
| Founder view | `apps/web/app/trust/page.tsx`, `apps/web/app/audit/page.tsx` |
| Internal API | `POST /api/v1/internal/approvals/{id}/{approve|reject|request-edit|escalate}` |

## Lifecycle of an external-impact action

1. Agent drafts → row inserted in `approval_queue.csv` with policy class.
2. Founder views the row in `/approvals`.
3. Founder clicks Approve / Reject / Edit / Escalate.
4. Decision recorded in `approval_decisions.csv` via the internal API.
5. A deterministic worker picks up approved rows and queues the actual
   external action (still gated by per-channel safety, e.g. suppression
   list checks).

Escalations also add a row in `incidents.csv` so the founder has a
clear "what's open?" view in `/trust`.
