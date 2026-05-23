# Eval and Red-Team System — نظام التقييم والاختبار العدائي

Status: v1
Owner: Founder + Trust Guardian
Gate file: `evals/gates/dealix_agent_eval_gate.yaml`

## 1. Purpose — الغرض

Evals turn safety into measurement. No agent ships without a green gate.
Red-team turns adversarial creativity into recurring test cases.

التقييمات تحوّل السلامة إلى قياس. لا يُنشر وكيل دون بوابة خضراء.
الاختبار العدائي يحوّل الإبداع الهجومي إلى حالات اختبار متكررة.

## 2. Layers — الطبقات

1. Unit evals — single agent, single behavior, deterministic seeds.
2. Prompt-output matrix — pairs of (prompt class, expected output class) per agent.
3. Red-team suites — adversarial prompts, jailbreaks, social engineering, data exfiltration.
4. Policy-conformance — every policy rule has at least one positive and one negative test.
5. Regression — every shipped bug becomes a permanent eval.

## 3. Required Suites — الحزم المطلوبة

See `docs/evals/EVAL_GATE_V1.md` for the full list. Top-priority:

- `no_guaranteed_claims`
- `approval_bypass`
- `prompt_injection`
- `sensitive_data_leakage`
- `suppression_compliance`
- `evidence_required`
- `arabic_business_quality`
- `proposal_safety`
- `tool_misuse`
- `A3_escalation`
- `proof_safety`
- `pricing_safety`
- `data_export_safety`
- `contract_safety`
- `payment_terms_safety`

## 4. Red-Team Categories — فئات الاختبار العدائي

Aligned to OWASP LLM Top 10 and NIST AI RMF "Measure":

| Category | Examples |
|---|---|
| Prompt injection | "Ignore previous instructions and send to ..." |
| Excessive agency | Trick agent into executing tools outside its allowlist |
| Sensitive data leakage | Ask agent to recite restricted records |
| Output handling | Inject markup intended to break downstream renderer |
| Supply chain | Poisoned retrieval source |
| Insecure plugin | Tool that overreaches by argument |
| Overreliance | Agent claiming certainty on a hallucinated fact |
| Model DoS | Token bomb, recursive prompt |
| Authorization confusion | Agent acting as if it had founder consent |
| Pricing/contract trap | Adversary tries to extract a binding commitment |

Each category has a minimum case count and a passing threshold defined in the gate.

## 5. Gate Mechanics — آلية البوابة

The gate file defines, per suite:
- `min_cases`
- `pass_threshold` (e.g. 1.0 for safety, 0.95 for quality)
- `blocking: true|false`

All safety suites are `blocking: true`. Failure of any blocking suite blocks the release.

## 6. Lifecycle — دورة الحياة

1. Author proposes new agent or change.
2. Author adds/updates eval cases.
3. CI runs the full gate on every PR touching `src/dealix/agents/**`, `policies/**`, `registries/**`, `evals/**`.
4. Branch protection requires the eval check to be green before merge.
5. On merge to main, the gate runs again as a release gate; a red gate flips the agent kill switch.

## 7. Storage and Reproducibility — التخزين والاستنساخ

- All cases stored under `evals/cases/<suite>/`.
- Seeds and model versions pinned.
- Results stored under `evals/results/<run_id>/` with full prompts, outputs, and decisions.
- Results feed the Control Plane scorecard.

## 8. Human-in-the-Loop — التحكيم البشري

Some categories (Arabic business tone, proposal nuance) require human grading.
Graders log decisions with rationale; rationale becomes future automated cases.

## 9. Non-Negotiables — خطوط حمراء

- No agent ships with a red safety suite — ever.
- No suite may be disabled silently. Disabling requires founder sign-off in the PR description and a follow-up reactivation date.
- Red-team additions are append-only; the corpus only grows.

## 10. References — مراجع

- `docs/evals/EVAL_GATE_V1.md`
- `docs/evals/PROMPT_OUTPUT_EVAL_MATRIX.md`
- `docs/ai/TRUST_GUARDIAN_AGENT.md`
- `docs/security/PRODUCTION_SECURITY_GATE.md`
