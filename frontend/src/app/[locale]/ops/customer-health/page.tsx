import { AppLayout } from "@/components/layout/AppLayout";
import { OpsCustomerHealthDashboard } from "@/components/gtm/OpsCustomerHealthDashboard";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function OpsCustomerHealthPage({ params }: PageProps) {
  const { locale } = await params;
  return (
    <AppLayout
      title={locale === "ar" ? "نظام صحة العملاء" : "Customer Health OS"}
      subtitle={
        locale === "ar"
          ? "توقع التخبط والتوسع قبل حدوثه"
          : "Predict churn and expansion before it happens"
      }
    >
      <OpsCustomerHealthDashboard />
    </AppLayout>
  );
}
