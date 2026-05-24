import { getTranslations } from "next-intl/server";
import { AppLayout } from "@/components/layout/AppLayout";
import { CeoOsHub } from "@/components/founder-ceo/CeoOsHub";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function CeoOsPage({ params }: PageProps) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "nav" });

  return (
    <AppLayout title={t("ceoOs")} subtitle="CEO Operating System — daily / weekly rhythm">
      <CeoOsHub />
    </AppLayout>
  );
}
