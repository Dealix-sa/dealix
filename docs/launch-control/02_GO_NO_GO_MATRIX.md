# Go / No-Go Matrix — Dealix — مصفوفة الانطلاق وعدمه

The definitive launch decision. Everything on the GO list is approved for launch. Everything on the NO-GO list stays off — no exceptions at launch. The matrix is enforced by the governing rule: the system never sends externally.

## Governing rule — القاعدة الحاكمة

**EN:** AI drafts, ranks, and recommends. Founder reviews, approves, and sends manually. The system never sends externally.

**AR:** الذكاء الاصطناعي يصيغ ويرتّب ويوصي. المؤسس يراجع ويعتمد ويرسل يدويًا. النظام لا يرسل خارجيًا إطلاقًا.

## GO — مسموح بالإطلاق

These are approved to go live.

| # | GO item — بند الانطلاق | Condition — الشرط |
|---|---|---|
| 1 | Public website launch — إطلاق الموقع العام | Manual QA complete |
| 2 | Commercial positioning — التموضع التجاري | Copy matches approved deck |
| 3 | 400 review-only drafts — 400 مسودة للمراجعة فقط | None auto-sent |
| 4 | Founder manual review — مراجعة المؤسس اليدوية | Review queue operational |
| 5 | Media / social planning — تخطيط الإعلام والتواصل | Calendar schema only |
| 6 | Manual social posting — النشر الاجتماعي اليدوي | Founder posts by hand |
| 7 | Paid diagnostics — جلسات تشخيص مدفوعة | SOP + pricing ready |
| 8 | Discovery calls — مكالمات استكشاف | Intake routes to founder |
| 9 | Proposals — العروض | Templates reviewed |
| 10 | Pilot planning — تخطيط التجربة القيادية | Scope documented |
| 11 | Analytics schema — مخطط التحليلات | No PII without basis |
| 12 | Delivery prep — تجهيز التسليم | SOPs ready |

## NO-GO — ممنوع عند الإطلاق

These are off. None may be enabled at launch.

| # | NO-GO item — بند الحظر | Why — السبب |
|---|---|---|
| 1 | Automated email sending — إرسال بريد آلي | Violates the no-send rule |
| 2 | WhatsApp cold outreach — تواصل واتساب بارد | Not an offered service; boundary breach |
| 3 | LinkedIn automation — أتمتة لينكدإن | Not an offered service |
| 4 | Website form auto-submit — إرسال النموذج آليًا | Must create review item only |
| 5 | Bulk sending — إرسال جماعي | No external send by the system |
| 6 | Paid ads live without tracking/compliance — إعلانات مدفوعة بلا تتبّع/امتثال | Unmeasured, non-compliant spend |
| 7 | Processing sensitive data before agreement — معالجة بيانات حساسة قبل الاتفاقية | PDPL and consent breach |
| 8 | External sending from GitHub Actions — إرسال خارجي من GitHub Actions | CI must never send externally |

## Decision — القرار

- **GO** only when: every GO item meets its condition **and** every NO-GO item is confirmed off.
- **NO-GO** if: any NO-GO item is enabled, or any P0 line in `01_LAUNCH_SCORECARD.md` is Red.
- Record the decision with date and owner. Attach evidence per `03_EVIDENCE_PACK.md`.

## Arabic summary — ملخص عربي

قائمة الانطلاق محددة: الموقع، التموضع، 400 مسودة للمراجعة، المراجعة اليدوية، تخطيط الإعلام، النشر اليدوي، التشخيص المدفوع، مكالمات الاستكشاف، العروض، تخطيط التجربة، مخطط التحليلات، وتجهيز التسليم. قائمة الحظر محددة كذلك: لا إرسال بريد آلي، لا تواصل واتساب بارد، لا أتمتة لينكدإن، لا إرسال آلي للنموذج، لا إرسال جماعي، لا إعلانات مدفوعة بلا تتبّع/امتثال، لا معالجة بيانات حساسة قبل الاتفاقية، ولا إرسال خارجي من GitHub Actions.

## Related — روابط

- `docs/launch-control/01_LAUNCH_SCORECARD.md`
- `docs/launch-control/03_EVIDENCE_PACK.md`
- `docs/ops/API_COMMERCIAL_LAUNCH_QA.md`

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
