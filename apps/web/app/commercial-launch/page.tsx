import Link from "next/link";

const outcomes = [
  "غرفة قيادة يومية للفرص والمتابعات والعروض",
  "مسودات عميل واضحة تخضع لمراجعة بشرية",
  "Proof Pack أسبوعي يوضح ماذا تغير وما القرار التالي",
  "مسار واضح من التشخيص إلى Sprint ثم Retainer",
];

const painPoints = [
  "فرص تضيع بين واتساب، الإيميل، المكالمات، وملفات Excel.",
  "عروض تُحضّر ثم تختفي بدون متابعة موحدة أو owner واضح.",
  "الإدارة لا ترى تقريرًا يوميًا يحول البيانات إلى next actions.",
  "الفرق تستخدم أدوات كثيرة، لكن لا يوجد operating rhythm واحد.",
];

const packages = [
  {
    name: "AI Revenue Diagnostic",
    price: "0–1,500 SAR",
    fit: "مناسب إذا تبغى تعرف أين تضيع الفرص قبل أي بناء.",
  },
  {
    name: "7-Day Revenue Command Room Sprint",
    price: "5,000–12,000 SAR",
    fit: "أفضل عرض أولي: نركب نظام متابعة وعروض وتشغيل يومي خلال أسبوع.",
  },
  {
    name: "Managed OS Retainer",
    price: "3,000–25,000 SAR / month",
    fit: "بعد ظهور proof، نتحول إلى تشغيل شهري وتحسين مستمر.",
  },
];

const operatingSteps = [
  ["01", "Map", "نرسم مسار الفرص الحالي ونحدد أين يحدث التعطل."],
  ["02", "Command", "نبني ledgers وغرفة قيادة يومية للمتابعة والعروض."],
  ["03", "Draft", "نجهز مسودات عميل واضحة للمراجعة البشرية."],
  ["04", "Operate", "نقيس الردود، المتابعات، والعروض ونحدث القرار اليومي."],
  ["05", "Prove", "نغلق الأسبوع بـ Proof Pack وخطة 30 يوم."],
];

const trustRules = [
  "كل قرار حساس يخضع لمراجعة بشرية.",
  "لا توجد مدفوعات حية في هذه المرحلة.",
  "لا نستخدم شعارات عملاء أو نتائج غير موثقة.",
  "كل قيمة مذكورة هي نطاق تقديري وليست وعدًا بنتيجة مالية.",
];

function SectionTitle({ eyebrow, title, children }: { eyebrow: string; title: string; children?: React.ReactNode }) {
  return (
    <div style={{ maxWidth: 820 }}>
      <p className="eyebrow">{eyebrow}</p>
      <h2>{title}</h2>
      {children ? <p>{children}</p> : null}
    </div>
  );
}

export default function CommercialLaunchPage() {
  return (
    <main className="grid" dir="rtl">
      <section className="card card-gold dot-pattern" style={{ position: "relative", overflow: "hidden" }}>
        <p className="eyebrow">Dealix Commercial Launch</p>
        <h1 style={{ maxWidth: 920 }}>
          حوّل فوضى المتابعة والعروض إلى <span className="gradient-text">Revenue Command Room</span>
          <br /> خلال 7 أيام
        </h1>
        <p style={{ maxWidth: 760, fontSize: "1.12rem" }}>
          Dealix يبني للشركات السعودية نظام تشغيل يومي يربط الفرص، المتابعات، العروض،
          وقرارات الإدارة في workflow واضح قابل للقياس — بدون وعود مبالغ فيها.
        </p>
        <div className="actions" aria-label="Commercial launch actions">
          <Link href="/book">احجز تشخيص 15 دقيقة</Link>
          <Link href="/pricing">شاهد الباقات</Link>
          <Link href="/commercial-launch#process">كيف نشتغل؟</Link>
        </div>
      </section>

      <section className="cards" aria-label="Commercial outcomes">
        {outcomes.map((outcome) => (
          <article className="card" key={outcome}>
            <span className="badge badge-gold">Outcome</span>
            <h3 style={{ marginTop: "var(--sp-4)" }}>{outcome}</h3>
          </article>
        ))}
      </section>

      <section className="card" aria-labelledby="pain-title">
        <SectionTitle eyebrow="Why now" title="المشكلة ليست نقص أدوات — المشكلة غياب نظام تشغيل يومي">
          أغلب الشركات عندها واتساب، CRM، إيميل، وExcel. لكن لا يوجد خط واحد يقول للإدارة:
          من نتابع؟ ماذا نجهز؟ من المسؤول؟ وما الدليل أن التشغيل تحسن؟
        </SectionTitle>
        <div className="cards" style={{ marginTop: "var(--sp-6)" }}>
          {painPoints.map((pain) => (
            <article className="card" key={pain}>
              <h3>ألم تشغيلي</h3>
              <p>{pain}</p>
            </article>
          ))}
        </div>
      </section>

      <section id="process" className="card" aria-labelledby="process-title">
        <SectionTitle eyebrow="Operating model" title="طريقة Dealix: Map → Command → Draft → Operate → Prove">
          نبدأ صغيرًا بإثبات تشغيل حقيقي، ثم نوسع إلى Retainer أو SaaS workspace بعد ظهور
          الدليل.
        </SectionTitle>
        <div className="cards" style={{ marginTop: "var(--sp-6)" }}>
          {operatingSteps.map(([number, title, body]) => (
            <article className="card" key={number}>
              <p className="stat-value" style={{ fontSize: "2rem" }}>{number}</p>
              <h3>{title}</h3>
              <p>{body}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="card" aria-labelledby="packages-title">
        <SectionTitle eyebrow="Commercial packages" title="ابدأ بعرض واضح بدل مشروع مفتوح">
          الباقات مصممة لتقليل المخاطرة: تشخيص، Sprint قصير، ثم تشغيل شهري بعد proof.
        </SectionTitle>
        <div className="cards" style={{ marginTop: "var(--sp-6)" }}>
          {packages.map((pack) => (
            <article className="card hover-gold" key={pack.name}>
              <span className="badge badge-emerald">Founder-led</span>
              <h3 style={{ marginTop: "var(--sp-4)" }}>{pack.name}</h3>
              <p className="stat-value" style={{ fontSize: "1.8rem" }}>{pack.price}</p>
              <p>{pack.fit}</p>
              <Link href="/book" className="btn btn-secondary">احجز مراجعة</Link>
            </article>
          ))}
        </div>
      </section>

      <section className="card" aria-labelledby="trust-title">
        <SectionTitle eyebrow="Trust first" title="قوة Dealix أنها تشغّل بدون تهور">
          الإطلاق التجاري الحالي يبني ثقة العميل قبل التوسع. كل شيء حساس يبقى تحت مراجعة
          بشرية واضحة.
        </SectionTitle>
        <ul style={{ marginTop: "var(--sp-4)" }}>
          {trustRules.map((rule) => (
            <li key={rule}>{rule}</li>
          ))}
        </ul>
      </section>

      <section className="card card-gold text-center" aria-labelledby="final-cta">
        <p className="eyebrow">Next step</p>
        <h2 id="final-cta">ابدأ بتشخيص واحد، لا بمشروع ضخم</h2>
        <p>
          إذا ظهر الألم واضحًا، نغلق Sprint. إذا لم يظهر، لا نوسع. هذا هو المسار التجاري
          الأقل مخاطرة والأكثر قابلية للبيع الآن.
        </p>
        <div className="actions" style={{ justifyContent: "center" }}>
          <Link href="/book">احجز المراجعة</Link>
          <Link href="/offers">راجع العروض</Link>
        </div>
      </section>
    </main>
  );
}
