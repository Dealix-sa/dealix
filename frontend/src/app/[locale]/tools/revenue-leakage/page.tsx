import type { Metadata } from "next";
import { PublicFunnelLayout } from "@/components/gtm/PublicFunnelLayout";
import { RevenueLeakageCalculator } from "@/components/wave3/tools/RevenueLeakageCalculator";
import { buildWave3Metadata } from "@/lib/gtmMetadata";

type PageProps = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  return buildWave3Metadata(
    locale,
    "/tools/revenue-leakage",
    "Revenue Leakage Calculator — تقدير تعليمي",
    "Revenue Leakage Calculator — Educational estimate",
    "تقدير تعليمي للقيمة المعرّضة للخطر بسبب الفرص بلا متابعة. الأرقام استرشادية وليست ضماناً.",
    "An educational estimate of value at risk from un-followed-up opportunities. Indicative, not a guarantee.",
  );
}

export default function RevenueLeakagePage() {
  return (
    <PublicFunnelLayout>
      <RevenueLeakageCalculator />
    </PublicFunnelLayout>
  );
}
