import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Commercial Launch OS — Dealix",
  description:
    "Dealix Commercial Launch OS for Saudi/GCC B2B: 5 launch verticals, a clear SAR offer ladder, a daily review-only draft + social factory, and a trust-first, approval-first motion. The system never sends or posts — the founder reviews and publishes manually.",
  alternates: { canonical: "/commercial-launch" }
};

const stats = [
  { value: "5", label: "Launch verticals · قطاعات" },
  { value: "400+", label: "Daily review-only drafts · مسودات يومية" },
  { value: "130+", label: "Daily social drafts · منشورات يومية" },
  { value: "0", label: "Auto-sends · إرسال آلي" }
];

const verticals = [
  { en: "Facilities Management & Maintenance", ar: "إدارة المرافق والصيانة", pain: "SLA breaches & unbilled work orders", painAr: "غرامات SLA وأعمال غير مفوترة" },
  { en: "Contracting & Project Controls", ar: "المقاولات وضبط المشاريع", pain: "Variation value lost to slow approvals", painAr: "قيمة أوامر التغيير تُفقد ببطء الاعتماد" },
  { en: "Real Estate & Property Operations", ar: "العقار وإدارة الأملاك", pain: "Renewals & arrears depend on memory", painAr: "التجديدات والمتأخرات تعتمد على الذاكرة" },
  { en: "Legal & Professional Services", ar: "المكاتب القانونية والخدمات المهنية", pain: "Partner time trapped in intake/billing", painAr: "وقت الشركاء في الاستقبال والفوترة" },
  { en: "Consulting, Training & B2B Services", ar: "الاستشارات والتدريب وخدمات B2B", pain: "Proposals & reporting cap capacity", painAr: "العروض والتقارير تحدّ من الطاقة" }
];

const ladder = [
  { en: "Entry Diagnostic / AI Workflow Audit", ar: "تشخيص مبدئي / تدقيق سير عمل", price: "499 – 2,500 SAR", badge: "badge-emerald" },
  { en: "Paid Pilot", ar: "تجربة مدفوعة", price: "5,000 – 25,000 SAR", badge: "badge-ocean" },
  { en: "Department OS", ar: "نظام تشغيل القسم", price: "25,000 – 150,000 SAR", badge: "badge-violet" },
  { en: "Monthly Retainer", ar: "اشتراك شهري", price: "3,000 – 25,000 SAR / mo", badge: "badge-cyan" },
  { en: "Enterprise Custom OS", ar: "نظام تشغيل مؤسسي مخصص", price: "150,000+ SAR", badge: "badge-gold" }
];

const steps = [
  { en: "Generate daily opportunities + drafts", ar: "توليد فرص ومسودات يومية" },
  { en: "Score: quality + compliance + safety", ar: "تقييم: جودة وامتثال وأمان" },
  { en: "Place in the Founder Review Queue", ar: "وضعها في قائمة مراجعة المؤسس" },
  { en: "Founder personalises & sends manually", ar: "المؤسس يخصّص ويرسل يدويًا" }
];

const trust = [
  { en: "Approval-first — a human approves every external commitment.", ar: "الموافقة أولاً — إنسان يعتمد كل التزام خارجي." },
  { en: "Evidence-first — we share a proof asset before any ask.", ar: "الدليل أولاً — نشارك دليلًا قبل أي طلب." },
  { en: "Privacy-first — no access to your client data; redacted samples only.", ar: "الخصوصية أولاً — دون وصول لبياناتكم؛ عينات محجوبة فقط." },
  { en: "No guarantees, no hype — conservative, provable claims only.", ar: "لا ضمانات ولا مبالغة — ادعاءات متحفظة وقابلة للإثبات فقط." }
];

const faqs = [
  { q: "Do you send emails or post for us automatically?", a: "No. The system only drafts. It never sends email, posts to social, runs ads, or automates LinkedIn/WhatsApp. You review and publish manually.", qAr: "هل ترسلون أو تنشرون آليًا؟", aAr: "لا. النظام يكتب المسودات فقط. لا إرسال بريد ولا نشر ولا إعلانات ولا أتمتة. أنت تراجع وتنشر يدويًا." },
  { q: "Do you need access to our data?", a: "No. We work on redacted samples you choose to share, founder-reviewed, with no retention beyond the engagement.", qAr: "هل تحتاجون الوصول لبياناتنا؟", aAr: "لا. نعمل على عينات محجوبة تختارونها، بمراجعة المؤسس، دون الاحتفاظ بها بعد الارتباط." },
  { q: "Do you guarantee results?", a: "No. We share a proof asset first so you can judge the value before paying for anything beyond the diagnostic.", qAr: "هل تضمنون النتائج؟", aAr: "لا. نشارك دليلًا أولًا لتقدير القيمة قبل الدفع لما بعد التشخيص." }
];

export default function CommercialLaunchPage() {
  return (
    <main className="container" style={{ paddingTop: 48, paddingBottom: 80 }}>
      {/* Hero */}
      <section className="card-gold" style={{ marginBottom: 40 }}>
        <p className="eyebrow">Dealix Commercial Launch OS · السوق السعودي والخليجي</p>
        <h1>A governed B2B revenue &amp; operations OS — built trust-first.</h1>
        <p style={{ maxWidth: 760 }}>
          نظام تشغيل تجاري يولّد فرصًا يومية، يصنّفها، ويجهّز مسودات عالية الجودة — ثم يضعها
          في قائمة مراجعة المؤسس. <strong>لا يُرسل ولا ينشر أي شيء دون موافقة المؤسس.</strong>
        </p>
        <p style={{ maxWidth: 760 }} dir="ltr">
          Dealix drafts the work; the founder reviews and sends manually. No automated
          sending, no social auto-posting, no ad spend, no LinkedIn/WhatsApp automation,
          no scraping, no secrets.
        </p>
        <div className="actions" style={{ display: "flex", gap: 12, flexWrap: "wrap", marginTop: 16 }}>
          <a className="btn btn-primary" href="mailto:hello@dealix.me?subject=Request%20a%20Dealix%20workflow%20diagnostic">
            Book diagnostic · احجز تشخيصًا
          </a>
          <a className="btn btn-secondary" href="mailto:hello@dealix.me?subject=Request%20a%20Dealix%20workflow%20audit">
            Request workflow audit · اطلب تدقيق سير عمل
          </a>
        </div>
        <div className="cards" style={{ marginTop: 24 }}>
          {stats.map((s) => (
            <div key={s.label} style={{ textAlign: "center" }}>
              <div className="stat-value">{s.value}</div>
              <div className="stat-label">{s.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* Verticals */}
      <section style={{ marginBottom: 40 }}>
        <p className="eyebrow">First 5 verticals · أول 5 قطاعات</p>
        <div className="grid-3">
          {verticals.map((v) => (
            <article className="card" key={v.en}>
              <span className="badge badge-gold">Vertical</span>
              <h3 style={{ marginTop: 12 }}>{v.en}</h3>
              <p dir="rtl" style={{ color: "rgba(255,255,255,0.8)" }}>{v.ar}</p>
              <p style={{ marginTop: 8 }} dir="ltr"><strong>Pain:</strong> {v.pain}</p>
              <p dir="rtl"><strong>الألم:</strong> {v.painAr}</p>
            </article>
          ))}
        </div>
      </section>

      {/* Offer ladder */}
      <section style={{ marginBottom: 40 }}>
        <p className="eyebrow">Offer ladder (SAR) · سلّم العروض</p>
        <div className="grid-3">
          {ladder.map((o, i) => (
            <article className="card" key={o.en}>
              <span className={`badge ${o.badge}`}>Rung {i + 1}</span>
              <h3 style={{ marginTop: 12 }}>{o.en}</h3>
              <p dir="rtl" style={{ color: "rgba(255,255,255,0.8)" }}>{o.ar}</p>
              <p className="stat-value" style={{ fontSize: "1.4rem" }}>{o.price}</p>
            </article>
          ))}
        </div>
        <p style={{ marginTop: 12 }}>
          No guaranteed ROI. Every claim is conservative and provable. · لا عائد مضمون؛ كل ادعاء متحفّظ وقابل للإثبات.
        </p>
      </section>

      {/* How it works */}
      <section style={{ marginBottom: 40 }}>
        <p className="eyebrow">How the daily loop works · كيف تعمل الدورة اليومية</p>
        <div className="grid-2">
          {steps.map((s, i) => (
            <article className="card" key={s.en}>
              <span className="badge badge-ocean">Step {i + 1}</span>
              <h4 style={{ marginTop: 10 }} dir="ltr">{s.en}</h4>
              <p dir="rtl">{s.ar}</p>
            </article>
          ))}
        </div>
      </section>

      {/* Social & media OS */}
      <section className="card" style={{ marginBottom: 40 }}>
        <p className="eyebrow">Social &amp; Media OS · نظام السوشال والإعلام</p>
        <h2>Daily marketing drafts — review-only.</h2>
        <p dir="ltr">
          A daily, founder-review-only factory for LinkedIn, X, Instagram, newsletters,
          blog outlines, ad copy (no spend) and PR pitches — bilingual AR + EN, scored for
          quality and compliance. Nothing is posted, scheduled, or boosted automatically.
        </p>
        <p dir="rtl">
          مصنع يومي للمراجعة فقط: لينكدإن، إكس، إنستغرام، النشرات، مخططات المقالات، نصوص
          الإعلانات (بلا صرف)، ومقترحات العلاقات العامة — بالعربية والإنجليزية ومقيّمة للجودة
          والامتثال. لا نشر ولا جدولة ولا تعزيز آلي.
        </p>
      </section>

      {/* Trust */}
      <section style={{ marginBottom: 40 }}>
        <p className="eyebrow">Trust-first · approval-first · الثقة أولاً</p>
        <div className="grid-2">
          {trust.map((t) => (
            <article className="card" key={t.en}>
              <p dir="ltr" style={{ color: "#fff" }}>{t.en}</p>
              <p dir="rtl">{t.ar}</p>
            </article>
          ))}
        </div>
      </section>

      {/* FAQ */}
      <section style={{ marginBottom: 40 }}>
        <p className="eyebrow">FAQ · الأسئلة الشائعة</p>
        <div className="cards">
          {faqs.map((f) => (
            <article className="card" key={f.q}>
              <h4 dir="ltr">{f.q}</h4>
              <p dir="ltr">{f.a}</p>
              <h4 dir="rtl" style={{ marginTop: 12 }}>{f.qAr}</h4>
              <p dir="rtl">{f.aAr}</p>
            </article>
          ))}
        </div>
      </section>

      {/* Final CTA */}
      <section className="card-gold">
        <p className="eyebrow">Get started · ابدأ</p>
        <h2>Book a founder-led diagnostic · احجز تشخيصًا بقيادة المؤسس</h2>
        <p dir="ltr">
          Request a workflow audit on one revenue-critical process. We share a proof asset
          first — no access to your data required.
        </p>
        <div className="actions" style={{ display: "flex", gap: 12, flexWrap: "wrap", marginTop: 16 }}>
          <a className="btn btn-primary" href="mailto:hello@dealix.me?subject=Book%20a%20Dealix%20diagnostic">
            Book diagnostic / Request workflow audit →
          </a>
        </div>
      </section>
    </main>
  );
}
