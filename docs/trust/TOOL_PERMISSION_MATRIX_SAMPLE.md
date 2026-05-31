# Tool Permission Matrix — Sample — مصفوفة صلاحيات الأدوات (عيّنة)

> **Sample — illustrative.** This matrix defines which agents may invoke which tools, and under what approval class. Cells use: `allowed`, `approval_required`, `forbidden`. Each customer engagement maintains its own matrix.
>
> **عيّنة توضيحية.** تحدّد هذه المصفوفة أي وكيل يستطيع استدعاء أي أداة، وتحت أي فئة موافقة. القيم: مسموح، يتطلب موافقة، ممنوع. لكل ارتباط مصفوفته الخاصة.

---

## 1. Matrix — المصفوفة

| Tool / Agent | `revenue_hunter` | `trust_agent` | `proposal_drafter` | `follow_up_agent` | `evidence_pack_assembler` |
|---|---|---|---|---|---|
| `email_send` | forbidden | forbidden | forbidden | approval_required (Founder) | forbidden |
| `crm_write` | approval_required (Reviewer) | forbidden | forbidden | approval_required (Reviewer) | forbidden |
| `payments_read` | forbidden | approval_required (Reviewer) | forbidden | forbidden | approval_required (Reviewer) |
| `payments_write` | forbidden | forbidden | forbidden | forbidden | forbidden |
| `file_export` | approval_required (Reviewer) | allowed | approval_required (Reviewer) | forbidden | allowed |
| `mcp_external_search` | allowed | approval_required (Reviewer) | approval_required (Reviewer) | forbidden | forbidden |
| `code_exec` | forbidden | forbidden | forbidden | forbidden | approval_required (Founder) |
| `calendar_write` | approval_required (Reviewer) | forbidden | forbidden | approval_required (Reviewer) | forbidden |
| `contract_draft` | forbidden | forbidden | approval_required (Founder) | forbidden | forbidden |

---

## 2. Per-Tool Rationale — مبرّر كل أداة

### `email_send`
External communication on the customer's behalf. Only `follow_up_agent` may draft an external message, and only with Founder-class approval per send. No automated cold outreach. Cold WhatsApp, cold email, LinkedIn automation, and scraping are not offered services.

### `crm_write`
Writing to the customer's source-of-truth system. Reviewer approval required for any write; reads default to allowed within the agent's data class boundary.

### `payments_read`
Reading payments and ledger data is treated as Regulated. Only `trust_agent` and `evidence_pack_assembler` may read, and only under Reviewer approval, for the purpose of attribution and evidence assembly.

### `payments_write`
Forbidden across all agents. No agent writes to money systems. Any future enablement would require an explicit founder decision and a new permission entry.

### `file_export`
Producing artifacts to internal storage. Allowed for `trust_agent` and `evidence_pack_assembler`; reviewer-gated elsewhere. External delivery requires a separate human-led step.

### `mcp_external_search`
External search through the MCP gateway. The gateway enforces rate limits, policy checks, and an audit trail. `revenue_hunter` has standing access for public-source research; `trust_agent` and `proposal_drafter` are reviewer-gated.

### `code_exec`
Execution of code by an agent. Forbidden by default. `evidence_pack_assembler` may invoke code execution for log compilation tasks only, under Founder-class approval, in a sandboxed environment.

### `calendar_write`
Booking on behalf of internal team members. Reviewer-gated for `revenue_hunter` and `follow_up_agent`. External invites still require the named human operator to send.

### `contract_draft`
Drafting contractual language. Allowed only for `proposal_drafter` under Founder-class approval. No agent finalizes or signs contracts.

---

## 3. Matrix Rules — قواعد المصفوفة

1. **Forbidden is forbidden.** No runtime override.
2. **Approval class is enforced at the MCP gateway.** No agent can call a tool without the policy check.
3. **Changes to this matrix require founder sign-off** and are logged in the Approval Center.
4. **Quarterly review.** A stale matrix older than 90 days triggers an out-of-cycle audit.
5. **No cross-tenant tool invocation.** A tool call is scoped to the customer tenant on whose behalf the agent is acting.

**AR.**
١. الممنوع ممنوع، ولا يُتجاوز لحظة التشغيل.
٢. فئة الموافقة تُفرض عند بوابة MCP. لا استدعاء أداة بلا فحص.
٣. تعديلات المصفوفة تستوجب اعتماد المؤسس وتُسجَّل في مركز الموافقات.
٤. مراجعة ربعية. مصفوفة أقدم من 90 يومًا تُطلق تدقيقًا خارج الدورة.
٥. لا استدعاء أداة عبر المستأجرين. كل نداء محصور بمستأجر العميل الذي يعمل الوكيل لحسابه.

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.*

Related: `/home/user/dealix/docs/trust/AGENT_REGISTRY_SAMPLE.md` · `/home/user/dealix/docs/trust/MCP_REVIEW_CHECKLIST.md` · `/home/user/dealix/docs/trust/AI_USE_POLICY_SAMPLE.md`
