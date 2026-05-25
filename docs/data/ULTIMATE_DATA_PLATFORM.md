# Ultimate Data Platform

> The system of record for every fact that matters to Dealix.
> If it affects revenue, trust, client delivery, or external action, it must become a record.

---

## 1. Phased build

The data platform is built in **five phases**, in order. You may not start phase N+1 before phase N is in operation.

### Phase 1 — Private Ops CSV
- **What:** CSV files under `private_ops/` (gitignored), one file per core table.
- **Why:** fastest path to operating evidence; zero infra cost; bootstrappable today.
- **Constraint:** read by the runtime, written by workers, exported to console via internal API.
- **Exit:** at least 14 days of clean operation; or the moment we hit the L7 trigger (see §5).

### Phase 2 — Postgres Primary
- **What:** managed Postgres becomes the operational source of truth.
- **Why:** concurrent writes, referential integrity, transactions, indexes, recovery.
- **Constraint:** CSV becomes a periodic export only — no longer a primary source.
- **Exit:** all reads go through Postgres; CSV exports run nightly and round-trip cleanly.

### Phase 3 — Event Log
- **What:** an append-only `events` table that captures every external-impact action, approval, worker run.
- **Why:** auditability, replay, downstream analytics, regulatory readiness.
- **Constraint:** events are immutable; corrections are new events, never updates.
- **Exit:** every external-impact endpoint emits exactly one event; replays reconstruct the state.

### Phase 4 — Metrics Layer
- **What:** materialized views + aggregations for business, DORA, AI, and finance metrics.
- **Why:** the founder console must read fast, even at high record counts.
- **Constraint:** every metric on the console maps to exactly one named query in the metrics layer.
- **Exit:** page latency < 500ms with 1M+ rows; every metric has an SLO.

### Phase 5 — Warehouse
- **What:** columnar warehouse (BigQuery / Snowflake / DuckDB on object storage).
- **Why:** historical analysis, sector learning, model evaluation, revenue forecasting.
- **Constraint:** the operational store is never queried for analytics.
- **Exit:** weekly forecasts published; model retrains read from the warehouse.

---

## 2. Core tables (operational schema)

Every table below has the same five baseline columns unless noted:
`id`, `created_at`, `updated_at`, `created_by`, `tenant_id`.

### 2.1 `accounts`
| Column         | Type        | Notes                                   |
|----------------|-------------|-----------------------------------------|
| handle         | text unique | Slug (e.g., "alrajhi-takaful").         |
| legal_name_ar  | text        |                                         |
| legal_name_en  | text        |                                         |
| sector         | text        | Sector tag.                             |
| region         | text        | Saudi region.                           |
| size_band      | text        | 1–10, 11–50, …                          |
| status         | enum        | `prospect`, `engaged`, `client`, `lost`.|

### 2.2 `contacts`
| Column      | Type        | Notes                                   |
|-------------|-------------|-----------------------------------------|
| account_id  | fk(accounts)|                                         |
| full_name   | text        |                                         |
| role        | text        |                                         |
| email       | text        | Indexed.                                |
| phone_e164  | text        | Indexed.                                |
| consent     | enum        | `none`, `opt_in`, `opt_out`.            |

### 2.3 `signals`
| Column      | Type        | Notes                                   |
|-------------|-------------|-----------------------------------------|
| account_id  | fk(accounts)|                                         |
| kind        | text        | `tender`, `hiring`, `news`, `funding`.  |
| source      | text        | Source name.                            |
| url         | text        |                                         |
| observed_at | timestamptz |                                         |

### 2.4 `lead_intelligence`
| Column         | Type        | Notes                                |
|----------------|-------------|--------------------------------------|
| account_id     | fk(accounts)|                                      |
| fit_score      | smallint    | 0–100.                               |
| intent_score   | smallint    | 0–100.                               |
| signal_count   | smallint    |                                      |
| icp_match      | boolean     |                                      |
| notes          | text        |                                      |

### 2.5 `outreach_queue`
| Column         | Type        | Notes                                |
|----------------|-------------|--------------------------------------|
| account_id     | fk(accounts)|                                      |
| contact_id     | fk(contacts)|                                      |
| draft_id       | text        |                                      |
| channel        | enum        | `email`, `whatsapp`, `linkedin`.     |
| state          | enum        | `drafted`, `approved`, `sent`, `rejected`. |
| scheduled_for  | timestamptz |                                      |

### 2.6 `approval_queue`
| Column         | Type        | Notes                                |
|----------------|-------------|--------------------------------------|
| subject_type   | text        | `outreach`, `sample`, `proposal`, …  |
| subject_id     | text        |                                      |
| class          | enum        | `A0`, `A1`, `A2`, `A3`.              |
| policy_result  | jsonb       | See §6.                              |
| evidence       | jsonb       |                                      |
| state          | enum        | `pending`, `decided`.                |

### 2.7 `approval_decisions`
| Column          | Type        | Notes                                |
|-----------------|-------------|--------------------------------------|
| approval_id     | fk(approval_queue) |                               |
| actor           | text        | `founder` / role.                    |
| decision        | enum        | `approved`, `rejected`, `edit`, `escalated`. |
| note            | text        |                                      |
| decided_at      | timestamptz |                                      |

### 2.8 `conversation_log`
| Column          | Type        | Notes                                |
|-----------------|-------------|--------------------------------------|
| account_id      | fk(accounts)|                                      |
| contact_id      | fk(contacts)|                                      |
| direction       | enum        | `outbound`, `inbound`.               |
| channel         | enum        | `email`, `whatsapp`, `linkedin`.     |
| message_body    | text        |                                      |
| classification  | enum        | `positive`, `neutral`, `negative`, `ooo`.|
| occurred_at     | timestamptz |                                      |

### 2.9 `sample_queue`
| Column          | Type        | Notes                                |
|-----------------|-------------|--------------------------------------|
| account_id      | fk(accounts)|                                      |
| sample_kind     | text        | e.g., `sector_pulse`, `mini_report`. |
| asset_url       | text        |                                      |
| state           | enum        | `draft`, `qa`, `approved`, `delivered`. |

### 2.10 `proposal_queue`
| Column          | Type        | Notes                                |
|-----------------|-------------|--------------------------------------|
| account_id      | fk(accounts)|                                      |
| offer           | text        | e.g., `499_SAR_sprint`.              |
| amount_sar      | numeric(10,2)|                                     |
| state           | enum        | `draft`, `sent`, `accepted`, `closed_lost`. |
| sent_at         | timestamptz |                                      |

### 2.11 `payment_capture_queue`
| Column          | Type        | Notes                                |
|-----------------|-------------|--------------------------------------|
| proposal_id     | fk(proposal_queue) |                               |
| amount_sar      | numeric(10,2)|                                     |
| state           | enum        | `awaiting`, `paid`, `plan`, `lost`.  |
| next_followup   | timestamptz |                                      |

### 2.12 `delivery_queue`
| Column          | Type        | Notes                                |
|-----------------|-------------|--------------------------------------|
| client_handle   | text        |                                      |
| stage           | enum        | `intake`, `delivery`, `qa`, `handoff`, `feedback`. |
| qa_status       | enum        | `pending`, `pass`, `fail`.           |
| started_at      | timestamptz |                                      |

### 2.13 `retention_queue`
| Column          | Type        | Notes                                |
|-----------------|-------------|--------------------------------------|
| client_handle   | text        |                                      |
| health_score    | smallint    | 0–100.                               |
| action          | enum        | `retainer_ask`, `referral_ask`, `renewal`. |

### 2.14 `proof_library`
| Column          | Type        | Notes                                |
|-----------------|-------------|--------------------------------------|
| client_handle   | text        |                                      |
| kind            | enum        | `case_study`, `testimonial`, `sample`.|
| approved        | boolean     |                                      |
| asset_url       | text        |                                      |

### 2.15 `worker_runs`
| Column          | Type        | Notes                                |
|-----------------|-------------|--------------------------------------|
| worker_id       | text        |                                      |
| started_at      | timestamptz |                                      |
| finished_at     | timestamptz |                                      |
| status          | enum        | `ok`, `failed`, `retried`, `skipped`.|
| error           | text        |                                      |
| retry_of        | fk(worker_runs)|                                  |

### 2.16 `audit_events`
| Column          | Type        | Notes                                |
|-----------------|-------------|--------------------------------------|
| actor           | text        |                                      |
| action          | text        | e.g., `approve`, `send`, `qa_pass`.  |
| subject_type    | text        |                                      |
| subject_id      | text        |                                      |
| decision        | text        |                                      |
| payload_digest  | text        | SHA-256.                             |
| trace_id        | text        |                                      |
| occurred_at     | timestamptz |                                      |

### 2.17 `ai_eval_results`
| Column          | Type        | Notes                                |
|-----------------|-------------|--------------------------------------|
| suite           | text        | `prompt_injection`, `refusal`, …     |
| prompt_id       | text        |                                      |
| input_hash      | text        |                                      |
| output_hash     | text        |                                      |
| pass            | boolean     |                                      |
| evaluator       | text        | model / rule / human.                |

### 2.18 `finance_events`
| Column          | Type        | Notes                                |
|-----------------|-------------|--------------------------------------|
| kind            | text        | `invoice`, `payment`, `ai_cost`, `tool_cost`. |
| amount_sar      | numeric(12,2)|                                     |
| client_handle   | text        | Optional.                            |
| reference       | text        | Provider reference (Stripe id, …).   |
| occurred_at     | timestamptz |                                      |

### 2.19 `product_usage`
| Column          | Type        | Notes                                |
|-----------------|-------------|--------------------------------------|
| feature_id      | text        |                                      |
| actor           | text        | client / partner / founder.          |
| usage_count     | int         |                                      |
| occurred_on     | date        |                                      |

### 2.20 `incidents`
| Column          | Type        | Notes                                |
|-----------------|-------------|--------------------------------------|
| severity        | enum        | `sev1`–`sev4`.                       |
| summary         | text        |                                      |
| opened_at       | timestamptz |                                      |
| closed_at       | timestamptz |                                      |
| postmortem_url  | text        |                                      |

---

## 3. Event log

Phase 3 introduces a single `events` table with the schema:

| Column           | Type        | Notes                                |
|------------------|-------------|--------------------------------------|
| event_id         | uuid        | Primary key.                         |
| event_type       | text        | e.g., `approval.decided`.            |
| aggregate_type   | text        | e.g., `approval`.                    |
| aggregate_id     | text        |                                      |
| occurred_at      | timestamptz |                                      |
| actor            | text        |                                      |
| trace_id         | text        |                                      |
| payload          | jsonb       | Domain payload, validated by schema. |
| payload_digest   | text        | SHA-256.                             |

Append-only. No `UPDATE`/`DELETE`. Schemas live in `dealix/events/schemas/`.

---

## 4. Lineage & provenance

Every row in an operational table carries:
- `created_by` — the worker or actor that wrote it.
- `source_event_id` — the event that produced it (Phase 3+).
- `source_provenance` — JSON: `{ source_name, source_url, fetched_at, license }` for any externally-sourced data.

Provenance is mandatory for `accounts`, `contacts`, `signals`, `lead_intelligence`, and `proof_library`. Without provenance, the row is rejected at write time.

---

## 5. Triggers (when to move phases)

| Trigger                                                                   | Move to phase |
|----------------------------------------------------------------------------|---------------|
| Two writers race on the same CSV row and one is lost.                      | Phase 2.      |
| Auditor asks for a complete decision history.                              | Phase 3.      |
| Console page exceeds 500ms p95.                                            | Phase 4.      |
| Founder asks for sector trends across >180 days.                           | Phase 5.      |

Do not migrate phases for any reason **other than** a trigger above. "It would be nicer" is not a trigger.

---

## 6. Backups & restore

- Postgres: daily logical backups (`pg_dump`) + WAL archive.
- Object storage for warehouse extracts: lifecycle to cold storage after 90 days.
- **Restore drill:** at least once per quarter, a clean restore is performed in a sandbox; restore time is recorded; the founder reviews it.

A backup that has not been restored is not a backup.

---

## 7. Privacy & sovereignty

- Default residency: Saudi Arabia (KSA region) for managed Postgres and warehouse.
- PII fields (`contacts.email`, `contacts.phone_e164`) are encrypted at rest with a per-tenant key.
- Suppression list is consulted at write time for `outreach_queue` and `conversation_log` — a write that violates suppression is rejected and logged as a trust flag.

---

## 8. Rule

> **If it affects revenue, trust, client delivery, or external action, it must become a record.**

If a fact exists only in a person's head, a chat message, or an ephemeral file, it doesn't exist for Dealix.
