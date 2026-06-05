# Outreach Draft Lab

> النظام يبني درافتات، لكنه لا يرسل. كل رسالة يدوية وبموافقة المؤسس.

The Draft Lab composes tailored, evidence-backed outreach drafts and **queues them
for manual founder review and manual send**. It never sends. Engine:
`scripts/targeting_draft_lab.py`.

---

## Draft types

```
first_touch_message.md      follow_up_message.md
diagnostic_invite.md        command_sprint_offer.md
partner_outreach.md         post_diagnostic_summary.md
proposal_note.md
```

The router's `draft_type` selects the template. The default first touch is the
Command Sprint offer message.

---

## Every draft must contain

- Company name.
- A stated **reason for targeting** (a positive signal).
- A **respectfully-phrased weakness / opportunity** (opportunity, not criticism).
- A suitable **offer**.
- **One** CTA.
- No exaggerated promises.
- No auto-send.

These rules are enforced in code by `validate_draft()`:

| Check | Fails if |
|-------|----------|
| `missing_company_name` | no company name |
| `missing_evidence` | no `source_urls` |
| `cta_must_be_single` | more or fewer than one `؟`/`?` |
| `banned_phrase:*` | contains a guarantee / hype phrase (نضمن، مضمون، 100%، 10x، …) |
| `auto_send_must_be_false` | `auto_send` is truthy |
| `founder_approval_required` | `approval_required != "founder"` |

---

## Template (AR)

```
السلام عليكم [الاسم]،
راجعت حضور [الشركة] بشكل سريع، وواضح أن عندكم [إشارة إيجابية].
الفرصة التي لاحظتها ليست "أداة AI" فقط، بل تنظيم أول operating loop حول:
الفرص، المتابعة، الدليل، والقرار التنفيذي القادم.
أبني Dealix كنظام تشغيل أعمال AI للشركات السعودية. نبدأ عادة بـ Command Sprint
لمدة 7 أيام يطلع: Revenue Map، Proof Register، Executive Command Brief، Next Action Board.
بدون إرسال تلقائي أو وعود مبالغ فيها. فقط تشخيص وتشغيل أولي قابل للمراجعة.
يناسبك أرسل لك Diagnostic مختصر؟
```

---

## Output

`out/drafts_for_review.md` — each block is stamped:

```
<!-- DRAFT — APPROVAL_REQUIRED: founder — DO NOT AUTO-SEND -->
…
**APPROVAL_REQUIRED:** founder · **AUTO_SEND:** false
```

```bash
python scripts/targeting_draft_lab.py \
  --in data/targeting/company_master.jsonl --out data/targeting/out --limit 10
```

Tested by `tests/test_targeting_pipeline.py`.
