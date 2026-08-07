# No-Overclaim Policy

> **Status:** Hard policy. No claim without evidence.
> **Companion:** `docs/proposal/PROOF_PACK_TEMPLATE_AR.md` + `docs/trust/SAFE_CLAIMS_LIBRARY_AR.md`.

## The principle

> Every claim in Dealix copy is bound to a proof_id. If the proof_id is missing, the claim is not allowed.

## The 5 banned claim patterns

### 1. Guaranteed outcomes

- "نضمن X."
- "مضمون."
- "100%."
- "بدون فشل."
- "مؤكد."

These are banned in all client-facing copy.

### 2. Time-bound guarantees

- "في 30 يوم."
- "خلال أسبوع."
- "بنهاية الشهر."
- "ستلاحظ الفرق فوراً."

These imply a guarantee on the timeline. Banned.

### 3. Round numbers without baseline

- "2X."
- "10x."
- "5 أضعاف."
- "100% زيادة."

Banned unless paired with a real baseline + a proof_id.

### 4. Comparative superlatives

- "الأفضل."
- "الأقوى."
- "رقم 1."
- "ما في منافس."

Banned in all client-facing copy.

### 5. Replacement claims

- "يستبدل فريقك."
- "يحل محل VA."
- "يلغي الحاجة لـ CRM."

Banned. Dealix is a layer, not a replacement.

## The 5 allowed claim patterns

### 1. "We can show you" (evidence-bound)

- "نقدر نوريك 10 فرص ضايعة في 5 أيام."
- "نقدر نقيس [metric] في الأسبوع 2."

These are claims about Dealix's capability, not about the outcome for the client.

### 2. "We will measure" (proof-metric)

- "نحدد مقياس نجاح."
- "نقيس [metric] في الأسبوع 2 والـ 4."

These are commitments to measure, not commitments to outcomes.

### 3. "If we miss it, we stop" (founder commitment)

- "لو ما حققنا المقياس، نوقف."
- "الـ pilot بدون التزام طويل."

These are commitments from Dealix, not guarantees of client outcomes.

### 4. "Past cases ranged from X to Y" (n=3+ only)

- "في 3 حالات، النتيجة تراوحت من SAR X إلى SAR Y."

Only allowed with n=3+, anonymized, with a proof_id reference.

### 5. "It depends on" (honest framing)

- "النتائج تعتمد على النطاق والتبني."
- "ما نقدر نتوقع بدون فهم عملياتك."

This is the most honest framing. Use it when in doubt.

## The trust preflight check

The preflight flags any draft that:

- Contains a banned pattern.
- Has no `evidence_level` field.
- References a `proof_id` that does not exist in the library.
- References a `proof_id` that is expired.
- Has a number without a baseline.

## The proof pack connection

Every claim that survives the preflight references a proof pack. The proof pack has:

- `claim` (the exact claim).
- `evidence_level` (L2 minimum for client-facing).
- `evidence_type` (case_study, benchmark, audit_finding, expert_opinion).
- `source` (where the evidence came from).
- `limitation` (what the evidence does NOT support).
- `expiry_date_iso` (when to re-approve).

## The escalation

- If a draft fails the preflight, the drafter rewrites.
- If a draft passes the preflight but the founder rejects it, the founder's reason is logged.
- If a draft is approved by the founder but the preflight would reject it, the founder's override is logged with a reason.

## When to update

- When a new claim pattern emerges (e.g. a new industry enters).
- When a new proof pack is added to the library.
- When a violation occurs in the wild.
- When the policy needs to be tightened (more bans) or loosened (more allows).
