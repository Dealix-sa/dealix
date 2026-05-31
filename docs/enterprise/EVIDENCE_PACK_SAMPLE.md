# Evidence Pack — Sample

Every delivered offer ships with an evidence pack that the customer can
audit. The pack is assembled from real artifacts produced during
delivery — no marketing-only material.

## Contents

1. **Scope intake summary** — what we agreed to deliver, what we did
   not, and the boundaries we will not cross.
2. **Agent + tool inventory** — which agents touched the workspace,
   which tools they were allowed to call, and the lifecycle stage of
   each at the time of delivery.
3. **Approval log** — every action that went through
   `dealix.governance.approvals.ApprovalGate`, with timestamps,
   decision, and approver.
4. **Provenance map** — for any deliverable that draws on external
   data, the source trust level and sanitization status.
5. **Quality checklist** — the run of the
   `dealix.hermes.delivery.quality_checklists.run_quality_checklist`
   against the offer's playbook (see
   [`dealix/hermes/delivery/`](../../dealix/hermes/delivery/)).
6. **Outcome reconciliation** — verified-revenue events tied to the
   engagement, with attribution breakdown.
7. **Risk register** — open and closed risks identified during the
   engagement, with mitigation status.
8. **Sign-off** — counter-signed by the workspace owner and the
   founder, with the next-review date.

## Quality gates (offer-specific)

The quality gates below are taken directly from
[`dealix/hermes/delivery/ai_trust_kit_delivery.py`](../../dealix/hermes/delivery/ai_trust_kit_delivery.py):

- `no_overclaim`
- `data_scope_defined`
- `approval_flow_documented`
- `risk_register_signed_off`

A gate failure blocks delivery; the playbook step is reopened until the
gate passes.
