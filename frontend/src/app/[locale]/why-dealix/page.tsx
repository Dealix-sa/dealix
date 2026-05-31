import type { Metadata } from "next";
import { WhyDealixPage } from "@/components/gtm/WhyDealixPage";

type Props = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr
      ? "لماذا Dealix؟ — نتائج مقيسة للسوق السعودي"
      : "Why Dealix? — Measurable Results for the Saudi Market",
    description: isAr
      ? "مقارنة، شهادات العملاء، حاسبة ROI، وأسعار شفافة. أثبت القيمة قبل الدفع."
      : "Comparison, client testimonials, ROI calculator, and transparent pricing. Prove value before you pay.",
    alternates: { canonical: `https://dealix.me/${locale}/why-dealix` },
  };
}

export default function WhyDealixRoute() {
  return <WhyDealixPage />;
}
