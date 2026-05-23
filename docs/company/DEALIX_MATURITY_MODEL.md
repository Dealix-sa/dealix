# Dealix Maturity Model — نموذج النضج

Status: v1
Owner: Founder

## 1. Purpose — الغرض

This model defines the stages Dealix progresses through.
Each stage has entry criteria, exit criteria, and the evidence required to claim it.
A stage is not claimed until the evidence is in `evals/results/` and on the Control Plane scorecard.

نموذج النضج يحدد المراحل التي تمر بها Dealix.
كل مرحلة لها معايير دخول، معايير خروج، وإثبات مطلوب.
لا تُعلن مرحلة دون أن يكون الإثبات في `evals/results/` وعلى لوحة التحكم.

## 2. The Five Stages — المراحل الخمس

### Stage 1 — Brand-Ready (جاهز للعلامة)
Entry: company exists in concept.
Exit when:
- Public-facing brand, name, identity registered.
- Public site live with non-committal positioning.
- Privacy, ToS, refund, PDPL posture documented.
- No false claims; no proof publication.
Evidence: brand kit, legal docs, screenshots, audit of public claims.

### Stage 2 — Distribution-Ready (جاهز للتوزيع)
Entry: brand-ready met.
Exit when:
- ICP defined and qualified accounts in the queue.
- Outreach drafts produced by the Revenue Agent Swarm.
- Founder approval workflow live; nothing leaves without approval.
- Suppression lists honored.
- Eval gate green on `arabic_business_quality`, `no_guaranteed_claims`, `suppression_compliance`.
Evidence: registry entries, eval results, sample drafts in `/opt/dealix-ops-private/outreach/drafts/`.

### Stage 3 — Revenue-Ready (جاهز للإيراد)
Entry: distribution-ready met.
Exit when:
- At least one pilot delivered with structured scorecard.
- Proposal drafter live; no pricing commitments outside approval.
- Renewal/expansion signals tracked.
- Audit trail complete for every revenue motion.
Evidence: pilot scorecards, signed proposal drafts, audit log filtered to revenue events.

### Stage 4 — AI-Governed (محكوم بالذكاء الاصطناعي)
Entry: revenue-ready met.
Exit when:
- Trust Guardian live and non-bypassable.
- Full eval gate green, including red-team suites.
- Control Plane API live with auth gate.
- DORA metrics tracked.
- Worker mesh observable; freshness SLO met.
Evidence: gate file passing in CI, control plane summary endpoint, DORA dashboard.

### Stage 5 — Sovereign (سيادي)
Entry: AI-governed met.
Exit when:
- Saudi data residency posture verified.
- PDPL data subject rights operable end-to-end.
- Model routing policy-driven; no provider lock-in.
- Founder can operate the company from one console.
- Single-operator drill passes monthly.
Evidence: residency attestation, DSR runbook execution, routing config, drill report.

## 3. Demotion Rules — قواعد التراجع

Any of the following triggers automatic demotion by one stage until remediated:
- A red safety eval suite.
- A policy bypass incident.
- An external action sent without approval.
- An unbacked public claim discovered.
- A Trust Guardian disablement without recorded founder approval.

## 4. Scoring — التسجيل

The Control Plane scorecard reports current stage and the % completion toward the next stage based on the evidence checklist.

## 5. Cadence — الإيقاع

- Weekly: progress review by founder.
- Monthly: maturity audit, evidence refresh.
- Quarterly: external review (legal, security) where applicable.

## 6. Anti-Pattern: Claiming Stages — نمط محظور

A stage is not a marketing claim. It is an internal operating state.
No external surface (website, deck, pitch) may claim a stage that the scorecard does not confirm.

## 7. References — مراجع

- `docs/company/DEALIX_SOVEREIGN_AI_OPERATING_COMPANY.md`
- `docs/control_plane/DEALIX_CONTROL_PLANE.md`
- `docs/evals/EVAL_GATE_V1.md`
- `docs/engineering/ULTIMATE_OBSERVABILITY_DORA.md`
