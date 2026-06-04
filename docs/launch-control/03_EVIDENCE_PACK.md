# Evidence Pack — Dealix Launch — حزمة الأدلة

The artifacts that prove the launch is ready and safe. The founder attaches these to the Go/No-Go decision. Evidence is produced by launch and verification scripts and stored under `outputs/`. No artifact may contain PII or unproven claims.

## Why an evidence pack — لماذا حزمة أدلة

The launch decision must be defensible. Each GO item and each NO-GO item is backed by a file the founder can open and read. If an artifact is missing, the related item is treated as Red.

## Artifact map — خريطة المخرجات

| Artifact | Path | What it proves — ما يُثبته |
|---|---|---|
| Commercial launch outputs | `outputs/commercial_launch/` | Drafts generated, all marked review-only; counts and statuses |
| Final verification (JSON) | `outputs/final_launch_control/final_verification.json` | Machine-readable launch verification result |
| Final verification (MD) | `outputs/final_launch_control/final_verification.md` | Human-readable verification summary |
| Safety audit | `outputs/final_launch_control/safety_audit.json` | No send endpoints, no outbound imports, endpoints read-only |
| API QA result | `outputs/final_launch_control/api_commercial_qa.json` | Read-only commercial endpoints present; `/health` present; no send paths |

## What each artifact must contain — ما يجب أن يحتويه كل مخرج

### `outputs/commercial_launch/`
- [ ] Count of drafts produced (target: 400 review-only).
- [ ] Every draft flagged review-only / DRAFT_ONLY; zero auto-sent.
- [ ] No external recipient was contacted.
- [ ] No PII persisted beyond what the agreement allows.

### `final_verification.json` / `.md`
- [ ] Overall status: pass / fail.
- [ ] Per-section results aligned to `01_LAUNCH_SCORECARD.md`.
- [ ] Timestamp and the commit/build reference verified.
- [ ] The `.md` mirrors the `.json` for human review.

### `safety_audit.json`
- [ ] No email/WhatsApp/LinkedIn send endpoint detected.
- [ ] No outbound send imports in the API surface.
- [ ] All listed commercial endpoints are read-only (GET).
- [ ] Result is pass with the offending paths listed if fail.

```json
{
  "audit": "safety_audit",
  "send_endpoints_found": [],
  "outbound_send_imports": [],
  "non_readonly_commercial_endpoints": [],
  "health_endpoint_present": true,
  "result": "pass"
}
```

## How evidence maps to the decision — ربط الأدلة بالقرار

| Decision item | Backing artifact |
|---|---|
| GO #3 — 400 review-only drafts | `outputs/commercial_launch/` |
| NO-GO #1, #5 — no automated/bulk send | `safety_audit.json` |
| NO-GO #8 — no external send from CI | `safety_audit.json` + CI logs |
| Scorecard C1–C2 — no send path, read-only API | `api_commercial_qa.json` |
| Overall GO/No-Go | `final_verification.json` + `.md` |

## Storage & integrity — التخزين والسلامة

- [ ] Artifacts stored under `outputs/` and referenced in the decision record.
- [ ] No artifact contains email, phone, national ID, or real customer names.
- [ ] Artifacts regenerated if the build changes before launch.

## Arabic summary — ملخص عربي

حزمة الأدلة هي ما يجعل قرار الإطلاق قابلًا للدفاع. تُنتج السكربتات مخرجات تحت `outputs/`: مخرجات الإطلاق التجاري، نتيجة التحقق النهائي بصيغتي JSON وMD، وتدقيق السلامة الذي يثبت عدم وجود نقاط إرسال خارجية وأن نقاط النهاية للقراءة فقط. أي مخرج ناقص يجعل البند المرتبط أحمر.

## Related — روابط

- `docs/launch-control/01_LAUNCH_SCORECARD.md`
- `docs/launch-control/02_GO_NO_GO_MATRIX.md`
- `docs/ops/API_COMMERCIAL_LAUNCH_QA.md`

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
