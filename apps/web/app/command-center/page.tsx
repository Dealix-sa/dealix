"use client";

import PageShell from "@/components/PageShell";
import SectionHeader from "@/components/SectionHeader";
import CommandPanel from "@/components/CommandPanel";
import CTA from "@/components/CTA";

export default function CommandCenterPage() {
  return (
    <PageShell>
      <section className="card dot-pattern" style={{ position: "relative", overflow: "hidden", paddingTop: "clamp(40px,6vw,72px)", paddingBottom: "clamp(40px,6vw,72px)" }}>
        <p className="eyebrow">غرفة القيادة</p>
        <h1 style={{ maxWidth: 860 }}>قراراتك اليومية في لوحة واحدة</h1>
        <p style={{ maxWidth: 680, fontSize: "1.15rem", lineHeight: 1.7 }}>
          Command Center يربط إشارات عملك: مبيعات، سمعة، تسليم، أرقام. لا حاجة لعشرة ملفات إكسل.
        </p>
        <CTA href="/book" label="اطلب عرضاً" />
      </section>

      <section>
        <SectionHeader title="ما الذي تراه في غرفة القيادة؟" />
        <div className="cards">
          <CommandPanel title="إشارات المبيعات">
            <ul>
              <li>عدد المتابعات المعلقة</li>
              <li>العروض المرسلة ونسبة القبول</li>
              <li>أعلى مصدر إيرادات</li>
            </ul>
          </CommandPanel>
          <CommandPanel title="إشارات السمعة">
            <ul>
              <li>سرعة الرد على التقييمات</li>
              <li>متوسط التقييم الشهري</li>
              <li>تنبيهات التقييم السلبي</li>
            </ul>
          </CommandPanel>
          <CommandPanel title="إشارات التسليم">
            <ul>
              <li>مشاريع ضمن الموعد</li>
              <li>مشاريع متأخرة وسبب التأخير</li>
              <li>درجة رضا العميل</li>
            </ul>
          </CommandPanel>
        </div>
      </section>
    </PageShell>
  );
}
