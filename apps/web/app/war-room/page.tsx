"use client";

import PageShell from "@/components/PageShell";
import SectionHeader from "@/components/SectionHeader";
import MetricCard from "@/components/MetricCard";
import CommandPanel from "@/components/CommandPanel";
import CTA from "@/components/CTA";

export default function WarRoomPage() {
  return (
    <PageShell>
      <section className="card dot-pattern" style={{ position: "relative", overflow: "hidden", paddingTop: "clamp(40px,6vw,72px)", paddingBottom: "clamp(40px,6vw,72px)" }}>
        <p className="eyebrow">غرفة الحرب</p>
        <h1 style={{ maxWidth: 860 }}>حالة المعركة التجارية اليوم</h1>
        <p style={{ maxWidth: 680, fontSize: "1.15rem", lineHeight: 1.7 }}>
          غرفة الحرب ليست للمتابعات اليومية فقط. هي للقرارات التي تحدد الأسبوع.
        </p>
        <CTA href="/book" label="اطلب دخول غرفة الحرب" />
      </section>

      <section aria-label="Platform statistics">
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))", gap: "var(--sp-4)" }}>
          <MetricCard value="١٢" label="حساب نشط" />
          <MetricCard value="٤" label="مسودات بانتظار المراجعة" />
          <MetricCard value="٢" label="متابعات مستحقة" />
          <MetricCard value="١" label="عرض جاهز" />
        </div>
      </section>

      <section>
        <SectionHeader title="الإجراءات الحرجة" />
        <div className="cards">
          <CommandPanel title="مراجعة المسودات">
            <p>٤ مسودات متابعة بانتظار مراجعتك. راجعها قبل الساعة ٤ مساءً.</p>
          </CommandPanel>
          <CommandPanel title="متابعة العرض">
            <p>عرض Revenue OS لـ Acme Saudi في انتظار إرساله بعد التعديل.</p>
          </CommandPanel>
          <CommandPanel title="تشخيص جديد">
            <p>جلسة استكشاف مع Beta Clinic غداً الساعة ١٠ صباحاً.</p>
          </CommandPanel>
        </div>
      </section>
    </PageShell>
  );
}
