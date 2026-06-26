import Link from "next/link";

const capabilities = [
  "Company pain radar",
  "Offer fit recommendation",
  "Objection and negotiation playbook",
  "Approved company voice profile",
  "Founder review queue",
  "Reply classification and next action",
];

const guardrails = [
  "لا يستخدم اسم شخص أو منصب بدون تصريح واضح.",
  "لا يرسل خارجيًا بشكل افتراضي.",
  "لا يكتب وعود ROI أو نتائج غير موثقة.",
  "كل ألم يكتب كفرضية حتى يتم تأكيده.",
  "كل إجراء حساس يحتاج مراجعة بشرية.",
];

const stages = [
  ["01", "Diagnose", "يقرأ إشارات الشركة ويحوّلها إلى فرضية ألم واضحة."],
  ["02", "Position", "يختار العرض الأنسب حسب القطاع والألم والمرحلة."],
  ["03", "Draft", "يجهز مسودة محترمة بأسلوب الشركة المعتمد."],
  ["04", "Negotiate", "يقترح ردود تفاوض مبنية على scope وproof وليس ضغطًا."],
  ["05", "Review", "يرسل كل شيء إلى queue مراجعة قبل أي خطوة خارجية."],
];

export default function SalesIntelligencePage() {
  return (
    <main className="grid" dir="rtl">
      <section className="card card-gold">
        <p className="eyebrow">Dealix Sales Intelligence OS</p>
        <h1>Sales Agent قوي — لكن مصرح، قابل للمراجعة، وغير مضلل</h1>
        <p>
          هذه الطبقة تجعل Dealix يفهم ألم كل شركة، يختار العرض المناسب، يجهز ردود وتفاوضات
          بأسلوب الشركة، ثم يضعها في مسار مراجعة واضح. القوة هنا ليست في الإرسال المفتوح؛
          القوة في التشخيص، الدقة، والالتزام.
        </p>
        <div className="actions">
          <Link href="/commercial-launch">صفحة الإطلاق التجاري</Link>
          <Link href="/growth-control">ضوابط النمو</Link>
        </div>
      </section>

      <section className="cards" aria-label="Sales intelligence capabilities">
        {capabilities.map((capability) => (
          <article className="card" key={capability}>
            <span className="badge badge-emerald">Capability</span>
            <h3 style={{ marginTop: "var(--sp-4)" }}>{capability}</h3>
          </article>
        ))}
      </section>

      <section className="card">
        <p className="eyebrow">Workflow</p>
        <h2>من ألم الشركة إلى رد تفاوضي قابل للمراجعة</h2>
        <div className="cards" style={{ marginTop: "var(--sp-6)" }}>
          {stages.map(([number, title, body]) => (
            <article className="card" key={number}>
              <p className="stat-value" style={{ fontSize: "2rem" }}>{number}</p>
              <h3>{title}</h3>
              <p>{body}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="card">
        <p className="eyebrow">Guardrails</p>
        <h2>الحدود التي تخلي الخدمة قابلة للبيع للشركات الجادة</h2>
        <ul>
          {guardrails.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </section>
    </main>
  );
}
