import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Commercial Launch — Dealix",
  description:
    "Dealix Commercial Launch OS for the Saudi/GCC B2B market: 5 launch verticals, a clear SAR offer ladder, and a trust-first, approval-first motion. Review-only — nothing is sent without founder approval.",
  alternates: { canonical: "/commercial-launch" }
};

const verticals = [
  { en: "Facilities Management & Maintenance", ar: "إدارة المرافق والصيانة" },
  { en: "Contracting & Project Controls", ar: "المقاولات وضبط المشاريع" },
  { en: "Real Estate & Property Operations", ar: "العقار وإدارة الأملاك" },
  { en: "Legal & Professional Services", ar: "المكاتب القانونية والخدمات المهنية" },
  { en: "Consulting, Training & B2B Services", ar: "الاستشارات والتدريب وخدمات B2B" }
];

const ladder = [
  { en: "Entry Diagnostic / AI Workflow Audit", ar: "تشخيص مبدئي / تدقيق سير عمل", price: "499 – 2,500 SAR" },
  { en: "Paid Pilot", ar: "تجربة مدفوعة", price: "5,000 – 25,000 SAR" },
  { en: "Department OS", ar: "نظام تشغيل القسم", price: "25,000 – 150,000 SAR" },
  { en: "Monthly Retainer", ar: "اشتراك شهري", price: "3,000 – 25,000 SAR / mo" },
  { en: "Enterprise Custom OS", ar: "نظام تشغيل مؤسسي مخصص", price: "150,000+ SAR" }
];

const trust = [
  { en: "Approval-first: a human approves every external commitment.", ar: "الموافقة أولاً: إنسان يعتمد كل التزام خارجي." },
  { en: "Evidence-first: we share a proof asset before any ask.", ar: "الدليل أولاً: نشارك دليلًا قبل أي طلب." },
  { en: "Privacy-first: no access to your client data; redacted samples only.", ar: "الخصوصية أولاً: دون وصول لبيانات عملائكم؛ عينات محجوبة فقط." },
  { en: "No guarantees, no hype — conservative, provable claims only.", ar: "لا ضمانات ولا مبالغة — ادعاءات متحفظة وقابلة للإثبات فقط." }
];

export default function CommercialLaunchPage() {
  return (
    <main className="grid">
      <section className="card">
        <p className="eyebrow">Dealix Commercial Launch · السوق السعودي والخليجي</p>
        <h1>A governed B2B revenue & operations OS — built trust-first.</h1>
        <p>
          نظام تشغيل تجاري يولّد فرصًا يومية، يصنّفها، ويجهّز مسودات عالية الجودة — ثم
          يضعها في قائمة مراجعة المؤسس. <strong>لا يُرسل أي شيء دون موافقة المؤسس.</strong>
        </p>
        <p>
          Dealix drafts the work; the founder reviews and sends manually. No automated
          sending, no LinkedIn automation, no WhatsApp cold outreach.
        </p>
      </section>

      <section className="card">
        <p className="eyebrow">First 5 verticals · أول 5 قطاعات</p>
        <div className="cards">
          {verticals.map((v) => (
            <article className="card" key={v.en}>
              <h2>{v.en}</h2>
              <p dir="rtl">{v.ar}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="card">
        <p className="eyebrow">Offer ladder (SAR) · سلّم العروض</p>
        <div className="cards">
          {ladder.map((o, i) => (
            <article className="card" key={o.en}>
              <p className="eyebrow">Rung {i + 1}</p>
              <h2>{o.en}</h2>
              <p dir="rtl">{o.ar}</p>
              <p><strong>{o.price}</strong></p>
            </article>
          ))}
        </div>
        <p>No guaranteed ROI. Every claim is conservative and provable.</p>
      </section>

      <section className="card">
        <p className="eyebrow">Trust-first · approval-first</p>
        <ul>
          {trust.map((t) => (
            <li key={t.en}>
              {t.en}<br />
              <span dir="rtl">{t.ar}</span>
            </li>
          ))}
        </ul>
      </section>

      <section className="card">
        <p className="eyebrow">Get started · ابدأ</p>
        <h2>Book a founder-led diagnostic · احجز تشخيصًا بقيادة المؤسس</h2>
        <p>
          Request a workflow audit on one revenue-critical process. We share a proof
          asset first — no access to your data required.
        </p>
        <p>
          <a className="cta" href="mailto:hello@dealix.me?subject=Request%20a%20Dealix%20workflow%20diagnostic">
            Book diagnostic / Request workflow audit →
          </a>
        </p>
      </section>
    </main>
  );
}
