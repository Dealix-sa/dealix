# Revenue Intelligence Warehouse — مخزن البيانات لذكاء الإيرادات

**Purpose / الغرض**
Architecture doc for the warehouse that backs Dealix's Revenue Intelligence delivery. Defines tables, retention windows, freshness SLA per table, and downstream consumers. This is **not** the delivery playbook — that lives in `docs/27_delivery_playbooks/REVENUE_INTELLIGENCE_DELIVERY_PLAYBOOK.md`.
وثيقة معمارية لمخزن البيانات الذي يدعم تسليم Revenue Intelligence. تعرّف الجداول، نوافذ الاحتفاظ، تحديث الحداثة لكل جدول، والمستهلكين النهائيين. ليست هذه دليل التسليم — الدليل في `docs/27_delivery_playbooks/REVENUE_INTELLIGENCE_DELIVERY_PLAYBOOK.md`.

**Owner placeholder:** Data steward = `<founder>` initially; co-owned with Data Ops Assistant.
**Cadence:** Schema review quarterly. Freshness checks daily. Retention sweep monthly. / مراجعة المخطط فصليًا. فحص الحداثة يوميًا. كنس الاحتفاظ شهريًا.
**KPIs:** (1) % of tables meeting freshness SLA, (2) % of records with complete source passport per `docs/04_data_os/SOURCE_PASSPORT.md`, (3) count of retention violations (target: 0).
**Risk if missing / مخاطر الغياب:** Downstream reports drift. PDPL exposure rises silently. Customer-facing claims rest on unaligned data. / تقارير المستهلك تنحرف. التعرّض لـ PDPL يرتفع بصمت. تستند ادعاءات العميل على بيانات غير متماشية.

---

## EN summary

The warehouse is the single store from which Dealix builds Revenue Intelligence outputs. Eight canonical tables, each with a defined schema, retention window, and freshness SLA. Two principles dominate: every row carries a source passport, and every PII field is classified at write-time per the Data OS rules. Downstream consumers are explicitly named — nothing is "general purpose".

## ملخص بالعربية

المخزن مصدر بيانات واحد تبني عليه Dealix مخرجات Revenue Intelligence. ثمانية جداول قياسية، لكل منها مخطط، نافذة احتفاظ، وSLA حداثة. مبدآن مهيمنان: كل صف يحمل source passport، وكل حقل PII يُصنَّف وقت الكتابة وفق قواعد Data OS. المستهلكون النهائيون مسمَّون صراحة — لا «استخدام عام».

---

## الجداول الثمانية / The eight canonical tables

> الجدول الفعلي بأي تقنية تخزين. هذا مخطط منطقي مُلزم. / The actual table in any storage technology. This is the binding logical schema.

### 1. `accounts`

```json
{
  "account_id": "string (uuid)",
  "label_opaque": "string (no PII)",
  "sector": "enum",
  "subsector": "string",
  "size_band": "enum (micro|small|mid|large)",
  "region": "string",
  "stage": "enum (target|engaged|pilot|customer|dormant|exited)",
  "created_at": "timestamp",
  "updated_at": "timestamp",
  "source_passport_id": "string (fk to source_passport)"
}
```

- Retention: 24 months after `stage = exited`.
- Freshness SLA: updated_at within 7 days for `stage in (engaged, pilot, customer)`.

### 2. `contacts`

```json
{
  "contact_id": "string (uuid)",
  "account_id": "string (fk to accounts)",
  "role_tag": "string (e.g., 'ops-director')",
  "pii_class": "enum (P0|P1|P2|P3) per docs/04_data_os/PII_CLASSIFICATION.md",
  "consent_status": "enum (none|written-opt-in|implicit-business-context|withdrawn)",
  "consent_evidence_path": "string (relative path)",
  "channel_preferences": "array of enum (email|call|in-person|written-doc)",
  "last_touch_at": "timestamp",
  "created_at": "timestamp",
  "updated_at": "timestamp",
  "source_passport_id": "string (fk to source_passport)"
}
```

- Retention: per `docs/ops/PDPL_RETENTION_POLICY.md` for the highest pii_class in the record.
- Freshness SLA: `last_touch_at` audited weekly. No record with consent_status=withdrawn used after withdrawal date.

### 3. `signals`

```json
{
  "signal_id": "string (uuid)",
  "account_id": "string (fk)",
  "signal_type": "enum (sector-event|hiring|expansion|public-disclosure|customer-said)",
  "observed_at": "timestamp",
  "source": "string (public source url or passport id)",
  "summary": "string",
  "confidence": "enum (low|med|high)",
  "expires_at": "timestamp",
  "source_passport_id": "string (fk)"
}
```

- Retention: 18 months unless linked to an active opportunity.
- Freshness SLA: signals older than `expires_at` are not used in outreach materials.

### 4. `outreach_events`

```json
{
  "event_id": "string (uuid)",
  "account_id": "string (fk)",
  "contact_id": "string (fk, nullable)",
  "channel": "enum (email|call|in-person|written-doc|event|referral)",
  "direction": "enum (inbound|outbound)",
  "occurred_at": "timestamp",
  "owner_role": "string",
  "artifact_path": "string (relative path to the artifact, if any)",
  "approval_record_id": "string (fk to approval_matrix log)",
  "compliance_check_id": "string (fk)"
}
```

- Retention: 36 months.
- Freshness SLA: `occurred_at` logged within 24 hours of the event.
- Hard rule: every outbound event references an `approval_record_id` per `docs/governance/APPROVAL_MATRIX.md`.

### 5. `replies`

```json
{
  "reply_id": "string (uuid)",
  "outreach_event_id": "string (fk, nullable)",
  "account_id": "string (fk)",
  "contact_id": "string (fk, nullable)",
  "channel": "enum",
  "received_at": "timestamp",
  "intent_label": "enum (interested|neutral|declined|out-of-office|delegated|unclear)",
  "next_action": "string",
  "filed_in": "string (relative path)"
}
```

- Retention: 36 months.
- Freshness SLA: `received_at` logged within 24 hours.

### 6. `proposals`

```json
{
  "proposal_id": "string (uuid)",
  "account_id": "string (fk)",
  "version": "string",
  "service_id": "string (fk to docs/company/SERVICE_REGISTRY.md)",
  "scope_summary": "string",
  "amount_sar": "number",
  "discount_pct": "number",
  "payment_terms": "string (e.g., 'Net-15')",
  "deal_desk_id": "string (fk, nullable, per docs/revenue/DEAL_DESK_SYSTEM.md)",
  "status": "enum (draft|sent|in-review|signed|declined|expired)",
  "sent_at": "timestamp",
  "signed_at": "timestamp",
  "artifact_path": "string"
}
```

- Retention: 84 months (regulatory + commercial memory).
- Freshness SLA: `status` updated within 48 hours of any change.

### 7. `payments`

```json
{
  "payment_id": "string (uuid)",
  "account_id": "string (fk)",
  "proposal_id": "string (fk)",
  "invoice_id": "string (per docs/revenue/INVOICE_FLOW.md)",
  "amount_sar": "number",
  "currency": "string (default SAR)",
  "received_at": "timestamp",
  "method": "enum",
  "reconciled_at": "timestamp",
  "reconciliation_source": "string (per docs/revenue/PAYMENT_RECONCILIATION.md)"
}
```

- Retention: 120 months (regulatory).
- Freshness SLA: `reconciled_at` within 7 days of receipt.

### 8. `proofs`

```json
{
  "proof_id": "string (uuid)",
  "account_id": "string (fk)",
  "proposal_id": "string (fk, nullable)",
  "proof_event_type": "enum (per docs/07_proof_os/PROOF_EVENTS.md)",
  "value_class": "enum (estimated|observed|verified per docs/08_value_os/ESTIMATED_OBSERVED_VERIFIED_VALUE.md)",
  "value_amount_sar": "number",
  "observed_at": "timestamp",
  "evidence_path": "string (relative path)",
  "permission_to_publish": "enum (yes|no|not-asked)",
  "case_safe_summary_path": "string (nullable)"
}
```

- Retention: 60 months minimum.
- Freshness SLA: `observed_at` logged within 7 days; `evidence_path` populated before any external use.

---

## نوافذ الاحتفاظ / Retention summary

| Table | Retention | Trigger for purge |
|---|---|---|
| accounts | 24 months after exit | quarterly sweep |
| contacts | per PDPL pii_class | monthly sweep |
| signals | 18 months | expiry timestamp |
| outreach_events | 36 months | quarterly sweep |
| replies | 36 months | quarterly sweep |
| proposals | 84 months | regulatory floor |
| payments | 120 months | regulatory floor |
| proofs | 60 months | quarterly sweep |

> Any record with consent withdrawal triggers an immediate purge of personal fields per `docs/ops/PDPL_RETENTION_POLICY.md`. The opaque record stub may remain for audit. / أي صف بسحب موافقة يُطلِق مسح فوريًا للحقول الشخصية.

---

## SLA الحداثة / Freshness SLA

| Table | Freshness SLA |
|---|---|
| accounts | 7 days for active stages |
| contacts | weekly audit; immediate for consent changes |
| signals | not used after `expires_at` |
| outreach_events | 24 hours |
| replies | 24 hours |
| proposals | 48 hours after any status change |
| payments | 7 days from receipt |
| proofs | 7 days from observation |

Any table missing its SLA twice in a month is escalated as a Data Ops bottleneck signal per `docs/people/FOUNDER_BOTTLENECK_REMOVAL.md`.

---

## المستهلكون النهائيون / Downstream consumers

The following reports read from this warehouse. **No other consumer is approved** without a written request to the data steward.

| Consumer | Tables read | Refresh cadence | Reference doc |
|---|---|---|---|
| CEO brief | accounts, proposals, payments, proofs | weekly | `docs/company/MONTHLY_EXECUTIVE_NARRATIVE.md` |
| Founder leverage report | outreach_events, replies, proposals | weekly | `docs/founder/FOUNDER_LEVERAGE_DASHBOARD.md` |
| Capital allocation report | proposals, payments, proofs | monthly | `docs/operating_finance/CAPITAL_ALLOCATION_DASHBOARD.md` |
| Pipeline health | accounts, proposals, outreach_events | daily | `docs/ops/daily_scorecard.md` |
| Trust pack assembly | proofs (permission_to_publish = yes only) | per delivery | `docs/14_trust_os/TRUST_PACK.md` |
| Win/loss review | proposals, replies, proofs | per closed deal | `docs/revenue/WIN_LOSS_REVIEW.md` |

> A consumer added without a written request becomes a shadow consumer. Shadow consumers are killed on detection. / المستهلك المُضاف بدون طلب مكتوب يصبح "ظليًا". المستهلكون الظليون يُلغَوْن عند الاكتشاف.

---

## مبادئ المعمارية / Architectural principles

### EN

- **Source passport mandatory.** No row without a passport id. Reference `docs/04_data_os/SOURCE_PASSPORT.md`.
- **PII classification at write-time.** Cannot defer to read-time. Reference `docs/04_data_os/PII_CLASSIFICATION.md`.
- **Append-only where possible.** Proposals and payments are versioned, not updated in place.
- **No silent schema change.** Any field addition or change runs through `docs/ai_governance/AI_CHANGE_CONTROL.md` if any downstream consumer is AI.
- **Least privilege on access.** Per role, only the tables and columns needed. Audited monthly.

### AR

- **passport إلزامي.** لا صف بلا معرّف passport.
- **تصنيف PII وقت الكتابة.** لا يُؤجَّل لوقت القراءة.
- **إضافة فقط حيث أمكن.** المقترحات والمدفوعات مُعرّفة بإصدارات، لا تُعدَّل في مكانها.
- **لا تغيير صامت في المخطط.** أي إضافة حقل أو تعديل تمر عبر AI Change Control إن كان أي مستهلك AI.
- **أقل صلاحية.** لكل دور فقط الجداول والأعمدة اللازمة. تُدقَّق شهريًا.

---

## القواعد التي لا تُكسر / Hard rules

- No PII outside its declared class. No re-classification without governance review.
- No row used for a customer-facing claim without a `proofs` row backing it.
- No outbound event without `approval_record_id` populated.
- No payment row without a reconciliation source per `docs/revenue/PAYMENT_RECONCILIATION.md`.
- No table queried by a consumer not listed here, ever.

---

## Disclosure / إفصاح

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
The schemas above are logical and binding regardless of storage technology. They are not contracts about delivery commitments.

## Related canonical docs

- `docs/27_delivery_playbooks/REVENUE_INTELLIGENCE_DELIVERY_PLAYBOOK.md`
- `docs/data/DATA_READINESS_STANDARD.md`
- `docs/data/SOVEREIGN_DATA_MODEL.md`
- `docs/04_data_os/PII_CLASSIFICATION.md`
- `docs/04_data_os/SOURCE_PASSPORT.md`
- `docs/04_data_os/DATA_RETENTION_POLICY.md`
- `docs/04_data_os/DATA_QUALITY_SCORE.md`
- `docs/07_proof_os/PROOF_EVENTS.md`
- `docs/08_value_os/ESTIMATED_OBSERVED_VERIFIED_VALUE.md`
- `docs/revenue/INVOICE_FLOW.md`
- `docs/revenue/PAYMENT_RECONCILIATION.md`
- `docs/ops/PDPL_RETENTION_POLICY.md`
- `docs/ai_governance/AI_CHANGE_CONTROL.md`
