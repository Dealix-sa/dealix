"use client";

import PageShell from "@/components/PageShell";
import SectionHeader from "@/components/SectionHeader";
import OfferCard from "@/components/OfferCard";
import ProofPanel from "@/components/ProofPanel";
import CTA from "@/components/CTA";

const offers = [
  { icon: "⚡", title: "Revenue OS", description: "نظام إيراد كامل: تسجيل، تصنيف، متابعة، تقارير.", href: "/offers", badge: "الأكثر طلباً" },
  { icon: "🛡️", title: "Review & Reputation OS", description: "حماية السمعة وجمع التقييمات بشكل منظم.", href: "/offers" },
  { icon: "📊", title: "Command Center", description: "غرفة قيادة تنفيذية لاتخاذ القرار اليومي.", href: "/offers" },
  { icon: "🚚", title: "Delivery OS", description: "تسليم المشاريع والخدمات بمواعيد واضحة وجودة قابلة للقياس.", href: "/offers" },
];

export default function SalesMachinePage() {
  return (
    <PageShell>
      <section className="card dot-pattern" style={{ position: "relative", overflow: "hidden", paddingTop: "clamp(40px,6vw,72px)", paddingBottom: "clamp(40px,6vw,72px)" }}>
        <p className="eyebrow">آلة المبيعات</p>
        <h1 style={{ maxWidth: 860 }}>حوّل متابعاتك إلى آلة مبيعات منظمة</h1>
        <p style={{ maxWidth: 680, fontSize: "1.15rem", lineHeight: 1.7 }}>
          Dealix لا يرسل رسائل تلقائية. هو يبني لك نظاماً: مسارات، نماذج، مسودات مراجعة، وإثبات قيمة.
        </p>
        <CTA href="/book" label="احجز مراجعة تشغيلية" />
      </section>

      <section>
        <SectionHeader eyebrow="العروض" title="ما الذي نبنيه لك؟" description="أنظمة تشغيلية واقعية، لا برامج سحابية عامة." />
        <div className="cards">
          {offers.map((o) => (
            <OfferCard key={o.title} {...o} />
          ))}
        </div>
      </section>

      <ProofPanel items={[
        { label: "مسودات المراجعة", value: "100%" },
        { label: "بدون إرسال تلقائي", value: "نعم" },
        { label: "وقت التشخيص", value: "٢٠ دقيقة" },
      ]} />
    </PageShell>
  );
}
