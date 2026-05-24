import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { StrategyAssumptionsPanel } from "@/components/founder-ceo/StrategyAssumptionsPanel";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function StrategyPage({ params }: PageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "nav" });

  return (
    <AppLayout
      title={t("strategy")}
      subtitle="North Star, goal tree, and falsifiable bets"
    >
      <StrategyAssumptionsPanel />
    </AppLayout>
  );
}
