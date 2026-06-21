import Link from "next/link";

export const metadata = {
  title: "العروض والأنظمة — Dealix",
  description: "٦ عروض من التشخيص المجاني إلى أنظمة المؤسسات. كل شركة B2B سعودية تجد ما يناسبها.",
};

const offers = [
  {
    id: "free",
    tier: "١",
    name: "التشخيص المجاني",
    nameEn: "Free Diagnostic",
    price: "مجاني",
    priceDetail: "٠ ريال",
    duration: "٣٠ دقيقة",
    color: "#10B981",
    highlight: false,
    ideal: "أصحاب الشركات الذين يريدون فهم وضعهم قبل أي التزام",
    deliverables: [
      "جلسة زووم أو واتساب ٣٠ دقيقة مع المؤسس",
      "تحليل أكبر ٣ ثغرات إيراد في عملياتك",
      "ملخص مكتوب يصلك خلال ٢٤ ساعة",
      "توصية الخطوة التالية — بدون أي بيع",
    ],
    notFor: "من لا يملك صلاحية اتخاذ القرار في شركته",
    cta: "احجز التشخيص المجاني الآن",
    ctaHref: "/book",
    primary: false,
  },
  {
    id: "micro",
    tier: "٢",
    name: "ميكرو سبرينت",
    nameEn: "Micro Sprint",
    price: "٤٩٩ ريال",
    priceDetail: "دفعة واحدة",
    duration: "يوم – يومان",
    color: "#F59E0B",
    highlight: false,
    ideal: "من يريد تجربة حل حقيقي قبل الاستثمار الكبير",
    deliverables: [
      "نظام مصغر يعمل فعلاً — مش عرض تقديمي",
      "أتمتة مهمة واحدة تستنزف وقت فريقك",
      "كود مسلّم بالكامل تملكه أنت",
      "دليل استخدام بالعربية",
    ],
    notFor: "من يريد حل مشاكل متعددة في وقت واحد",
    cta: "اطلب الميكرو سبرينت",
    ctaHref: "/book",
    primary: false,
  },
  {
    id: "data",
    tier: "٣",
    name: "حزمة البيانات الذكية",
    nameEn: "Data Intelligence Pack",
    price: "١,٥٠٠ ريال",
    priceDetail: "مرة واحدة",
    duration: "٣–٥ أيام",
    color: "#0066FF",
    highlight: false,
    ideal: "من يريد قاعدة بيانات عملاء محتملين جاهزة للاستخدام",
    deliverables: [
      "٥٠+ شركة مستهدفة منتقاة لقطاعك",
      "بيانات كاملة: الاسم، المسمى، القناة، الأولوية",
      "تقييم ICP لكل شركة (A/B/C)",
      "جاهز للتصدير إلى CRM أو واتساب مباشرة",
    ],
    notFor: "من لديه قاعدة بيانات كافية بالفعل",
    cta: "اطلب حزمة البيانات",
    ctaHref: "/book",
    primary: false,
  },
  {
    id: "managed",
    tier: "٤",
    name: "التشغيل المُدار",
    nameEn: "Managed AI Operations",
    price: "٢,٩٩٩–٤,٩٩٩ ريال",
    priceDetail: "شهرياً",
    duration: "اشتراك شهري",
    color: "#D4AF37",
    highlight: true,
    ideal: "الشركات التي تريد نظاماً يشتغل بدون تدخل يومي",
    deliverables: [
      "تقرير أولويات يومي في واتساب",
      "إدارة قائمة المتابعات والصفقات المتأخرة",
      "مسودات رسائل جاهزة للمراجعة والإرسال",
      "تحديث أسبوعي للأداء مع توصيات",
      "دعم مباشر عبر واتساب",
    ],
    notFor: "من يريد تسليم المسؤولية الكاملة بدون متابعة",
    cta: "اشترك في التشغيل المُدار",
    ctaHref: "/book",
    primary: true,
  },
  {
    id: "sprint",
    tier: "٥",
    name: "سبرينت التشخيص والتحويل",
    nameEn: "Transformation Diagnostic Sprint",
    price: "٧,٥٠٠–٢٥,٠٠٠ ريال",
    priceDetail: "دفعة واحدة",
    duration: "٣–٧ أيام",
    color: "#D4AF37",
    highlight: true,
    ideal: "الشركات الجادة في بناء نظام إيراد متكامل بسرعة",
    deliverables: [
      "خريطة تسرب الإيراد الكاملة بأرقام دقيقة",
      "Revenue OS مخصص لعملياتك الفعلية",
      "Proof Pack — حزمة إثبات القيمة",
      "خطة تطبيق ١٤ يوم واضحة",
      "تدريب الفريق على الاستخدام",
      "دعم ٣٠ يوم بعد التسليم",
    ],
    notFor: "الشركات التي تريد فهم وضعها فقط دون بناء نظام",
    cta: "احجز سبرينت التشخيص",
    ctaHref: "/book",
    primary: true,
  },
  {
    id: "enterprise",
    tier: "٦",
    name: "نظام مؤسسي مخصص",
    nameEn: "Custom Enterprise AI System",
    price: "٢٥,٠٠٠–١٠٠,٠٠٠+ ريال",
    priceDetail: "حسب النطاق",
    duration: "٤–١٢ أسبوعاً",
    color: "#EF4444",
    highlight: false,
    ideal: "المؤسسات الكبيرة التي تحتاج نظاماً مخصصاً بالكامل",
    deliverables: [
      "نظام AI مخصص من الصفر لعملياتك",
      "تكامل مع ERP، CRM، SAP، أو أي نظام حالي",
      "دعم Multi-tenant لفروع وأقسام متعددة",
      "SLA مضمون + دعم مخصص",
      "تدريب شامل للفريق + توثيق كامل",
    ],
    notFor: "الشركات الصغيرة التي لا تحتاج تكاملات معقدة",
    cta: "تحدث مع الفريق",
    ctaHref: "/book",
    primary: false,
  },
];

const systems = [
  { icon: "💬", name: "WhatsApp Revenue OS", nameAr: "نظام إيرادات واتساب" },
  { icon: "⭐", name: "Review Intelligence OS", nameAr: "نظام ذكاء التقييمات" },
  { icon: "🏢", name: "AI Business Command Center", nameAr: "غرفة القيادة" },
  { icon: "📣", name: "Brand Intelligence OS", nameAr: "ذكاء العلامة التجارية" },
  { icon: "📈", name: "Growth Engine OS", nameAr: "محرك النمو" },
  { icon: "❤️", name: "Customer Experience OS", nameAr: "تجربة العملاء" },
  { icon: "👥", name: "AI Agent Workforce OS", nameAr: "قوى العمل الذكية" },
];

export default function OffersPage() {
  return (
    <main style={{ display: "flex", flexDirection: "column", gap: "var(--sp-12)", paddingBottom: "var(--sp-16)" }}>

      {/* Nav */}
      <nav className="navbar" aria-label="Primary navigation">
        <Link href="/" className="navbar-brand">Dealix</Link>
        <ul className="navbar-links" role="list">
          <li><Link href="/">الرئيسية</Link></li>
          <li><Link href="/pricing">التسعير</Link></li>
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
        <p className="eyebrow" style={{ display: "flex", justifyContent: "center" }}>سلّم العروض</p>
        <h1 style={{ maxWidth: "760px", margin: "0 auto var(--sp-4)" }}>
          ٦ عروض، مسار واحد نحو{" "}
          <span className="gradient-text">نظام إيراد حقيقي</span>
        </h1>
        <p style={{ maxWidth: "560px", margin: "0 auto var(--sp-8)", color: "rgba(255,255,255,0.65)", fontSize: "1.05rem", lineHeight: 1.8 }}>
          كل عميل يبدأ من التشخيص المجاني. نقرر مع بعض الخطوة التالية. لا فخ تسعير.
        </p>
        <Link href="/book" className="btn btn-primary" style={{ fontSize: "1rem", padding: "14px 32px" }}>
          ابدأ بالتشخيص المجاني
        </Link>
      </section>

      {/* Offers */}
      <section>
        <div style={{ display: "flex", flexDirection: "column", gap: "var(--sp-6)" }}>
          {offers.map(({ id, tier, name, nameEn, price, priceDetail, duration, color, highlight, ideal, deliverables, notFor, cta, ctaHref, primary }) => (
            <article
              key={id}
              className="card"
              style={{
                padding: "clamp(24px,4vw,48px)",
                border: highlight ? "2px solid var(--dealix-gold)" : undefined,
                background: highlight ? "rgba(212,175,55,0.04)" : undefined,
              }}
            >
              <div style={{ display: "grid", gridTemplateColumns: "1fr auto", gap: "var(--sp-4)", alignItems: "flex-start", marginBottom: "var(--sp-6)" }}>
                <div>
                  <div style={{ display: "flex", alignItems: "center", gap: "var(--sp-3)", marginBottom: "var(--sp-2)" }}>
                    <span style={{
                      width: 36, height: 36, borderRadius: "50%",
                      background: color, display: "inline-flex",
                      alignItems: "center", justifyContent: "center",
                      color: "#001F3F", fontWeight: 800, fontSize: "0.9rem",
                      flexShrink: 0,
                    }}>
                      {tier}
                    </span>
                    {highlight && (
                      <span className="badge badge-gold">الأكثر طلباً</span>
                    )}
                  </div>
                  <h2 style={{ fontSize: "clamp(1.2rem,3vw,1.8rem)", marginBottom: "var(--sp-1)" }}>{name}</h2>
                  <p style={{ fontSize: "0.82rem", color: "rgba(255,255,255,0.40)" }}>{nameEn}</p>
                </div>
                <div style={{ textAlign: "left" }}>
                  <div style={{ fontSize: "clamp(1.3rem,3vw,1.9rem)", fontWeight: 800, color, fontFamily: "var(--font-display)", lineHeight: 1 }}>
                    {price}
                  </div>
                  <p style={{ fontSize: "0.78rem", color: "rgba(255,255,255,0.40)", marginTop: "var(--sp-1)" }}>{priceDetail}</p>
                  <p style={{ fontSize: "0.80rem", color: "rgba(255,255,255,0.50)", marginTop: "var(--sp-1)" }}>⏱ {duration}</p>
                </div>
              </div>

              <div className="divider-gold" />

              <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))", gap: "var(--sp-6)" }}>
                <div>
                  <p style={{ fontSize: "0.80rem", fontWeight: 700, color: "rgba(255,255,255,0.45)", marginBottom: "var(--sp-3)", textTransform: "uppercase", letterSpacing: "0.08em" }}>
                    ماذا تحصل؟
                  </p>
                  <ul style={{ listStyle: "none", padding: 0, display: "flex", flexDirection: "column", gap: "var(--sp-2)" }}>
                    {deliverables.map((d) => (
                      <li key={d} style={{ fontSize: "0.90rem", color: "rgba(255,255,255,0.72)", display: "flex", gap: "var(--sp-2)", alignItems: "flex-start" }}>
                        <span style={{ color: "#10B981", flexShrink: 0, marginTop: "2px" }}>✓</span>
                        {d}
                      </li>
                    ))}
                  </ul>
                </div>
                <div>
                  <p style={{ fontSize: "0.80rem", fontWeight: 700, color: "rgba(255,255,255,0.45)", marginBottom: "var(--sp-3)", textTransform: "uppercase", letterSpacing: "0.08em" }}>
                    مثالي لـ
                  </p>
                  <p style={{ fontSize: "0.90rem", color: "rgba(255,255,255,0.65)", lineHeight: 1.7, marginBottom: "var(--sp-5)" }}>
                    {ideal}
                  </p>
                  <p style={{ fontSize: "0.78rem", fontWeight: 700, color: "rgba(255,255,255,0.35)", marginBottom: "var(--sp-2)", textTransform: "uppercase", letterSpacing: "0.08em" }}>
                    ليس لـ
                  </p>
                  <p style={{ fontSize: "0.85rem", color: "rgba(255,255,255,0.40)", lineHeight: 1.65 }}>{notFor}</p>
                </div>
              </div>

              <div style={{ marginTop: "var(--sp-6)" }}>
                <Link
                  href={ctaHref}
                  className={primary ? "btn btn-primary" : "btn btn-secondary"}
                  style={{ fontSize: "0.92rem", padding: "12px 28px" }}
                >
                  {cta} →
                </Link>
              </div>
            </article>
          ))}
        </div>
      </section>

      {/* Systems */}
      <section className="card" style={{ padding: "clamp(32px,5vw,56px)" }}>
        <p className="eyebrow">أنظمة التشغيل المتاحة</p>
        <h2 style={{ marginBottom: "var(--sp-4)" }}>٧ أنظمة تشغيل — تختار ما يناسبك</h2>
        <p style={{ color: "rgba(255,255,255,0.60)", marginBottom: "var(--sp-6)", maxWidth: "520px" }}>
          كل سبرينت يبني واحداً أو أكثر بناءً على أولوياتك.
        </p>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))", gap: "var(--sp-3)" }}>
          {systems.map(({ icon, name, nameAr }) => (
            <div
              key={name}
              style={{
                padding: "var(--sp-4) var(--sp-5)",
                background: "rgba(255,255,255,0.04)",
                border: "1px solid rgba(255,255,255,0.07)",
                borderRadius: "var(--r-md)",
                display: "flex", alignItems: "center", gap: "var(--sp-3)",
              }}
            >
              <span style={{ fontSize: "1.4rem" }}>{icon}</span>
              <div>
                <p style={{ fontSize: "0.85rem", fontWeight: 600, color: "#fff" }}>{name}</p>
                <p style={{ fontSize: "0.75rem", color: "rgba(255,255,255,0.45)" }}>{nameAr}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section style={{ textAlign: "center" }}>
        <h2 style={{ marginBottom: "var(--sp-4)" }}>مو متأكد من أي عرض يناسبك؟</h2>
        <p style={{ color: "rgba(255,255,255,0.60)", marginBottom: "var(--sp-6)", maxWidth: "440px", margin: "0 auto var(--sp-6)" }}>
          احجز التشخيص المجاني. نساعدك تختار بناءً على وضعك الفعلي.
        </p>
        <Link href="/book" className="btn btn-primary" style={{ fontSize: "1rem", padding: "14px 36px" }}>
          احجز التشخيص المجاني
        </Link>
      </section>

    </main>
  );
}
