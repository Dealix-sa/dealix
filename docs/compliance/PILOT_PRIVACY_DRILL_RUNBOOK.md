# Dealix Pilot Privacy Evidence Drill Runbook

> Status: `draft_only / SYNTHETIC_ONLY / counsel_approval_required`  
> Control issue: `#918`  
> Release posture: `FAIL_CLOSED / NO_REAL_CUSTOMER_DATA / NO_LIVE_SEND / NO_PRODUCTION_MUTATION`

This runbook converts the privacy launch requirements into repeatable evidence drills. It is an internal engineering and governance aid, not legal advice, a compliance certification, or permission to process customer data.

## 1. Hard boundary

Until every applicable gate in `PILOT_PRIVACY_EVIDENCE_LEDGER.csv` has dated evidence and accountable approval:

- use synthetic aliases and disposable non-production tenants only;
- do not import customer CRM exports, contact workbooks, messages, personal prompts, payment records, or support records;
- do not send email, WhatsApp, LinkedIn, SMS, proposals, invoices, or calendar invitations;
- do not change production databases, backups, domains, environment variables, secrets, provider settings, or retention settings;
- do not describe a drill result as legal approval or PDPL compliance.

A status of `blocked` or `counsel_required` is expected and safe. Missing evidence never becomes implicit approval.

## 2. Evidence rules

Every drill record must include:

1. evidence ID from the ledger;
2. UTC execution timestamp;
3. repository commit SHA and application version;
4. environment name and explicit confirmation that it is disposable/non-production;
5. synthetic tenant/contact aliases only;
6. exact test method and expected result;
7. observed result, pass/fail, and exceptions;
8. redacted logs, manifests, hashes, screenshots, or reports;
9. executor and independent reviewer roles;
10. rollback/cleanup confirmation;
11. a link stored in the ledger, never a secret or raw personal record.

No gate may be marked `passed` when `Evidence Link` or `Executed At` is blank.

## 3. Preflight

Before each technical drill:

- confirm the environment is not production;
- create unique synthetic aliases such as `tenant-alpha-test` and `contact-optout-test`;
- verify no fixture resembles a real person, company contact, phone number, email address, payment reference, or customer record;
- capture a baseline manifest and record count;
- confirm audit logging is enabled without secrets or raw message content;
- define cleanup and rollback before execution;
- stop immediately if any real or ambiguous data appears.

## 4. PE-003 — Tenant isolation drill

### Objective

Prove that one tenant cannot read, write, enumerate, export, or act on another tenant's synthetic records.

### Method

1. Create two disposable synthetic tenants with separate users and roles.
2. Create distinguishable synthetic objects for each supported in-scope resource.
3. Verify authorized same-tenant read/write behavior.
4. Attempt cross-tenant access through direct IDs, list filters, exports, search, background jobs, and any admin-like route included in the pilot.
5. Verify every cross-tenant attempt is denied and produces a non-sensitive audit event.
6. Repeat with the lowest and highest non-platform roles.

### Pass criteria

- all authorized same-tenant cases pass;
- every cross-tenant attempt is denied;
- no identifier, count, metadata, or payload from the other tenant leaks;
- audit evidence is tenant-scoped and contains no secret or raw personal data.

### Required evidence

A redacted matrix of route/action, role, expected status, observed status, tenant alias, and log reference.

## 5. PE-004 — Export drill

### Objective

Prove that a tenant-scoped export is complete for the synthetic fixture and contains nothing from another tenant.

### Method

1. Build a fixture manifest for one synthetic tenant.
2. Request the supported export through the intended authenticated path.
3. Compare exported object types and counts to the fixture manifest.
4. Scan the export for the second tenant's aliases and prohibited fields.
5. Hash the export and evidence manifest.
6. Delete the export after review according to the test cleanup plan.

### Pass criteria

- the export matches the fixture manifest;
- no cross-tenant data or secret appears;
- the request and delivery are auditable;
- the temporary export is removed after evidence capture.

## 6. PE-005 — Deletion drill

### Objective

Prove that an approved tenant-scoped deletion removes synthetic data from every documented primary store and queue, with explicit handling for backups and immutable audit evidence.

### Method

1. Record pre-deletion counts and identifiers from the synthetic fixture.
2. Execute the intended deletion workflow.
3. Query every documented primary store, cache, queue, search index, file/object store, and analytics path included in the pilot.
4. Verify background retries cannot recreate the deleted records.
5. Document any immutable audit or legally retained test evidence by category and reason; do not assume an exception.
6. Verify the deletion result after a controlled service restart in the disposable environment.

### Pass criteria

- scoped synthetic records are not retrievable through supported or direct paths;
- no retry or integration recreates them;
- every exception is explicit, minimized, and independently reviewed;
- backup behavior is deferred to PE-008 rather than silently claimed.

## 7. PE-006 — Suppression and opt-out drill

### Objective

Prove that an opted-out synthetic identity cannot re-enter outreach eligibility even after re-import or workflow replay.

### Method

1. Create a synthetic contact with an explicit synthetic opt-in record.
2. record an opt-out/suppression event;
3. attempt re-import from each approved intake path;
4. replay qualification, draft generation, queue processing, and channel eligibility checks;
5. verify the identity remains suppressed across tenant workflows and compatibility exports;
6. verify suppression contains only the minimum stable identifier required for enforcement.

### Pass criteria

- re-import does not remove suppression;
- no draft/send eligibility is produced;
- no external provider call occurs;
- the blocked attempt and reason are auditable.

## 8. PE-007 — Breach-response tabletop

### Objective

Prove that owners can classify, contain, preserve evidence, assess notification duties, and communicate internally without exposing more data.

### Scenario

Use a fictional event involving synthetic tenant data only—for example, a test export becoming accessible to the wrong synthetic tenant.

### Tabletop steps

1. Record detection time and reporter.
2. Assign incident owner and severity using the current internal rubric.
3. Identify affected synthetic systems and data categories.
4. Define containment actions without changing production.
5. Preserve redacted evidence and establish an action log.
6. Determine which contractual, customer, insurer, provider, and regulatory notification decisions require counsel or accountable-owner review.
7. Draft—but do not send—internal and customer notification templates.
8. Record recovery, lessons, owners, and due dates.

### Pass criteria

- ownership and clock are explicit;
- containment and evidence preservation are actionable;
- notification is treated as a decision, not guessed;
- no external message is sent;
- lessons produce tracked remediation.

## 9. PE-008 — Backup, restore, deletion, and suppression interaction

### Objective

Prove that restoring a synthetic backup does not permanently revive deleted data or bypass suppression.

### Method

1. Create a disposable backup containing synthetic fixtures.
2. delete one fixture and suppress another;
3. restore into an isolated non-production environment;
4. apply the documented post-restore deletion/suppression reconciliation;
5. verify deleted records remain unavailable and suppressed identities remain ineligible;
6. destroy the disposable restored environment and record cleanup.

### Pass criteria

- restoration does not become a path around deletion or suppression;
- reconciliation steps are deterministic and owned;
- provider limitations are documented as blockers, not converted into a pass.

## 10. Provider and legal evidence gates

PE-001, PE-002, PE-009, PE-010, PE-011, and PE-012 require documentary evidence rather than a synthetic technical test.

The reviewer must verify, without guessing:

- actual provider and subprocessor names;
- actual regions and transfer chain;
- contract/DPA status;
- retention, deletion, backup, and support access terms;
- controller/processor roles and lawful basis;
- NDGP, DPO, DPIA, registration, and cross-border decisions;
- customer-specific SOW/DPA alignment with the deployed system.

Where evidence is unavailable, keep the gate blocked. Do not infer provider terms from marketing pages or an old screenshot.

## 11. Verification

Repository contract verification:

```bash
python -m pytest -q \
  tests/test_pilot_launch_pack.py \
  tests/test_pilot_privacy_evidence_pack.py \
  --no-cov
```

This command verifies the fail-closed artifact structure only. It does not execute provider, legal, production, or customer-data drills and does not authorize launch.

## 12. Release decision

A controlled real-data pilot remains `NO-GO` until:

- all applicable evidence-ledger gates are passed with links and timestamps;
- #918 has an accountable legal/risk decision;
- the customer-specific DPA and SOW are signed;
- the deployed security pack matches the actual provider configuration;
- tenant isolation, export, deletion, suppression, backup interaction, and breach drills have independent review;
- Founder, Privacy, Security, and customer owner approvals are recorded.

Until then: `NO_REAL_CUSTOMER_DATA`.
