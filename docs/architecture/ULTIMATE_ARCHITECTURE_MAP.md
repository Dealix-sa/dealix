# Ultimate Architecture Map — الخريطة المعمارية الشاملة

Status: v1
Owner: Founder

## 1. Purpose — الغرض

A single map that any new engineer, founder, or auditor can read in fifteen minutes to know exactly how Dealix is wired.

خريطة واحدة يقرأها مهندس جديد أو مؤسس أو مدقق خلال خمس عشرة دقيقة ليفهم بنية Dealix بالكامل.

## 2. Top-Level Diagram (Logical) — المخطط المنطقي

```
                        +-----------------------------+
                        |    Founder Console (L18)    |
                        +--------------+--------------+
                                       |
                        +--------------v--------------+
                        |     Control Plane API (L17) |
                        +--------------+--------------+
                                       |
                +----------------------+----------------------+
                |                      |                      |
        +-------v-------+      +-------v-------+      +-------v-------+
        | Approvals(L14)|      |  Audit (L15)  |      | Observability |
        +-------+-------+      +-------+-------+      |    (L16)      |
                |                      |              +-------+-------+
                |                      |                      |
        +-------v----------------------v----------------------v-------+
        |              Trust Guardian (L11) — fail closed             |
        +-------+-------------------+-----------------+---------------+
                |                   |                 |
        +-------v------+    +-------v------+   +------v-------+
        | Agent Runtime|    | Eval Gate    |   | Tool Layer   |
        |   (L10)      |    |   (L12)      |   |   (L9)       |
        +-------+------+    +--------------+   +------+-------+
                |                                     |
        +-------v------+                       +------v-------+
        | LLM Gateway  |<----------------------+ Workers (L13)|
        |   (L8)       |                       +------+-------+
        +--------------+                              |
                                              +-------v------+
                                              | Storage (L4) |
                                              +--------------+
```

## 3. Source Layout — تنظيم الكود

```
/policies/                          # L6
/registries/                        # L7
/evals/                             # L12
  /gates/
  /cases/
  /results/
/src/dealix/
  /agents/                          # L10
  /guardian/                        # L11
  /llm/                             # L8
  /tools/                           # L9
  /workers/                         # L13
  /approvals/                       # L14
  /audit/                           # L15
  /observability/                   # L16
  /api/internal/control/            # L17
/web/                               # L18
/docs/                              # this tree
/opt/dealix-ops-private/            # runtime artifacts (private, outside repo)
```

## 4. Boundary Map — حدود الثقة

| Boundary | From | To | Control |
|---|---|---|---|
| Internet | Visitor | Public site | WAF, no auth |
| Founder | Browser | Founder Console | Founder identity + IP allowlist |
| Console | Browser | Control Plane API | Internal token, audit |
| Internal | Console | Approvals/Audit/Observability | Same token, scoped |
| Runtime | Worker | LLM Gateway | Service identity, key isolation |
| Runtime | Agent | Tool | Allowlist enforcement |
| Runtime | Agent | Storage | `allowed_write_targets` only |
| Runtime | Any | Outbound network | Disallowed by default |

## 5. Data Map — خريطة البيانات

- Public: site copy, brand assets.
- Internal: ICP rubric, drafts, scorecards.
- Confidential: customer engagement records, pilot scorecards.
- Restricted: PII at full fidelity, payment data — agent prompts cannot see this tier.

## 6. Deployment Topology — طوبولوجيا النشر

- Web app and APIs deployed to managed environment with TLS and WAF.
- Worker mesh runs on the same cluster with separate service identity.
- Postgres primary, with read replicas as needed; backups daily; PITR enabled.
- LLM keys stored in a secrets manager, scoped per agent.

## 7. Failure Domains — مناطق الفشل

| Domain | Blast Radius | Mitigation |
|---|---|---|
| LLM provider outage | Drafting paused | Fallback provider; cached briefings |
| Postgres outage | Writes paused | CSV shadow retained; read-only mode |
| Worker host down | Schedule slip | Heartbeat alerts; auto-restart |
| Guardian crash | All writes blocked | Page founder; fail closed |
| Control plane down | Console blind | Static "service offline" banner |

## 8. Change Management — إدارة التغيير

- Branch protection requires: eval gate, security gate, lint, tests.
- All policy/registry changes require Trust Guardian review label.
- All releases tagged; deployments tracked for DORA.

## 9. References — مراجع

- `docs/architecture/AI_NATIVE_COMPANY_ARCHITECTURE.md`
- `docs/data/ULTIMATE_DATA_PLATFORM.md`
- `docs/runtime/WORKER_ORCHESTRATOR_V1.md`
- `docs/security/ULTIMATE_SECURITY_GOVERNANCE.md`
