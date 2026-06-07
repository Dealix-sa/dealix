export const metadata = {
  title: "خدمات Dealix — كتالوج أنظمة الذكاء الاصطناعي للشركات السعودية",
  description:
    "كتالوج Dealix الكامل: من تدقيق الـ workflow بأسبوع إلى أنظمة AI Agentic للصيانة والمشاريع والإيرادات والحوكمة، مع دعم وتطوير مستمر. AI يكتب، أنت ترسل.",
};

// ── Types ──────────────────────────────────────────────────────────────────

type PriceSar = {
  min: number;
  max: number;
  typical?: number;
  monthly?: boolean;
  note_ar?: string;
};

type Category =
  | "entry"
  | "pilot"
  | "vertical_system"
  | "governance"
  | "retainer"
  | "expansion";

interface Offer {
  id: string;
  name: string;
  name_ar: string;
  tagline: string;
  category: Category;
  price: PriceSar;
  best_for: string[];
  highlights: string[]; // deliverables or outcomes (Arabic labels)
}

// ── Catalog (hardcoded from os/03_OFFERS.yml — kept in sync manually) ────────

const offers: Offer[] = [
  {
    id: "WFA",
    name: "Agentic AI Workflow Audit",
    name_ar: "تدقيق الـ Workflow بالذكاء الاصطناعي",
    tagline:
      "نحلل workflow واحد ونطلع لكم خريطة كاملة لفرص AI Agents خلال 7 أيام",
    category: "entry",
    price: { min: 5000, max: 25000, typical: 15000 },
    best_for: [
      "شركات غير متأكدة من أين تبدأ مع الذكاء الاصطناعي",
      "فرق عمليات تعتمد على workflows يدوية",
      "شركات لديها مهام تقارير متكررة",
    ],
    highlights: [
      "خريطة الـ workflow الحالي خطوة بخطوة",
      "خريطة نقاط الألم والهدر والتكرار",
      "خريطة فرص إدخال AI Agents عمليًا",
      "خطة pilot لـ 30 يومًا + تقدير التكلفة",
    ],
  },
  {
    id: "AWP",
    name: "Agentic Workflow Pilot",
    name_ar: "تجربة Workflow بالـ Agentic AI",
    tagline: "نبني نموذج عملي يثبت القيمة خلال 30 يوم",
    category: "pilot",
    price: { min: 30000, max: 150000, typical: 75000 },
    best_for: [
      "شركات أنهت تدقيق الـ workflow وجاهزة لإثبات القيمة",
      "فرق تريد نموذجًا عمليًا على بيانات حقيقية",
      "شركات تريد مسار demo يعمل قبل التوسعة",
    ],
    highlights: [
      "نموذج عملي (prototype) على بيانات حقيقية أو عيّنة",
      "agent flow مُختبر ومُوثّق",
      "نقاط موافقة بشرية مُفعّلة",
      "وثيقة تسليم تقني + توصية المرحلة التالية",
    ],
  },
  {
    id: "MIOS",
    name: "Maintenance Intelligence OS",
    name_ar: "نظام الذكاء الاصطناعي للصيانة",
    tagline: "نظام AI Agentic متكامل لإدارة الصيانة، الفنيين، SLA، والتقارير",
    category: "vertical_system",
    price: { min: 40000, max: 500000, typical: 150000 },
    best_for: [
      "شركات إدارة المرافق",
      "مقاولو الصيانة",
      "فرق الخدمة الميدانية",
    ],
    highlights: [
      "كل بلاغ له SLA واضح ومتابعة تلقائية",
      "كشف الأعطال المتكررة قبل أن تتفاقم",
      "تقارير الفنيين تُولَّد تلقائيًا",
      "dashboard للإدارة يحدّث نفسه",
    ],
  },
  {
    id: "PCOS",
    name: "Project Controls AI OS",
    name_ar: "نظام الذكاء الاصطناعي للتحكم بالمشاريع",
    tagline:
      "نظام AI Agentic لمتابعة المشاريع، المخاطر، التقارير، والـ change requests",
    category: "vertical_system",
    price: { min: 50000, max: 500000, typical: 175000 },
    best_for: ["المقاولون", "فرق الـ PMO", "مكاتب الهندسة"],
    highlights: [
      "رصد المخاطر وتنبيه الإدارة تلقائيًا",
      "تقارير التقدم الأسبوعية تُولَّد تلقائيًا",
      "متابعة الموافقات المعلقة",
      "تتبع change requests من البداية للنهاية",
    ],
  },
  {
    id: "SKRAG",
    name: "Sovereign Knowledge / RAG System",
    name_ar: "نظام المعرفة السيادية",
    tagline: "مساعد AI داخلي يعمل على وثائقكم وسياساتكم — آمن ومتحكم به",
    category: "vertical_system",
    price: { min: 50000, max: 750000, typical: 200000 },
    best_for: [
      "المؤسسات الكبيرة",
      "الجهات شبه الحكومية",
      "المؤسسات كثيفة السياسات والوثائق",
    ],
    highlights: [
      "موظفوكم يسألون النظام بدل البحث اليدوي",
      "إجابات فورية من سياساتكم الداخلية",
      "استرجاع المعلومات من آلاف الوثائق في ثوانٍ",
      "وصول متحكَّم به — كل موظف يرى ما يحق له فقط",
    ],
  },
  {
    id: "ECC",
    name: "Executive AI Command Center",
    name_ar: "مركز قيادة الذكاء الاصطناعي التنفيذي",
    tagline: "CEO يرى كل شيء في لوحة واحدة — مخاطر، أداء، قرارات",
    category: "vertical_system",
    price: {
      min: 100000,
      max: 1000000,
      note_ar: "يبدأ من 100 ألف ويمتد حسب حجم المؤسسة",
    },
    best_for: [
      "مكاتب الرؤساء التنفيذيين",
      "الشركات القابضة",
      "المؤسسات الكبيرة متعددة الأقسام",
    ],
    highlights: [
      "لوحة تنفيذية تحدّث نفسها",
      "ملخص أبرز المخاطر من جميع الأقسام",
      "تقارير الأقسام تُجمَّع تلقائيًا",
      "النظام يقترح الإجراء التالي",
    ],
  },
  {
    id: "RAOS",
    name: "Revenue AI OS",
    name_ar: "نظام AI للإيرادات",
    tagline: "فريق المبيعات يركز على الإغلاق — AI يتولى البحث والتواصل والمتابعة",
    category: "vertical_system",
    price: { min: 40000, max: 300000, typical: 100000 },
    best_for: [
      "شركات B2B لديها فرق مبيعات",
      "شركات تواجه تحديات في توليد الـ leads",
    ],
    highlights: [
      "أتمتة البحث عن العملاء المحتملين",
      "صياغة رسائل تواصل مخصّصة",
      "تسلسلات متابعة منظّمة",
      "توليد مسودات العروض وتحديث الـ CRM",
    ],
  },
  {
    id: "AGP",
    name: "AI Governance Pack",
    name_ar: "حزمة حوكمة الذكاء الاصطناعي",
    tagline: "للشركات التي تريد AI آمنًا وقابلاً للمراجعة والامتثال",
    category: "governance",
    price: { min: 15000, max: 100000, typical: 35000 },
    best_for: [
      "شركات مترددة بسبب المخاطر",
      "القطاعات المنظَّمة",
      "شركات تحتاج امتثال PDPL",
    ],
    highlights: [
      "سياسة استخدام AI (عربي + إنجليزي)",
      "مصفوفة الصلاحيات والأدوار",
      "تصميم بوابات الموافقة البشرية",
      "إطار ضبط المخاطر + متطلبات سجل التدقيق",
    ],
  },
  {
    id: "RET",
    name: "AI Ops Retainer",
    name_ar: "خدمة الدعم والتطوير المستمر",
    tagline: "نظامكم يتحسن كل شهر — دعم، monitoring، تحسينات، وتوسعة",
    category: "retainer",
    price: { min: 8000, max: 80000, typical: 20000, monthly: true },
    best_for: [
      "أي عميل سلّمناه مشروعًا قائمًا",
      "شركات تريد تحسينًا شهريًا مستمرًا",
      "فرق تحتاج دعمًا ذا أولوية",
    ],
    highlights: [
      "مراقبة النظام وفحص الصحة",
      "إصلاح الأخطاء والتحسينات",
      "تقرير استخدام شهري",
      "تخطيط التوسعة + دعم ذو أولوية",
    ],
  },
  {
    id: "EXP",
    name: "Department Expansion",
    name_ar: "توسعة القسم أو الإدارة",
    tagline: "طبّقنا على قسم — الآن نوسّع على الشركة كاملة",
    category: "expansion",
    price: {
      min: 50000,
      max: 500000,
      note_ar: "يعتمد على حجم التوسعة",
    },
    best_for: [
      "pilot نجح وطُلبت توسعته",
      "قسم ثانٍ يطلب نفس النظام",
      "إدارة جديدة تنضم أو تكامل API إضافي",
    ],
    highlights: [
      "توسعة النظام الناجح على أقسام جديدة",
      "تكامل أنظمة وAPIs إضافية",
      "تدريب فرق إضافية",
      "حوكمة موحّدة عبر الأقسام",
    ],
  },
];

// ── Category metadata ───────────────────────────────────────────────────────

const categoryMeta: Record<
  Category,
  { label: string; badge: string; accent: string }
> = {
  entry: {
    label: "نقطة دخول",
    badge: "border-cyan-400/40 bg-cyan-400/10 text-cyan-200",
    accent: "text-cyan-300",
  },
  pilot: {
    label: "تجربة عملية",
    badge: "border-sky-400/40 bg-sky-400/10 text-sky-200",
    accent: "text-sky-300",
  },
  vertical_system: {
    label: "نظام متكامل",
    badge: "border-emerald-400/40 bg-emerald-400/10 text-emerald-200",
    accent: "text-emerald-300",
  },
  governance: {
    label: "حوكمة وامتثال",
    badge: "border-amber-400/40 bg-amber-400/10 text-amber-200",
    accent: "text-amber-300",
  },
  retainer: {
    label: "دعم مستمر",
    badge: "border-violet-400/40 bg-violet-400/10 text-violet-200",
    accent: "text-violet-300",
  },
  expansion: {
    label: "توسعة",
    badge: "border-fuchsia-400/40 bg-fuchsia-400/10 text-fuchsia-200",
    accent: "text-fuchsia-300",
  },
};

const categoryOrder: Category[] = [
  "entry",
  "pilot",
  "vertical_system",
  "governance",
  "retainer",
  "expansion",
];

// ── Helpers ──────────────────────────────────────────────────────────────────

const num = (n: number) => new Intl.NumberFormat("en-US").format(n);

function formatPrice(p: PriceSar): string {
  const suffix = p.monthly ? " ريال/شهر" : " ريال";
  return `${num(p.min)} – ${num(p.max)}${suffix}`;
}

function mailtoFor(nameAr: string): string {
  return `mailto:hello@dealix.me?subject=${encodeURIComponent(
    `استفسار عن ${nameAr}`,
  )}`;
}

// ── Card ──────────────────────────────────────────────────────────────────

function OfferCard({ offer }: { offer: Offer }) {
  const meta = categoryMeta[offer.category];
  return (
    <article className="flex flex-col rounded-3xl border border-white/10 bg-white/[0.03] p-7">
      <div className="flex items-center justify-between gap-3">
        <span
          className={`inline-flex rounded-full border px-3 py-1 text-xs font-bold ${meta.badge}`}
        >
          {meta.label}
        </span>
        <span className="text-xs font-bold text-slate-600" dir="ltr">
          {offer.id}
        </span>
      </div>

      <h3 className="mt-4 text-xl font-black text-slate-100">{offer.name_ar}</h3>
      <p className="mt-1 text-xs text-slate-500" dir="ltr">
        {offer.name}
      </p>
      <p className="mt-3 text-sm leading-7 text-slate-400">{offer.tagline}</p>

      <p className={`mt-4 text-lg font-black ${meta.accent}`}>
        {formatPrice(offer.price)}
      </p>
      {offer.price.note_ar && (
        <p className="mt-1 text-xs text-slate-500">{offer.price.note_ar}</p>
      )}

      <div className="mt-5">
        <p className="text-xs font-bold uppercase tracking-wide text-slate-500">
          الأنسب لـ
        </p>
        <ul className="mt-2 space-y-1.5">
          {offer.best_for.slice(0, 3).map((b) => (
            <li
              key={b}
              className="flex items-start gap-2 text-sm leading-6 text-slate-300"
            >
              <span className="mt-0.5 text-cyan-400">·</span>
              {b}
            </li>
          ))}
        </ul>
      </div>

      <div className="mt-5">
        <p className="text-xs font-bold uppercase tracking-wide text-slate-500">
          أبرز المخرجات
        </p>
        <ul className="mt-2 space-y-1.5">
          {offer.highlights.slice(0, 4).map((h) => (
            <li
              key={h}
              className="flex items-start gap-2 text-sm leading-6 text-slate-300"
            >
              <span className={`mt-0.5 ${meta.accent}`}>✓</span>
              {h}
            </li>
          ))}
        </ul>
      </div>

      <div className="flex-1" />

      <a
        href={mailtoFor(offer.name_ar)}
        className="mt-6 block rounded-2xl border border-white/15 bg-white/[0.04] px-5 py-3 text-center text-sm font-black text-white hover:bg-white/10"
      >
        استفسر عن {offer.name_ar}
      </a>
    </article>
  );
}

// ── Page ──────────────────────────────────────────────────────────────────

export default function ServicesPage() {
  return (
    <main dir="rtl" className="min-h-screen bg-[#06111f] text-white">
      {/* ── Hero ── */}
      <section className="mx-auto max-w-6xl px-6 py-20 md:py-24">
        <p className="mb-5 inline-flex rounded-full border border-cyan-300/30 px-4 py-2 text-sm text-cyan-100">
          كتالوج الخدمات
        </p>
        <h1 className="max-w-4xl text-4xl font-black leading-[1.15] md:text-6xl">
          خدمات Dealix: من تدقيق أسبوع إلى أنظمة AI Agentic كاملة.
        </h1>
        <p className="mt-7 max-w-3xl text-xl leading-9 text-slate-300">
          مسار واضح يبدأ بإثبات القيمة بأقل مخاطرة، ثم أنظمة متخصصة لقطاعكم، مع
          حوكمة آمنة ودعم مستمر يطوّر نظامكم كل شهر.
        </p>
        <p className="mt-5 text-sm text-slate-500">
          AI يكتب، أنت ترسل · لا auto-send · بيانات حقيقية فقط
        </p>
      </section>

      {/* ── Offers grouped by category ── */}
      {categoryOrder.map((cat) => {
        const items = offers.filter((o) => o.category === cat);
        if (items.length === 0) return null;
        const meta = categoryMeta[cat];
        return (
          <section
            key={cat}
            className="border-t border-white/5 py-14 first:border-t-0"
          >
            <div className="mx-auto max-w-6xl px-6">
              <div className="flex items-center gap-3">
                <span
                  className={`inline-flex rounded-full border px-3 py-1 text-xs font-bold ${meta.badge}`}
                >
                  {meta.label}
                </span>
                <span className="text-sm text-slate-600">
                  {items.length} {items.length === 1 ? "عرض" : "عروض"}
                </span>
              </div>
              <div className="mt-7 grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                {items.map((o) => (
                  <OfferCard key={o.id} offer={o} />
                ))}
              </div>
            </div>
          </section>
        );
      })}

      {/* ── Closing CTA ── */}
      <section className="mx-auto max-w-6xl px-6 py-20">
        <div className="rounded-3xl border border-cyan-300/20 bg-cyan-400/5 p-10 text-center md:p-14">
          <h2 className="text-3xl font-black md:text-4xl">
            غير متأكد من أين تبدأ؟
          </h2>
          <p className="mt-4 text-lg text-slate-300">
            ابدأ بتدقيق workflow منخفض المخاطر، أو شاهد كيف يعمل النظام يوميًا في
            غرفة القيادة.
          </p>
          <div className="mt-8 flex flex-wrap justify-center gap-4">
            <a
              href="/ar/now"
              className="rounded-2xl bg-cyan-400 px-10 py-4 text-xl font-black text-[#06111f] hover:bg-cyan-300"
            >
              غرفة القيادة — الآن
            </a>
            <a
              href="mailto:hello@dealix.me?subject=استفسار%20عن%20خدمات%20Dealix"
              className="rounded-2xl border border-white/20 px-10 py-4 text-xl font-semibold text-white hover:bg-white/10"
            >
              تواصل معنا
            </a>
          </div>
        </div>
      </section>

      {/* ── Footer nav ── */}
      <footer className="border-t border-white/5 py-10">
        <div className="mx-auto flex max-w-6xl flex-wrap justify-between gap-6 px-6 text-sm text-slate-500">
          <a href="/ar" className="font-black text-white hover:text-cyan-300">
            ← Dealix
          </a>
          <nav className="flex flex-wrap gap-6">
            <a href="/ar" className="hover:text-white">
              الرئيسية
            </a>
            <a href="/ar/now" className="hover:text-cyan-300">
              غرفة القيادة
            </a>
            <a href="/ar/p1" className="hover:text-cyan-300">
              P1 تشخيص
            </a>
            <a href="/ar/pricing" className="hover:text-white">
              الأسعار
            </a>
            <a href="mailto:hello@dealix.me" className="hover:text-white">
              تواصل معنا
            </a>
          </nav>
        </div>
      </footer>
    </main>
  );
}
