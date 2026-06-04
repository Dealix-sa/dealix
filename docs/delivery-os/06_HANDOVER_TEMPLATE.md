# Handover Template — قالب التسليم

The standard handover pack used at the end of every offer. It proves what was done, transfers what the client owns, and states limitations honestly. No lock-in.

قالب التسليم القياسي عند نهاية كل عرض. يُثبت ما تم، ويُسلّم ما يملكه العميل، ويذكر القيود بصدق. دون احتكار.

## When to use — متى يُستخدم

At Diagnostic delivery, Pilot close, each Department OS phase end, and at Retainer offboarding. Scale the depth to the offer; keep the structure identical.

## Handover pack contents — محتويات حزمة التسليم

1. **Cover summary** (AR + EN) — engagement, offer tier, dates, named owners.
2. **What was delivered** — scope completed vs. scope agreed, with any exclusions.
3. **Evidence** — run ledger export and value ledger export, with Estimated/Observed/Verified labels.
4. **Configuration and assets** — tuned prompts, policy registry export, dashboard access, integration boundaries.
5. **Documentation** — how the workflow runs, who approves what, and the review loop.
6. **Limitations** — what the work does not cover and what the numbers do not prove. See [07_proof_os/LIMITATIONS_POLICY.md](../07_proof_os/LIMITATIONS_POLICY.md).
7. **Recommended next step** — concrete and optional. See [07_EXPANSION_PLAYBOOK.md](07_EXPANSION_PLAYBOOK.md).
8. **Disclosures** — value labeling and approval boundary.

## Handover acceptance — قبول التسليم

The handover is complete when: the pack is approved in the governance ledger; the client owner has received it; access transfers are confirmed; and the engagement record is updated. For Retainer offboarding, add a clean data-deletion confirmation per the retention schedule.

## Boundaries restated — إعادة تأكيد الحدود

- **Human approval** — the handover pack itself is `draft_only` until founder approval.
- **Security** — access handed over with least privilege; any credentials rotated; PII handled per [04_data_os/PII_CLASSIFICATION.md](../04_data_os/PII_CLASSIFICATION.md).
- **No external send** — restated: the system never messaged the client's prospects or customers on their behalf.

## Bilingual delivery — التسليم ثنائي اللغة

AR section first, EN second, mirror-equivalent. File naming: `dealix_handover_<client_handle>_<offer>_<YYYYMMDD>`.

## Disclosure block (paste into every pack) — كتلة الإفصاح

> Outputs in this pack are labeled Estimated, Observed, or Verified. Estimated and Observed values are not guarantees. Dealix drafts, ranks, and recommends; humans approve and send manually; the system never sends externally.
>
> المخرجات موسومة كـ تقديرية أو ملحوظة أو مُتحقَّقة. القيم التقديرية والملحوظة ليست ضمانات. ديليكس يكتب المسودات ويرتّب ويوصي؛ والبشر يوافقون ويرسلون يدويًا؛ والنظام لا يرسل خارجيًا إطلاقًا.

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
