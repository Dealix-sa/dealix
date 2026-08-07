import type { Metadata } from "next";
import { AppLayout } from "@/components/layout/AppLayout";

interface PageProps { params: Promise<{ locale: string }>; }

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr ? "أنظمة AI مخصصة — Dealix" : "Custom AI Systems — Dealix",
    description: isAr
      ? "نبني أنظمة AI مخصصة للشركات تبدأ من workflow صغير يثبت القيمة ثم تتوسع."
      : "Custom AI systems that start with a value-proving workflow and scale safely.",
  };
}

export default async function CustomAISystemsPage({ params }: PageProps) {
  const { locale } = await params;
  const isAr = locale === "ar";
  const steps = isAr ? [
    "نرسم العملية الحالية ونحدد أين يضيع الوقت أو الإيراد.",
    "نختار workflow واحد عالي الأثر بدل بناء ضخم غير مثبت.",
    "نبني MVP خلال 2–4 أسابيع حسب النطاق.",
    "نضيف موافقات بشرية قبل أي إجراء خارجي حساس.",
    "نربط النظام بالبيانات والأدوات المناسبة.",
    "نقيس الأثر أسبوعياً ونوسع بعد الإثبات."
  ] : [
    "Map the current process and identify where time or revenue leaks.",
    "Pick one high-impact workflow instead of a large unproven build.",
    "Build an MVP in 2–4 weeks depending on scope.",
    "Add human approvals before sensitive external actions.",
    "Connect the system to the right data and tools.",
    "Measure impact weekly and scale after proof."
  ];

  return (
    <AppLayout
      title={isAr ? "أنظمة AI مخصصة للشركات" : "Custom AI Systems for Companies"}
      subtitle={isAr ? "نبني ما يخدم الإيراد والتشغيل — لا مجرد بوت" : "We build for revenue and operations — not just another bot"}
    >
      <div className="space-y-4">
        {steps.map((step, i) => (
          <div key={step} className="rounded-2xl border p-5">
            <strong>{String(i + 1).padStart(2, "0")}</strong>
            <p className="mt-2 text-muted-foreground">{step}</p>
          </div>
        ))}
      </div>
    </AppLayout>
  );
}
