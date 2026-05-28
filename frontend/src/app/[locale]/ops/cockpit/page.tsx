import { AppLayout } from "@/components/layout/AppLayout";
import { CockpitDashboard } from "@/components/gtm/CockpitDashboard";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function CockpitPage({ params }: PageProps) {
  const { locale } = await params;
  const isAr = locale === "ar";
  return (
    <AppLayout
      title={isAr ? "غرفة قيادة الفاوندر" : "Founder Cockpit"}
      subtitle={
        isAr
          ? "اللوحة الموحدة — ٧ لوحات تجمع revenue + approvals + frictions في عرض واحد."
          : "Unified daily view — 7 panels composing revenue + approvals + frictions."
      }
    >
      <CockpitDashboard isAr={isAr} />
    </AppLayout>
  );
}
