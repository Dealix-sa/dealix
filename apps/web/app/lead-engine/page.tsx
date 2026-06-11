"use client";

import PageShell from "@/components/PageShell";
import SectionHeader from "@/components/SectionHeader";
import CommandPanel from "@/components/CommandPanel";
import CTA from "@/components/CTA";

export default function LeadEnginePage() {
  return (
    <PageShell>
      <section className="card dot-pattern" style={{ position: "relative", overflow: "hidden", paddingTop: "clamp(40px,6vw,72px)", paddingBottom: "clamp(40px,6vw,72px)" }}>
        <p className="eyebrow">محرك العملاء المحتملين</p>
        <h1 style={{ maxWidth: 860 }}>من أول لمسة إلى جدولة التشخيص</h1>
        <p style={{ maxWidth: 680, fontSize: "1.15rem", lineHeight: 1.7 }}>
          محرك العملاء لا يجمع بيانات فقط. يصنفها، يحدد الأولوية، ويعد المسودات للمراجعة.
        </p>
        <CTA href="/book" label="احجز مراجعة" />
      </section>

      <section>
        <SectionHeader title="المراحل" />
        <div className="cards">
          <CommandPanel title="استيعاب">
            <p>جمع البيانات من النماذج والاستيراد واليدوي.</p>
          </CommandPanel>
          <CommandPanel title="التصنيف">
            <p>Fit × Pain × Budget × Urgency = Score.</p>
          </CommandPanel>
          <CommandPanel title="المسودات">
            <p>مسودات مخصصة لكل شريحة، بانتظار مراجعتك.</p>
          </CommandPanel>
        </div>
      </section>
    </PageShell>
  );
}
