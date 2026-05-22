import { AppLayout } from "@/components/layout/AppLayout";
import { OpsGCCExpansionRadar } from "@/components/gtm/OpsGCCExpansionRadar";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function OpsGCCExpansionPage({ params }: PageProps) {
  const { locale } = await params;
  return (
    <AppLayout
      title={locale === "ar" ? "رادار التوسع الخليجي" : "GCC Expansion Radar"}
      subtitle={
        locale === "ar"
          ? "استخباراتك لأسواق الخليج العربي"
          : "Market intelligence across the Gulf"
      }
    >
      <OpsGCCExpansionRadar />
    </AppLayout>
  );
}
