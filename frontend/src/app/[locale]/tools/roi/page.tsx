import type { Metadata } from "next";
import Link from "next/link";
import { RoiCalculator } from "./RoiCalculator";

type PageProps = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr ? "حاسبة العائد — Dealix" : "ROI Calculator — Dealix",
    description: isAr
      ? "احسب الإيراد المعرض للضياع شهرياً بسبب غياب Post-Lead Revenue Ops. مدخلات من واقع نشاطك، نتائج فورية، بلا إرسال خارجي."
      : "Estimate monthly revenue at risk from missing Post-Lead Revenue Ops. Inputs from your own funnel, instant results, no external send.",
  };
}

export default async function RoiPage({ params }: PageProps) {
  const { locale } = await params;
  const isAr = locale === "ar";
  const base = `/${locale}`;

  return (
    <div className="min-h-screen bg-background" dir={isAr ? "rtl" : "ltr"}>
      <header className="border-b border-border/60">
        <div className="mx-auto max-w-4xl px-6 py-4 flex flex-wrap gap-4 text-sm">
          <Link href={base} className="text-muted-foreground hover:text-foreground">
            {isAr ? "← الرئيسية" : "← Home"}
          </Link>
          <Link href={`${base}/proof-pack`} className="text-muted-foreground hover:text-foreground">
            Proof Pack
          </Link>
          <Link href={`${base}/dealix-diagnostic`} className="text-muted-foreground hover:text-foreground">
            {isAr ? "التشخيص" : "Diagnostic"}
          </Link>
        </div>
      </header>

      <main className={`mx-auto max-w-4xl px-6 py-12 ${isAr ? "text-right" : "text-left"}`}>
        <h1 className="text-3xl font-bold">
          {isAr ? "حاسبة الإيراد المعرض للضياع" : "Revenue-at-Risk Calculator"}
        </h1>
        <p className="mt-3 text-muted-foreground leading-relaxed">
          {isAr
            ? "أدخل أرقام funnel فعلية من شركتك. الحساب يحدث في متصفحك — لا نخزن أو نرسل البيانات. النتائج تقديرية وليست نتائج مضمونة."
            : "Enter real funnel numbers from your company. Math runs in your browser — we don't store or send the data. Results are estimates, not guarantees."}
        </p>

        <RoiCalculator locale={locale} />

        <section className="mt-12 rounded-lg border border-border/60 bg-card/30 p-5 text-sm leading-relaxed">
          <h2 className="text-sm font-semibold uppercase tracking-wider text-muted-foreground">
            {isAr ? "كيف نحسب" : "How we compute"}
          </h2>
          <ul className={`mt-3 space-y-2 ${isAr ? "pr-5" : "pl-5"} list-disc`}>
            <li>
              {isAr
                ? "Leads × معدل التحويل الحالي = صفقات مغلقة الآن."
                : "Leads × current conversion rate = deals closed today."}
            </li>
            <li>
              {isAr
                ? "Leads × التسرب (Leads بلا owner أو دليل) × قيمة الصفقة = إيراد معرض للضياع."
                : "Leads × leakage (leads without owner or evidence) × deal value = revenue at risk."}
            </li>
            <li>
              {isAr
                ? "نسبة الاسترداد الافتراضية 25% — مبنية على معدلات تعافي ما بعد الحوكمة في عينة Dealix الداخلية. عدّلها حسب ثقتك."
                : "Default recovery rate 25% — based on Dealix's internal post-governance recovery sample. Adjust to your confidence."}
            </li>
            <li>
              {isAr
                ? "كل المبالغ بالريال السعودي. لا ضمانات بنتائج — Dealix يثبت الحوكمة، السوق يقرر الإيراد."
                : "All amounts in SAR. No outcome guarantees — Dealix proves governance, the market decides revenue."}
            </li>
          </ul>
        </section>
      </main>
    </div>
  );
}
