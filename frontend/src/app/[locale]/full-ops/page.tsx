import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { FullOpsConsole } from "@/components/full-ops/FullOpsConsole";

interface FullOpsPageProps {
  params: Promise<{ locale: string }>;
}

export default async function FullOpsPage({ params }: FullOpsPageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "fullOps" });

  return (
    <AppLayout title={t("title")} subtitle={t("subtitle")}>
      <FullOpsConsole />
    </AppLayout>
  );
}
