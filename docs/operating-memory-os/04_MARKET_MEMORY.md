# ذاكرة السوق | Market Memory

> **AR:** ذاكرة السوق تجمع الإشارات والفرضيات حول القطاعات التي تعمل بها Dealix، مع مستوى ثقة ومرجع إثبات لكل سجل. الهدف بناء فهم تراكمي للسوق يُبنى على أدلة لا على انطباعات.
>
> **EN:** Market Memory captures signals and hypotheses about the sectors Dealix operates in, each with a confidence level and an evidence reference. The goal is a cumulative, evidence-based market understanding rather than impressions.

## بنية السجل | Record Structure

| الحقل Field | الوصف Description |
|---|---|
| `id` | معرّف السجل / record id |
| `sector` | القطاع / sector |
| `signal` | الإشارة الملاحَظة / observed signal |
| `hypothesis` | الفرضية المستنتجة / derived hypothesis |
| `confidence` | low \| medium \| high |
| `evidence_ref` | مرجع الدليل / evidence reference |
| `status` | draft \| approved \| archived |

## مصادر الإشارات | Signal Sources

- محادثات عملاء موثّقة بموافقة. / Approved, documented client conversations.
- أبحاث منشورة علنًا ومُقتبسة بمصدرها. / Publicly published research, cited.
- ملاحظات المؤسس الميدانية. / Founder field notes.

> **لا كشط** ولا جمع آلي لبيانات الطرف الثالث. / No scraping, no automated third-party data collection.

## مستويات الثقة | Confidence Levels

| المستوى Level | المعنى Meaning |
|---|---|
| `low` | إشارة مفردة غير مؤكدة / single unconfirmed signal |
| `medium` | إشارتان أو أكثر متوافقتان / two+ aligned signals |
| `high` | أدلة متعددة قابلة للتحقق / multiple verifiable evidences |

## الاستخدام | Usage

- يغذّي معايير التوسّع الرأسي في `../scale-readiness-os/02_VERTICAL_EXPANSION_CRITERIA.md`. / Feeds vertical-expansion criteria.
- يُربط بسجلات القرار عند تحديد الأولويات. / Linked to decision records when prioritizing.

## حدود الأمان | Safety Boundaries

- كل فرضية تبقى فرضية حتى يثبتها دليل — لا ادعاءات غير مثبتة. / Every hypothesis stays a hypothesis until proven — no unproven claims.
- AI prepares, Founder approves, Manual action only, No external sending.
- لا جذب وهمي ولا أرقام سوق مُختلقة. / No fake traction and no fabricated market numbers.
