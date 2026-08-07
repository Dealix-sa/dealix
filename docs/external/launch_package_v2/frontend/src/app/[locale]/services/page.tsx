import type { Metadata } from "next";
import { AppLayout } from "@/components/layout/AppLayout";

interface PageProps { params: Promise<{ locale: string }>; }

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr ? "الخدمات — Dealix" : "Services — Dealix",
    description: isAr
      ? "خدمات Dealix لتحويل المبيعات والمتابعة والبيانات إلى نظام نمو يومي قابل للقياس."
      : "Dealix services turn sales, follow-up, and data into a measurable daily growth system.",
  };
}

export default async function ServicesPage({ params }: PageProps) {
  const { locale } = await params;
  const isAr = locale === "ar";
  const services = isAr ? [
    ["Lead Engine", "اكتشاف وتصنيف فرص B2B حسب القطاع والألم واحتمالية التحويل."],
    ["Follow-up OS", "رسائل وخطط متابعة 72 ساعة قابلة للمراجعة قبل الإرسال."],
    ["Data to Revenue", "تحويل قوائم العملاء والCRM إلى أولويات قابلة للبيع."],
    ["Executive Briefs", "تقارير تنفيذية يومية وأسبوعية للقرارات والنمو."],
    ["Proof Packs", "توثيق المخرجات والأثر لكل Pilot أو مشروع."],
    ["Custom AI Systems", "أنظمة مخصصة للواتساب، CRM، التقارير، والأتمتة الداخلية."],
  ] : [
    ["Lead Engine", "Discover and score Saudi B2B opportunities by sector, pain, and conversion likelihood."],
    ["Follow-up OS", "Review-ready 72-hour follow-up plans and messaging drafts."],
    ["Data to Revenue", "Turn CRM, spreadsheets, and customer lists into a prioritized pipeline."],
    ["Executive Briefs", "Daily and weekly executive reports for growth decisions."],
    ["Proof Packs", "Evidence packages for every pilot or implementation."],
    ["Custom AI Systems", "Custom systems for WhatsApp, CRM, dashboards, and internal automation."],
  ];

  return (
    <AppLayout
      title={isAr ? "خدمات Dealix" : "Dealix Services"}
      subtitle={isAr ? "من الفرص إلى المتابعة إلى القرار التنفيذي" : "From opportunities to follow-up to executive decisions"}
    >
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {services.map(([title, body]) => (
          <section key={title} className="rounded-2xl border p-6">
            <h2 className="text-xl font-bold">{title}</h2>
            <p className="mt-3 text-muted-foreground">{body}</p>
          </section>
        ))}
      </div>
    </AppLayout>
  );
}
