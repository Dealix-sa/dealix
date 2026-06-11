"use client";

import PageShell from "@/components/PageShell";
import SectionHeader from "@/components/SectionHeader";
import CommandPanel from "@/components/CommandPanel";
import CTA from "@/components/CTA";

export default function DeliveryOsPage() {
  return (
    <PageShell>
      <section className="card dot-pattern" style={{ position: "relative", overflow: "hidden", paddingTop: "clamp(40px,6vw,72px)", paddingBottom: "clamp(40px,6vw,72px)" }}>
        <p className="eyebrow">نظام التسليم</p>
        <h1 style={{ maxWidth: 860 }}>سلّم بجودة قابلة للقياس</h1>
        <p style={{ maxWidth: 680, fontSize: "1.15rem", lineHeight: 1.7 }}>
          Delivery OS يضمن أن كل مشروع يخرج بموعده وبدرجة رضا معروفة مسبقاً.
        </p>
        <CTA href="/book" label="اطلب عرضاً" />
      </section>

      <section>
        <SectionHeader title="ما الذي نراقبه؟" />
        <div className="cards">
          <CommandPanel title="Milestones">
            <p>كل مرحلة لها معيار دخول ومعيار قبول.</p>
          </CommandPanel>
          <CommandPanel title="Client Updates">
            <p>تقارير دورية جاهزة للمراجعة قبل الإرسال.</p>
          </CommandPanel>
          <CommandPanel title="Quality Score">
            <p>درجة جودة بناءً على السرعة والدقة والرضا.</p>
          </CommandPanel>
        </div>
      </section>
    </PageShell>
  );
}
