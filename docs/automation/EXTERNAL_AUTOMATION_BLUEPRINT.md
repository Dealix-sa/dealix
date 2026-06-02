# Dealix External Automation Blueprint · مخطط الأتمتة الخارجية

> The external layer (n8n / Make / Zapier) is Dealix's **senses and reminders** —
> it gathers signals and prepares drafts. It **never** sends to a customer on its own.
> الطبقة الخارجية تجمع الإشارات وتجهّز المسودات، ولا ترسل لأي عميل من تلقاء نفسها.

This blueprint maps the external automation brain onto surfaces that **already exist**
in the repo, so nothing here is greenfield and nothing breaks the build.

Read first: [`AUTOMATION_PERMISSION_MODEL.md`](AUTOMATION_PERMISSION_MODEL.md) — every
workflow below operates at **`report_only` / queue-only** by default.

---

## 0) The hard line · الخط الأحمر

> **Master rule (`AGENTS.md`): never enable auto external sends in any environment.**

External workflows may:
- **read** signals (forms, sheets, GitHub, Railway, CRM),
- **write** drafts/reports into the repo or a ledger,
- **queue** an outreach draft for founder approval,
- **notify the founder** (the founder is an internal recipient, not a customer).

External workflows may **not**:
- send a message to a prospect/customer,
- scrape, run LinkedIn automation, or send cold WhatsApp (doctrine §3),
- write secrets into the repo or logs.

The boundary is enforced server-side: customer outreach flows through
`auto_client_acquisition/email/compliance.py::check_outreach` and the
`governance_os` gate — both reject un-approved or non-compliant sends.

---

## 1) Connection points (real) · نقاط الربط الحقيقية

| Concern | What already exists | How external layer connects |
| --- | --- | --- |
| Webhook entry | `api/routers/automation.py` (`/api/v1/automation/*`) | n8n → HTTP node → these endpoints |
| Signature verify | `api/security/webhook_signatures.py` (HubSpot, Calendly, **n8n**) | n8n HMAC header verified server-side; 401 on mismatch |
| Shared secret | pattern: `*_WEBHOOK_SECRET` in `.env.example` (e.g. `MOYASAR_WEBHOOK_SECRET`, `CALENDLY_WEBHOOK_SECRET`) | set an `N8N_WEBHOOK_SECRET` on the server; never commit it |
| CRM | HubSpot sync (`HUBSPOT_ACCESS_TOKEN`) | n8n reads/writes via HubSpot node |
| Booking | Calendly webhooks → `POST /api/v1/webhooks/calendly` | n8n listens / forwards |
| Read-only status | `GET /api/v1/automation/status`, `GET /api/v1/automation/today` | n8n polls for the daily plan |
| Founder brief | `scripts/dealix_founder_daily_brief.py` (`make cockpit`), `scripts/dealix_morning_digest.py` (`make v5-digest`) | n8n triggers / formats / delivers to founder |

> The endpoints `POST /api/v1/automation/daily-targeting/run` and
> `/api/v1/automation/followups/run` **build and queue** the plan; they do not send.
> Sending stays a separate, approval-gated human step.

---

## 2) Core workflows · مسارات العمل الأساسية

Each is **trigger → read → draft/queue → notify founder**. None auto-sends.

### 1. Founder Morning Brief · ملخص الصباح
- **Trigger:** daily 08:00 KSA.
- **Read:** GitHub open PRs + failed workflow runs; `GET /api/v1/automation/today`; `data/founder_briefs/`.
- **Draft:** Arabic founder brief (most-revenue-now, top PR to review, top tech risk, top prospect to chase, one Claude mission for today).
- **Deliver:** to the **founder** (Gmail / Telegram). Internal recipient — allowed.

### 2. New Lead Intake → GitHub Issue · التقاط ليد
- **Trigger:** new Google-Sheet row / HubSpot contact.
- **Action:** open a GitHub Issue using the `agent-command` template (`autonomy: pr_only`) asking the agent to create a bilingual outreach **draft**, discovery questions, suggested offer, and a risk note under `sales/prospects/<company>.md`.
- **Never:** message the lead directly.

### 3. Failed-CI Auto-Repair Request · إصلاح فشل CI
- **Trigger:** a workflow run fails.
- **Action:** open an Issue (`agent-command`, `pr_only`) with the workflow name, run URL, and failure summary, asking for a small PR that fixes the root cause. **Do not skip tests. Do not weaken CI.**

### 4. Revenue Follow-up (queue-only) · متابعة الإيراد
- **Data:** CRM / a prospect ledger.
- **Rule:** `contacted` + no reply after 2/4/7 days → prepare follow-up **draft #1/#2/breakup**; `replied positive` → create a discovery-call checklist; `demo booked` → create a client-prep doc.
- **Output:** drafts **queued** for founder approval — the founder releases each send.

### 5. Deploy Monitor · مراقبة النشر
- **Trigger:** Railway deploy status webhook.
- **Action:** on failure, alert the founder and open an Issue. (Deploy itself stays in GitHub Actions — see permission model L4/L5.)

### 6. Weekly Board Report · تقرير المجلس الأسبوعي
- **Trigger:** weekly.
- **Action:** assemble `reports/weekly/BOARD_REPORT.md` from PRs, KPIs, and the founder ledgers; deliver to the founder.

---

## 3) Automation matrix · مصفوفة الأتمتة

| Domain | Automation | Tool | Output (draft/queue only) |
| --- | --- | --- | --- |
| Code | CI + agent PRs | GitHub Actions | reviewable PRs |
| Sales | lead → draft → follow-up | n8n + Sheets/HubSpot | queued drafts |
| Marketing | sector research | n8n + agent | playbooks (PR) |
| Ops | onboarding SOP | agent | ops docs (PR) |
| Support | incident issue | GitHub | fast-fix PR |
| Deploy | staging after green CI | Railway + Actions | staging |
| Production | manual-approval deploy | GitHub Environment | safe release |
| Reports | daily/weekly briefs | scripts + n8n | founder clarity |
| Security | secret scan + audit | Actions (`security.yml`, CodeQL, Scorecard) | leak prevention |

---

## 4) Operating n8n safely · تشغيل n8n بأمان

- Keep n8n **updated** and isolate Code nodes / task runners (known CVE history in the Python Code node — patched in recent releases; do not run untrusted code nodes).
- Store every credential in n8n's credential store or the server env — **never** in a workflow JSON committed to git.
- Verify the `N8N_WEBHOOK_SECRET` HMAC on every inbound call (`webhook_signatures.py`); return 401 on mismatch.
- Treat n8n as **L0–L1 + queue** only. Escalation to L2+ happens **inside** GitHub (PRs), where review and audit live.

**Related:** [`AUTOMATION_PERMISSION_MODEL.md`](AUTOMATION_PERMISSION_MODEL.md) ·
[`CLOUD_CODE_COMMAND_CENTER.md`](CLOUD_CODE_COMMAND_CENTER.md)
