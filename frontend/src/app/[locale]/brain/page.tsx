import type { Metadata } from "next";
import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { BrainDashboard } from "@/components/company/BrainDashboard";

type Props = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr ? "عقل الشركة — Dealix" : "Company Brain — Dealix",
    description: isAr
      ? "القرار اليومي، رادار المستقبل، مذكرة المجلس، وخطة ٣٠ يوماً — في مكان واحد."
      : "Daily decision, future radar, board memo, and 30-day plan — in one place.",
    alternates: { canonical: `https://dealix.me/${locale}/brain` },
  };
}

export default async function BrainPage({ params }: Props) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "company" });

  return (
    <AppLayout title={t("title")} subtitle={t("subtitle")}>
      <BrainDashboard />
    </AppLayout>
  );
}