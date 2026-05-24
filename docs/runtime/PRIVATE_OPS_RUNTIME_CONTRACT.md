# Private Ops Runtime Contract — عقد التشغيل الخاص

Status: v1
Owner: Founder
Root: `/opt/dealix-ops-private/`

## 1. Purpose — الغرض

Defines the on-disk layout that all workers and agents use for inputs, outputs, queues, and audit. The repo never contains operational data; this private tree does.

يحدد بنية القرص التي يستخدمها كل العُمَّال والوكلاء للمدخلات، المخرجات، الطوابير، والتدقيق. المستودع لا يحوي بيانات تشغيل أبدًا؛ هذه الشجرة الخاصة هي مكانها.

## 2. Top-Level Layout — البنية العليا

```
/opt/dealix-ops-private/
  intelligence/
    inbox/
    received/
    quarantine/
    qualified/
  outreach/
    drafts/
    proposals/
    suppression/
  approvals/
    queue/
    decided/
    expired/
  trust/
    quarantine/
    risks/
    incidents/
  finance/
    cost/
    margin/
    reconciliation/
  runtime/
    heartbeats/
    briefings/
    locks/
```

## 3. Subdir Contracts — عقود المجلدات الفرعية

### intelligence/
- `inbox/` — raw CSVs and signals; readable by ingest workers only.
- `received/` — validated inputs (with `.schema.json`).
- `quarantine/` — rejected inputs with `.reason.txt`.
- `qualified/` — accounts that passed ICP rubric; consumed by the swarm.

### outreach/
- `drafts/` — A2 draft messages, AR+EN; one file per item; bound to a queue entry.
- `proposals/` — A2 proposal drafts; never includes binding pricing.
- `suppression/` — current suppression lists (do-not-contact, opt-out); enforced before any draft is queued.

### approvals/
- `queue/` — pending items awaiting founder decision; one file per item with evidence pointer.
- `decided/` — approved or rejected items; immutable.
- `expired/` — queue items that exceeded TTL; auto-archived.

### trust/
- `quarantine/` — Guardian-rejected outputs; reason and source preserved.
- `risks/` — open risks; one file per risk; severity, owner, status.
- `incidents/` — P0/P1/P2/P3 incident records.

### finance/
- `cost/` — daily/weekly cost rollups by agent, provider, domain.
- `margin/` — pilot and retainer margin reports.
- `reconciliation/` — provider invoices vs. observed usage.

### runtime/
- `heartbeats/` — worker heartbeat files; rotated.
- `briefings/` — founder daily briefings.
- `locks/` — process locks for single-writer guarantees.

## 4. File Conventions — اتفاقيات الملفات

- Names: `<domain>__<type>__<YYYYMMDDTHHMMSS>__<short-hash>.<ext>`.
- All structured files: JSON or YAML, UTF-8.
- Every file has a sidecar `.meta.json` with `producer`, `policy_version`, `class`, `data_tier`, `audit_entry_id`.

## 5. Permissions — الصلاحيات

- Tree owned by a single service user; agents and workers run as constrained sub-roles.
- No world-readable files.
- Backups encrypted; restore documented.
- Console never reads this tree directly; it reads via the Internal API.

## 6. Retention — الاحتفاظ

| Path | Retention |
|---|---|
| `inbox/` | 7 days then purge if processed |
| `received/` | 30 days hot, then cold archive |
| `quarantine/` | 180 days |
| `qualified/` | 90 days then archive |
| `drafts/` | until decided + 30 days |
| `decided/` | indefinite (immutable archive) |
| `risks/` | until closed + 1 year |
| `incidents/` | indefinite |

## 7. Promotion to Postgres — الترقية

- Files in `received/` are mirrored to shadow Postgres.
- Approved drafts in `decided/` are mirrored to primary Postgres via the promotion job.
- The on-disk tree remains the audit floor even after promotion.

## 8. Non-Negotiables — خطوط حمراء

- No agent writes outside its `allowed_write_targets` globs.
- No file is deleted before its hash is in the audit log.
- No restricted-tier data lives in `drafts/` or `proposals/`.
- No file is moved between dirs without an audit entry.

## 9. References — مراجع

- `docs/runtime/WORKER_ORCHESTRATOR_V1.md`
- `docs/runtime/ULTIMATE_WORKER_MESH.md`
- `docs/data/ULTIMATE_DATA_PLATFORM.md`
- `docs/security/ULTIMATE_SECURITY_GOVERNANCE.md`
