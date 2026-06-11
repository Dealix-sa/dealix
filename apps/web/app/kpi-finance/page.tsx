"use client";

import PageShell from "@/components/PageShell";
import SectionHeader from "@/components/SectionHeader";
import MetricCard from "@/components/MetricCard";

export default function KpiFinancePage() {
  return (
    <PageShell>
      <section className="card dot-pattern" style={{ position: "relative", overflow: "hidden", paddingTop: "clamp(40px,6vw,72px)", paddingBottom: "clamp(40px,6vw,72px)" }}>
        <p className="eyebrow">الأرقام والمالية</p>
        <h1 style={{ maxWidth: 860 }}>أرقام واضحة لاتخاذ قرار واثق</h1>
        <p style={{ maxWidth: 680, fontSize: "1.15rem", lineHeight: 1.7 }}>
          لا نعد بعائد. نبني نظاماً ترى من خلاله أين تذهب الإيرادات وأين تتسرب.
        </p>
      </section>

      <section aria-label="Finance statistics">
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))", gap: "var(--sp-4)" }}>
          <MetricCard value="٠" label="الأنابيب (ر.س)" />
          <MetricCard value="٠" label="مغلق هذا الشهر" />
          <MetricCard value="٠" label="متوسط الصفقة" />
          <MetricCard value="٠" label="دورة البيع (يوم)" />
        </div>
      </section>
    </PageShell>
  );
}
