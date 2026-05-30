import type { Metadata } from "next";
import { PublicFunnelLayout } from "@/components/gtm/PublicFunnelLayout";
import { SprintDemoViewer } from "@/components/demo/SprintDemoViewer";

type PageProps = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr ? "ديمو Dealix — شاهد النتائج في 60 ثانية" : "Dealix Demo — See Results in 60 Seconds",
    description: isAr
      ? "شاهد كيف يحلّل Dealix بياناتك ويعطيك أعلى 5 حسابات مرتّبة + Proof Pack في دقائق."
      : "See how Dealix analyses your data and delivers the top 5 ranked accounts + Proof Pack in minutes.",
  };
}

export default async function DemoPage({ params }: PageProps) {
  const { locale } = await params;
  const isAr = locale === "ar";

  return (
    <PublicFunnelLayout>
      <div className="space-y-8 max-w-2xl" dir={isAr ? "rtl" : "ltr"}>
        {/* Hero */}
        <header className={isAr ? "text-right" : ""}>
          <p className="text-xs font-semibold text-primary/70 uppercase tracking-widest mb-2">
            {isAr ? "ديمو مباشر" : "Live Demo"}
          </p>
          <h1 className="text-3xl font-bold tracking-tight">
            {isAr
              ? "شاهد Dealix في 60 ثانية"
              : "See Dealix in 60 Seconds"}
          </h1>
          <p className="mt-3 text-muted-foreground leading-relaxed">
            {isAr
              ? "هذه نتائج حقيقية من تحليل Sprint على بيانات B2B سعودية اصطناعية. كل Demo يُشغَّل فعلياً على الـ API."
              : "These are real results from a Sprint run on synthetic Saudi B2B data. Every demo calls the live API."}
          </p>
        </header>

        {/* Live Sprint Results */}
        <SprintDemoViewer />
      </div>
    </PublicFunnelLayout>
  );
}
