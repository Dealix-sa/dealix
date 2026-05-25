import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { OperatorContent } from "@/components/operator/OperatorContent";

interface OperatorPageProps {
  params: Promise<{ locale: string }>;
}

export default async function OperatorPage({ params }: OperatorPageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "operator" });

  return (
    <AppLayout title={t("title")} subtitle={t("subtitle")}>
      <OperatorContent />
    </AppLayout>
  );
}
