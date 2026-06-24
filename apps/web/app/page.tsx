import Link from "next/link";

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? "https://dealix.me";

const pains = [
  "فرص تضيع بين واتساب، الإيميل، المكالمات، وملفات Excel.",
  "عروض تتحضر ثم تختفي بدون متابعة موحدة أو مالك واضح.",
  "الإدارة لا ترى تقريرًا يوميًا يحول البيانات إلى قرار.",
  "الأدوات كثيرة، لكن لا يوجد operating rhythm واحد.",
];

const offers = [
  {
    title: "AI Revenue Diagnostic",
    price: "0–1,500 SAR",
    description: "تشخيص سريع لمسار الفرص والمتابعة قبل أي بناء كبير.",
    href: "/commercial-launch",
  },
  {
    title: "7-Day Revenue Command Room Sprint",
    price: "5,000–12,000 SAR",
    description: "غرفة قيادة يومية للفرص، المتابعات، العروض، والقرار الإداري.",
    href: "/commercial-launch",
  },
  {
    title: "Managed OS Retainer",
    price: "3,000–25,000 SAR / month",
    description: "تشغيل شهري وتحسين مستمر بعد إثبات القيمة في Sprint.",
    href: "/pricing",
  },
];

const systems = [
  ["Revenue Command Room", "متابعة فرص، عروض، next actions، وProof Pack يومي/أسبوعي."],
  ["Company Brain OS", "قرار إداري يومي، bottlenecks، ومذكرة تنفيذية أسبوعية."],
  ["Client Delivery OS", "تحويل كل عميل إلى workspace: intake، diagnosis، blueprint، proof."],
  ["Trust & Governance", "مراجعة بشرية، سجلات، ضوابط، ومنع وعود غير موثقة."],
];

const steps = [
  ["01", "Map", "نرسم مسار الفرص والتعطل الحالي."],
  ["02", "Build", "نجهز غرفة القيادة والـledgers الأساسية."],
  ["03", "Operate", "نحول البيانات إلى قرارات يومية ومسودات مراجعة."],
  ["04", "Prove", "ننتج Proof Pack وخطة 30 يوم."],
];

const trust = [
  "لا وعود ROI غير موثقة.",
  "لا شعارات عملاء وهمية.",
  "كل محتوى حساس يمر بمراجعة بشرية.",
  "البداية Founder-led وليست self-serve SaaS مفتوح.",
];

const structuredData = {
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  name: "Dealix",
  applicationCategory: "BusinessApplication",
  operatingSystem: "Web",
  url: siteUrl,
  description: "Saudi-first B2B AI operating system for revenue command, company brain, client delivery, and proof-driven operations.",
  areaServed: { "@type": "Country", name: "Saudi Arabia" },
  offers: { "@type": "Offer", priceCurrency: "SAR", availability: "https://schema.org/InStock" },
  publisher: { "@type": "Organization", name: "Dealix", url: siteUrl },
};

function Card({ children }: { children: React.ReactNode }) {
  return <article className="card hover-gold">{children}</article>;
}

export default function HomePage() {
  return (
    <>
      <nav className="navbar" aria-label="Primary navigation">
        <Link href="/" className="navbar-brand" aria-label="Dealix Home">
          Dealix
        </Link>
        <ul className="navbar-links" role="list">
          <li><Link href="/commercial-launch">الإطلاق التجاري</Link></li>
          <li><Link href="/offers">العروض</Link></li>
          <li><Link href="/pricing">التسعير</Link></li>
          <li><Link href="/book">احجز مراجعة</Link></li>
        </ul>
        <div className="actions" style={{ marginTop: 0 }}>
          <Link href="/commercial-launch" style={{ minHeight: 38, padding: "0 18px", fontSize: "0.82rem" }}>
            ابدأ الآن
          </Link>
        </div>
      </nav>

      <main className="grid">
        <script
          type="application/ld+json"
          suppressHydrationWarning
          dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }}
        />

        <section className="card card-gold dot-pattern animate-fade-up" aria-labelledby="hero-title">
          <p className="eyebrow">Saudi-first · Revenue-focused · Review-first</p>
          <h1 id="hero-title" style={{ maxWidth: 960 }}>
            Dealix يحوّل فوضى الفرص والمتابعة إلى <span className="gradient-text">Company Operating System</span>
          </h1>
          <p style={{ maxWidth: 760, fontSize: "1.15rem" }}>
            نظام تشغيل للشركات السعودية يربط الفرص، المتابعات، العروض، التسليم، وقرارات الإدارة في workflow يومي قابل للقياس خلال Sprint واضح.
          </p>
          <div className="actions" aria-label="Primary actions">
            <Link href="/commercial-launch">ابدأ بتشخيص تجاري</Link>
            <Link href="/pricing">راجع الباقات</Link>
            <Link href="/safety">شاهد طبقة الثقة</Link>
          </div>
        </section>

        <section className="cards" aria-label="Key positioning">
          <Card>
            <p className="stat-value">7</p>
            <p className="stat-label">أيام لإثبات التشغيل الأول</p>
          </Card>
          <Card>
            <p className="stat-value">SAR</p>
            <p className="stat-label">تسعير سعودي واضح</p>
          </Card>
          <Card>
            <p className="stat-value">Proof</p>
            <p className="stat-label">كل Sprint ينتهي بدليل تشغيل</p>
          </Card>
          <Card>
            <p className="stat-value">Human</p>
            <p className="stat-label">مراجعة بشرية للقرارات الحساسة</p>
          </Card>
        </section>

        <section className="card" aria-labelledby="pain-title" dir="rtl">
          <p className="eyebrow">المشكلة</p>
          <h2 id="pain-title">الشركات لا تحتاج أداة جديدة فقط — تحتاج إيقاع تشغيل يومي</h2>
          <p>
            Dealix يبدأ من الألم التشغيلي: أين تضيع الفرص؟ أين تتأخر المتابعة؟ لماذا لا تتحول البيانات إلى قرار؟
          </p>
          <div className="cards" style={{ marginTop: "var(--sp-6)" }}>
            {pains.map((pain) => (
              <Card key={pain}>
                <span className="badge badge-gold">Pain</span>
                <h3 style={{ marginTop: "var(--sp-4)" }}>{pain}</h3>
              </Card>
            ))}
          </div>
        </section>

        <section className="card" aria-labelledby="systems-title" dir="rtl">
          <p className="eyebrow">الأنظمة</p>
          <h2 id="systems-title">منصة واحدة تبدأ بـRevenue Command Room وتتوسع إلى Company OS</h2>
          <div className="cards" style={{ marginTop: "var(--sp-6)" }}>
            {systems.map(([title, description]) => (
              <Card key={title}>
                <h3>{title}</h3>
                <p>{description}</p>
              </Card>
            ))}
          </div>
        </section>

        <section className="card" aria-labelledby="process-title" dir="rtl">
          <p className="eyebrow">طريقة العمل</p>
          <h2 id="process-title">Map → Build → Operate → Prove</h2>
          <div className="cards" style={{ marginTop: "var(--sp-6)" }}>
            {steps.map(([number, title, description]) => (
              <Card key={number}>
                <p className="stat-value" style={{ fontSize: "2rem" }}>{number}</p>
                <h3>{title}</h3>
                <p>{description}</p>
              </Card>
            ))}
          </div>
        </section>

        <section className="card" aria-labelledby="offers-title" dir="rtl">
          <p className="eyebrow">العروض</p>
          <h2 id="offers-title">باقات واضحة للبيع الآن</h2>
          <div className="cards" style={{ marginTop: "var(--sp-6)" }}>
            {offers.map((offer) => (
              <Card key={offer.title}>
                <span className="badge badge-emerald">Founder-led</span>
                <h3 style={{ marginTop: "var(--sp-4)" }}>{offer.title}</h3>
                <p className="stat-value" style={{ fontSize: "1.6rem" }}>{offer.price}</p>
                <p>{offer.description}</p>
                <Link className="btn btn-secondary" href={offer.href}>اعرف أكثر</Link>
              </Card>
            ))}
          </div>
        </section>

        <section className="card" aria-labelledby="trust-title" dir="rtl">
          <p className="eyebrow">الثقة</p>
          <h2 id="trust-title">نمو منظم بدون مبالغة</h2>
          <ul>
            {trust.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </section>

        <section className="card card-gold text-center" aria-labelledby="cta-title" dir="rtl">
          <p className="eyebrow">ابدأ الآن</p>
          <h2 id="cta-title">ابدأ بتشخيص واحد بدل مشروع كبير</h2>
          <p>
            إذا كان الألم واضحًا، نبدأ Sprint. إذا لم يظهر دليل قيمة، لا نوسع. هذا هو الطريق التجاري العملي للإطلاق الآن.
          </p>
          <div className="actions" style={{ justifyContent: "center" }}>
            <Link href="/book">احجز مراجعة</Link>
            <Link href="/commercial-launch">صفحة الإطلاق التجاري</Link>
          </div>
        </section>

        <footer style={{ textAlign: "center", paddingTop: "var(--sp-8)", borderTop: "1px solid rgba(255,255,255,0.07)" }}>
          <p className="navbar-brand" style={{ justifyContent: "center", fontSize: "1.2rem", marginBottom: "var(--sp-3)" }}>
            Dealix
          </p>
          <div style={{ display: "flex", justifyContent: "center", gap: "var(--sp-4)", marginBottom: "var(--sp-4)", flexWrap: "wrap" }}>
            <Link href="/commercial-launch" style={{ color: "rgba(255,255,255,0.40)", fontWeight: 500, fontSize: "0.82rem" }}>الإطلاق التجاري</Link>
            <Link href="/offers" style={{ color: "rgba(255,255,255,0.40)", fontWeight: 500, fontSize: "0.82rem" }}>العروض</Link>
            <Link href="/pricing" style={{ color: "rgba(255,255,255,0.40)", fontWeight: 500, fontSize: "0.82rem" }}>التسعير</Link>
            <Link href="/book" style={{ color: "rgba(255,255,255,0.40)", fontWeight: 500, fontSize: "0.82rem" }}>احجز مراجعة</Link>
            <Link href="/legal" style={{ color: "rgba(255,255,255,0.40)", fontWeight: 500, fontSize: "0.82rem" }}>الشروط</Link>
          </div>
          <p style={{ fontSize: "0.82rem", color: "rgba(255,255,255,0.30)" }}>
            © 2026 Dealix · Saudi-first AI Operating Systems · <Link href="/safety" style={{ color: "rgba(255,255,255,0.40)", fontWeight: 500 }}>Safety</Link>
          </p>
        </footer>
      </main>
    </>
  );
}
