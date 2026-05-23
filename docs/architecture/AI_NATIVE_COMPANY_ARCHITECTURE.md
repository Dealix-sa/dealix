# AI-Native Company Architecture

Dealix is built as a founder-controlled, trust-gated AI-native company.
Architecture has three layers:

## 1. Human Layer

The founder runs the company through the Founder Console
(`apps/web/app/*`). Every external-impact decision is taken by a human.

## 2. Trust Layer

- Policy-as-Code (`policies/dealix_control_policy.yaml`)
- Agent Registry (`registries/agent_registry.yaml`)
- Eval Gate (`evals/gates/dealix_agent_eval_gate.yaml`)
- Audit log (private ops `trust/approval_decisions.csv`)
- Suppression list + trust flags (private ops)
- Internal API auth gate (`DEALIX_INTERNAL_TOKEN`)

## 3. Agent + Runtime Layer

- AI agents prepare, draft, score, and classify — never send.
- Workers update `runtime/worker_state.csv` and write report CSVs to
  the private ops tree.
- Internal API serves the Founder Console and records every decision.

## Data flow

```
public sources → research → lead_intelligence
intel + signals → outreach_draft (A2) → approval_queue
founder approval → approval_decisions (audit)
approved+allowed → external worker dispatch (manual or gated)
replies → conversation_log → reply_classifier → next agent
won deals → proposal_queue → finance/cash_collected
```
