import { AppLayout } from "@/components/layout/AppLayout";
import { StatusBoard } from "@/components/gtm/StatusBoard";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export const dynamic = "force-dynamic";

export default async function StatusPage({ params }: PageProps) {
  const { locale } = await params;
  const isAr = locale === "ar";
  return (
    <AppLayout
      title={isAr ? "حالة الخدمة" : "Service Status"}
      subtitle={
        isAr
          ? "حالة API + frontend + webhook + doctrine — يُحدّث كل ٦٠ ثانية."
          : "API + frontend + webhook + doctrine status — refreshes every 60s."
      }
    >
      <StatusBoard isAr={isAr} />
    </AppLayout>
  );
}
