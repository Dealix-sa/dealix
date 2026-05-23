# Proof Approval OS | نظام اعتماد الإثبات

## Purpose | الغرض
No proof artifact — case study, testimonial, logo wall mention, anonymized sample,
metric callout — is ever published or distributed without explicit written client
consent and founder approval. Proof Approval OS is the system that enforces that.

This is the most reputation-critical control in Dealix.

## Inputs | المدخلات
- Proof-event candidates from Ultimate Delivery OS closeout
- Engagement metrics + outcomes (internal)
- Client point-of-contact for consent
- Standard consent template (per format: case study, logo, testimonial, anonymized)
- Legal/PDPL requirements per data type

## Outputs | المخرجات
- `proof.artifacts`: artifact_id, client_id, type, content_pointer, consent_id,
  approval_state, publication_state, publication_channels, version_history
- `proof.consents`: consent_id, client_id, scope, signed_at, signed_by,
  expires_at, scope_documents
- Publication-ready artifact (only after consent + approval)
- Distribution handoff to Proof-to-Demand Machine

## Proof types | أنواع الإثبات
- **Named case study** — client name + outcome + quote
- **Anonymized case study** — sector + outcome, no client name
- **Logo placement** — client logo on website / deck
- **Testimonial quote** — short quote from named buyer
- **Metric callout** — specific outcome metric (with consent)
- **Sample / template artifact** — sanitized work artifact used as proof

## Consent gate | بوابة الموافقة
- Written consent required per artifact (email is acceptable; signed doc stronger)
- Consent scope must match artifact: a logo consent does not cover a metric callout
- Consent expires; default 24 months unless otherwise specified
- Client can revoke; revocation triggers takedown within 7 business days

## Approval pipeline | خط الاعتماد
1. Closeout produces proof-event candidate
2. Worker drafts artifact (anonymized first if applicable)
3. Founder reviews internally
4. Consent request drafted → approved → sent to client
5. Client returns written consent (matching scope)
6. Founder gives final A2 approval
7. Artifact moves to publishable state
8. Proof-to-Demand Machine may distribute

## Approval class | فئة الموافقة
- A1: internal artifact drafting, anonymization
- A2: every consent request send AND every artifact publication
- A3: any artifact referencing regulated/government clients; revocations

## Trust gate | بوابة الثقة
- No publication without `consent_state = signed` AND `approval_state = approved`
- Scope mismatch detector blocks publication
- Expired consent auto-pauses artifact distribution
- Revocation triggers takedown within 7 business days
- Policy snapshot + audit row per state transition

## Owner | المالك
Founder owns final approval. Client owns consent. Worker enforces gates.

## Worker name
`proof.approval_os`

## KPI | المؤشرات
- # active approved artifacts
- Consent-to-publication conversion rate
- Time: closeout → publishable artifact (target ≤ 45 days)
- # revocations (should remain rare; trend = trust health signal)
- # publications blocked by consent gate (should be > 0, proving gate works)

## Failure mode | حالات الفشل
- Artifact published with scope-mismatched consent
- Expired consent silently still distributing
- Revocation lag > 7 business days

## Recovery path | مسار الاسترداد
- Hard architectural block: publication path checks both gates every time
- Daily consent-expiry sweep; expired artifacts auto-paused
- Revocation triggers immediate takedown ticket with 7-day SLA + escalation
