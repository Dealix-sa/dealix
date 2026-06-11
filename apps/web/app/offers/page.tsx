"use client";

import PageShell from "@/components/PageShell";
import SectionHeader from "@/components/SectionHeader";
import OfferCard from "@/components/OfferCard";
import CTA from "@/components/CTA";

const offers = [
  { icon: "🔍", title: "Diagnostic Sprint", description: "تشخيص تشغيلي مدفوع خلال ٥ أيام. نحدد التسريبات ونرسم خريطة الإصلاح.", href: "/book", badge: "ابدأ هنا" },
  { icon: "⚡", title: "Revenue OS", description: "نظام إيراد شامل: scoring، مسودات، متابعة، تقارير.", href: "/book" },
  { icon: "🛡️", title: "Review & Reputation OS", description: "حماية السمعة، طلب التقييمات، مراقبة، ردود منظمة.", href: "/book" },
  { icon: "📊", title: "Command Center OS", description: "غرفة قيادة للمؤسس: KPIs، تنبيهات، تقرير يومي.", href: "/book" },
  { icon: "🚚", title: "Delivery OS", description: "تسليم بجودة قابلة للقياس: milestones، تقارير العميل، scorecards.", href: "/book" },
  { icon: "🏗️", title: "Custom Enterprise OS", description: "نظام مخصص للمؤسسات المعقدة: تكامل، حوكمة، امتثال.", href: "/book" },
  { icon: "🔁", title: "Managed OS Retainer", description: "إدارة مستمرة لنظامك التشغيلي: تحسين شهري، دعم، توسيع.", href: "/book" },
];

export default function OffersPage() {
  return (
    <PageShell>
      <section className="card dot-pattern" style={{ position: "relative", overflow: "hidden", paddingTop: "clamp(40px,6vw,72px)", paddingBottom: "clamp(40px,6vw,72px)" }}>
        <p className="eyebrow">العروض</p>
        <h1 style={{ maxWidth: 860 }}>اختر نظام التشغيل المناسب لشركتك</h1>
        <p style={{ maxWidth: 680, fontSize: "1.15rem", lineHeight: 1.7 }}>
          كل عرض يبدأ بتشخيص. لا نبيع حلولاً جاهزة قبل فهم الألم الحقيقي.
        </p>
        <CTA href="/book" label="احجز تشخيصاً" />
      </section>

      <section>
        <div className="cards">
          {offers.map((o) => (
            <OfferCard key={o.title} {...o} />
          ))}
        </div>
      </section>
    </PageShell>
  );
}
