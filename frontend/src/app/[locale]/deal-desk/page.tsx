import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { DealDeskPanel } from "@/components/founder-ceo/DealDeskPanel";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function DealDeskPage({ params }: PageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "nav" });

  return (
    <AppLayout title={t("dealDesk")} subtitle="Non-standard deal approval">
      <DealDeskPanel />
    </AppLayout>
  );
}
