import { AppLayout } from "@/components/layout/AppLayout";
import { OpsRetainerConversionEngine } from "@/components/gtm/OpsRetainerConversionEngine";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function OpsRetainerConversionPage({ params }: PageProps) {
  const { locale } = await params;
  return (
    <AppLayout
      title={locale === "ar" ? "محرك تحويل العقود الشهرية" : "Retainer Conversion Engine"}
      subtitle={
        locale === "ar"
          ? "تحديد العملاء الجاهزين للترقية إلى عقد شهري"
          : "Identify Sprint customers ready to upgrade to managed retainer"
      }
    >
      <OpsRetainerConversionEngine />
    </AppLayout>
  );
}
