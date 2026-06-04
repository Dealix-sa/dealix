const verticals = [
  { en: "Facilities Management & Maintenance", ar: "إدارة المرافق والصيانة" },
  { en: "Contracting & Project Controls", ar: "المقاولات وضبط المشاريع" },
  { en: "Real Estate & Property Operations", ar: "العقار وإدارة الأملاك" },
  { en: "Legal & Professional Services", ar: "المكاتب القانونية والخدمات المهنية" },
  { en: "Consulting, Training & B2B Services", ar: "الاستشارات والتدريب وخدمات B2B" }
];

const ladder = [
  { name: "Entry Diagnostic — AI Workflow Audit", price: "499–2,500 SAR", note: "workflow map + pain diagnosis + pilot recommendation" },
  { name: "Paid Pilot", price: "5,000–25,000 SAR", note: "working pilot + approval gates + measurable result" },
  { name: "Department OS", price: "25,000–150,000 SAR", note: "internal operating system for one department" },
  { name: "Monthly Retainer", price: "3,000–25,000 SAR/mo", note: "monitoring, improvements, monthly leadership report" },
  { name: "Enterprise Custom OS", price: "150,000+ SAR", note: "custom AI OS across multiple departments" }
];

const principles = [
  "AI recommends and drafts — it never sends on its own.",
  "Deterministic workflows verify every draft against quality and compliance gates.",
  "The founder approves. Nothing is sent automatically.",
  "Human-in-the-loop on every external action. Your data stays with you."
];

const ctas = [
  "Request a Workflow Audit",
  "Book a Diagnostic",
  "Start a Pilot"
];

export default function CommercialPage() {
  return (
    <main className="grid">
      <section className="card">
        <p className="eyebrow">Dealix — AI Revenue & Operations OS</p>
        <h1>A commercial operating system for Saudi/GCC B2B — approval-first, not blind automation.</h1>
        <p>
          Dealix is not a CRM, a chatbot, or a mass-outreach tool. It discovers B2B
          opportunities, drafts high-quality outreach, and runs every draft through
          quality, compliance, and safety gates — then puts it in a founder review queue.
        </p>
        <p>نظام تشغيل تجاري للشركات: يكتشف الفرص، يولّد مسودات، يمرّرها على بوابات الجودة والامتثال، ثم يضعها في طابور مراجعة المؤسس. لا إرسال تلقائي.</p>
      </section>

      <section className="card">
        <p className="eyebrow">Operating principles · مبادئ التشغيل</p>
        <h2>Trust-first. Human-in-the-loop. No blind automation.</h2>
        <ul>
          {principles.map((p) => (
            <li key={p}>{p}</li>
          ))}
        </ul>
      </section>

      <section className="card">
        <p className="eyebrow">First 5 verticals · أول 5 قطاعات</p>
        <div className="cards">
          {verticals.map((v, index) => (
            <article className="card" key={v.en}>
              <p className="eyebrow">Vertical {index + 1}</p>
              <h2>{v.en}</h2>
              <p>{v.ar}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="card">
        <p className="eyebrow">Offer ladder · سلّم العروض (SAR)</p>
        <div className="cards">
          {ladder.map((tier) => (
            <article className="card" key={tier.name}>
              <h2>{tier.name}</h2>
              <p className="eyebrow">{tier.price}</p>
              <p>{tier.note}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="card">
        <p className="eyebrow">Get started · ابدأ</p>
        <h2>Start with a low-risk diagnostic.</h2>
        <div className="cards">
          {ctas.map((cta) => (
            <article className="card" key={cta}>
              <h2>{cta}</h2>
            </article>
          ))}
        </div>
        <p>
          No guaranteed-ROI claims. No automated sending. Outreach is drafted for human
          review and sent manually by the founder after approval.
        </p>
      </section>
    </main>
  );
}
