"use client";

import PageShell from "@/components/PageShell";
import SectionHeader from "@/components/SectionHeader";
import ComparisonTable from "@/components/ComparisonTable";
import CTA from "@/components/CTA";

const rows = [
  { feature: "التشخيص قبل البيع", dealix: "نعم", others: "نادراً" },
  { feature: "مسودات مراجعة بشرية", dealix: "إلزامي", others: "تلقائي" },
  { feature: "إثبات القيمة L0–L5", dealix: "مضمن", others: "غير موجود" },
  { feature: "امتثال PDPL", dealix: "أصلي", others: "إضافي" },
  { feature: "دعم عربي/إنجليزي", dealix: "نعم", others: "إنجليزي فقط" },
  { feature: "تقارير تنفيذية أسبوعية", dealix: "نعم", others: "شهري" },
];

export default function PricingPage() {
  return (
    <PageShell>
      <section className="card dot-pattern" style={{ position: "relative", overflow: "hidden", paddingTop: "clamp(40px,6vw,72px)", paddingBottom: "clamp(40px,6vw,72px)" }}>
        <p className="eyebrow">التسعير</p>
        <h1 style={{ maxWidth: 860 }}>شفافية في التسعير. قيمة قبل الالتزام.</h1>
        <p style={{ maxWidth: 680, fontSize: "1.15rem", lineHeight: 1.7 }}>
          لا نعد بعائد استثمار محدد. نبني نظاماً قابلاً للقياس، ثم نتابع الأرقام معاً.
        </p>
      </section>

      <section>
        <SectionHeader title="لماذا Dealix؟" />
        <ComparisonTable rows={rows} />
      </section>

      <section className="card" style={{ marginTop: "var(--sp-8)" }}>
        <h3>نماذج التسعير</h3>
        <div className="cards" style={{ marginTop: "var(--sp-4)" }}>
          <div className="card" style={{ textAlign: "center" }}>
            <div className="stat-value" style={{ fontSize: "1.6rem" }}>٥,٠٠٠ – ١٠,٠٠٠ ر.س</div>
            <p className="stat-label">Diagnostic Sprint</p>
            <p style={{ fontSize: "0.85rem" }}>تشخيص تشغيلي + خريطة إصلاح</p>
          </div>
          <div className="card" style={{ textAlign: "center" }}>
            <div className="stat-value" style={{ fontSize: "1.6rem" }}>١٥,٠٠٠ – ٣٠,٠٠٠ ر.س</div>
            <p className="stat-label">Revenue OS (إعداد)</p>
            <p style={{ fontSize: "0.85rem" }}>شهري: ٣,٠٠٠ – ٧,٠٠٠ ر.س</p>
          </div>
          <div className="card" style={{ textAlign: "center" }}>
            <div className="stat-value" style={{ fontSize: "1.6rem" }}>حسب الطلب</div>
            <p className="stat-label">Custom Enterprise OS</p>
            <p style={{ fontSize: "0.85rem" }}>يبدأ من ١٠٠,٠٠٠ ر.س</p>
          </div>
        </div>
        <CTA href="/book" label="احجب تشخيصاً لتقدير دقيق" />
      </section>
    </PageShell>
  );
}
