import Link from "next/link";

export const metadata = {
  title: "التسعير — Dealix",
  description: "أسعار شفافة بالريال السعودي. من التشخيص المجاني إلى الأنظمة المؤسسية. لا رسوم خفية.",
};

const tiers = [
  {
    id: "free",
    name: "التشخيص المجاني",
    nameEn: "Free Diagnostic",
    setup: "٠",
    monthly: "—",
    duration: "٣٠ دقيقة",
    color: "#10B981",
    features: ["جلسة واحدة مع المؤسس", "تحليل ٣ ثغرات", "ملخص مكتوب", "توصية فورية"],
    cta: "ابدأ مجاناً",
    href: "/book",
    highlight: false,
  },
  {
    id: "micro",
    name: "ميكرو سبرينت",
    nameEn: "Micro Sprint",
    setup: "٤٩٩",
    monthly: "—",
    duration: "يوم – يومان",
    color: "#F59E0B",
    features: ["نظام مصغر يعمل", "أتمتة مهمة واحدة", "كود مسلّم كاملاً", "دليل عربي"],
    cta: "اطلب الآن",
    href: "/book",
    highlight: false,
  },
  {
    id: "data",
    name: "حزمة البيانات",
    nameEn: "Data Pack",
    setup: "١,٥٠٠",
    monthly: "—",
    duration: "مرة واحدة",
    color: "#0066FF",
    features: ["٥٠+ شركة مستهدفة", "تقييم ICP كامل", "جاهز للتصدير", "بيانات مدققة"],
    cta: "اطلب الآن",
    href: "/book",
    highlight: false,
  },
  {
    id: "managed",
    name: "التشغيل المُدار",
    nameEn: "Managed Ops",
    setup: "—",
    monthly: "٢,٩٩٩–٤,٩٩٩",
    duration: "شهرياً",
    color: "#D4AF37",
    features: ["تقرير يومي واتساب", "إدارة المتابعات", "مسودات جاهزة", "دعم مباشر"],
    cta: "اشترك",
    href: "/book",
    highlight: true,
  },
  {
    id: "sprint",
    name: "سبرينت التشخيص",
    nameEn: "Diagnostic Sprint",
    setup: "٧,٥٠٠–٢٥,٠٠٠",
    monthly: "—",
    duration: "٣–٧ أيام",
    color: "#D4AF37",
    features: ["Revenue OS كامل", "خريطة التسرب", "Proof Pack", "خطة ١٤ يوم", "دعم ٣٠ يوم"],
    cta: "احجز",
    href: "/book",
    highlight: true,
  },
  {
    id: "enterprise",
    name: "نظام مؤسسي",
    nameEn: "Enterprise",
    setup: "٢٥,٠٠٠+",
    monthly: "حسب الاتفاق",
    duration: "٤–١٢ أسبوعاً",
    color: "#EF4444",
    features: ["نظام مخصص كلياً", "تكامل كامل", "SLA مضمون", "تدريب الفريق", "توثيق شامل"],
    cta: "تحدث معنا",
    href: "/book",
    highlight: false,
  },
];

const rules = [
  "التشخيص المجاني لا يتطلب أي معلومات بطاقة ائتمانية.",
  "الـ Setup fee قابل للاسترداد خلال ١٤ يوم إذا لم تُقدَّم الخدمة.",
  "الاشتراك الشهري يُلغى بإشعار ٣٠ يوم — لا عقود سنوية إجبارية.",
  "لا auto-renewal بصمت — إشعار مسبق قبل ١٤ يوم من التجديد.",
  "الكود والتوثيق المُسلَّم ملكٌ لك بالكامل بعد الدفع.",
  "جميع الأسعار بالريال السعودي SAR شاملة VAT.",
];

export default function PricingPage() {
  return (
    <main style={{ display: "flex", flexDirection: "column", gap: "var(--sp-12)", paddingBottom: "var(--sp-16)" }}>

      {/* Nav */}
      <nav className="navbar" aria-label="Primary navigation">
        <Link href="/" className="navbar-brand">Dealix</Link>
        <ul className="navbar-links" role="list">
          <li><Link href="/">الرئيسية</Link></li>
          <li><Link href="/offers">العروض</Link></li>
          <li><Link href="/book">احجز</Link></li>
        </ul>
        <div className="actions" style={{ marginTop: 0 }}>
          <Link href="/book" className="btn btn-secondary" style={{ minHeight: 38, padding: "0 18px", fontSize: "0.85rem" }}>
            احجز التشخيص المجاني →
          </Link>
        </div>
      </nav>

      {/* Header */}
      <section className="card dot-pattern" style={{ padding: "clamp(40px,6vw,72px)", textAlign: "center" }}>
        <p className="eyebrow" style={{ display: "flex", justifyContent: "center" }}>التسعير</p>
        <h1 style={{ maxWidth: "700px", margin: "0 auto var(--sp-4)" }}>
          شفاف، بدون{" "}
          <span className="gradient-text">فخ</span>
        </h1>
        <p style={{ maxWidth: "520px", margin: "0 auto var(--sp-6)", color: "rgba(255,255,255,0.65)", fontSize: "1.05rem", lineHeight: 1.8 }}>
          ٦ عروض، كل واحد له سعر واضح. تبدأ مجاناً، تدفع فقط بعد ما تشوف القيمة.
        </p>
        <div style={{ display: "flex", gap: "var(--sp-3)", justifyContent: "center", flexWrap: "wrap" }}>
          <Link href="/book" className="btn btn-primary" style={{ fontSize: "0.95rem", padding: "12px 28px" }}>
            ابدأ بالتشخيص المجاني
          </Link>
          <Link href="/offers" className="btn btn-secondary" style={{ fontSize: "0.95rem", padding: "12px 24px" }}>
            تفاصيل العروض
          </Link>
        </div>
      </section>

      {/* Pricing Cards */}
      <section aria-labelledby="pricing-grid-title">
        <h2 id="pricing-grid-title" style={{ marginBottom: "var(--sp-6)" }}>جميع العروض بنظرة واحدة</h2>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))", gap: "var(--sp-4)" }}>
          {tiers.map(({ id, name, nameEn, setup, monthly, duration, color, features, cta, href, highlight }) => (
            <article
              key={id}
              className="card"
              style={{
                padding: "var(--sp-8) var(--sp-6)",
                position: "relative",
                display: "flex", flexDirection: "column",
                border: highlight ? "2px solid var(--dealix-gold)" : undefined,
                background: highlight ? "rgba(212,175,55,0.04)" : undefined,
              }}
            >
              {highlight && (
                <span style={{
                  position: "absolute", top: "-12px", right: "20px",
                  background: "var(--dealix-gold)", color: "#001F3F",
                  fontSize: "0.72rem", fontWeight: 700, padding: "3px 12px",
                  borderRadius: "var(--r-pill)", letterSpacing: "0.05em",
                }}>
                  الأكثر طلباً
                </span>
              )}

              <p style={{ fontSize: "0.75rem", color: "rgba(255,255,255,0.40)", marginBottom: "var(--sp-2)", letterSpacing: "0.05em" }}>{nameEn}</p>
              <h3 style={{ fontSize: "1.15rem", marginBottom: "var(--sp-4)", color: "#fff" }}>{name}</h3>

              <div style={{ marginBottom: "var(--sp-2)" }}>
                <p style={{ fontSize: "0.75rem", color: "rgba(255,255,255,0.40)", marginBottom: "var(--sp-1)", textTransform: "uppercase", letterSpacing: "0.06em" }}>Setup</p>
                <span style={{ fontSize: "1.9rem", fontWeight: 800, color, fontFamily: "var(--font-display)", lineHeight: 1 }}>
                  {setup}
                </span>
                {setup !== "—" && setup !== "٠" && <span style={{ fontSize: "0.85rem", color: "rgba(255,255,255,0.45)", marginRight: "var(--sp-1)" }}> ريال</span>}
              </div>

              <div style={{ marginBottom: "var(--sp-5)" }}>
                <p style={{ fontSize: "0.75rem", color: "rgba(255,255,255,0.40)", marginBottom: "var(--sp-1)", textTransform: "uppercase", letterSpacing: "0.06em" }}>شهرياً</p>
                <span style={{ fontSize: "1.1rem", fontWeight: 700, color: monthly === "—" ? "rgba(255,255,255,0.30)" : "rgba(255,255,255,0.85)" }}>
                  {monthly}{monthly !== "—" && <span style={{ fontSize: "0.80rem", fontWeight: 400, color: "rgba(255,255,255,0.45)", marginRight: "4px" }}> ريال</span>}
                </span>
              </div>

              <p style={{ fontSize: "0.80rem", color: "rgba(255,255,255,0.45)", marginBottom: "var(--sp-5)" }}>⏱ {duration}</p>

              <div className="divider-gold" />

              <ul style={{ listStyle: "none", padding: 0, display: "flex", flexDirection: "column", gap: "var(--sp-2)", marginBottom: "var(--sp-6)", flex: 1 }}>
                {features.map((f) => (
                  <li key={f} style={{ fontSize: "0.87rem", color: "rgba(255,255,255,0.70)", display: "flex", gap: "var(--sp-2)", alignItems: "flex-start" }}>
                    <span style={{ color: "#10B981", flexShrink: 0 }}>✓</span>
                    {f}
                  </li>
                ))}
              </ul>

              <Link
                href={href}
                className={highlight ? "btn btn-primary" : "btn btn-secondary"}
                style={{ width: "100%", textAlign: "center", fontSize: "0.88rem" }}
              >
                {cta} →
              </Link>
            </article>
          ))}
        </div>
      </section>

      {/* Comparison Table */}
      <section aria-labelledby="comparison-title">
        <h2 id="comparison-title" style={{ marginBottom: "var(--sp-6)" }}>مقارنة سريعة</h2>
        <div style={{ overflowX: "auto" }}>
          <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "0.88rem" }}>
            <thead>
              <tr style={{ background: "rgba(212,175,55,0.08)", borderBottom: "2px solid rgba(212,175,55,0.2)" }}>
                <th style={{ padding: "var(--sp-4)", textAlign: "right", color: "rgba(255,255,255,0.60)", fontWeight: 700, fontSize: "0.78rem", textTransform: "uppercase", letterSpacing: "0.08em" }}>العرض</th>
                <th style={{ padding: "var(--sp-4)", textAlign: "center", color: "rgba(255,255,255,0.60)", fontWeight: 700, fontSize: "0.78rem", textTransform: "uppercase", letterSpacing: "0.08em" }}>السعر (SAR)</th>
                <th style={{ padding: "var(--sp-4)", textAlign: "center", color: "rgba(255,255,255,0.60)", fontWeight: 700, fontSize: "0.78rem", textTransform: "uppercase", letterSpacing: "0.08em" }}>المدة</th>
                <th style={{ padding: "var(--sp-4)", textAlign: "center", color: "rgba(255,255,255,0.60)", fontWeight: 700, fontSize: "0.78rem", textTransform: "uppercase", letterSpacing: "0.08em" }}>مناسب لـ</th>
              </tr>
            </thead>
            <tbody>
              {[
                ["التشخيص المجاني", "مجاني", "٣٠ دقيقة", "الجميع"],
                ["ميكرو سبرينت", "٤٩٩", "١–٢ يوم", "من يريد تجربة قبل الالتزام"],
                ["حزمة البيانات", "١,٥٠٠", "مرة واحدة", "من يحتاج بيانات عملاء محتملين"],
                ["التشغيل المُدار", "٢,٩٩٩–٤,٩٩٩/شهر", "شهري", "الشركات التي تريد تشغيلاً مستمراً"],
                ["سبرينت التشخيص", "٧,٥٠٠–٢٥,٠٠٠", "٣–٧ أيام", "من يريد نظاماً متكاملاً بسرعة"],
                ["نظام مؤسسي", "٢٥,٠٠٠+", "٤–١٢ أسبوع", "المؤسسات الكبيرة"],
              ].map(([name, price, duration, suitable], i) => (
                <tr
                  key={name}
                  style={{
                    borderBottom: "1px solid rgba(255,255,255,0.06)",
                    background: i % 2 === 0 ? "transparent" : "rgba(255,255,255,0.02)",
                  }}
                >
                  <td style={{ padding: "var(--sp-4)", fontWeight: 600, color: "#fff" }}>{name}</td>
                  <td style={{ padding: "var(--sp-4)", textAlign: "center", color: "var(--dealix-gold)", fontWeight: 700 }}>{price}</td>
                  <td style={{ padding: "var(--sp-4)", textAlign: "center", color: "rgba(255,255,255,0.60)" }}>{duration}</td>
                  <td style={{ padding: "var(--sp-4)", textAlign: "center", color: "rgba(255,255,255,0.50)", fontSize: "0.82rem" }}>{suitable}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* Pricing Rules */}
      <section className="card" style={{ padding: "clamp(24px,4vw,40px)", border: "1px solid rgba(212,175,55,0.15)" }}>
        <h2 style={{ marginBottom: "var(--sp-5)", fontSize: "1.2rem", color: "var(--dealix-gold)" }}>
          قواعد التسعير — لا مفاجآت
        </h2>
        <ul style={{ listStyle: "none", padding: 0, display: "flex", flexDirection: "column", gap: "var(--sp-3)" }}>
          {rules.map((rule) => (
            <li key={rule} style={{ fontSize: "0.92rem", color: "rgba(255,255,255,0.70)", display: "flex", gap: "var(--sp-3)", alignItems: "flex-start", lineHeight: 1.65 }}>
              <span style={{ color: "var(--dealix-gold)", flexShrink: 0, marginTop: "2px" }}>✓</span>
              {rule}
            </li>
          ))}
        </ul>
      </section>

      {/* CTA */}
      <section style={{ textAlign: "center" }}>
        <h2 style={{ marginBottom: "var(--sp-4)" }}>جاهز تبدأ؟</h2>
        <p style={{ color: "rgba(255,255,255,0.60)", marginBottom: "var(--sp-6)", maxWidth: "420px", margin: "0 auto var(--sp-6)" }}>
          ابدأ بالتشخيص المجاني — ٣٠ دقيقة تعطيك وضوح كامل عن شركتك.
        </p>
        <div style={{ display: "flex", gap: "var(--sp-3)", justifyContent: "center", flexWrap: "wrap" }}>
          <Link href="/book" className="btn btn-primary" style={{ fontSize: "1rem", padding: "14px 32px" }}>
            احجز التشخيص المجاني
          </Link>
          <Link href="/offers" className="btn btn-secondary" style={{ fontSize: "1rem", padding: "14px 24px" }}>
            تفاصيل العروض
          </Link>
        </div>
      </section>

    </main>
  );
}
