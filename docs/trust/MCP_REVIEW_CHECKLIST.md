# MCP Review Checklist — قائمة مراجعة بوابة MCP

Used before wiring any new MCP server or tool into a deployed agent. No exceptions; every item must be checked, with the result logged in the Approval Center and signed off per the approval class declared for the tool.

تُستخدَم قبل توصيل أي خادم أو أداة MCP إلى وكيل منشور. بلا استثناءات؛ يُفحص كل بند وتُسجَّل النتيجة في مركز الموافقات ويُعتمد وفق الفئة المُعلَنة.

---

## A. Identity & Ownership — الهوية والملكية

- [ ] **A.1** The MCP server has a single, named owner inside the customer or Dealix team.
- [ ] **A.2** Vendor identity is verified against an authoritative source (vendor domain, signed binary, or vetted package registry).
- [ ] **A.3** The owner has signed a written undertaking acknowledging the policy obligations of the tool.
- [ ] **A.4** Backup owner is named and reachable.

## B. Data Exposure — انكشاف البيانات

- [ ] **B.1** Data classes the tool will read are enumerated (Public / Internal / Customer-Tenant / Regulated / Secret).
- [ ] **B.2** Data classes the tool may write or transmit are enumerated separately.
- [ ] **B.3** Cross-tenant exposure is explicitly forbidden or, if required, routed through a documented Founder-class approval.
- [ ] **B.4** PII or PDPL-regulated fields are redacted or tokenized before tool invocation.
- [ ] **B.5** A data flow diagram is attached.

## C. Write Capabilities — قدرات الكتابة

- [ ] **C.1** Every write capability is listed individually (create, update, delete, archive).
- [ ] **C.2** Writes to money systems are forbidden by default; any exception requires explicit Founder-class approval.
- [ ] **C.3** Writes to contract systems are forbidden without a named human signatory.
- [ ] **C.4** Idempotency keys are required for write operations where the tool supports them.

## D. Rate Limits & Cost — التحديد والتكلفة

- [ ] **D.1** Rate limits are configured at the MCP gateway (per second, per minute, per day).
- [ ] **D.2** A cost ceiling is configured per agent per day; alert thresholds at 60% and 90%.
- [ ] **D.3** Backoff and circuit-breaker behaviour are documented and tested.

## E. Prompt-Injection Surface — سطح حقن الموجّهات

- [ ] **E.1** Inputs the tool returns to the agent are classified (trusted / untrusted).
- [ ] **E.2** Untrusted content is wrapped in a quarantine block before reaching the model.
- [ ] **E.3** Tool descriptions and parameter names are reviewed for instruction-following bait.
- [ ] **E.4** A red-team session has been run against the tool with at least three injection patterns and the outcomes logged.

## F. Secrets Handling — معالجة الأسرار

- [ ] **F.1** Credentials are stored in the approved vault — never in environment variables visible to the agent runtime.
- [ ] **F.2** Tokens are scoped to the minimum required permission set.
- [ ] **F.3** Rotation schedule is set and recorded.
- [ ] **F.4** No secret value appears in any agent prompt or log entry — confirmed by a redaction sweep.

## G. Kill-Switch Path — مسار مفتاح الإيقاف

- [ ] **G.1** A documented kill switch can disable the tool within five minutes for all agents.
- [ ] **G.2** The kill-switch owner is the Founder office; delegations are explicit and logged.
- [ ] **G.3** Kill-switch invocation produces an Evidence Pack delta entry automatically.
- [ ] **G.4** A quarterly fire-drill is scheduled.

## H. Audit Hooks — خطاطيف التدقيق

- [ ] **H.1** Every tool invocation is logged with actor, action, target, payload hash, approval class, approver, and timestamp.
- [ ] **H.2** Logs are tamper-evident (signed or append-only).
- [ ] **H.3** Logs are queryable from the Evidence Pack assembly pipeline.
- [ ] **H.4** Retention windows are set per the Data Boundaries policy.

## I. Approval Class & Review Cadence — فئة الموافقة ودورية المراجعة

- [ ] **I.1** The tool's approval class is declared (Auto / Reviewer / Founder / Board) and recorded in the Tool Permission Matrix.
- [ ] **I.2** Approval class changes require founder sign-off.
- [ ] **I.3** Review cadence is set (default: quarterly).
- [ ] **I.4** Any S0 or S1 incident triggers an out-of-cycle review.

## J. Documentation & Customer Disclosure — التوثيق والإفصاح للعميل

- [ ] **J.1** The tool is reflected in the Tool Permission Matrix delivered to the customer.
- [ ] **J.2** Material changes are communicated to the customer's executive sponsor before activation.
- [ ] **J.3** The Evidence Pack template includes the tool in its snapshots.
- [ ] **J.4** A plain-language summary of the tool's purpose is filed for the customer audit committee.

---

## Sign-off — الاعتماد

```
Tool: __________________________________________
MCP server identity: ___________________________
Approval class: Auto / Reviewer / Founder / Board
Reviewer name: _________________________________
Founder approval (if applicable): ______________
Date: __________________________________________
Approval reference: ____________________________
```

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.*

Related: `/home/user/dealix/docs/trust/TOOL_PERMISSION_MATRIX_SAMPLE.md` · `/home/user/dealix/docs/trust/DATA_BOUNDARIES_SAMPLE.md` · `/home/user/dealix/docs/trust/INCIDENT_RESPONSE_SAMPLE.md`
