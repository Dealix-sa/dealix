import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { HypergrowthMetricsPanel } from "@/components/founder-ceo/HypergrowthMetricsPanel";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function MetricsPage({ params }: PageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "nav" });

  return (
    <AppLayout title={t("metrics")} subtitle="Hypergrowth Metrics — three-tier tree">
      <HypergrowthMetricsPanel />
    </AppLayout>
  );
}
