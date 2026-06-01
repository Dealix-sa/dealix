# AI Usage Policy — سياسة استخدام الذكاء الاصطناعي

**Version:** 1.0 | **Owner:** Founder | **Effective Date:** 2026-06-01 | **Review:** Annually

Cross-links: [DATA_HANDLING_POLICY.md](DATA_HANDLING_POLICY.md) | [HUMAN_APPROVAL_MATRIX.md](HUMAN_APPROVAL_MATRIX.md) | [../01_CLAUDE.md](../01_CLAUDE.md) | [INCIDENT_RESPONSE.md](INCIDENT_RESPONSE.md)

---

## Purpose — الغرض

This policy governs how Dealix uses AI models, agents, and automated systems — both in delivering services to clients and in running internal operations. It defines what is permitted, what is prohibited, and what requires human review.

تحكم هذه السياسة كيفية استخدام ديليكس للنماذج والوكلاء الآليين والأنظمة التلقائية — سواء في تقديم الخدمات للعملاء أو في إدارة العمليات الداخلية. تحدد ما هو مسموح به وما هو محظور وما يستوجب مراجعة بشرية.

---

## 1. Permitted Uses — الاستخدامات المسموح بها

The following AI uses are approved within Dealix operations:

| Use — الاستخدام | Details — التفاصيل |
|---|---|
| Workflow automation | Automating repetitive operational tasks — report generation, data classification, alert routing |
| Draft generation | Generating drafts of outreach messages, proposals, reports, and documentation — all drafts reviewed before external use |
| Analysis and pattern recognition | Processing client operational data to identify patterns, anomalies, and optimization opportunities |
| Research and summarization | Summarizing publicly available sector information, company profiles, and industry reports |
| Internal decision support | Generating recommendations and priority lists for founder review — never replacing the review itself |
| Code generation | Generating, reviewing, and testing code for client workflow systems |
| Content drafting | Drafting bilingual (AR/EN) communications, templates, and documentation |

---

## 2. Prohibited Uses — الاستخدامات المحظورة

These uses are prohibited without exception:

| Prohibited Use — الاستخدام المحظور | Reason — السبب |
|---|---|
| Final decisions without human review | AI outputs are recommendations. No contract, message, deployment, or deletion happens without a human approving it. |
| Processing personal data (PII) without consent or DPA | PDPL violation. All personal data processing requires legal basis documented in a signed DPA. |
| Client impersonation | AI does not send messages as the client, from the client's accounts, or on behalf of the client without explicit written approval. |
| Guaranteed outcome claims | AI-generated estimates are not guarantees. No message, proposal, or report claims guaranteed results. |
| Training models on client data | Client data is never used to train, fine-tune, or evaluate any AI model without explicit written consent — which Dealix does not currently seek. |
| Autonomous external actions | AI agents do not send emails, make calls, or take actions that reach external parties without founder approval. |
| Cold automation (WhatsApp blast, LinkedIn auto-DM) | Explicitly prohibited per [../06_APPROVAL_GATES.yml](../06_APPROVAL_GATES.yml) and [../growth/ANTI_BAN_GUARDIAN.yml](../growth/ANTI_BAN_GUARDIAN.yml). |
| Storing client secrets in prompts | API keys, passwords, and credentials are never included in AI prompts or conversation history. |

---

## 3. Human Oversight Requirements — متطلبات الإشراف البشري

Every AI output that reaches or affects an external party requires human review. Reference [HUMAN_APPROVAL_MATRIX.md](HUMAN_APPROVAL_MATRIX.md) for the specific approver and SLA per action type.

| Output Type — نوع المخرج | Human Review Required | Approver |
|---|---|---|
| Outreach message draft | Yes — before any send | Founder |
| Proposal draft | Yes — before sharing with client | Founder |
| Pricing recommendation | Yes — before quoting | Founder |
| Deployment to client production | Yes | Founder |
| Client-facing report | Yes — before delivery | Founder or designated reviewer |
| Internal analysis (not shared externally) | No — auto-approved | Agent |
| Code for internal test environment | No — auto-approved | Agent |
| Code for client production | Yes | Founder |

---

## 4. Transparency Rules — قواعد الشفافية

| Rule — القاعدة |
|---|
| Clients are informed when a Dealix deliverable was generated or substantially assisted by AI — this is standard disclosure, not a liability. |
| Dealix does not represent AI-generated content as exclusively human-authored when it was not. |
| Limitations of AI outputs are declared to clients — e.g., "this classification model has a tested accuracy of [X]% on [data type]" — not presented as infallible. |
| When an AI system makes an error that affects a client, the error is disclosed per [INCIDENT_RESPONSE.md](INCIDENT_RESPONSE.md) protocols. |

---

## 5. Model Selection Principles — مبادئ اختيار النموذج

| Principle — المبدأ | Application — التطبيق |
|---|---|
| Fit for purpose | Use the model appropriate for the task. Do not use a large, expensive model for a task a smaller model handles adequately. |
| No over-capability | Do not grant a model more permissions, context, or data access than needed for the specific task. |
| Cost awareness | LLM API costs are tracked per project and included in unit economics. Unexpected cost increases are flagged. |
| No model for personal data by default | Personal data (PII) is not sent to external LLM APIs without explicit client consent and DPA coverage. |
| Fallback defined | Every system that uses an LLM has a defined fallback behavior if the model returns an error or unexpected output. |

---

## 6. Prompt Security — أمان الأوامر

| Rule — القاعدة |
|---|
| No client secrets (API keys, passwords, tokens) in any prompt |
| No client PII in prompts unless DPA explicitly covers LLM processing |
| No Dealix internal credentials in prompts |
| System prompts do not contain information that would be damaging if extracted — they should be written assuming they could be leaked |
| Prompt injection protections are implemented in any system that processes user-supplied input that feeds into a prompt |

---

## Policy Enforcement — تطبيق السياسة

Violations of this policy are reported to the Founder immediately. Any AI output that bypasses human approval gates, processes unauthorized data, or makes an external action without approval is treated as an incident per [INCIDENT_RESPONSE.md](INCIDENT_RESPONSE.md). This policy is reviewed annually or after any significant AI system change.

---

> **Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة**
