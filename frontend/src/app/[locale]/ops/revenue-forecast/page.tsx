import { AppLayout } from "@/components/layout/AppLayout";
import { OpsRevenueForecastDashboard } from "@/components/gtm/OpsRevenueForecastDashboard";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function OpsRevenueForecastPage({ params }: PageProps) {
  const { locale } = await params;
  return (
    <AppLayout
      title={locale === "ar" ? "توقعات الإيرادات" : "Revenue Forecast"}
      subtitle={
        locale === "ar"
          ? "استخبارات الـ 90 يوم القادمة"
          : "90-day pipeline intelligence"
      }
    >
      <OpsRevenueForecastDashboard />
    </AppLayout>
  );
}
