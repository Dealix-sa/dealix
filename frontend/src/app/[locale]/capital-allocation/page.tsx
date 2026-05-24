import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { CapitalAllocationPanel } from "@/components/founder-ceo/CapitalAllocationPanel";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function CapitalAllocationPage({ params }: PageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "nav" });

  return (
    <AppLayout
      title={t("capitalAllocation")}
      subtitle="Quarterly buckets, ROI matrix — records intent only"
    >
      <CapitalAllocationPanel />
    </AppLayout>
  );
}
