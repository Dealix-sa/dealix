import Link from "next/link";

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? "https://dealix.me";

const launchOffers = [
  {
    title: "Revenue Command Room OS",
    pain: "الفرص والعروض والمتابعات موجودة، لكن لا تتحول إلى قرار يومي واضح.",
    outcome: "غرفة قيادة تعرض العملاء الساخنين، المتابعات المتأخرة، العروض المفتوحة، وأول 10 إجراءات اليوم.",
    timeline: "7 أيام",
    price: "5,000–12,000 ريال",
    href: "/revenue-machine",
  },
  {
    title: "Company Brain OS",
    pain: "الإدارة ترى تقارير كثيرة لكن لا ترى القرار الأهم اليوم.",
    outcome: "Daily CEO Decision + Future Radar + 30-Day Action Plan مبني على إشارات الإيراد والمتابعة والمخاطر.",
    timeline: "14 يوم",
    price: "7,500–25,000 ريال",
    href: "/brain",
  },
  {
    title: "WhatsApp / Inbox Follow-up OS",
    pain: "واتساب والإيميل يتحولون إلى مقبرة فرص ومحادثات بلا owner.",
    outcome: "تصنيف المحادثات، queue متابعة، مسودات ردود، وتقرير يومي بدون إرسال تلقائي.",
    timeline: "7–10 أيام",
    price: "5,000–12,000 ريال",
    href: "/outreach-review",
  },
  {
    title: "AI Trust & Compliance OS",
    pain: "الشركة تستخدم AI بدون سياسة، صلاحيات، أو مراجعة بشرية واضحة.",
    outcome: "AI usage policy، approval gates، data handling SOP، وسجل مراجعة للمخرجات الحساسة.",
    timeline: "7 أيام",
    price: "7,500–25,000 ريال",
    href: "/safety",
  },
];

const proofBlocks = [
  ["No fake ROI", "لا نعد بدخل مضمون؛ نثبت الأثر بتقارير وقرارات وقياسات تشغيلية."],
  ["Draft-first", "كل تواصل خارجي يبدأ كمسودة، ثم يراجعها الإنسان قبل الإرسال."],
  ["Saudi B2B", "اللغة، القطاعات، التسعير، وطرق البيع مبنية على واقع الشركات السعودية."],
  ["Proof Pack", "كل مشروع ينتهي بملف قبل/بعد، قرارات، مخاطر، وأعمال منجزة."],
];

const sectors = [
  "العيادات",
  "العقار",
  "اللوجستيات",
  "التدريب",
  "وكالات التسويق",
  "خدمات B2B",
  "معارض السيارات",
  "المكاتب المهنية",
];

const processSteps = [
  ["01", "Map", "نفهم الإيراد، العملاء، القنوات، المتابعة، والبيانات الموجودة."],
  ["02", "Design", "نحوّل الألم إلى workflow واحد واضح، قبولاته محددة ومخاطره معروفة."],
  ["03", "Build", "نبني dashboard، ledgers، drafts، reports، وapproval gates بدون تعطيل أنظمتك الحالية."],
  ["04", "Operate", "نشغل اليوم التجاري: فرص، متابعات، عروض، قرارات، وتقرير مؤسس يومي."],
  ["05", "Scale", "بعد proof، نضيف التكاملات والإرسال المحكوم والـretainer الشهري."],
];

const structuredData = {
  "@context": "https://schema.org",
  "@type": "Organization",
  name: "Dealix",
  url: siteUrl,
  areaServed: { "@type": "Country", name: "Saudi Arabia" },
  description:
    "Dealix builds AI operating systems for Saudi B2B companies: revenue command rooms, company brain, follow-up OS, client delivery, and AI trust controls.",
  knowsAbout: [
    "Revenue Operations",
    "AI Governance",
    "B2B Sales Operations",
    "Saudi Business Automation",
    "Client Delivery Systems",
  ],
};

export default function HomePage() {
  return (
    <>
      <nav className="navbar" aria-label="Primary navigation">
        <Link href="/" className="navbar-brand" aria-label="Dealix Home">
          Dealix
        </Link>
        <ul className="navbar-links" role="list">
          <li><Link href="/revenue-machine">Revenue OS</Link></li>
          <li><Link href="/brain">Company Brain</Link></li>
          <li><Link href="/pricing">Pricing</Link></li>
          <li><Link href="/founder/command-room">غرفة القيادة</Link></li>
          <li><Link href="/book">Book Review</Link></li>
        </ul>
        <div className="actions" style={{ marginTop: 0 }}>
          <Link href="/ar" style={{ minHeight: 38, padding: "0 18px", fontSize: "0.82rem" }}>
            عربي
          </Link>
          <Link href="/book" style={{ minHeight: 38, padding: "0 18px", fontSize: "0.82rem" }}>
            احجز مراجعة →
          </Link>
        </div>
      </nav>

      <main className="grid">
        <script
          type="application/ld+json"
          suppressHydrationWarning
          dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }}
        />

        <section
          className="card dot-pattern animate-fade-up"
          aria-labelledby="hero-title"
          style={{
            position: "relative",
            overflow: "hidden",
            paddingTop: "clamp(44px,7vw,86px)",
            paddingBottom: "clamp(44px,7vw,86px)",
          }}
        >
          <div
            aria-hidden="true"
            style={{
              position: "absolute",
              inset: "-120px auto auto -120px",
              width: 460,
              height: 460,
              background: "radial-gradient(circle, rgba(212,175,55,0.14), transparent 68%)",
              pointerEvents: "none",
            }}
          />

          <p className="eyebrow">Saudi B2B · Founder-led · Approval-first AI</p>
          <h1 id="hero-title" style={{ maxWidth: 980 }}>
            نبني للشركات السعودية <span className="gradient-text">AI Operating Systems</span>
            <br /> تضبط الإيراد، المتابعة، والقرار اليومي.
          </h1>
          <p style={{ maxWidth: 760, fontSize: "1.16rem", lineHeight: 1.85 }}>
            Dealix ليست شات بوت ولا CRM عادي. نحن نبني نظام تشغيل عملي يربط المبيعات، واتساب، العروض،
            التقارير، التسليم، والحوكمة في workflow يومي قابل للقياس — مع مراجعة بشرية قبل أي إجراء خارجي حساس.
          </p>

          <div className="actions" aria-label="Primary actions">
            <Link href="/book">احجز مراجعة تشغيلية</Link>
            <Link href="/pricing">شاهد الباقات</Link>
            <Link href="/safety">كيف نحافظ على الأمان؟</Link>
          </div>
        </section>

        <section className="grid-3" aria-label="Commercial proof points">
          {proofBlocks.map(([title, text]) => (
            <article className="card" key={title}>
              <span className="badge badge-gold">{title}</span>
              <p style={{ marginTop: "var(--sp-4)" }}>{text}</p>
            </article>
          ))}
        </section>

        <section className="card" aria-labelledby="problem-title">
          <p className="eyebrow">The real problem</p>
          <h2 id="problem-title">الشركة لا تحتاج أدوات أكثر؛ تحتاج نظام تشغيل يومي.</h2>
          <div className="grid-2">
            <div>
              <h3>قبل Dealix</h3>
              <ul>
                <li>فرص تأتي من واتساب، إيميل، اتصال، موقع — ولا تدخل في قرار يومي.</li>
                <li>العروض تُرسل ثم تختفي المتابعة.</li>
                <li>الإدارة ترى أرقامًا متأخرة بدل next action اليوم.</li>
                <li>AI يُستخدم بشكل عشوائي بدون سياسة أو approval gates.</li>
              </ul>
            </div>
            <div>
              <h3>بعد Dealix</h3>
              <ul>
                <li>كل فرصة لها owner، status، next action، وreview date.</li>
                <li>كل follow-up يظهر في queue واضحة.</li>
                <li>كل صباح يوجد CEO decision وcommercial command report.</li>
                <li>كل رسالة خارجية تبدأ draft وتحتاج مراجعة بشرية.</li>
              </ul>
            </div>
          </div>
        </section>

        <section aria-labelledby="offers-title">
          <p className="eyebrow">What we sell first</p>
          <h2 id="offers-title">باقات إطلاق قابلة للبيع خلال أيام، لا مشاريع ضخمة بلا proof.</h2>
          <div className="cards">
            {launchOffers.map((offer) => (
              <article className="card" key={offer.title}>
                <span className="badge badge-emerald">{offer.timeline}</span>
                <h3 style={{ marginTop: "var(--sp-4)" }}>{offer.title}</h3>
                <p><strong>الألم:</strong> {offer.pain}</p>
                <p><strong>الناتج:</strong> {offer.outcome}</p>
                <p className="text-gold" style={{ fontWeight: 800 }}>Suggested range: {offer.price}</p>
                <Link href={offer.href} className="btn btn-secondary">افتح التفاصيل →</Link>
              </article>
            ))}
          </div>
        </section>

        <section className="card" aria-labelledby="process-title">
          <p className="eyebrow">Delivery method</p>
          <h2 id="process-title">Map → Design → Build → Operate → Scale</h2>
          <div className="grid-3">
            {processSteps.map(([step, title, text]) => (
              <article key={step} style={{ padding: "var(--sp-4)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: "var(--r-lg)" }}>
                <span className="badge badge-gold">{step}</span>
                <h3 style={{ marginTop: "var(--sp-3)" }}>{title}</h3>
                <p>{text}</p>
              </article>
            ))}
          </div>
        </section>

        <section className="card card-gold" aria-labelledby="sectors-title">
          <p className="eyebrow">Saudi sectors</p>
          <h2 id="sectors-title">نبدأ من القطاعات التي يظهر فيها ألم المتابعة والإيراد بسرعة.</h2>
          <div style={{ display: "flex", flexWrap: "wrap", gap: "var(--sp-2)" }}>
            {sectors.map((sector) => (
              <span className="badge badge-gold" key={sector}>{sector}</span>
            ))}
          </div>
        </section>

        <section className="card" aria-labelledby="outbound-title">
          <p className="eyebrow">High-velocity, not spam</p>
          <h2 id="outbound-title">استهداف يومي قوي، لكن يحافظ على السمعة والدومين.</h2>
          <p>
            النظام الصحيح ليس إرسال عشوائي. النظام الصحيح: 100 شركة تُبحث يوميًا، 40 تُتحقق،
            25 مسودة تُكتب، 10–15 رسالة تُراجع يدويًا، 3 مكالمات، وعرض واحد واضح — مع opt-out وsource_url لكل target.
          </p>
          <div className="actions">
            <Link href="/outreach-review">راجع مسودات الاستهداف</Link>
            <Link href="/command-center">افتح غرفة القيادة</Link>
          </div>
        </section>

        <section className="card" aria-labelledby="final-cta-title" style={{ textAlign: "center" }}>
          <p className="eyebrow">Start small. Prove fast. Scale safely.</p>
          <h2 id="final-cta-title">ابدأ بـ7 أيام على ألم واحد واضح.</h2>
          <p style={{ maxWidth: 720, margin: "0 auto var(--sp-6)" }}>
            إذا كان عندك واتساب مزدحم، عروض بلا متابعة، أو فريق لا يعرف أولويات اليوم،
            نبدأ بتشخيص سريع ثم نبني sprint واضح بنتائج تشغيلية قابلة للمراجعة.
          </p>
          <div className="actions" style={{ justifyContent: "center" }}>
            <Link href="/book">احجز مراجعة Dealix</Link>
            <Link href="/offers">شاهد العروض</Link>
          </div>
        </section>

        <footer style={{ textAlign: "center", paddingTop: "var(--sp-8)", borderTop: "1px solid rgba(255,255,255,0.07)" }}>
          <p className="navbar-brand" style={{ justifyContent: "center", fontSize: "1.2rem", marginBottom: "var(--sp-3)" }}>
            Dealix
          </p>
          <div style={{ display: "flex", justifyContent: "center", gap: "var(--sp-4)", marginBottom: "var(--sp-4)", flexWrap: "wrap" }}>
            <Link href="/revenue-machine" style={{ color: "rgba(255,255,255,0.46)", fontWeight: 500, fontSize: "0.82rem" }}>Revenue OS</Link>
            <Link href="/brain" style={{ color: "rgba(255,255,255,0.46)", fontWeight: 500, fontSize: "0.82rem" }}>Company Brain</Link>
            <Link href="/pricing" style={{ color: "rgba(255,255,255,0.46)", fontWeight: 500, fontSize: "0.82rem" }}>Pricing</Link>
            <Link href="/book" style={{ color: "rgba(255,255,255,0.46)", fontWeight: 500, fontSize: "0.82rem" }}>Book</Link>
            <Link href="/legal" style={{ color: "rgba(255,255,255,0.46)", fontWeight: 500, fontSize: "0.82rem" }}>Legal</Link>
          </div>
          <p style={{ fontSize: "0.82rem", color: "rgba(255,255,255,0.34)" }}>
            © 2026 Dealix · Saudi-first AI Operating Systems · no uncontrolled external sending
          </p>
        </footer>
      </main>
    </>
  );
}
