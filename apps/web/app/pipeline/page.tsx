"use client";

import PageShell from "@/components/PageShell";
import SectionHeader from "@/components/SectionHeader";
import CommandPanel from "@/components/CommandPanel";

export default function PipelinePage() {
  return (
    <PageShell>
      <section className="card dot-pattern" style={{ position: "relative", overflow: "hidden", paddingTop: "clamp(40px,6vw,72px)", paddingBottom: "clamp(40px,6vw,72px)" }}>
        <p className="eyebrow">خط الأنابيب</p>
        <h1 style={{ maxWidth: 860 }}>رؤية واضحة لكل مرحلة في خط الأنابيب</h1>
        <p style={{ maxWidth: 680, fontSize: "1.15rem", lineHeight: 1.7 }}>
          من أول لمسة إلى التوقيع. كل مرحلة لها معيار دخول ومعيار خروج.
        </p>
      </section>

      <section>
        <SectionHeader title="المراحل" />
        <div className="cards">
          <CommandPanel title="Lead">
            <p>معلومات الاتصال مسجلة. لم يتم التواصل بعد.</p>
          </CommandPanel>
          <CommandPanel title="Qualified">
            <p>الألم مؤكد. الميزانية والجدول الزمني واضحان.</p>
          </CommandPanel>
          <CommandPanel title="Diagnostic Scheduled">
            <p>جلسة استكشاف محددة. التحضير جارٍ.</p>
          </CommandPanel>
          <CommandPanel title="Proposal Sent">
            <p>العرض مرسل وفي انتظار المراجعة.</p>
          </CommandPanel>
          <CommandPanel title="Negotiation">
            <p>التفاوض على النطاق والتسعير.</p>
          </CommandPanel>
          <CommandPanel title="Closed Won">
            <p>تم التوقيع. الانتقال إلى التسليم.</p>
          </CommandPanel>
        </div>
      </section>
    </PageShell>
  );
}
