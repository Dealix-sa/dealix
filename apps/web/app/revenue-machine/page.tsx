"use client";

import PageShell from "@/components/PageShell";
import SectionHeader from "@/components/SectionHeader";
import CommandPanel from "@/components/CommandPanel";
import CTA from "@/components/CTA";

export default function RevenueMachinePage() {
  return (
    <PageShell>
      <section className="card dot-pattern" style={{ position: "relative", overflow: "hidden", paddingTop: "clamp(40px,6vw,72px)", paddingBottom: "clamp(40px,6vw,72px)" }}>
        <p className="eyebrow">آلة الإيرادات</p>
        <h1 style={{ maxWidth: 860 }}>نظام إيراد يعمل حتى وأنت نائم</h1>
        <p style={{ maxWidth: 680, fontSize: "1.15rem", lineHeight: 1.7 }}>
          لا إرسال تلقائي. لكن هناك نظام يجهز كل شيء: المسودات، المتابعات، التقارير.
        </p>
        <CTA href="/book" label="ابدأ بتشخيص" />
      </section>

      <section>
        <SectionHeader title="المكونات" />
        <div className="cards">
          <CommandPanel title="Scoring">
            <p>كل عميل محتمل يحصل على درجة واضحة.</p>
          </CommandPanel>
          <CommandPanel title="Outreach Drafts">
            <p>مسودات جاهزة بالعربية والإنجليزية.</p>
          </CommandPanel>
          <CommandPanel title="Pipeline">
            <p>مراحل واضحة من Lead إلى Closed Won.</p>
          </CommandPanel>
        </div>
      </section>
    </PageShell>
  );
}
