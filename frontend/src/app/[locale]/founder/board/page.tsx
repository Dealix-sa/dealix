import { AppLayout } from "@/components/layout/AppLayout";
import { DailyBoardPanel } from "@/components/founder/DailyBoardPanel";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function FounderBoardPage({ params }: PageProps) {
  const { locale } = await params;
  const isAr = locale === "ar";
  return (
    <AppLayout
      title={isAr ? "لوحة اليوم" : "Daily Board"}
      subtitle={isAr ? "أعلى الفرص اليوم — مسودّات للاعتماد والإرسال اليدوي" : "Today's top leads — drafts to approve and send manually"}
    >
      <DailyBoardPanel />
    </AppLayout>
  );
}
