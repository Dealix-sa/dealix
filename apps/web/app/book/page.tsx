"use client";

import PageShell from "@/components/PageShell";
import SectionHeader from "@/components/SectionHeader";
import CTA from "@/components/CTA";
import WhatsAppCTA from "@/components/WhatsAppCTA";
import { mailtoLink } from "@/lib/contact";

export default function BookPage() {
  return (
    <PageShell>
      <section className="card dot-pattern" style={{ position: "relative", overflow: "hidden", paddingTop: "clamp(40px,6vw,72px)", paddingBottom: "clamp(40px,6vw,72px)" }}>
        <p className="eyebrow">احجز الآن</p>
        <h1 style={{ maxWidth: 860 }}>احجز مراجعة تشغيلية استراتيجية</h1>
        <p style={{ maxWidth: 680, fontSize: "1.15rem", lineHeight: 1.7 }}>
          جلسة مدتها ٢٠ دقيقة. نستمع إلى أكبر ألم تشغيلي تواجهه، ونرسل لك خريطة واضحة للتحسين.
          لا بيع. لا ضغط. فقط تشخيص.
        </p>

        <div className="divider-gold" />

        <h3>ما الذي يحدث في الجلسة؟</h3>
        <ul style={{ maxWidth: 680 }}>
          <li>نستمع إلى وضعك التشغيلي الحالي</li>
          <li>نحدد تسريب الإيرادات الأكثر احتمالاً</li>
          <li>نرسل لك ملخصاً تشخيصياً خلال ٢٤ ساعة</li>
          <li>نقترح خطوة واحدة يمكنك تنفيذها فوراً</li>
        </ul>

        <h3>لمن هذه الجلسة؟</h3>
        <ul style={{ maxWidth: 680 }}>
          <li>أصحاب الشركات B2B في السعودية</li>
          <li>فرق المبيعات التي تريد نظاماً بدلاً من الفوضى</li>
          <li>من يريد تحويل متابعات الواتساب إلى مسار منظم</li>
        </ul>

        <h3>لمن ليست هذه الجلسة؟</h3>
        <ul style={{ maxWidth: 680 }}>
          <li>من يبحث عن حل سحري بدون تغيير عمليات</li>
          <li>من لا يملك صلاحية اتخاذ قرار في الشركة</li>
          <li>من يريد ضمان عائد استثمار محدد مسبقاً</li>
        </ul>

        <h3>ما الذي تحتاج تحضيره؟</h3>
        <p style={{ maxWidth: 680 }}>
          لا شيء معقد. فقط أجب عن هذا السؤال قبل الجلسة: ما أكبر شيء يستنزف وقت فريقك اليوم؟
        </p>

        <div className="actions" style={{ alignItems: "center" }}>
          <CTA href={mailtoLink("طلب مراجعة تشغيلية")} label="ارسل طلب مراجعة عبر البريد" />
          <WhatsAppCTA
            message="السلام عليكم، أريد حجز مراجعة تشغيلية استراتيجية (20 دقيقة) مع Dealix."
            label="راسلنا على واتساب"
            fallbackSubject="طلب مراجعة تشغيلية"
          />
        </div>

        <p style={{ fontSize: "0.82rem", color: "rgba(255,255,255,0.40)", marginTop: "var(--sp-4)" }}>
          أو عبر <a href="/contact" style={{ color: "rgba(255,255,255,0.65)" }}>صفحة التواصل</a>. لا نستخدم حجز خارجي تلقائي.
        </p>
      </section>
    </PageShell>
  );
}
