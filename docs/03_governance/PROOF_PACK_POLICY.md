# سياسة حزمة الإثبات — Proof Pack Policy

> **القاعدة / The Rule:** لا إثبات مزيّف، ولا شهادات مزيّفة. كل إثبات حقيقي وقابل للتتبع.
> **No fake proof. No fake testimonials. Every proof is real and traceable.**
> **Proof Law (`docs/00_constitution/DEALIX_LAWS.md`): لا مشروع بلا Proof Pack.**

Canonical: `CLAUDE.md` Hard rules, `docs/00_constitution/NON_NEGOTIABLES.md`,
`docs/00_constitution/WHAT_DEALIX_REFUSES.md`. Claims link here via `CLAIMS_REGISTER.md`.

## ما هي حزمة الإثبات / What a Proof Pack is

A **Proof Pack** is a self-contained, traceable evidence artifact for a single claim or deliverable. It contains:
- The **claim** it supports (must match a row in `CLAIMS_REGISTER.md`).
- The **evidence** (data, screenshots, test output, before/after, signed customer result).
- The **source** and method (how it was measured; reproducible where possible).
- **Consent status** for any customer-identifying content (see written-approval rule below).
- An **owner**, **date**, and **Proof Pack ID** used as the Evidence link in the Claims Register.

A claim cannot be marked **Evidence-backed** without a Proof Pack ID (or a passing test/code path).

## مستويات الإثبات / Evidence levels (L0–L5)

| Level | Meaning | Can it back a public "Evidence-backed" claim? |
|---|---|---|
| **L0** | Assertion only — no evidence. A **Hypothesis**, must be framed as such. | No |
| **L1** | Internal artifact / design intent / `DOCS_ONLY`. | No — internal only |
| **L2** | Working capability demonstrated internally (`INTERNAL`/`BETA`, reproducible). | Only if surface shows the real status label |
| **L3** | Verified by automated test / code path enforcing the behavior. | Yes (capability claims) |
| **L4** | Real customer result, de-identified, measured and reproducible. | Yes |
| **L5** | Named customer result with **written approval** to publish name/logo/quote. | Yes (publish-grade) |

Match the claim to the lowest sufficient level. Map module status (`docs/00_platform_truth/MODULE_STATUS_MAP.md`)
honestly — never present `FUTURE`/`BETA`/`INTERNAL`/`DOCS_ONLY` as `LIVE`.

## ممنوع / Forbidden

- **No fake proof** — no fabricated metrics, mock results presented as real, or staged screenshots.
- **No fake testimonials** — no invented quotes, no "representative" customers that do not exist.
- **No fake scarcity** — no manufactured urgency (see `NO_SPAM_POLICY.md`).
- **No guaranteed-outcome proof** — never present evidence in a way that guarantees revenue or results.
- **No publishing customer identity without written approval** (next section).

## موافقة كتابية لاسم/شعار/اقتباس العميل / Written approval to publish customer name, logo, or quote

- Publishing any **customer name, logo, or quote** requires **written approval from that customer**, recorded before publish.
- Until approval exists, present results **anonymized** (e.g. "a Riyadh-based distributor"), i.e. L4 not L5.
- The publish action itself is a customer-facing external action and goes through `HUMAN_APPROVAL_POLICY.md`
  (drafted, queued, founder-approved). The written customer consent is attached to the Proof Pack and Decision Passport.

## الربط بسجل الإدعاءات / Linking proof to the Claims Register

1. Create the Proof Pack and assign a Proof Pack ID.
2. In `CLAIMS_REGISTER.md`, set the claim's **Status** to Evidence-backed and put the Proof Pack ID in **Evidence link**.
3. If no Proof Pack exists yet, the claim stays **Hypothesis** and the surface must read as a hypothesis.
4. If a claim was unsafe and reworded, log it as **Rewritten** with both versions.

> No public claim ships without either a Proof Pack (Evidence-backed) or explicit hypothesis framing.
