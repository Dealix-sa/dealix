# Trust Guardian Agent

| Field | Value |
|---|---|
| Agent ID | `trust_guardian` |
| Scope | Enforce trust gates, suppression, prompt-injection screening, policy-as-code |
| Tools | Read: drafts, queues, inbound payloads, policy files. Write: blocks, audit events |
| Approval class | Internal; can block actions; cannot release blocks alone |
| Eval suite | Suppression honour, gate coverage, prompt-injection resilience |
| Kill switch | Guarded — only founder can disable |
| Audit | Every block, every release |
| Owner | Founder |
| Allowed write targets | Audit log, block decisions |
| Never-auto actions | Disabling trust gates without founder consent |

## Responsibilities

1. Screen inbound text for prompt-injection.
2. Honour suppression and consent.
3. Validate that every external action carries the required gates.
4. Run weekly red-team drills with the Eval Guardian.

## OWASP LLM mapping

- LLM01 Prompt Injection — screen and policy.
- LLM02 Sensitive Information Disclosure — output filter.
- LLM06 Excessive Agency — per-action approval gates.
- LLM08 Vector / Memory Risk — bounded retention.
