import { AppLayout } from "@/components/layout/AppLayout";
import { FullOpsConsole } from "@/components/full-ops/FullOpsConsole";

interface FullOpsPageProps {
  params: Promise<{ locale: string }>;
}

export default async function FullOpsPage({ params }: FullOpsPageProps) {
  const { locale } = await params;
  const isAr = locale === "ar";

  return (
    <AppLayout
      title={isAr ? "مركز التشغيل الكامل" : "Full Ops Console"}
      subtitle={
        isAr
          ? "يشغّل دورة المبيعات ذاتياً حتى بوابة الموافقة"
          : "Runs the sales cycle autonomously — up to the approval gate"
      }
    >
      <FullOpsConsole />
    </AppLayout>
  );
}
