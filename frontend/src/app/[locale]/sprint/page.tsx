import type { Metadata } from "next";
import { AppLayout } from "@/components/layout/AppLayout";
import { SprintPage } from "@/components/gtm/SprintPage";

type Props = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr
      ? "Revenue Intelligence Sprint — 499 ر.س / 7 أيام"
      : "Revenue Intelligence Sprint — 499 SAR / 7 Days",
    description: isAr
      ? "تتبّع تقدم سبرينت ذكاء الإيراد خلال 7 أيام من جمع البيانات إلى تسليم Proof Pack."
      : "Track your 7-day Revenue Intelligence Sprint from data collection through Proof Pack delivery.",
    alternates: { canonical: `https://dealix.me/${locale}/sprint` },
  };
}

export default function SprintHubPage() {
  return (
    <AppLayout>
      <SprintPage />
    </AppLayout>
  );
}
