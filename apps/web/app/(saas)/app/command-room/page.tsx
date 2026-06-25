const dailyMetrics = [
  ["100", "accounts researched", "بحث شركات يومي بدون إرسال عشوائي"],
  ["40", "verified targets", "تحقق من source_url والقطاع"],
  ["25", "sales packs", "مسودات وملاحظات تفاوض"],
  ["10-15", "founder reviews", "مراجعة بشرية قبل أي خطوة"],
  ["1-2", "discovery calls", "تأهيل حقيقي قبل proposal"],
  ["1", "scoped proposal", "عرض واحد واضح بعد التأهيل"],
];

const operatingLanes = [
  {
    title: "Pain Targeting",
    body: "تحويل كل شركة إلى فرضية ألم، buyer persona، source_url، وnext action.",
  },
  {
    title: "Sales Agent Packs",
    body: "مسودات عربية، أسئلة discovery، اعتراضات، وحدود تفاوض لكل قطاع.",
  },
  {
    title: "Company Brain",
    body: "قرار يومي، فرص، مخاطر، bottlenecks، وخطة 30 يوم.",
  },
  {
    title: "Pipeline Control",
    body: "تشخيص، Sprint، proposal، retainer، وproof pack بعد التسليم.",
  },
  {
    title: "Trust Gates",
    body: "لا نتائج وهمية، لا إرسال غير مراجع، لا استخدام بيانات حساسة بلا ضوابط.",
  },
  {
    title: "HubSpot OS",
    body: "Products، tasks، notes، deals، وoperating queue بعد موافقة المؤسس.",
  },
];

const founderActions = [
  "راجع أعلى 10 شركات مؤهلة اليوم.",
  "اختر 3 شركات للاتصال أو مراجعة الرسالة.",
  "جهز proposal واحد فقط بعد discovery واضح.",
  "حدّث HubSpot task status بعد كل مكالمة.",
  "لا توسع scope قبل ظهور proof pack.",
];

export default function SaasCommandRoomPage() {
  return (
    <main className="grid mx-auto max-w-7xl p-8" dir="rtl">
      <section className="card card-gold dot-pattern">
        <p className="eyebrow">Dealix Strategic Command Room</p>
        <h1>غرفة قيادة تجارية حقيقية للمؤسس</h1>
        <p style={{ maxWidth: 860 }}>
          هذه الصفحة تجمع الاستهداف، Sales Agent، Company Brain، HubSpot OS، والتفاوض في نظام تشغيل يومي واحد.
          الهدف: تحويل كل يوم إلى فرص مؤهلة، مسودات مراجعة، قرارات واضحة، وعروض قابلة للبيع.
        </p>
        <p className="mt-3 font-semibold">Communication mode: draft and review first.</p>
      </section>

      <section className="cards" aria-label="Daily command metrics">
        {dailyMetrics.map(([value, label, note]) => (
          <article className="card" key={label}>
            <p className="stat-value">{value}</p>
            <p className="stat-label">{label}</p>
            <p>{note}</p>
          </article>
        ))}
      </section>

      <section className="card" aria-labelledby="lanes-title">
        <p className="eyebrow">Operating lanes</p>
        <h2 id="lanes-title">الطبقات التي تشغّل Dealix تجاريًا</h2>
        <div className="cards" style={{ marginTop: "var(--sp-6)" }}>
          {operatingLanes.map((lane) => (
            <article className="card hover-gold" key={lane.title}>
              <h3>{lane.title}</h3>
              <p>{lane.body}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="grid-2">
        <article className="card card-gold">
          <p className="eyebrow">Founder actions</p>
          <h2>أهم إجراءات اليوم</h2>
          <ul>
            {founderActions.map((action) => (
              <li key={action}>{action}</li>
            ))}
          </ul>
        </article>
        <article className="card">
          <p className="eyebrow">Run pack generator</p>
          <h2>ولّد Sales Agent Pack لشركة محددة</h2>
          <pre style={{ textAlign: "left", direction: "ltr" }}>
            python scripts/commercial/generate_sales_agent_company_brain_pack.py --company "Sample Riyadh Company" --sector b2b_services --city Riyadh --source-url "manual_review_required"
          </pre>
        </article>
      </section>
    </main>
  );
}
