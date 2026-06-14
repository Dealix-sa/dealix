# 02 — Market Intelligence OS

**Status: BETA** · محرّك البحث والنمو — The Research & Growth Engine

> هذه هي **عدسة الأنظمة (systems lens)**. العدسة التسويقية (GTM lens) تعيش في [../01_go_to_market/MARKET_INTELLIGENCE_OS.md](../01_go_to_market/MARKET_INTELLIGENCE_OS.md) — راجعها للنمو والمبيعات. هنا نصف المحرّك كنظام.

> Market Intelligence ليست أداة تنقيب جماعي. هي **مُولِّد فرص مُثبتة بأدلة**، مُخرَجه مسودّات تنتظر موافقة المؤسس.

## الغرض — Purpose

Market Intelligence OS هو محرّك البحث الذي يحوّل سوقًا واسعًا إلى **قائمة قصيرة موثّقة بالدليل**. يبحث عن الشركات، يُصفّيها، يُسجّل دليل كل مرشّح، يُقيّمه، يكشف نقطة ضعفه التشغيلية، يقترح زاوية استهداف، ويبني مسودّات للمراجعة — **لا يرسل شيئًا**.

## القيمة للعميل — Value to Customer

- **Company Intelligence Brief** موثّق بمصدر علني لكل ادعاء.
- زاوية استهداف مبنية على ألم مرئي، لا على افتراض.
- قائمة قصيرة جاهزة للقرار، لا قائمة خام طويلة.

## القدرات الأساسية — Core Capabilities

- **Research** — بحث عن شركات ضمن قطاع/معيار محدّد.
- **Filter** — تصفية حسب ملاءمة الـ ICP.
- **Evidence record** — `evidence_source` لكل مرشّح (مصدر علني مسموح).
- **Score** — تقييم عبر [../01_go_to_market/TARGETING_SCORECARD.md](../01_go_to_market/TARGETING_SCORECARD.md).
- **Weakness detection** — كشف pain signal من دليل مرئي.
- **Angle proposal** — اقتراح زاوية استهداف مبنية على الألم.
- **Draft building** — بناء مسودّات للمراجعة البشرية فقط.

## قاعدة القُمع — The Funnel Rule

| المرحلة | العدد | البوّابة |
|---|---|---|
| Research candidates | 400 | مصدر دليل علني لكل مرشّح |
| Scored targets | 80 | اجتاز التقييم الأساسي |
| Founder shortlist | 20 | اختيار يدوي من المؤسس |
| Drafts | 10 | لكل مسودّة `evidence_source` |
| Manual sends | 5 | موافقة المؤسس + إرسال يدوي |

القُمع يضيق عمدًا: من 400 بحث إلى 5 إرسالات يدوية بالكامل. الجودة فوق الحجم.

## المُدخلات والمُخرجات — Inputs / Outputs

| المُدخلات — Inputs | المُخرجات — Outputs |
|---|---|
| قطاع/معيار + تعريف ICP | Company Intelligence Brief |
| مصادر علنية مسموحة | Scored shortlist (top 20) |
| ألم تشخيصي من Delivery OS | Drafts (10) موثّقة بالدليل |

## البوّابات والقواعد — Gates / Rules

- **Every target needs evidence** — لا `evidence_source` = لا هدف.
- **No scraping behind login** — نحترم شروط المصدر و `robots.txt`.
- **Drafts only, no auto-send** — لا يُرسَل شيء تلقائيًا.
- **No mass WhatsApp, no bulk outreach.**
- **No customer data for model training.**

راجع: [../05_governance_os/APPROVAL_POLICY.md](../05_governance_os/APPROVAL_POLICY.md) و [../02_saudi_positioning/WHATSAPP_BOUNDARY.md](../02_saudi_positioning/WHATSAPP_BOUNDARY.md).

## حلقة الرادار — The Market Radar Loop

```
market signals  →  pattern detection  →  product roadmap input
       ↑__________________________________________|
```

الألم المتكرّر بين المرشّحين يتحوّل إلى مُدخَل لخارطة المنتج: ما يطلبه السوق أكثر من مرّة يصبح ميزة، ثم منتجًا.

## الربط بالأنظمة الأخرى — Connects To

- يُغذّي **top of funnel** لـ [REVENUE_OS.md](REVENUE_OS.md).
- يُسلّم Company Intelligence Brief إلى [COMMAND_OS.md](COMMAND_OS.md).
- كل ادعاء يربطه [PROOF_OS.md](PROOF_OS.md) بدليله.
- يتعلّم من ألم التشخيص الصادر من [DELIVERY_OS.md](DELIVERY_OS.md) (Diagnostic-to-Data loop).

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
