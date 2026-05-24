import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { EnterpriseSalesPanel } from "@/components/founder-ceo/EnterpriseSalesPanel";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function EnterpriseSalesPage({ params }: PageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "nav" });

  return (
    <AppLayout
      title={t("enterpriseSales")}
      subtitle="Enterprise motion + multi-threading"
    >
      <EnterpriseSalesPanel />
    </AppLayout>
  );
}
