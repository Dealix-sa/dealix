# 021 — Inventory the scattered legal/compliance templates (do not draft new ones)

- **Finding:** The original scope of this plan was "draft legal/compliance
  templates (Quote, SOW, DPA, SLA-light, Data Classification, Access-
  Retention Matrix, Subprocessor register, Case Study Consent, incident
  process)." Direct repo search during this audit found **that work
  already exists — repeatedly, in the same sprawl pattern already flagged
  elsewhere in this backlog** (docs/ structural sprawl, `auto_client_acquisition`
  dead-module duplication). Confirmed counts:
  - **DPA**: 5 separate documents — `templates/contracts/dpa_ar.md` (88
    lines), `docs/legal/DPA_TEMPLATE_AR.md` (142 lines, "v1.0 — 2026-05-12"),
    `docs/DPA_PILOT_TEMPLATE.md` (34 lines), `docs/DPA_DEALIX_FULL.md`
    (349 lines, "Version 2.0... executable for first 3 paid pilots; lawyer
    review scheduled within 90 days"), `docs/transformation/enterprise_package/DPA_TEMPLATE_AR_EN.md`
    (49 lines) — plus a checklist at `docs/wave8/DPA_CHECKLIST_AR_EN.md`.
  - **SOW / Proposal**: `docs/commercial/PILOT_SOW_AND_ACCEPTANCE_TEMPLATE_AR.md`
    (117 lines), `sales/PILOT_PROPOSAL_TEMPLATE_AR.md` (45 lines),
    `sales/PROPOSAL_TEMPLATE_AR.md` (104 lines).
  - **SLA**: `templates/contracts/sla_ar.md`,
    `docs/enterprise/SLA_SLO_DRAFT_AR.md`, `docs/delivery/WORKFLOW_SLA.md`,
    `docs/company_os/enterprise/SLA_AND_SUPPORT_MODEL_AR.md` (4 docs),
    plus 4 separate *code* modules under `auto_client_acquisition/`
    (`support_os/sla.py`, `customer_inbox_v10/sla_policy.py`,
    `support_inbox/sla_monitor.py`, `service_quality/sla_tracker.py`).
  - **Incident response**: 10 hits across `docs/` and
    `auto_client_acquisition/` (4 separate `incident_response.py` modules
    alone, in `runtime_safety_os`, `risk_resilience_os`,
    `institutional_control_os`, `compliance_trust_os`).
  - **Subprocessor register**: exists as both
    `docs/32_enterprise_readiness/SUBPROCESSOR_LIST.md` and the public
    `landing/subprocessors.html`.
  - **Consent**: no single "Case Study Consent" template found by name,
    but 5+ consent-tracking *code* modules exist
    (`auto_client_acquisition/compliance_os/consent_ledger.py`,
    `customer_data_plane/consent_registry.py`, etc.) plus
    `app/outbound/consent.py` and 4 doctrine-guard tests referencing
    consent.
  Drafting a *sixth* DPA or a *fifth* SLA doc would make this problem
  worse, not better. What's actually missing is a founder-facing answer
  to "which one do I actually hand a customer," and a check for a
  genuinely absent piece: a standalone **Case Study Consent** template and
  a standalone **Access & Retention Matrix** / **Data Classification
  Sheet** (neither turned up a dedicated template by name — confirm this
  gap is real, don't assume).
- **Category:** docs / legal
- **Wave:** maintenance
- **Effort:** M   **Confidence:** HIGH
- **Written against commit:** aae97bcefcf73e74aef8c75ac593238dc1ed690e

## Drift check (run first)
```bash
git rev-parse HEAD   # if != aae97bcefcf73e74aef8c75ac593238dc1ed690e, re-run the discovery greps in this plan fresh before trusting the file list above
```

## Context (inlined)
- This plan produces an **inventory + a founder-facing recommendation**,
  modeled on plan 013's `scripts/ops/build_os_module_wiring_catalog.py`
  pattern — it does not merge, rewrite, or delete any existing legal
  document, and it does not draft new DPA/SOW/SLA content (that would
  require licensed legal judgment this plan explicitly declines to make).
- The only genuinely new content this plan may add is for a confirmed gap
  (e.g. Case Study Consent) — and even then, as a short, clearly-labeled
  draft requiring licensed legal review before use, per this plan's
  category.

## Steps
1. Write `scripts/ops/build_legal_docs_catalog.py` (mirror the structure
   of `scripts/ops/build_verify_catalog.py` / `build_os_module_wiring_catalog.py`
   if the latter exists by this point — check `plans/013` first): glob for
   documents matching each category above (DPA, SOW/Proposal, SLA,
   Incident Response, Subprocessor, Consent, Data Classification,
   Access & Retention) across `docs/`, `templates/`, `sales/`, `landing/`,
   and emit a table to `docs/ops/LEGAL_DOCS_CATALOG.md`: category | path |
   line count | version/status line (if present) | last commit date
   (`git log -1 --format=%ad -- <path>`) | references the current 2-offer
   registry or the old offer ladder (grep for "499 SAR" / "quote_only" /
   etc. as a signal).
   **Gate:** `python3 scripts/ops/build_legal_docs_catalog.py` → writes the file without error.
2. Add `tests/test_legal_docs_catalog.py` asserting the catalog is
   regenerable and non-empty for each category found during this audit
   (freshness guard, mirroring `tests/test_verify_catalog.py`'s pattern) —
   this does not judge which doc is "best," only that the catalog stays
   in sync with the repo.
   **Gate:** `python3 -m pytest tests/test_legal_docs_catalog.py -q` → passes.
3. At the top of `docs/ops/LEGAL_DOCS_CATALOG.md`, add a short preamble (no
   legal judgment, just facts + a process) stating: these documents were
   never reconciled into one canonical set; for each category, the
   founder (with licensed legal counsel) should pick one canonical
   document, mark it "CANONICAL" in its own header, and mark the rest with
   a one-line pointer to the canonical choice (same pattern as plan 014's
   `00_constitution`/`00_foundation` pointer-file approach) — do not make
   that pick in this plan.
   **Gate:** `grep -n "CANONICAL" docs/ops/LEGAL_DOCS_CATALOG.md` → the
   instruction text is present (as guidance, not applied to any file).
4. Confirm whether a standalone Case Study Consent template genuinely
   doesn't exist (`grep -rli "case.study.*consent\|consent.*case.study"
   docs/ sales/ templates/`). If it's truly absent, add one short draft —
   `sales/CASE_STUDY_CONSENT_TEMPLATE_AR.md` — covering: what will be
   shared, anonymization options, revocation right, and a signature block,
   clearly headed "Template only — lawyer review required" matching the
   existing convention seen in `docs/transformation/enterprise_package/DPA_TEMPLATE_AR_EN.md:1-4`.
   If a near-equivalent already exists under a different name, do not
   duplicate it — add it to the catalog instead.
   **Gate:** either the new file exists with the required disclaimer
   header, or the catalog shows an existing equivalent was found.
5. Confirm whether a standalone Data Classification Sheet / Access &
   Retention Matrix genuinely doesn't exist
   (`grep -rli "data classification\|access.*retention matrix" docs/`).
   Apply the same logic as step 4: add one short labeled draft only if
   the gap is real, otherwise catalog the existing equivalent.
   **Gate:** same pattern as step 4's gate.

## Done criteria (machine-checkable)
- [ ] `python3 scripts/ops/build_legal_docs_catalog.py && python3 -m pytest tests/test_legal_docs_catalog.py -q` → passes
- [ ] `docs/ops/LEGAL_DOCS_CATALOG.md` exists and lists at least the DPA,
      SOW, SLA, Incident Response, and Subprocessor categories found
      during this audit
- [ ] `make full-repo-test` → all required gates PASS

## Out of scope (do not touch)
- Do not merge, rewrite, or delete any existing DPA/SOW/SLA/incident
  document — only catalog them and recommend a process for the founder
  to pick a canonical one.
- Do not draft new DPA, SOW, or SLA content — those categories already
  have multiple candidates; the gap here is consolidation, not creation.
- Do not make any legal judgment about which document is contractually
  sound — this plan is a repo-hygiene inventory, not a legal review.
- Any new file this plan does add (steps 4-5, only if the gap is
  confirmed real) must carry a "Template only — lawyer review required"
  header, matching existing convention.

## STOP conditions
- If any category's discovery grep turns up so many hits (10+) that a
  simple table becomes unreadable → STOP and group by sub-theme in the
  catalog rather than producing an unusable wall of rows.
- If step 4 or 5's gap-check finds an existing near-equivalent under a
  name this plan's greps missed → STOP adding a new file, catalog the
  existing one instead; do not create a 6th DPA-shaped problem by
  drafting a redundant new document.
