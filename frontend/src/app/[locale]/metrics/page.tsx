import { AppLayout } from "@/components/layout/AppLayout";
import { KPIDashboard } from "@/components/dashboard/KPIDashboard";

interface MetricsPageProps {
  params: Promise<{ locale: string }>;
}

export default async function MetricsPage({ params }: MetricsPageProps) {
  const { locale } = await params;
  return (
    <AppLayout
      title={locale === "ar" ? "مؤشرات الأداء" : "KPI Dashboard"}
      subtitle={
        locale === "ar"
          ? "مؤشرات الأداء الرئيسية للشركة"
          : "Company performance metrics"
      }
    >
      <KPIDashboard />
    </AppLayout>
  );
}
