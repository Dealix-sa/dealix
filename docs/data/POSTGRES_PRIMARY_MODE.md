# Postgres Primary Mode — وضع التشغيل الأساسي لقاعدة البيانات

Status: v1
Owner: Founder

## 1. Purpose — الغرض

Defines how primary Postgres is configured, accessed, and protected as the operating store of Dealix.

يحدد كيفية تهيئة Postgres الأساسي والوصول إليه وحمايته كمخزن التشغيل لـ Dealix.

## 2. Topology — الطوبولوجيا

- Single primary writer.
- Read replicas for analytics and control plane heavy reads.
- Connection pool in front of the primary (PgBouncer or equivalent).
- Backups: daily snapshot + continuous WAL for PITR.
- TLS required on all connections.

## 3. Roles — الأدوار

| Role | Permissions | Used by |
|---|---|---|
| `dealix_app_rw` | read/write on app schemas | API service |
| `dealix_app_ro` | read on app schemas | Control plane reads, console |
| `dealix_ingest` | write on staging schemas | Promotion job only |
| `dealix_admin` | DDL | Migrations only, via CI |
| `dealix_audit` | append on audit schema | Audit writer only |
| `dealix_dba` | superuser-equivalent | Founder break-glass |

No agent ever holds a DB role directly. Agents call services; services call DB.

## 4. Schemas — المخططات

- `app` — operating tables (accounts, drafts, queues).
- `staging` — promoted-from-shadow intermediate tables.
- `audit` — append-only audit entries.
- `control` — materialized views for the control plane.
- `analytics` — warehouse-bound exports.

## 5. RLS — الأمن على مستوى الصف

- RLS enabled on every table that may carry confidential or restricted data.
- Policies bind to a `data_tier` column and the caller's role.
- Default policy denies; explicit grants per tier.

## 6. Migrations — الترحيلات

- Managed by a single migration tool, versioned in the repo.
- Reviewed in PR; require Trust Guardian label for any change to `audit` or `control` schemas.
- Applied in CI against the staging DB before production.
- Production migrations require founder approval token at deploy time.

## 7. Backups and Restore — النسخ والاستعادة

- Daily snapshot, retained 30 days.
- PITR window: 7 days.
- Restore drill: monthly, output recorded in DORA/MTTR metrics.
- Cold archive: weekly to immutable storage with 1-year retention.

## 8. Observability — الرصد

Metrics published:
- Connection pool saturation.
- Replication lag.
- Slow queries (top 10 daily).
- WAL volume.
- Failed login attempts.
- RLS denial counts (signal for misconfigured callers).

## 9. Failure Modes — أنماط الفشل

- Primary unavailable -> API enters read-only mode; CSV inbox keeps queuing; founder is paged.
- Replica lag exceeds threshold -> control plane reads switch to primary with rate limit.
- Disk pressure -> alarms before fill; archive job rotated.

## 10. Non-Negotiables — خطوط حمراء

- No direct DB access from agent runtime.
- No restricted data in plain text outside `app` (and only in columns explicitly classified).
- No DDL outside CI.
- No backup deletion without audit entry.

## 11. References — مراجع

- `docs/data/ULTIMATE_DATA_PLATFORM.md`
- `docs/security/ULTIMATE_SECURITY_GOVERNANCE.md`
- `docs/engineering/ULTIMATE_OBSERVABILITY_DORA.md`
- `docs/runtime/PRIVATE_OPS_RUNTIME_CONTRACT.md`
