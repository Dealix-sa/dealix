# Failure Response Playbook — Dealix Launch — دليل الاستجابة للأعطال

What to do when something breaks during launch. Each scenario has a detect, contain, fix, and verify path. The first priority in every case is to confirm the system did not send externally.

## Severity levels — مستويات الخطورة

| Level | Meaning — المعنى | Response time |
|---|---|---|
| SEV-1 | Any external send occurred, or sensitive-data exposure | Immediate stop |
| SEV-2 | Public claim violation, or broken commercial route | Same hour |
| SEV-3 | Cosmetic or non-blocking issue | Same day |

## Scenario 1 — A message was sent externally — إرسال خارجي وقع

**SEV-1.**
- **Detect:** outcome log or audit shows a send the founder did not approve.
- **Contain:** disable the path immediately; stop the daily loop.
- **Fix:** confirm root cause; restore the no-send guarantee; re-run `safety_audit.json`.
- **Verify:** `safety_audit.json` returns pass with empty send lists.

## Scenario 2 — Forbidden claim is live — ادعاء محظور منشور

**SEV-2.**
- **Detect:** QA or a reader finds "guaranteed ROI", "100%", "replace your team", "automate everything", "no human needed", or fake urgency.
- **Contain:** remove or replace the copy at once.
- **Fix:** restore approved copy from `docs/site-launch/03_COPY_DECK_AR_EN.md`.
- **Verify:** re-run the claim-safety pass in `docs/site-launch/02_SEO_CHECKLIST.md`.

## Scenario 3 — Public route down — صفحة عامة معطّلة

**SEV-2 (commercial route) / SEV-3 (informational).**
- **Detect:** site check returns non-200 or a broken CTA.
- **Contain:** note the route; route users around it if possible.
- **Fix:** restore the route; confirm CTA targets in `docs/site-launch/01_PAGE_MAP.md`.
- **Verify:** route loads 200 in AR and EN.

## Scenario 4 — Sensitive data processed too early — معالجة مبكرة لبيانات حساسة

**SEV-1.**
- **Detect:** intake or delivery handled sensitive data before an agreement.
- **Contain:** stop processing; isolate the data.
- **Fix:** confirm PDPL-aware handling; delete or quarantine per retention policy.
- **Verify:** agreement and basis are in place before any further processing.

## Scenario 5 — API exposes a non-read-only path — نقطة نهاية غير للقراءة فقط

**SEV-1.**
- **Detect:** API QA finds a send endpoint or a non-GET commercial endpoint.
- **Contain:** disable the endpoint.
- **Fix:** restore read-only commercial surface per `docs/ops/API_COMMERCIAL_LAUNCH_QA.md`.
- **Verify:** `api_commercial_qa.json` and `safety_audit.json` both pass.

## Scenario 6 — Paid ads live without tracking/compliance — إعلانات بلا تتبّع/امتثال

**SEV-2.**
- **Detect:** ad spend started before tracking and compliance were confirmed.
- **Contain:** pause the campaign.
- **Fix:** add tracking and compliance; confirm no PII captured without basis.
- **Verify:** tracking validated, compliance recorded, then resume if approved.

## After any incident — بعد أي حادث

- [ ] Record the incident: what, when, severity, fix.
- [ ] Update the affected control doc.
- [ ] Re-run the relevant evidence artifact.
- [ ] Confirm with the scorecard before resuming the daily loop.

## Arabic summary — ملخص عربي

دليل الاستجابة يغطّي ستة سيناريوهات: إرسال خارجي، ادعاء محظور منشور، صفحة معطّلة، معالجة مبكرة لبيانات حساسة، نقطة نهاية غير للقراءة فقط، وإعلانات بلا تتبّع/امتثال. لكل سيناريو مسار: اكتشاف، احتواء، إصلاح، تحقق. الأولوية الأولى دائمًا التأكد من أن النظام لم يرسل خارجيًا.

## Related — روابط

- `docs/launch-control/03_EVIDENCE_PACK.md`
- `docs/ops/API_COMMERCIAL_LAUNCH_QA.md`
- `docs/ops/INCIDENT_RESPONSE_QUICKCARD.md`

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
