"use client";

import Link from "next/link";
import { useState } from "react";

/* ─── Data ───────────────────────────────────────────────────────── */

const problems = [
  { icon: "💬", title: "فوضى الواتساب", desc: "استفسارات تضيع بين المحادثات، ومتابعات تُنسى حتى يختار العميل منافسك." },
  { icon: "🕐", title: "تأخر المتابعة", desc: "متوسط ٣–٧ أيام تأخر في الرد يكلّف شركات B2B ما يزيد على ٣٠٪ من صفقاتها." },
  { icon: "📊", title: "لا أرقام واضحة", desc: "لا تعرف معدل التحويل، ولا متوسط الصفقة، ولا أين يتسرب الإيراد كل شهر." },
  { icon: "🤖", title: "AI بدون تحكم", desc: "أدوات AI تعمل بعشوائية — ترسل بدون موافقة، وتلتزم بدون صلاحية." },
  { icon: "📋", title: "عمليات يدوية", desc: "فريقك يقضي ساعات في نسخ البيانات بدل إغلاق الصفقات وخدمة العملاء." },
];

const systems = [
  { icon: "💬", name: "WhatsApp Revenue OS", nameAr: "نظام إيرادات واتساب", desc: "حوّل كل استفسار إلى عرض سعر في دقائق. متابعة آلية، مسودات تنتظر موافقتك." },
  { icon: "⭐", name: "Review Intelligence OS", nameAr: "نظام ذكاء التقييمات", desc: "اجمع التقييمات الإيجابية، تعامل مع الشكاوى قبل انتشارها، وابنِ سمعة رقمية قوية." },
  { icon: "🏢", name: "AI Command Center", nameAr: "غرفة قيادة AI", desc: "لوحة تحكم يومية بأولويات المبيعات، الصفقات المتأخرة، والفرص المفوّتة." },
  { icon: "📣", name: "Brand Intelligence OS", nameAr: "نظام ذكاء العلامة التجارية", desc: "راقب ذكرك في السوق، حدد ما يقوله عنك عملاؤك ومنافسوك." },
  { icon: "📈", name: "Growth Engine OS", nameAr: "محرك النمو", desc: "اكتشف فرص توسيع الإيراد من عملائك الحاليين — upsell وcross-sell مبني على بيانات فعلية." },
  { icon: "❤️", name: "Customer Experience OS", nameAr: "نظام تجربة العملاء", desc: "تتبع صحة كل عميل، تنبّه مبكر قبل الإلغاء، ومتابعة استباقية." },
  { icon: "👥", name: "AI Agent Workforce OS", nameAr: "نظام قوى العمل AI", desc: "أتمتة المهام المتكررة مع حوكمة كاملة — كل إجراء يحتاج موافقة قبل التنفيذ." },
];

const steps = [
  { num: "١", title: "التشخيص المجاني (٣٠ دقيقة)", desc: "نتحدث، نحدد أكبر ٣ ثغرات إيراد في عمليتك، ونرسل لك ملخصاً فورياً." },
  { num: "٢", title: "الميكرو سبرينت (٤٩٩ ريال)", desc: "خلال يوم–يومين نبني نظاماً مصغراً جاهزاً للتجربة ويُثبت القيمة قبل أي التزام." },
  { num: "٣", title: "سبرينت التشخيص (٧,٥٠٠–٢٥,٠٠٠ ريال)", desc: "٣–٧ أيام. نبني الخريطة الكاملة لتسرب الإيراد، خطة التطبيق، وعرض الإثبات." },
  { num: "٤", title: "التشغيل المستمر (٢,٩٩٩–٤,٩٩٩ ريال/شهر)", desc: "نشغّل النظام شهرياً — تقارير يومية، صفقات محدّثة، وتحسين مستمر." },
];

const offers = [
  {
    id: "free",
    name: "التشخيص المجاني",
    price: "مجاني",
    duration: "٣٠ دقيقة",
    badge: "ادخل من هنا",
    badgeColor: "var(--dealix-emerald)",
    features: ["تحليل أكبر ٣ ثغرات", "ملخص مكتوب خلال ٢٤ س", "بدون أي التزام"],
  },
  {
    id: "micro",
    name: "ميكرو سبرينت",
    price: "٤٩٩ ريال",
    duration: "يوم – يومان",
    badge: "بداية سريعة",
    badgeColor: "var(--dealix-amber)",
    features: ["نظام مصغر جاهز للتجربة", "إثبات القيمة قبل الالتزام", "تسليم كامل للكود"],
  },
  {
    id: "data",
    name: "حزمة البيانات",
    price: "١,٥٠٠ ريال",
    duration: "مرة واحدة",
    badge: "أصل دائم",
    badgeColor: "var(--dealix-ocean)",
    features: ["قاعدة بيانات منظّمة", "٥٠+ شركة مستهدفة", "جاهز للحملات التسويقية"],
  },
  {
    id: "managed",
    name: "التشغيل المُدار",
    price: "٢,٩٩٩–٤,٩٩٩ ريال",
    duration: "شهرياً",
    badge: "الأكثر طلباً",
    badgeColor: "var(--dealix-gold)",
    features: ["تقارير يومية", "إدارة الصفقات والمتابعات", "تحسين مستمر"],
    highlight: true,
  },
  {
    id: "sprint",
    name: "سبرينت التشخيص",
    price: "٧,٥٠٠–٢٥,٠٠٠ ريال",
    duration: "٣–٧ أيام",
    badge: "الدخول الرئيسي",
    badgeColor: "var(--dealix-gold)",
    features: ["خريطة تسرب الإيراد", "نظام Revenue OS كامل", "Proof Pack للاقتناع الداخلي"],
    highlight: true,
  },
  {
    id: "enterprise",
    name: "نظام مخصص للمؤسسات",
    price: "٢٥,٠٠٠–١٠٠,٠٠٠+ ريال",
    duration: "٤–١٢ أسبوعاً",
    badge: "Enterprise",
    badgeColor: "var(--dealix-coral)",
    features: ["نظام AI مخصص كلياً", "تكامل مع أنظمتك الحالية", "دعم مستمر ومضمون SLA"],
  },
];

const trustItems = [
  { icon: "🇸🇦", title: "سعودي أولاً", desc: "مبني للسوق السعودي — لغة عربية، تسعير بالريال، قوانين محلية." },
  { icon: "🔒", title: "متوافق مع PDPL", desc: "حوكمة بيانات كاملة تتوافق مع نظام حماية البيانات الشخصية السعودي." },
  { icon: "🧾", title: "ZATCA-Aware", desc: "فواتير رقمية متوافقة مع متطلبات الزكاة والضريبة." },
  { icon: "✅", title: "موافقة أولاً", desc: "كل إجراء AI يحتاج موافقة بشرية — لا إرسال تلقائي بدون إذن صريح." },
];

const faqs = [
  {
    q: "هل يمكن تجربة Dealix قبل الدفع؟",
    a: "نعم. التشخيص المجاني (٣٠ دقيقة) يعطيك فهماً كاملاً لوضعك مع توصيات عملية — بدون أي تكلفة أو التزام.",
  },
  {
    q: "كم يستغرق بناء النظام؟",
    a: "سبرينت التشخيص يستغرق ٣–٧ أيام. الميكرو سبرينت يوم–يومان. التشغيل المستمر يبدأ فوراً بعد انتهاء السبرينت.",
  },
  {
    q: "هل Dealix آمن على بيانات شركتي؟",
    a: "نعم. بنيّنا النظام من الأساس ليكون متوافقاً مع PDPL السعودي. لا بيانات تُشارك مع أطراف ثالثة بدون إذن صريح منك.",
  },
  {
    q: "ما الفرق بين Dealix وأدوات AI الأخرى؟",
    a: "Dealix ليس أداة — هو نظام تشغيل كامل. كل قرار AI يمر بموافقتك. مبني للسوق السعودي، يتحدث العربية، ويعمل مع بيانات شركتك الفعلية.",
  },
  {
    q: "هل يمكن الإلغاء بسهولة؟",
    a: "نعم. الاشتراك الشهري قابل للإلغاء بإشعار ٣٠ يوم. لا عقود سنوية إجبارية، لا auto-renewal خفي.",
  },
  {
    q: "ماذا يحدث بعد الانتهاء من السبرينت؟",
    a: "تحصل على الكود والتوثيق والنظام كاملاً. إذا أردت التشغيل المستمر معنا — ممتاز. وإذا أردت الاستقلال — الخيار لك.",
  },
];

const results = [
  { value: "٣٠٪+", label: "زيادة في معدل التحويل" },
  { value: "< ٢٤ س", label: "متوسط وقت الرد بعد التطبيق" },
  { value: "٧ أيام", label: "للحصول على نظام تشغيل كامل" },
  { value: "> ٧٠٪", label: "هامش ربح على الخدمة" },
];

const structuredData = {
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  name: "Dealix",
  description: "نظام Revenue OS للشركات السعودية B2B — تحويل المبيعات إلى نظام تشغيل ذكي خلال ٧ أيام",
  url: "https://dealix.me",
  areaServed: { "@type": "Country", name: "Saudi Arabia" },
  priceRange: "٤٩٩–١٠٠,٠٠٠+ SAR",
  hasOfferCatalog: {
    "@type": "OfferCatalog",
    name: "Dealix Offer Ladder",
    itemListElement: [
      { "@type": "Offer", name: "التشخيص المجاني", price: "0", priceCurrency: "SAR" },
      { "@type": "Offer", name: "ميكرو سبرينت", price: "499", priceCurrency: "SAR" },
      { "@type": "Offer", name: "سبرينت التشخيص", price: "7500", priceCurrency: "SAR" },
    ],
  },
};

/* ─── FAQ Item ────────────────────────────────────────────────────── */
function FAQItem({ q, a }: { q: string; a: string }) {
  const [open, setOpen] = useState(false);
  return (
    <div
      style={{
        borderBottom: "1px solid rgba(255,255,255,0.08)",
        paddingBottom: "var(--sp-4)",
        marginBottom: "var(--sp-4)",
      }}
    >
      <button
        onClick={() => setOpen(!open)}
        style={{
          width: "100%",
          background: "none",
          border: "none",
          cursor: "pointer",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          gap: "var(--sp-4)",
          textAlign: "right",
          padding: 0,
        }}
        aria-expanded={open}
      >
        <span style={{ color: "#fff", fontWeight: 600, fontSize: "1rem", lineHeight: 1.5, flex: 1, textAlign: "right" }}>
          {q}
        </span>
        <span style={{
          color: "var(--dealix-gold)",
          fontSize: "1.4rem",
          fontWeight: 300,
          flexShrink: 0,
          transform: open ? "rotate(45deg)" : "none",
          transition: "transform 0.2s",
          display: "inline-block",
        }}>
          +
        </span>
      </button>
      {open && (
        <p style={{
          marginTop: "var(--sp-3)",
          color: "rgba(255,255,255,0.70)",
          lineHeight: 1.7,
          fontSize: "0.95rem",
        }}>
          {a}
        </p>
      )}
    </div>
  );
}

/* ─── Page ────────────────────────────────────────────────────────── */
export default function HomePage() {
  return (
    <>
      <script
        type="application/ld+json"
        suppressHydrationWarning
        dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }}
      />

      {/* ══ NAVBAR ══════════════════════════════════════════════════ */}
      <nav className="navbar" aria-label="Primary navigation">
        <Link href="/" className="navbar-brand" aria-label="Dealix Home">
          Dealix
        </Link>
        <ul className="navbar-links" role="list">
          <li><Link href="/offers">العروض</Link></li>
          <li><Link href="/pricing">التسعير</Link></li>
          <li><Link href="/ar">عربي</Link></li>
          <li><Link href="/book">احجز التشخيص</Link></li>
        </ul>
        <div className="actions" style={{ marginTop: 0, gap: "var(--sp-2)" }}>
          <Link href="/book" className="btn btn-secondary" style={{ minHeight: 38, padding: "0 20px", fontSize: "0.85rem" }}>
            احجز التشخيص المجاني →
          </Link>
        </div>
      </nav>

      <main style={{ display: "flex", flexDirection: "column", gap: "var(--sp-12)" }}>

        {/* ══ HERO ════════════════════════════════════════════════════ */}
        <section
          className="card dot-pattern animate-fade-up"
          aria-labelledby="hero-title"
          style={{ position: "relative", overflow: "hidden", padding: "clamp(48px,8vw,96px) clamp(24px,5vw,64px)" }}
        >
          <div aria-hidden="true" style={{
            position: "absolute", top: "-120px", right: "-80px",
            width: "500px", height: "500px",
            background: "radial-gradient(circle, rgba(212,175,55,0.10), transparent 65%)",
            pointerEvents: "none",
          }} />
          <div aria-hidden="true" style={{
            position: "absolute", bottom: "-60px", left: "-60px",
            width: "300px", height: "300px",
            background: "radial-gradient(circle, rgba(0,102,255,0.08), transparent 65%)",
            pointerEvents: "none",
          }} />

          <p className="eyebrow" style={{ marginBottom: "var(--sp-5)" }}>
            🇸🇦 سعودي أولاً · موافقة أولاً · نتائج أولاً
          </p>

          <h1 id="hero-title" style={{ maxWidth: "860px", marginBottom: "var(--sp-6)" }}>
            حوّل شركتك إلى{" "}
            <span className="gradient-text">آلة إيراد</span>
            <br />
            خلال ٧ أيام
          </h1>

          <p style={{ maxWidth: "640px", fontSize: "1.18rem", lineHeight: 1.8, color: "rgba(255,255,255,0.80)", marginBottom: "var(--sp-8)" }}>
            Dealix يبني لشركتك <strong style={{ color: "#fff" }}>نظام تشغيل Revenue OS</strong> متكامل — يجمع المبيعات، المتابعة، وذكاء الأعمال في مكان واحد يعمل بموافقتك.
          </p>

          <p style={{ fontSize: "0.92rem", color: "rgba(255,255,255,0.50)", marginBottom: "var(--sp-3)" }}>
            مخصص لشركات B2B السعودية التي تعاني من فوضى الواتساب وضياع الصفقات
          </p>

          <div className="actions" aria-label="Primary actions" style={{ gap: "var(--sp-3)" }}>
            <Link href="/book" className="btn btn-primary" style={{ fontSize: "1rem", padding: "14px 32px", minHeight: 52 }}>
              احجز التشخيص المجاني
            </Link>
            <Link href="/offers" className="btn btn-secondary" style={{ fontSize: "1rem", padding: "14px 28px", minHeight: 52 }}>
              شوف العروض والأسعار →
            </Link>
          </div>

          <p style={{ marginTop: "var(--sp-5)", fontSize: "0.82rem", color: "rgba(255,255,255,0.35)" }}>
            لا تحتاج بطاقة ائتمانية · التشخيص مجاني تماماً · نبدأ خلال ٢٤ ساعة
          </p>
        </section>

        {/* ══ RESULTS BAR ═════════════════════════════════════════════ */}
        <section aria-label="Results metrics">
          <div style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(160px,1fr))",
            gap: "var(--sp-4)",
          }}>
            {results.map(({ value, label }) => (
              <div key={label} className="card" style={{ textAlign: "center", padding: "var(--sp-8) var(--sp-4)" }}>
                <div className="stat-value" style={{ fontSize: "clamp(1.8rem,4vw,2.8rem)", color: "var(--dealix-gold)" }}>
                  {value}
                </div>
                <p className="stat-label" style={{ marginTop: "var(--sp-2)" }}>{label}</p>
              </div>
            ))}
          </div>
        </section>

        {/* ══ PROBLEM ══════════════════════════════════════════════════ */}
        <section aria-labelledby="problem-title">
          <p className="eyebrow">المشكلة</p>
          <h2 id="problem-title" style={{ marginBottom: "var(--sp-3)" }}>
            ماذا تعاني شركات B2B السعودية اليوم؟
          </h2>
          <p style={{ color: "rgba(255,255,255,0.60)", maxWidth: "560px", marginBottom: "var(--sp-8)" }}>
            إذا كانت هذه المشاكل مألوفة — Dealix مصنوع لك.
          </p>
          <div className="cards">
            {problems.map(({ icon, title, desc }) => (
              <article key={title} className="card" style={{ borderTop: "3px solid rgba(212,175,55,0.3)" }}>
                <div style={{ fontSize: "2rem", marginBottom: "var(--sp-3)" }}>{icon}</div>
                <h3 style={{ marginBottom: "var(--sp-2)", fontSize: "1.1rem" }}>{title}</h3>
                <p style={{ fontSize: "0.9rem", color: "rgba(255,255,255,0.65)", lineHeight: 1.7 }}>{desc}</p>
              </article>
            ))}
          </div>
        </section>

        {/* ══ SOLUTION ═════════════════════════════════════════════════ */}
        <section aria-labelledby="solution-title" className="card" style={{ padding: "clamp(32px,5vw,64px)" }}>
          <p className="eyebrow">الحل</p>
          <h2 id="solution-title" style={{ marginBottom: "var(--sp-3)" }}>
            Dealix يبني لك نظام تشغيل كامل
          </h2>
          <p style={{ color: "rgba(255,255,255,0.60)", maxWidth: "560px", marginBottom: "var(--sp-8)" }}>
            ليس أداة. ليس chatbot. نظام تشغيل متكامل يعمل بموافقتك.
          </p>

          <div className="cards">
            {systems.map(({ icon, name, nameAr, desc }) => (
              <article key={name} className="card" style={{ padding: "var(--sp-6)", background: "rgba(255,255,255,0.03)" }}>
                <div style={{ fontSize: "1.8rem", marginBottom: "var(--sp-3)" }}>{icon}</div>
                <h3 style={{ fontSize: "0.95rem", marginBottom: "var(--sp-1)", color: "var(--dealix-gold)" }}>{name}</h3>
                <p style={{ fontSize: "0.80rem", color: "rgba(255,255,255,0.45)", marginBottom: "var(--sp-3)" }}>{nameAr}</p>
                <p style={{ fontSize: "0.88rem", color: "rgba(255,255,255,0.70)", lineHeight: 1.65 }}>{desc}</p>
              </article>
            ))}
          </div>
        </section>

        {/* ══ HOW IT WORKS ═════════════════════════════════════════════ */}
        <section aria-labelledby="steps-title">
          <p className="eyebrow">كيف يعمل</p>
          <h2 id="steps-title" style={{ marginBottom: "var(--sp-3)" }}>
            ٤ خطوات من الفوضى إلى النظام
          </h2>
          <p style={{ color: "rgba(255,255,255,0.60)", maxWidth: "560px", marginBottom: "var(--sp-8)" }}>
            تبدأ مجاناً، تثبت القيمة أولاً، ثم تقرر.
          </p>
          <div style={{ display: "flex", flexDirection: "column", gap: "var(--sp-4)" }}>
            {steps.map(({ num, title, desc }, i) => (
              <div
                key={num}
                className="card"
                style={{
                  display: "flex",
                  gap: "var(--sp-6)",
                  alignItems: "flex-start",
                  padding: "var(--sp-6)",
                  borderRight: "3px solid var(--dealix-gold)",
                }}
              >
                <div style={{
                  flexShrink: 0,
                  width: 52, height: 52,
                  borderRadius: "50%",
                  background: i === 0 ? "var(--dealix-emerald)" : i === 3 ? "var(--dealix-gold)" : "rgba(212,175,55,0.15)",
                  display: "flex", alignItems: "center", justifyContent: "center",
                  fontSize: "1.3rem", fontWeight: 800, color: "#fff",
                  fontFamily: "var(--font-display)",
                }}>
                  {num}
                </div>
                <div>
                  <h3 style={{ marginBottom: "var(--sp-2)", fontSize: "1.05rem" }}>{title}</h3>
                  <p style={{ color: "rgba(255,255,255,0.65)", fontSize: "0.92rem", lineHeight: 1.7 }}>{desc}</p>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* ══ OFFER LADDER ═════════════════════════════════════════════ */}
        <section aria-labelledby="offers-title">
          <p className="eyebrow">العروض والأسعار</p>
          <h2 id="offers-title" style={{ marginBottom: "var(--sp-3)" }}>
            سلّم العروض — ابدأ من أي مستوى
          </h2>
          <p style={{ color: "rgba(255,255,255,0.60)", maxWidth: "560px", marginBottom: "var(--sp-8)" }}>
            كل عميل يبدأ من التشخيص المجاني. لا فخ تسعير، لا عقود طويلة قبل إثبات القيمة.
          </p>

          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))", gap: "var(--sp-4)" }}>
            {offers.map(({ id, name, price, duration, badge, badgeColor, features, highlight }) => (
              <article
                key={id}
                className="card"
                style={{
                  padding: "var(--sp-8) var(--sp-6)",
                  position: "relative",
                  border: highlight ? `2px solid var(--dealix-gold)` : undefined,
                  background: highlight ? "rgba(212,175,55,0.05)" : undefined,
                }}
              >
                {badge && (
                  <span style={{
                    position: "absolute", top: "-12px", right: "20px",
                    background: badgeColor, color: "#001F3F",
                    fontSize: "0.72rem", fontWeight: 700, padding: "3px 12px",
                    borderRadius: "var(--r-pill)", letterSpacing: "0.05em",
                  }}>
                    {badge}
                  </span>
                )}

                <h3 style={{ fontSize: "1.1rem", marginBottom: "var(--sp-2)", color: "#fff" }}>{name}</h3>

                <div style={{ marginBottom: "var(--sp-1)" }}>
                  <span style={{ fontSize: "1.8rem", fontWeight: 800, color: "var(--dealix-gold)", fontFamily: "var(--font-display)" }}>
                    {price}
                  </span>
                </div>
                <p style={{ fontSize: "0.82rem", color: "rgba(255,255,255,0.45)", marginBottom: "var(--sp-5)" }}>{duration}</p>

                <div className="divider-gold" />

                <ul style={{ listStyle: "none", padding: 0, display: "flex", flexDirection: "column", gap: "var(--sp-2)", marginBottom: "var(--sp-6)" }}>
                  {features.map((f) => (
                    <li key={f} style={{ fontSize: "0.88rem", color: "rgba(255,255,255,0.72)", display: "flex", gap: "var(--sp-2)", alignItems: "flex-start" }}>
                      <span style={{ color: "var(--dealix-emerald)", flexShrink: 0 }}>✓</span>
                      {f}
                    </li>
                  ))}
                </ul>

                <Link
                  href="/book"
                  className={highlight ? "btn btn-primary" : "btn btn-secondary"}
                  style={{ width: "100%", textAlign: "center", fontSize: "0.88rem" }}
                >
                  {id === "free" ? "احجز التشخيص المجاني" : "تواصل معنا"}
                </Link>
              </article>
            ))}
          </div>

          <div style={{ textAlign: "center", marginTop: "var(--sp-6)" }}>
            <Link href="/pricing" style={{ color: "var(--dealix-gold)", fontWeight: 600, fontSize: "0.92rem" }}>
              عرض جدول المقارنة الكامل →
            </Link>
          </div>
        </section>

        {/* ══ TRUST ════════════════════════════════════════════════════ */}
        <section aria-labelledby="trust-title" className="card" style={{ padding: "clamp(32px,5vw,64px)" }}>
          <p className="eyebrow">الثقة والأمان</p>
          <h2 id="trust-title" style={{ marginBottom: "var(--sp-8)" }}>
            مبني للسوق السعودي من الأساس
          </h2>
          <div className="cards">
            {trustItems.map(({ icon, title, desc }) => (
              <div key={title} className="card" style={{ textAlign: "center", padding: "var(--sp-8) var(--sp-6)" }}>
                <div style={{ fontSize: "2.5rem", marginBottom: "var(--sp-4)" }}>{icon}</div>
                <h3 style={{ fontSize: "1rem", marginBottom: "var(--sp-2)", color: "var(--dealix-gold)" }}>{title}</h3>
                <p style={{ fontSize: "0.88rem", color: "rgba(255,255,255,0.65)", lineHeight: 1.65 }}>{desc}</p>
              </div>
            ))}
          </div>
        </section>

        {/* ══ FAQ ══════════════════════════════════════════════════════ */}
        <section aria-labelledby="faq-title">
          <p className="eyebrow">أسئلة شائعة</p>
          <h2 id="faq-title" style={{ marginBottom: "var(--sp-8)" }}>
            أسئلة يسألها كل مؤسس
          </h2>
          <div className="card" style={{ padding: "var(--sp-8) clamp(24px,4vw,48px)" }}>
            {faqs.map(({ q, a }) => (
              <FAQItem key={q} q={q} a={a} />
            ))}
          </div>
        </section>

        {/* ══ FINAL CTA ════════════════════════════════════════════════ */}
        <section
          className="card dot-pattern"
          aria-labelledby="cta-title"
          style={{
            textAlign: "center",
            padding: "clamp(48px,8vw,96px) clamp(24px,5vw,64px)",
            position: "relative", overflow: "hidden",
          }}
        >
          <div aria-hidden="true" style={{
            position: "absolute", top: "50%", left: "50%",
            transform: "translate(-50%,-50%)",
            width: "500px", height: "500px",
            background: "radial-gradient(circle, rgba(212,175,55,0.08), transparent 65%)",
            pointerEvents: "none",
          }} />

          <p className="eyebrow" style={{ justifyContent: "center", display: "flex" }}>
            ابدأ اليوم
          </p>
          <h2 id="cta-title" style={{ marginBottom: "var(--sp-4)" }}>
            جاهز تحوّل شركتك؟
          </h2>
          <p style={{
            maxWidth: "520px", margin: "0 auto var(--sp-8)",
            fontSize: "1.05rem", color: "rgba(255,255,255,0.65)", lineHeight: 1.8,
          }}>
            ٣٠ دقيقة تشخيص مجاني. تخرج بخريطة واضحة لأكبر ٣ ثغرات في إيراد شركتك.
            لا بيع، لا ضغط — فقط وضوح.
          </p>

          <div className="actions" style={{ justifyContent: "center", gap: "var(--sp-3)" }}>
            <Link href="/book" className="btn btn-primary" style={{ fontSize: "1.05rem", padding: "16px 40px", minHeight: 56 }}>
              احجز التشخيص المجاني الآن
            </Link>
            <Link href="/offers" className="btn btn-secondary" style={{ fontSize: "1.05rem", padding: "16px 32px", minHeight: 56 }}>
              شوف جميع العروض
            </Link>
          </div>

          <p style={{ marginTop: "var(--sp-5)", fontSize: "0.82rem", color: "rgba(255,255,255,0.30)" }}>
            أو تواصل معنا مباشرة عبر الواتساب ←{" "}
            <a href="https://wa.me/966500000000" style={{ color: "rgba(255,255,255,0.50)", fontWeight: 600 }}>
              +966 50 000 0000
            </a>
          </p>
        </section>

        {/* ══ FOOTER ═══════════════════════════════════════════════════ */}
        <footer
          role="contentinfo"
          style={{
            borderTop: "1px solid rgba(255,255,255,0.07)",
            paddingTop: "var(--sp-10)",
            paddingBottom: "var(--sp-8)",
          }}
        >
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: "var(--sp-8)", marginBottom: "var(--sp-8)" }}>
            <div>
              <p className="navbar-brand" style={{ fontSize: "1.3rem", marginBottom: "var(--sp-3)" }}>Dealix</p>
              <p style={{ fontSize: "0.85rem", color: "rgba(255,255,255,0.45)", lineHeight: 1.7, maxWidth: "240px" }}>
                نظام Revenue OS للشركات السعودية B2B. مبني على موافقتك، لا يرسل بدون إذن.
              </p>
            </div>
            <div>
              <p style={{ fontWeight: 700, fontSize: "0.88rem", color: "rgba(255,255,255,0.60)", marginBottom: "var(--sp-4)", letterSpacing: "0.08em", textTransform: "uppercase" }}>العروض</p>
              <nav aria-label="Offers navigation">
                {[["التشخيص المجاني", "/book"], ["ميكرو سبرينت", "/offers"], ["سبرينت التشخيص", "/offers"], ["التشغيل المُدار", "/offers"]].map(([label, href]) => (
                  <Link key={label} href={href} style={{ display: "block", color: "rgba(255,255,255,0.45)", fontSize: "0.88rem", marginBottom: "var(--sp-2)", fontWeight: 500 }}>
                    {label}
                  </Link>
                ))}
              </nav>
            </div>
            <div>
              <p style={{ fontWeight: 700, fontSize: "0.88rem", color: "rgba(255,255,255,0.60)", marginBottom: "var(--sp-4)", letterSpacing: "0.08em", textTransform: "uppercase" }}>المنتج</p>
              <nav aria-label="Product navigation">
                {[["الصفحة الرئيسية", "/"], ["الأنظمة", "/offers"], ["التسعير", "/pricing"], ["الأمان", "/safety"]].map(([label, href]) => (
                  <Link key={label} href={href} style={{ display: "block", color: "rgba(255,255,255,0.45)", fontSize: "0.88rem", marginBottom: "var(--sp-2)", fontWeight: 500 }}>
                    {label}
                  </Link>
                ))}
              </nav>
            </div>
            <div>
              <p style={{ fontWeight: 700, fontSize: "0.88rem", color: "rgba(255,255,255,0.60)", marginBottom: "var(--sp-4)", letterSpacing: "0.08em", textTransform: "uppercase" }}>تواصل</p>
              <a href="https://wa.me/966500000000" style={{ display: "block", color: "rgba(255,255,255,0.45)", fontSize: "0.88rem", marginBottom: "var(--sp-2)", fontWeight: 500 }}>
                واتساب
              </a>
              <a href="mailto:founder@dealix.sa" style={{ display: "block", color: "rgba(255,255,255,0.45)", fontSize: "0.88rem", marginBottom: "var(--sp-2)", fontWeight: 500 }}>
                البريد الإلكتروني
              </a>
              <Link href="/book" style={{ display: "block", color: "var(--dealix-gold)", fontSize: "0.88rem", fontWeight: 600 }}>
                احجز التشخيص →
              </Link>
            </div>
          </div>

          <div style={{ borderTop: "1px solid rgba(255,255,255,0.05)", paddingTop: "var(--sp-6)", display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "var(--sp-4)" }}>
            <p style={{ fontSize: "0.80rem", color: "rgba(255,255,255,0.25)" }}>
              © 2026 Dealix · جميع الحقوق محفوظة · PDPL متوافق · ZATCA-Aware
            </p>
            <div style={{ display: "flex", gap: "var(--sp-6)" }}>
              <Link href="/legal" style={{ color: "rgba(255,255,255,0.30)", fontSize: "0.80rem", fontWeight: 500 }}>الشروط</Link>
              <Link href="/safety" style={{ color: "rgba(255,255,255,0.30)", fontSize: "0.80rem", fontWeight: 500 }}>الأمان</Link>
              <a href="https://github.com/Dealix-sa/dealix" style={{ color: "rgba(255,255,255,0.30)", fontSize: "0.80rem", fontWeight: 500 }}>GitHub</a>
            </div>
          </div>
        </footer>

      </main>
    </>
  );
}
