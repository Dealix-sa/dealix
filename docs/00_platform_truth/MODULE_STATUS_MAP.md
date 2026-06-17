# Module Status Map — خريطة حالة الوحدات

> الحقيقة الصادقة عن **ما هو جاهز اليوم** مقابل **ما هو رؤية**. الشركة ذات الأنظمة الأربعة عشر هي الهدف؛ الجاهز للبيع الآن هو الإسفين فقط.
> The honest truth about **what is ready today** vs. **what is vision**. The 14-OS company is the goal; what is sellable now is the wedge only.
>
> المصدر الأعلى / Upstream truth: `PLATFORM_SOURCE_OF_TRUTH.md`.

الحالة / Status: **LIVE (canonical)** · آخر تحديث / Last updated: 2026-06-05

---

## 1. وسوم الحالة / Status Labels

| الوسم / Label | المعنى / Meaning |
|---|---|
| **LIVE** | يعمل في الإنتاج ويُسلَّم لعملاء حقيقيين. Running in production, delivered to real customers. |
| **BETA** | يعمل لكن تحت تجربة محدودة ومراقبة. Working but under limited, monitored trial. |
| **INTERNAL** | يعمل لكن للفريق فقط، لا يُباع. Works, internal-only, not sold. |
| **DOCS_ONLY** | موصوف في الوثائق فقط، لا كود تشغيلي بعد. Documented only, no operating code yet. |
| **BLOCKED** | متوقّف بانتظار قرار/مصدر/قانون. Blocked pending a decision/source/legal. |
| **FUTURE** | على الروادماب، لم يبدأ. On the roadmap, not started. |
| **DEPRECATED** | كان موجودًا، أُوقف. Existed, retired. |

---

## 2. حالة الأنظمة الأربعة عشر / The 14 OS Status

| # | النظام / OS | الحالة / Status | يُباع الآن؟ / Sellable now? | المالك / Owner | بوّابة الترقية / Gate to advance |
|---|---|---|---|---|---|
| 01 | Command OS | **BETA** | نعم — ضمن Command Pack. Yes, inside the pack. | Founder | 3 Command Packs مُسلَّمة بثبات. |
| 02 | Market Intelligence OS | **BETA** | نعم — Company Intelligence Brief. | Founder | جودة دليل ثابتة عبر 3 تسليمات. |
| 03 | Revenue OS | **BETA** | نعم — Revenue Map. | Founder | Revenue Map مُتبنّى من عميل واحد. |
| 04 | Proof OS | **LIVE** | نعم — Proof Register/Pack. Code chain موجود. | Founder | 3 Proof Packs مكتملة. |
| 05 | Delivery OS | **BETA (Lite)** | جزئيًّا — Next Action Board فقط. Partial. | Founder | لوح تسليم كامل بمهام وحالات. |
| 06 | Client OS | **DOCS_ONLY** | لا / No. | Founder | أول عميل Managed نشط. |
| 07 | Support OS | **DOCS_ONLY** | لا / No. | Founder | حاجة دعم حقيقية من عميل Executive. |
| 08 | Finance OS | **BETA (payments)** | جزئيًّا — Moyasar sandbox فقط. Sandbox only. | Founder | تسوية إنتاج + ربط ربحية لكل عميل. |
| 09 | Data OS | **LIVE** | بنية تحتية — PDPL، تصنيف PII، مصدر. Infrastructure. | Founder | سجلّ احتفاظ + تدقيق دوري مُفعَّل. |
| 10 | Governance OS | **LIVE** | بنية تحتية — بوّابات وموافقات تحكم الإسفين. | Founder | فئات A0–A5 مُؤتمتة كاملة. |
| 11 | Knowledge OS | **INTERNAL** | لا للبيع — يُسرّع التسليم داخليًّا. | Founder | مكتبة قوالب موسومة ومعاد استخدامها. |
| 12 | Agent OS | **BETA** | لا للبيع — وكلاء داخليون بعقود. Internal agents. | Founder | عقود + اختبارات + rollback لكل وكيل. |
| 13 | Partner OS | **FUTURE** | لا / No. | Founder | أول شريك توزيع موقَّع. |
| 14 | Academy OS | **FUTURE** | لا / No. | Founder | أول منهج تدريب مُسلَّم لفريق عميل. |

---

## 3. حالة مخرجات Command Sprint / Sprint Sub-deliverable Status

| المخرَج / Deliverable | النظام المصدر / Source OS | الحالة / Status | جاهز للبيع؟ / Sellable? | بوّابة الترقية / Gate |
|---|---|---|---|---|
| Company Intelligence Brief | Market Intelligence | **BETA** | نعم / Yes | جودة دليل ثابتة + مصدر موثّق. |
| Revenue Map | Revenue OS | **BETA** | نعم / Yes | اعتماد العميل للخريطة. |
| Proof Register | Proof OS | **LIVE** | نعم / Yes | — (جاهز). |
| Executive Command Brief | Command OS | **BETA** | نعم / Yes | قرار تالٍ واضح يخرج منه. |
| Approval Register | Governance OS | **LIVE** | نعم / Yes | — (جاهز). |
| Next Action Board | Delivery OS Lite | **BETA** | نعم / Yes | ترقية إلى لوح تسليم كامل. |

---

## 4. ملخّص: يُباع الآن مقابل المستقبل / Sellable Now vs. Future

### يُباع الآن / Sellable Now (الإسفين / the wedge)
- **Free Business Diagnostic** (تشخيص).
- **Dealix Command Sprint** → Command Pack كامل.
- الأنظمة التي تشغّله: Market Intelligence, Revenue, **Proof (LIVE)**, Command, **Governance (LIVE)**, Delivery Lite.
- بنية تحتية حقيقية تحته: **Data OS (LIVE)**, **Governance OS (LIVE)**, Payments (Moyasar sandbox).

### قريب / Near (بعد إثبات الإسفين / after the wedge proves)
- Business OS Setup + **Managed Business OS** (Starter Command, Business Ops) — يعتمدان على ترقية Client + Delivery من BETA إلى LIVE.

### مستقبل / Future (رؤية لا عرض / vision, not offer)
- Client OS, Support OS, Finance OS (كامل), Partner OS, Academy OS, Executive OS.
- هذه **لا تُباع اليوم** ولا تُذكر كقدرة جاهزة في أي رسالة عميل.

> القاعدة الصادقة: إن لم يكن الوسم `LIVE` أو `BETA`، **لا يُباع ولا يُوعَد به**. نبيع ما نسلّمه، ونوثّق ما نخطّط له.

---

## روابط مرجعية / Cross-links

- المصدر الكامل / Source of truth: `PLATFORM_SOURCE_OF_TRUTH.md`
- البنية / Architecture: `DEALIX_BUSINESS_OS_ARCHITECTURE.md`
- سلّم العروض / Offer ladder: `PRODUCT_FAMILY_MAP.md`
- برج التحكّم / Control tower: `LAUNCH_CONTROL_TOWER.md`

---

*القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.*
