import Link from "next/link";

const services = [
  {
    title: "Revenue Command Room OS",
    buyer: "CEO / Founder / Sales Director",
    pain: "الفرص والعروض والمتابعات لا تتحول إلى قرار يومي.",
    outcome: "غرفة قيادة تعرض hot accounts، follow-ups، proposals، وnext actions.",
    sprint: "7 days",
  },
  {
    title: "Company Brain OS",
    buyer: "CEO / Operations Director",
    pain: "معرفة الشركة وقراراتها متناثرة بين ملفات ومحادثات وأشخاص.",
    outcome: "ذاكرة تشغيلية وCEO daily decision وfuture radar.",
    sprint: "14 days",
  },
  {
    title: "AI Sales Agent OS",
    buyer: "Sales Director / Founder",
    pain: "الردود والتأهيل والتفاوض تعتمد على اجتهاد كل شخص.",
    outcome: "Sales agent بصوت الشركة، يكتب drafts، يؤهل، ويرتب اعتراضات وتفاوض.",
    sprint: "7-14 days",
  },
  {
    title: "Follow-up Recovery OS",
    buyer: "Sales / Support / Clinics / Real Estate",
    pain: "واتساب والإيميل ممتلئة بفرص لا يملكها أحد.",
    outcome: "تصنيف، queue، drafts، SLA، ومتابعة يومية بدون إرسال غير محكوم.",
    sprint: "7 days",
  },
  {
    title: "AI Trust & Governance OS",
    buyer: "CEO / Compliance / IT",
    pain: "AI يُستخدم بلا سياسة أو مراجعة أو حدود بيانات.",
    outcome: "سياسة AI، approval gates، data SOP، وسجل مراجعة.",
    sprint: "7 days",
  },
  {
    title: "Client Delivery OS",
    buyer: "Agencies / Consultancies / Service Firms",
    pain: "التسليم، التقارير، proof، والتجديدات غير موحدة.",
    outcome: "intake، scope cards، delivery board، proof pack، renewal prompts.",
    sprint: "10-14 days",
  },
];

export default function ServicesPage() {
  return (
    <main>
      <section className="card dot-pattern" style={{ textAlign: "center" }}>
        <p className="eyebrow">Dealix Service Arsenal</p>
        <h1>خدمات AI Operating Systems للشركات السعودية</h1>
        <p style={{ maxWidth: 760, margin: "0 auto" }}>
          Dealix لا يبيع أداة واحدة. Dealix يبني أنظمة تشغيل للشركة: الإيراد، المتابعة، Sales Agents،
          Company Brain، التسليم، والحوكمة — تبدأ بسبرنت صغير ثم تتحول إلى retainer وتشغيل شهري.
        </p>
        <div className="actions" style={{ justifyContent: "center" }}>
          <Link href="/book">احجز مراجعة تشغيلية</Link>
          <Link href="/pricing">شاهد التسعير</Link>
        </div>
      </section>

      <section className="cards">
        {services.map((service) => (
          <article className="card" key={service.title}>
            <span className="badge badge-gold">{service.sprint}</span>
            <h2 style={{ fontSize: "1.45rem", marginTop: "var(--sp-4)" }}>{service.title}</h2>
            <p><strong>Buyer:</strong> {service.buyer}</p>
            <p><strong>Pain:</strong> {service.pain}</p>
            <p><strong>Outcome:</strong> {service.outcome}</p>
          </article>
        ))}
      </section>

      <section className="card card-gold" style={{ textAlign: "center" }}>
        <p className="eyebrow">Best first step</p>
        <h2>لا تبدأ بكل شيء. اختر ألم واحد ونثبته خلال 7 أيام.</h2>
        <p style={{ maxWidth: 680, margin: "0 auto" }}>
          إذا الشركة عندها واتساب مزدحم، عروض بلا متابعة، أو فريق مبيعات غير منظم، نبدأ بـRevenue أو Follow-up Sprint.
          إذا الإدارة نفسها تحتاج ذاكرة وقرار يومي، نبدأ بـCompany Brain.
        </p>
        <div className="actions" style={{ justifyContent: "center" }}>
          <Link href="/book">ابدأ التشخيص</Link>
        </div>
      </section>
    </main>
  );
}
