import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { FounderLeveragePanel } from "@/components/founder-ceo/FounderLeveragePanel";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function FounderLeveragePage({ params }: PageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "nav" });

  return (
    <AppLayout title={t("founderLeverage")} subtitle="Make / Manage / Move">
      <FounderLeveragePanel />
    </AppLayout>
  );
}
